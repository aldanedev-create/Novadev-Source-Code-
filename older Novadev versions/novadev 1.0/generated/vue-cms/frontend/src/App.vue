<script setup>
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

const pages = [
  {
    "name": "Dashboard",
    "title": "CMS Dashboard",
    "path": "/dashboard"
  },
  {
    "name": "Posts",
    "title": "Posts",
    "path": "/posts"
  }
]
</script>

<template>
  <div class="app-shell">
    <Sidebar app-name="VueCMS" :pages="pages" />
    <main class="workspace">
      <Navbar app-name="VueCMS" :pages="pages" />
      <RouterView />
    </main>
  </div>
</template>
