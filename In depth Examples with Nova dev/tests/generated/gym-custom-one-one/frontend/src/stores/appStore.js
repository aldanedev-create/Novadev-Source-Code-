import { defineStore } from 'pinia'
import api from '../services/api'

const config = {
  "name": "GymCustomOneOne",
  "mode": "custom",
  "styling": "Tailwind",
  "style": {
    "system": "Tailwind",
    "primary": "#2563eb",
    "accent": "#0f172a",
    "surface": "#f8fafc",
    "radius": "medium",
    "density": "comfortable"
  },
  "tables": {
    "Member": {
      "resource": "members",
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
        },
        {
          "name": "plan",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    },
    "CheckIn": {
      "resource": "check-ins",
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
          "name": "memberName",
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
      "name": "Members",
      "title": "Members",
      "path": "/members"
    }
  ],
  "workflows": {
    "MemberCheckIn": {
      "slug": "member-check-in",
      "input": "Member",
      "uses": "GymTools.status",
      "creates": [
        "CheckIn"
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
