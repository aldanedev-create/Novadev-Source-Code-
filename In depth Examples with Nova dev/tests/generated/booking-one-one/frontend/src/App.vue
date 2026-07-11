<script setup>
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

const pages = [
  {
    "name": "Bookings",
    "title": "Bookings",
    "path": "/bookings"
  }
]
</script>

<template>
  <div class="min-h-screen bg-[var(--nova-surface)] text-[var(--nova-text)] lg:grid lg:grid-cols-[17rem_1fr]">
    <Sidebar app-name="BookingOneOne" :pages="pages" />
    <main class="min-w-0 grid grid-rows-[auto_1fr]">
      <Navbar app-name="BookingOneOne" :pages="pages" />
      <RouterView />
    </main>
  </div>
</template>
