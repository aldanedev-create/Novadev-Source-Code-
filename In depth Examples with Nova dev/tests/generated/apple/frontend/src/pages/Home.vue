<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import HeroBlock from '../components/HeroBlock.vue'
import StatCard from '../components/StatCard.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = []
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


onMounted(() => {
  reloadPageData()
})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">Landing</p>
      <h1>Apple Market</h1>
    </div>



    <HeroBlock :hero="{&quot;title&quot;: &quot;Fresh Apples Delivered Fast&quot;, &quot;subtitle&quot;: &quot;Premium orchard apples, gift boxes, juice packs, and weekly fruit bundles for homes, cafes, and offices.&quot;, &quot;action&quot;: &quot;Shop Apples&quot;, &quot;to&quot;: &quot;/shop&quot;}" />
    <StatCard title="Honeycrisp Boxes" value="&quot;$24.99&quot;" />
    <StatCard title="Organic Green Apples" value="&quot;$18.50&quot;" />
    <StatCard title="Family Fruit Bundle" value="&quot;$39.99&quot;" />
    <p class="empty">Unsupported component: button</p>
  </section>
</template>
