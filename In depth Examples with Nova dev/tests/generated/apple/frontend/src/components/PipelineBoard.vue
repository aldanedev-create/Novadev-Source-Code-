<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, required: true },
  rows: { type: Array, default: () => [] },
  stageField: { type: String, default: 'stage' },
  fields: { type: Array, default: () => [] }
})

const grouped = computed(() => {
  const groups = {}
  props.rows.forEach((row) => {
    const stage = row[props.stageField] || 'Unassigned'
    if (!groups[stage]) groups[stage] = []
    groups[stage].push(row)
  })
  return groups
})
</script>

<template>
  <section class="panel pipeline-section">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ rows.length }} records</span>
    </div>
    <div class="pipeline-board">
      <article v-for="(items, stage) in grouped" :key="stage" class="pipeline-column">
        <h3>{{ stage }}</h3>
        <div v-for="(row, index) in items" :key="row.id || index" class="pipeline-card">
          <strong>{{ row.name || row.clientName || row.title || 'Record' }}</strong>
          <p v-for="field in fields" :key="field">{{ field }}: {{ row[field] }}</p>
        </div>
      </article>
    </div>
  </section>
</template>
