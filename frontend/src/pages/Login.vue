<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api.js'

const username = ref('')
const password = ref('')
const message = ref('')
const router = useRouter()

async function login() {
  try {
    const res = await api.post(`/token/`, {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    message.value = 'Login successful'
    router.push('/merchant')
  } catch (err) {
    message.value = 'Invalid credentials'
  }
}
</script>

<template>
  <div class="mx-auto max-w-md">
    <div class="card">
      <h1 class="text-2xl font-bold mb-4">Merchant login</h1>
      <form @submit.prevent="login" class="space-y-3">
        <input v-model="username" placeholder="Username" class="input" />
        <input v-model="password" type="password" placeholder="Password" class="input" />
        <button type="submit" class="btn-primary w-full">Login</button>
      </form>
      <p class="mt-3 text-sm subtle">{{ message }}</p>
      <p class="mt-4 text-sm subtle">
        Don’t have an account?
        <router-link to="/signup" class="text-blue-600 hover:underline">Sign up here</router-link>
      </p>
    </div>
  </div>
</template>

