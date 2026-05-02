import React, { useEffect, useState } from 'react'
import { Container, Typography, Box, TextField, MenuItem, Button, Alert } from '@mui/material'
import NotificationList from '../components/NotificationList'
import { fetchNotifications } from '../lib/api'

const TYPES = ['', 'Event', 'Result', 'Placement']

export default function Priority() {
	const [n, setN] = useState(10)
	const [type, setType] = useState('')
	const [items, setItems] = useState([])
	const [error, setError] = useState(null)

	const load = async () => {
		setError(null)
		try {
			const data = await fetchNotifications({ limit: n, page: 1, notification_type: type || undefined })
			const list = data.notifications || data
			const viewed = JSON.parse(localStorage.getItem('viewed_notifications_v1') || '[]')
			setItems(list.map(n => ({ ...n, viewed: viewed.includes(n.id) })))
		} catch (err) {
			setError(err.message || 'Failed to fetch')
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
				<Typography variant="h4">Priority Notifications</Typography>
				<Button href="/" variant="outlined">All Notifications</Button>
			</Box>
			<Box display="flex" gap={2} mb={2} flexWrap="wrap">
				<TextField label="Top N" type="number" value={n} onChange={e => setN(Number(e.target.value) || 1)} sx={{ width: 120 }} />
				<TextField select label="Type" value={type} onChange={e => setType(e.target.value)} sx={{ width: 200 }}>
					{TYPES.map(t => <MenuItem key={t} value={t}>{t || 'All'}</MenuItem>)}
				</TextField>
				<Button variant="contained" onClick={load}>Fetch</Button>
			</Box>
			{error && <Alert severity="error">{error}</Alert>}
			<NotificationList items={items} onMarkSeen={markSeen} />
		</Container>
	)
}