import * as React from 'react'
import Head from 'next/head'
import { CssBaseline } from '@mui/material'
import '../styles/globals.css'

export default function MyApp({ Component, pageProps }) {
	return (
		<React.Fragment>
			<Head>
				<meta name="viewport" content="initial-scale=1, width=device-width" />
				<title>Campus Notifications</title>
			</Head>
			<CssBaseline />
			<Component {...pageProps} />
		</React.Fragment>
	)
}