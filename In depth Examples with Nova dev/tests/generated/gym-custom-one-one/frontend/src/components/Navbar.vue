<script setup>
defineProps({
  appName: { type: String, required: true },
  pages: { type: Array, required: true }
})
</script>

<template>
  <header class="min-h-16 border-b border-slate-200 bg-white/90 px-6 flex items-center justify-between gap-4 backdrop-blur">
    <strong>{{ appName }}</strong>
    <div class="flex items-center gap-3 text-sm text-[var(--nova-muted)]">
      <span>{{ pages.length }} pages</span>
      <a href="/api/health" target="_blank" rel="noreferrer">API Health</a>
    </div>
  </header>
</template>
