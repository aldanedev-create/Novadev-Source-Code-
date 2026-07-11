<script setup>
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

const pages = [
  {
    "name": "Bundles",
    "title": "Apple Bundles",
    "path": "/bundles"
  },
  {
    "name": "Checkout",
    "title": "Checkout",
    "path": "/checkout"
  },
  {
    "name": "Dashboard",
    "title": "Apple Dashboard",
    "path": "/dashboard"
  },
  {
    "name": "Home",
    "title": "Apple Market",
    "path": "/home"
  },
  {
    "name": "ProductDetails",
    "title": "Apple Product Details",
    "path": "/product-details"
  },
  {
    "name": "Reviews",
    "title": "Customer Reviews",
    "path": "/reviews"
  },
  {
    "name": "Settings",
    "title": "Apple Settings",
    "path": "/settings"
  },
  {
    "name": "Shop",
    "title": "Shop Apples",
    "path": "/shop"
  }
]
</script>

<template>
  <div class="min-h-screen bg-[var(--nova-surface)] text-[var(--nova-text)] lg:grid lg:grid-cols-[17rem_1fr]">
    <Sidebar app-name="Apple" :pages="pages" />
    <main class="min-w-0 grid grid-rows-[auto_1fr]">
      <Navbar app-name="Apple" :pages="pages" />
      <RouterView />
    </main>
  </div>
</template>
