import { defineStore } from 'pinia'
import api from '../services/api'

const config = {
  "name": "WebShield",
  "tables": {
    "Scan": {
      "resource": "scans",
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
          "name": "target",
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
        },
        {
          "name": "score",
          "type": "int",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    }
  },
  "pages": [
    {
      "name": "Dashboard",
      "title": "WebShield Dashboard",
      "path": "/dashboard"
    }
  ]
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
    tableRows: (state) => (tableName) => state.rows[tableName] || []
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
    }
  }
})
