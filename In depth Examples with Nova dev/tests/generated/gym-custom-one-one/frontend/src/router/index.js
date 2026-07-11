import { createRouter, createWebHistory } from 'vue-router'
import Members from '../pages/Members.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
  { path: '/', redirect: "/members" },
  { path: "/members", name: "Members", component: Members }
  ]
})

export default router
