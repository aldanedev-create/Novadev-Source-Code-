import express from 'express'
import cors from 'cors'
import { router } from './routes.js'

const app = express()
const port = Number(process.env.PORT || 5000)

app.use(cors())
app.use(express.json())
app.use('/api', router)

app.listen(port, () => {
  console.log(`NovaDev Express backend running on http://127.0.0.1:${port}`)
})
