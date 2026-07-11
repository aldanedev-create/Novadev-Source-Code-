<script setup>
import { computed, onMounted } from 'vue'
import { useAppStore } from '../stores/appStore'
import DataTable from '../components/DataTable.vue'
import FormBuilder from '../components/FormBuilder.vue'
import StatCard from '../components/StatCard.vue'
import ChartBlock from '../components/ChartBlock.vue'

const store = useAppStore()

function schema(tableName) {
  return store.tableSchema(tableName)
}

function rows(tableName) {
  return computed(() => store.tableRows(tableName))
}

async function createRow(tableName, payload) {
  await store.createRow(tableName, payload)
}

async function deleteRow(tableName, row) {
  await store.deleteRow(tableName, row)
}

onMounted(() => {
  store.loadTable("Post")
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">NovaDev 0.5 Vue Page</p>
      <h1>Posts</h1>
    </div>
    <p class="empty">Unsupported component: title</p>
    <FormBuilder
      title="Post Form"
      :fields="["title", "slug", "body", "published"]"
      submit-label="Save Post"
      @submit="createRow('Post', $event)"
    />
    <DataTable
      title="Post"
      table-name="Post"
      :columns="["title", "slug", "published"]"
      :rows="rows('Post').value"
      :primary-key="schema('Post')?.primaryKey || 'id'"
      @delete="deleteRow('Post', $event)"
    />
  </section>
</template>
