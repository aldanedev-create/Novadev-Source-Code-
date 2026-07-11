<script setup>
defineProps({
  title: { type: String, required: true },
  rows: { type: Array, default: () => [] },
  fields: { type: Array, default: () => [] }
})
</script>

<template>
  <section class="panel record-section">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ rows.length }} records</span>
    </div>
    <div class="record-grid">
      <article v-for="(row, index) in rows" :key="row.id || index" class="record-card">
        <strong>{{ row.name || row.title || row.clientName || row.speaker || title }}</strong>
        <dl>
          <template v-for="field in fields" :key="field">
            <dt>{{ field }}</dt>
            <dd>{{ row[field] }}</dd>
          </template>
        </dl>
      </article>
      <p v-if="rows.length === 0" class="empty">No records yet.</p>
    </div>
  </section>
</template>
