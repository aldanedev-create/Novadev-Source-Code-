import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'
import Products from '../pages/Products.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
  { path: '/', redirect: "/dashboard" },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/products", name: "Products", component: Products }
  ]
})

export default router
