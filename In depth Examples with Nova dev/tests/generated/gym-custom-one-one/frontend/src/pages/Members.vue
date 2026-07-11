<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAppStore } from '../stores/appStore'
import RecordSection from '../components/RecordSection.vue'
import DataTable from '../components/DataTable.vue'

const store = useAppStore()
const workflowResult = ref(null)
const pageTables = [
  "Member"
]
const workflowsByInput = {
  "Member": "MemberCheckIn"
}
const workflowsByCreate = {
  "CheckIn": "MemberCheckIn"
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
      <h1>Members</h1>
    </div>

    <RecordSection
      title="Members"
      :rows="rows('Member').value"
      :fields="[&quot;name&quot;, &quot;email&quot;, &quot;plan&quot;]"
    />
    <DataTable
      title="Member"
      table-name="Member"
      :columns="[&quot;name&quot;, &quot;email&quot;, &quot;plan&quot;]"
      :rows="rows('Member').value"
      :primary-key="schema('Member')?.primaryKey || 'id'"
      @delete="deleteRow('Member', $event)"
    />
  </section>
</template>
