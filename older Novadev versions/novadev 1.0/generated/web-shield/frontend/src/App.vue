<script setup>
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

const pages = [
  {
    "name": "Dashboard",
    "title": "WebShield Dashboard",
    "path": "/dashboard"
  }
]
</script>

<template>
  <div class="app-shell">
    <Sidebar app-name="WebShield" :pages="pages" />
    <main class="workspace">
      <Navbar app-name="WebShield" :pages="pages" />
      <RouterView />
    </main>
  </div>
</template>
