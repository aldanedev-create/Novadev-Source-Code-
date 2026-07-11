<script setup>
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

const pages = [
  {
    "name": "Dashboard",
    "title": "ALChicken Dashboard",
    "path": "/dashboard"
  },
  {
    "name": "Products",
    "title": "Products",
    "path": "/products"
  },
  {
    "name": "Orders",
    "title": "Orders",
    "path": "/orders"
  }
]
</script>

<template>
  <div class="app-shell">
    <Sidebar app-name="ALChicken" :pages="pages" />
    <main class="workspace">
      <Navbar app-name="ALChicken" :pages="pages" />
      <RouterView />
    </main>
  </div>
</template>
