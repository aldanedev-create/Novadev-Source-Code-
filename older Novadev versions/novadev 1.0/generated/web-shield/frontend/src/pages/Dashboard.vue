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
  store.loadTable("Scan")
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">NovaDev 1.0 Vue Page</p>
      <h1>WebShield Dashboard</h1>
    </div>
    <p class="empty">Unsupported component: title</p>
    <StatCard title="Scans" :value="rows('Scan').value.length" />
    <DataTable
      title="Scan"
      table-name="Scan"
      :columns="[&quot;target&quot;, &quot;status&quot;, &quot;score&quot;]"
      :rows="rows('Scan').value"
      :primary-key="schema('Scan')?.primaryKey || 'id'"
      @delete="deleteRow('Scan', $event)"
    />
  </section>
</template>
