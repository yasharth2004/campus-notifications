import axios from 'axios'
const BASE = 'http://20.207.122.201/evaluation-service/notifications'

export async function fetchNotifications({ limit=20, page=1, notification_type } = {}) {
	const params = { limit, page }
	if (notification_type) params.notification_type = notification_type
	const res = await axios.get(BASE, { params, timeout: 10000 })
	return res.data
}