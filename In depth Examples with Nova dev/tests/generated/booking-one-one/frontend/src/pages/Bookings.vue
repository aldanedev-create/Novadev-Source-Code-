<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import HeroBlock from '../components/HeroBlock.vue'
import RecordSection from '../components/RecordSection.vue'
import FormBuilder from '../components/FormBuilder.vue'
import WorkflowResult from '../components/WorkflowResult.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = [
  "Booking",
  "Service"
]
const workflowsByInput = {
  "Booking": "CreateBooking"
}
const workflowsByCreate = {
  "Booking": "CreateBooking"
}
const cartTable = ""

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
      <p class="eyebrow">Booking</p>
      <h1>Bookings</h1>
    </div>

    <HeroBlock :hero="{&quot;title&quot;: &quot;Booking Calendar&quot;, &quot;subtitle&quot;: &quot;Booking-specific workflow example&quot;}" />
    <RecordSection
      title="Services"
      :rows="rows('Service').value"
      :fields="[&quot;name&quot;, &quot;duration&quot;]"
    />
    <FormBuilder
      title="Booking Form"
      :fields="[&quot;customerName&quot;, &quot;serviceName&quot;, &quot;status&quot;]"
      submit-label="Book"
      @submit="submitPayload('Booking', $event)"
    />
    <WorkflowResult :result="workflowResult" />
  </section>
</template>
