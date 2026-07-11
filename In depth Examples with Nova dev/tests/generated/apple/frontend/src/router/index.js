import { createRouter, createWebHistory } from 'vue-router'
import Bundles from '../pages/Bundles.vue'
import Checkout from '../pages/Checkout.vue'
import Dashboard from '../pages/Dashboard.vue'
import Home from '../pages/Home.vue'
import ProductDetails from '../pages/ProductDetails.vue'
import Reviews from '../pages/Reviews.vue'
import Settings from '../pages/Settings.vue'
import Shop from '../pages/Shop.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
  { path: '/', redirect: "/bundles" },
  { path: "/bundles", name: "Bundles", component: Bundles },
  { path: "/checkout", name: "Checkout", component: Checkout },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/home", name: "Home", component: Home },
  { path: "/product-details", name: "ProductDetails", component: ProductDetails },
  { path: "/reviews", name: "Reviews", component: Reviews },
  { path: "/settings", name: "Settings", component: Settings },
  { path: "/shop", name: "Shop", component: Shop }
  ]
})

export default router
