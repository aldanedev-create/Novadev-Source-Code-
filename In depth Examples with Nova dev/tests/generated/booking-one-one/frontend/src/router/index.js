import { createRouter, createWebHistory } from 'vue-router'
import Bookings from '../pages/Bookings.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
  { path: '/', redirect: "/bookings" },
  { path: "/bookings", name: "Bookings", component: Bookings }
  ]
})

export default router
