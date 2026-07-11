<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import HeroBlock from '../components/HeroBlock.vue'
import FormBuilder from '../components/FormBuilder.vue'
import StatCard from '../components/StatCard.vue'
import WorkflowResult from '../components/WorkflowResult.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = [
  "CartItem"
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
      <p class="eyebrow">Landing</p>
      <h1>Apple Bundles</h1>
    </div>


    <HeroBlock :hero="{&quot;title&quot;: &quot;Apple Bundles For Every Home&quot;, &quot;subtitle&quot;: &quot;Choose starter, family, office, or juice boxes with fresh orchard selections.&quot;, &quot;action&quot;: &quot;Start Bundle&quot;, &quot;to&quot;: &quot;/checkout&quot;}" />
    <StatCard title="Starter Box" value="&quot;6 apples&quot;" />
    <StatCard title="Family Box" value="&quot;18 apples&quot;" />
    <StatCard title="Office Box" value="&quot;48 apples&quot;" />
    <StatCard title="Juice Pack" value="&quot;Apples plus cider&quot;" />
    <FormBuilder
      title="CartItem Form"
      :fields="[&quot;productName&quot;, &quot;quantity&quot;, &quot;price&quot;]"
      submit-label="Add Bundle"
      @submit="submitPayload('CartItem', $event)"
    />
    <WorkflowResult :result="workflowResult" />
  </section>
</template>
