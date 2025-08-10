import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import { isTokenValid } from './auth'
import './assets/main.css'

import Merchant from './pages/Merchant.vue'
import Buyer from './pages/Buyer.vue'
import Signup from './pages/Signup.vue'
import Login from './pages/Login.vue'

const routes = [
  { path: '/', redirect: '/merchant' },
  { path: '/signup', component: Signup, meta: { public: true } },
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/pay/:id', name: 'pay', component: Buyer, props: true, meta: { public: true } },
  { path: '/merchant', component: Merchant, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isPublic = to.matched.some(r => r.meta.public)
  const needsAuth = to.matched.some(r => r.meta.requiresAuth)

  if (isPublic) return next()
  if (needsAuth && !isTokenValid()) return next('/login')
  next()
})
createApp(App).use(router).mount('#app')
