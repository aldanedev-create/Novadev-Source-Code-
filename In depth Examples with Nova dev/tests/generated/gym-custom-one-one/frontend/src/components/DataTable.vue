<script setup>
defineProps({
  title: { type: String, default: 'Table' },
  tableName: { type: String, required: true },
  columns: { type: Array, default: () => [] },
  rows: { type: Array, default: () => [] },
  primaryKey: { type: String, default: 'id' }
})

const emit = defineEmits(['delete'])
</script>

<template>
  <section class="panel">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ rows.length }} records</span>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th v-for="column in columns" :key="column">{{ column }}</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row[primaryKey]">
            <td v-for="column in columns" :key="column">{{ row[column] }}</td>
            <td>
              <button class="ghost-button" @click="emit('delete', row)">Delete</button>
            </td>
          </tr>
          <tr v-if="rows.length === 0">
            <td :colspan="columns.length + 1" class="empty">No rows yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
