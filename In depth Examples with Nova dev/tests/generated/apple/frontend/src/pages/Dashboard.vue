<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import DataTable from '../components/DataTable.vue'
import StatCard from '../components/StatCard.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = [
  "Order",
  "Product"
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
      <p class="eyebrow">Dashboard</p>
      <h1>Apple Dashboard</h1>
    </div>



    <StatCard title="Revenue" value="&quot;$18,420&quot;" />
    <StatCard title="Orders" value="&quot;128&quot;" />
    <StatCard title="Products" value="&quot;42&quot;" />
    <StatCard title="Cart Items" value="&quot;19&quot;" />
    <DataTable
      title="Product"
      table-name="Product"
      :columns="[&quot;name&quot;, &quot;category&quot;, &quot;price&quot;, &quot;stock&quot;, &quot;badge&quot;]"
      :rows="rows('Product').value"
      :primary-key="schema('Product')?.primaryKey || 'id'"
      @delete="deleteRow('Product', $event)"
    />
    <DataTable
      title="Order"
      table-name="Order"
      :columns="[&quot;customerName&quot;, &quot;email&quot;, &quot;total&quot;, &quot;status&quot;]"
      :rows="rows('Order').value"
      :primary-key="schema('Order')?.primaryKey || 'id'"
      @delete="deleteRow('Order', $event)"
    />
  </section>
</template>
