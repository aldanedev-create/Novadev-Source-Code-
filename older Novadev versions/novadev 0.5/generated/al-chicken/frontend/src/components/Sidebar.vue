<script setup>
defineProps({
  appName: { type: String, required: true },
  pages: { type: Array, required: true }
})
</script>

<template>
  <aside class="sidebar">
    <RouterLink class="brand" to="/">
      <span class="brand-mark">N</span>
      <strong>{{ appName }}</strong>
    </RouterLink>
    <nav class="nav-list">
      <RouterLink v-for="page in pages" :key="page.path" :to="page.path" class="nav-link">
        {{ page.title }}
      </RouterLink>
    </nav>
  </aside>
</template>
