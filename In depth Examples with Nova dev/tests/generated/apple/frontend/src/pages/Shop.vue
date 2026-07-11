<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import CatalogGrid from '../components/CatalogGrid.vue'
import DataTable from '../components/DataTable.vue'
import StatCard from '../components/StatCard.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = [
  "CartItem",
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

async function addToCart(row) {
  if (!cartTable) return
  await store.createRow(cartTable, cartPayload(row))
  await reloadPageData()
}

function cartPayload(row) {
  const payload = {}
  payload["productName"] = row.name || row.title || row.productName || ''
  payload["quantity"] = 1
  payload["price"] = Number(row.price || row.amount || 0)
  return payload
}

onMounted(() => {
  reloadPageData()
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">Catalog</p>
      <h1>Shop Apples</h1>
    </div>


    <StatCard title="Free Delivery" value="&quot;Orders over $50&quot;" />
    <StatCard title="Today Only" value="&quot;10% off bundles&quot;" />
    <StatCard title="Customer Rating" value="&quot;4.9 stars&quot;" />
    <CatalogGrid
      title="Product"
      :rows="rows('Product').value"
      :fields="[&quot;name&quot;, &quot;category&quot;, &quot;price&quot;, &quot;rating&quot;, &quot;stock&quot;, &quot;badge&quot;]"
      :can-add-to-cart="true"
      @add-to-cart="addToCart"
    />
    <DataTable
      title="CartItem"
      table-name="CartItem"
      :columns="[&quot;productName&quot;, &quot;quantity&quot;, &quot;price&quot;]"
      :rows="rows('CartItem').value"
      :primary-key="schema('CartItem')?.primaryKey || 'id'"
      @delete="deleteRow('CartItem', $event)"
    />
  </section>
</template>
