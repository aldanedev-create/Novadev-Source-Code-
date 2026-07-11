<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import DataTable from '../components/DataTable.vue'
import StatCard from '../components/StatCard.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = [
  "Review"
]
const workflowsByInput = {
  "CartItem": "AddToCart",
  "Order": "Checkout"
}
const workflowsByCreate = {
  "CartItem": "AddToCart",
  "Order": "Checkout"
}
const cartTable = "CartItem"

function schema(tableName) {
  return store.tableSchema(tableName)
}

function rows(tableName) {
  return computed(() => store.tableRows(tableName))
}

function workflowForTable(tableName) {
  return workflowsByInput[tableName] || workflowsByCreate[tableName] || ''
}

async function reloadPageData() {
  await Promise.all(pageTables.map((tableName) => store.loadTable(tableName)))
}


async function deleteRow(tableName, row) {
  await store.deleteRow(tableName, row)
}

onMounted(() => {
  reloadPageData()
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">Detail</p>
      <h1>Apple Product Details</h1>
    </div>


    <StatCard title="Crisp Taste" value="&quot;Sweet and fresh&quot;" />
    <StatCard title="Farm Source" value="&quot;Local orchard&quot;" />
    <StatCard title="Delivery" value="&quot;1-2 days&quot;" />
    <DataTable
      title="Review"
      table-name="Review"
      :columns="[&quot;customer&quot;, &quot;product&quot;, &quot;rating&quot;, &quot;comment&quot;]"
      :rows="rows('Review').value"
      :primary-key="schema('Review')?.primaryKey || 'id'"
      @delete="deleteRow('Review', $event)"
    />
    <p class="empty">Unsupported component: button</p>
    <p class="empty">Unsupported component: button</p>
  </section>
</template>
