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
  // This page does not need initial table data.
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">NovaDev 0.5 Vue Page</p>
      <h1>ALChicken Dashboard</h1>
    </div>
    <p class="empty">Unsupported component: title</p>
    <StatCard title="Products" :value="rows('Product').value.length" />
    <StatCard title="Orders" :value="rows('Order').value.length" />
  </section>
</template>
