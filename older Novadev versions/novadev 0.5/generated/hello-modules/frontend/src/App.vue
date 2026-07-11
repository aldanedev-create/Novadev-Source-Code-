<script setup>
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

const pages = [
  {
    "name": "Dashboard",
    "title": "Dashboard",
    "path": "/dashboard"
  },
  {
    "name": "Products",
    "title": "Products From Imported Module",
    "path": "/products"
  }
]
</script>

<template>
  <div class="app-shell">
    <Sidebar app-name="HelloModules" :pages="pages" />
    <main class="workspace">
      <Navbar app-name="HelloModules" :pages="pages" />
      <RouterView />
    </main>
  </div>
</template>
