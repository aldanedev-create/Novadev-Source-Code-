import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'
import Posts from '../pages/Posts.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
  { path: '/', redirect: "/dashboard" },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/posts", name: "Posts", component: Posts }
  ]
})

export default router
