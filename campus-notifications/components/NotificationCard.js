import React from 'react'
import { Card, CardContent, Typography, Chip, Button, Box } from '@mui/material'

export default function NotificationCard({ notification, onMarkSeen }) {
	const isNew = !notification.viewed
	return (
		<Card variant="outlined" sx={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
			<CardContent>
				<Box display="flex" justifyContent="space-between" alignItems="start">
					<Box>
						<Typography variant="subtitle2" color="text.secondary">{notification.notification_type}</Typography>
						<Typography variant="h6">{notification.title || notification.message || 'Notification'}</Typography>
					</Box>
					{isNew && <Chip color="primary" label="NEW" />}
				</Box>
				{notification.message && <Typography variant="body2" sx={{ mt: 1 }}>{notification.message}</Typography>}
			</CardContent>
			<Box sx={{ p: 1, pt: 0 }}>
				<Button size="small" onClick={onMarkSeen}>Mark seen</Button>
			</Box>
		</Card>
	)
}