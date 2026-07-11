<script setup>
defineProps({
  hero: { type: Object, default: () => ({}) }
})
</script>

<template>
  <section class="hero-block">
    <div>
      <h2>{{ hero.title || 'Untitled' }}</h2>
      <p v-if="hero.subtitle">{{ hero.subtitle }}</p>
      <p v-if="hero.text">{{ hero.text }}</p>
    </div>
    <RouterLink v-if="hero.action && hero.to" class="primary-button hero-action" :to="hero.to">
      {{ hero.action }}
    </RouterLink>
  </section>
</template>
