import { defineStore } from 'pinia'
import api from '../services/api'

const config = {
  "name": "Apple",
  "mode": "ecommerce",
  "styling": "Tailwind",
  "style": {
    "system": "Tailwind",
    "primary": "#0f766e",
    "accent": "#ef4444",
    "surface": "#ffffff",
    "radius": "small",
    "density": "compact"
  },
  "tables": {
    "CartItem": {
      "resource": "cart-items",
      "primaryKey": "id",
      "fields": [
        {
          "name": "id",
          "type": "auto",
          "auto": true,
          "secure": false,
          "unique": false
        },
        {
          "name": "productName",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "quantity",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "price",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    },
    "Order": {
      "resource": "orders",
      "primaryKey": "id",
      "fields": [
        {
          "name": "id",
          "type": "auto",
          "auto": true,
          "secure": false,
          "unique": false
        },
        {
          "name": "customerName",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "email",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "address",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "total",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "status",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    },
    "Product": {
      "resource": "products",
      "primaryKey": "id",
      "fields": [
        {
          "name": "id",
          "type": "auto",
          "auto": true,
          "secure": false,
          "unique": false
        },
        {
          "name": "name",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "category",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "price",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "oldPrice",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "image",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "rating",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "stock",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "description",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "badge",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    },
    "Review": {
      "resource": "reviews",
      "primaryKey": "id",
      "fields": [
        {
          "name": "id",
          "type": "auto",
          "auto": true,
          "secure": false,
          "unique": false
        },
        {
          "name": "customer",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "product",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "rating",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "comment",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    }
  },
  "pages": [
    {
      "name": "Bundles",
      "title": "Apple Bundles",
      "path": "/bundles"
    },
    {
      "name": "Checkout",
      "title": "Checkout",
      "path": "/checkout"
    },
    {
      "name": "Dashboard",
      "title": "Apple Dashboard",
      "path": "/dashboard"
    },
    {
      "name": "Home",
      "title": "Apple Market",
      "path": "/home"
    },
    {
      "name": "ProductDetails",
      "title": "Apple Product Details",
      "path": "/product-details"
    },
    {
      "name": "Reviews",
      "title": "Customer Reviews",
      "path": "/reviews"
    },
    {
      "name": "Settings",
      "title": "Apple Settings",
      "path": "/settings"
    },
    {
      "name": "Shop",
      "title": "Shop Apples",
      "path": "/shop"
    }
  ],
  "workflows": {
    "AddToCart": {
      "slug": "add-to-cart",
      "input": "CartItem",
      "uses": "",
      "creates": [
        "CartItem"
      ]
    },
    "Checkout": {
      "slug": "checkout",
      "input": "Order",
      "uses": "",
      "creates": [
        "Order"
      ]
    }
  }
}

export const useAppStore = defineStore('app', {
  state: () => ({
    config,
    rows: {},
    loading: false,
    error: ''
  }),
  getters: {
    tableSchema: (state) => (tableName) => state.config.tables[tableName],
    tableRows: (state) => (tableName) => state.rows[tableName] || [],
    workflow: (state) => (workflowName) => state.config.workflows[workflowName]
  },
  actions: {
    async loadTable(tableName) {
      const schema = this.tableSchema(tableName)
      if (!schema) return
      this.loading = true
      this.error = ''
      try {
        const data = await api.list(schema.resource)
        this.rows[tableName] = data.rows || []
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    async createRow(tableName, payload) {
      const schema = this.tableSchema(tableName)
      const row = await api.create(schema.resource, payload)
      await this.loadTable(tableName)
      return row
    },
    async deleteRow(tableName, row) {
      const schema = this.tableSchema(tableName)
      const id = row[schema.primaryKey]
      await api.remove(schema.resource, id)
      await this.loadTable(tableName)
    },
    async runWorkflow(workflowName, payload) {
      const workflow = this.workflow(workflowName)
      if (!workflow) throw new Error(`Unknown workflow: ${workflowName}`)
      return api.workflow(workflow.slug, payload)
    }
  }
})
