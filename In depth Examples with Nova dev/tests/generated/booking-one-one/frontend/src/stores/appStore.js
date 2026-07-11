import { defineStore } from 'pinia'
import api from '../services/api'

const config = {
  "name": "BookingOneOne",
  "mode": "booking",
  "styling": "Tailwind",
  "style": {
    "system": "Tailwind",
    "primary": "#0891b2",
    "accent": "#164e63",
    "surface": "#ecfeff",
    "radius": "medium",
    "density": "comfortable"
  },
  "tables": {
    "Service": {
      "resource": "services",
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
          "name": "duration",
          "type": "int",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    },
    "Customer": {
      "resource": "customers",
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
          "name": "email",
          "type": "email",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    },
    "Booking": {
      "resource": "bookings",
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
          "name": "serviceName",
          "type": "text",
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
    }
  },
  "pages": [
    {
      "name": "Bookings",
      "title": "Bookings",
      "path": "/bookings"
    }
  ],
  "workflows": {
    "CreateBooking": {
      "slug": "create-booking",
      "input": "Booking",
      "uses": "BookingTools.confirm",
      "creates": [
        "Booking"
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
