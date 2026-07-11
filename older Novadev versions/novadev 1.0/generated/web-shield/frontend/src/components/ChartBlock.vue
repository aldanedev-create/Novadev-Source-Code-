<script setup>
defineProps({
  title: { type: String, required: true },
  type: { type: String, default: 'bar' }
})
</script>

<template>
  <section class="panel chart-block">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ type }}</span>
    </div>
    <div class="chart-placeholder">
      <span>Chart component placeholder</span>
    </div>
  </section>
</template>
