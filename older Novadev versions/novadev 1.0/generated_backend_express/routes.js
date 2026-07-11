import express from 'express'
import { DATA } from './models.js'

export const router = express.Router()
const RESOURCES = {
  "products": "Product",
  "cart-items": "CartItem",
  "orders": "Order"
}

router.get('/health', (req, res) => res.json({ ok: true, backend: 'Express' }))

router.get('/:resource', (req, res) => {
  const table = RESOURCES[req.params.resource]
  if (!table) return res.status(404).json({ error: 'Unknown resource' })
  res.json({ rows: DATA[table] || [] })
})
