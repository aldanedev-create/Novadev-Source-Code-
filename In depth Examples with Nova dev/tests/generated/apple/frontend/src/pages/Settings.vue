<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import FormBuilder from '../components/FormBuilder.vue'
import StatCard from '../components/StatCard.vue'
import WorkflowResult from '../components/WorkflowResult.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = [
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


async function submitPayload(tableName, payload) {
  const workflowName = workflowForTable(tableName)
  if (workflowName) {
    workflowResult.value = await store.runWorkflow(workflowName, payload)
  } else {
    workflowResult.value = await store.createRow(tableName, payload)
  }
  await reloadPageData()
}

onMounted(() => {
  reloadPageData()
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">Dashboard</p>
      <h1>Apple Settings</h1>
    </div>


    <StatCard title="Store Status" value="&quot;Open&quot;" />
    <StatCard title="Delivery Region" value="&quot;Citywide&quot;" />
    <StatCard title="Payment Mode" value="&quot;Online and Cash&quot;" />
    <FormBuilder
      title="Product Form"
      :fields="[&quot;name&quot;, &quot;category&quot;, &quot;price&quot;, &quot;oldPrice&quot;, &quot;image&quot;, &quot;rating&quot;, &quot;stock&quot;, &quot;description&quot;, &quot;badge&quot;]"
      submit-label="Save Product"
      @submit="submitPayload('Product', $event)"
    />
    <WorkflowResult :result="workflowResult" />
  </section>
</template>
