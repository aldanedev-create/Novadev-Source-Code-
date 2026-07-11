<script setup>
defineProps({
  appName: { type: String, required: true },
  pages: { type: Array, required: true }
})
</script>

<template>
  <header class="topbar">
    <strong>{{ appName }}</strong>
    <div class="topbar-actions">
      <span>{{ pages.length }} pages</span>
      <a href="/api/health" target="_blank" rel="noreferrer">API Health</a>
    </div>
  </header>
</template>
