import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
  { path: '/', redirect: "/dashboard" },
  { path: "/dashboard", name: "Dashboard", component: Dashboard }
  ]
})

export default router
