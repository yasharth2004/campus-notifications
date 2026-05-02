import React, { useEffect, useState } from 'react'
import { Container, Typography, Box, Button, Alert } from '@mui/material'
import NotificationList from '../components/NotificationList'
import { fetchNotifications } from '../lib/api'

export default function AllNotifications() {
	const [items, setItems] = useState([])
	const [error, setError] = useState(null)
	const [loading, setLoading] = useState(false)

	const load = async () => {
		setLoading(true)
		setError(null)
		try {
			const data = await fetchNotifications({ limit: 50, page: 1 })
			// API assumed to return array in data.notifications or data
			const list = data.notifications || data
			const viewed = JSON.parse(localStorage.getItem('viewed_notifications_v1') || '[]')
			// mark viewed flag for UI
			const mapped = list.map(n => ({ ...n, viewed: viewed.includes(n.id) }))
			setItems(mapped)
		} catch (err) {
			setError(err.message || 'Failed to fetch')
		} finally {
			setLoading(false)
		}
	}

	useEffect(() => { load() }, [])

	const markSeen = (id) => {
		const viewed = new Set(JSON.parse(localStorage.getItem('viewed_notifications_v1') || '[]'))
		viewed.add(id)
		localStorage.setItem('viewed_notifications_v1', JSON.stringify(Array.from(viewed)))
		setItems(prev => prev.map(p => p.id === id ? { ...p, viewed: true } : p))
	}

	return (
		<Container maxWidth="lg" sx={{ py: 4 }}>
			<Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
				<Typography variant="h4">All Notifications</Typography>
				<Button href="/priority" variant="contained">Priority Notifications</Button>
			</Box>
			{error && <Alert severity="error">{error} <Button onClick={load}>Retry</Button></Alert>}
			<NotificationList items={items} onMarkSeen={markSeen} loading={loading} />
		</Container>
	)
}