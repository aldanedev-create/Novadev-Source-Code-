<script setup>
defineProps({
  appName: { type: String, required: true },
  pages: { type: Array, required: true }
})
</script>

<template>
  <aside class="bg-slate-950 text-white p-5 flex flex-col gap-5">
    <RouterLink class="flex min-h-11 items-center gap-3" to="/">
      <span class="grid h-9 w-9 place-items-center rounded-nova bg-[var(--nova-primary)] font-black text-white">N</span>
      <strong>{{ appName }}</strong>
    </RouterLink>
    <nav class="grid gap-2">
      <RouterLink v-for="page in pages" :key="page.path" :to="page.path" class="rounded-nova px-3 py-2 text-sm font-medium opacity-80 hover:bg-white/10 hover:opacity-100">
        {{ page.title }}
      </RouterLink>
    </nav>
  </aside>
</template>
