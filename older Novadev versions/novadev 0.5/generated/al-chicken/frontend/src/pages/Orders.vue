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
  store.loadTable("Order")
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">NovaDev 0.5 Vue Page</p>
      <h1>Orders</h1>
    </div>
    <p class="empty">Unsupported component: layout</p>
    <p class="empty">Unsupported component: title</p>
    <DataTable
      title="Order"
      table-name="Order"
      :columns="[&quot;customer_name&quot;, &quot;total&quot;, &quot;status&quot;]"
      :rows="rows('Order').value"
      :primary-key="schema('Order')?.primaryKey || 'id'"
      @delete="deleteRow('Order', $event)"
    />
  </section>
</template>
