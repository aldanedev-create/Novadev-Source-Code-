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
      <p class="eyebrow">Landing</p>
      <h1>Customer Reviews</h1>
    </div>


    <StatCard title="Average Rating" value="&quot;4.9 / 5&quot;" />
    <StatCard title="Repeat Customers" value="&quot;82%&quot;" />
    <StatCard title="Orders Delivered" value="&quot;12400+&quot;" />
    <DataTable
      title="Review"
      table-name="Review"
      :columns="[&quot;customer&quot;, &quot;product&quot;, &quot;rating&quot;, &quot;comment&quot;]"
      :rows="rows('Review').value"
      :primary-key="schema('Review')?.primaryKey || 'id'"
      @delete="deleteRow('Review', $event)"
    />
  </section>
</template>
