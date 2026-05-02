import React from 'react'
import { Grid, CircularProgress, Box, Typography } from '@mui/material'
import NotificationCard from './NotificationCard'

export default function NotificationList({ items = [], onMarkSeen, loading=false }) {
	if (loading) return <Box display="flex" justifyContent="center" py={6}><CircularProgress /></Box>
	if (!items || items.length === 0) return <Typography>No notifications</Typography>
	return (
		<Grid container spacing={2}>
			{items.map(n => (
				<Grid item xs={12} sm={6} md={4} key={n.id}>
					<NotificationCard notification={n} onMarkSeen={() => onMarkSeen(n.id)} />
				</Grid>
			))}
		</Grid>
	)
}
