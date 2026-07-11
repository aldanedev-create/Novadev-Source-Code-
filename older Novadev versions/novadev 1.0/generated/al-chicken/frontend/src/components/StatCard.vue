<script setup>
defineProps({
  title: { type: String, required: true },
  value: { type: [String, Number], default: 'Ready' }
})
</script>

<template>
  <article class="stat-card">
    <span>{{ title }}</span>
    <strong>{{ value }}</strong>
  </article>
</template>
