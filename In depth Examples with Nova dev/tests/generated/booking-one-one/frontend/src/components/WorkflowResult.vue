<script setup>
defineProps({
  result: { default: null }
})
</script>

<template>
  <section v-if="result" class="panel workflow-result">
    <div class="panel-heading">
      <h2>Result</h2>
      <span>workflow</span>
    </div>
    <pre>{{ JSON.stringify(result, null, 2) }}</pre>
  </section>
</template>
