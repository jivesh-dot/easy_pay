<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api.js'
import { useApiErrors } from '../composables/useApiErrors';
const { message, fieldErrors, fromAxios, reset } = useApiErrors();

// const username = ref('')
const email = ref('')
const password = ref('')
const businessName = ref('')
// const message = ref('')
const router = useRouter()

async function signup() {
 reset();
  try {
    await api.post(`/register/`, {
    //   username: username.value,
      email: email.value,
      password: password.value,
      business_name: businessName.value
    })
    message.value = 'Signup successful!!! Redirecting to login...'
    setTimeout(() => router.push('/login'), 1200)
  } catch (err) {
    fromAxios(err);
  }
}
</script>

<template>
  <div class="mx-auto max-w-md">
    <div class="card">
      <h1 class="text-2xl font-bold mb-4">Create your account</h1>
      <form @submit.prevent="signup" class="space-y-3">
        <!-- <input v-model="username" placeholder="Username" class="input" /> -->
        <input v-model="email" type="email" placeholder="Email" class="input" />
        <input v-model="password" type="password" placeholder="Password" class="input" />
        <input v-model="businessName" placeholder="Business name" class="input" />
        <button type="submit" class="btn-primary w-full">Sign Up</button>
      </form>
      <p class="mt-3 text-sm subtle">{{ message }}</p>
      <p class="mt-4 text-sm subtle">
        Already have an account?
        <router-link to="/login" class="text-blue-600 hover:underline">Login</router-link>
      </p>
    </div>
  </div>
</template>
