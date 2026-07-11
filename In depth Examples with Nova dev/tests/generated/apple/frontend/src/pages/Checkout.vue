<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import FormBuilder from '../components/FormBuilder.vue'
import StatCard from '../components/StatCard.vue'
import WorkflowResult from '../components/WorkflowResult.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = [
  "Order"
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
      <p class="eyebrow">Checkout</p>
      <h1>Checkout</h1>
    </div>


    <StatCard title="Secure Checkout" value="&quot;Fast order review&quot;" />
    <StatCard title="Delivery Window" value="&quot;Choose your day&quot;" />
    <FormBuilder
      title="Order Form"
      :fields="[&quot;customerName&quot;, &quot;email&quot;, &quot;address&quot;, &quot;total&quot;, &quot;status&quot;]"
      submit-label="Place Order"
      @submit="submitPayload('Order', $event)"
    />
    <WorkflowResult :result="workflowResult" />
  </section>
</template>
