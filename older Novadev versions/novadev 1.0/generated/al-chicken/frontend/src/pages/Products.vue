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
  store.loadTable("Product")
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">NovaDev 0.5 Vue Page</p>
      <h1>Products</h1>
    </div>
    <p class="empty">Unsupported component: layout</p>
    <p class="empty">Unsupported component: title</p>
    <FormBuilder
      title="Product Form"
      :fields="[&quot;name&quot;, &quot;price&quot;, &quot;stock&quot;, &quot;image&quot;]"
      submit-label="Add Product"
      @submit="createRow('Product', $event)"
    />
    <DataTable
      title="Product"
      table-name="Product"
      :columns="[&quot;name&quot;, &quot;price&quot;, &quot;stock&quot;]"
      :rows="rows('Product').value"
      :primary-key="schema('Product')?.primaryKey || 'id'"
      @delete="deleteRow('Product', $event)"
    />
  </section>
</template>
