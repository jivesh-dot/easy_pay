<script setup>
import { onMounted } from 'vue'
import { frontEndUrl } from '../api'
import { usePaymentIntent } from '../composables/usePaymentIntent'

function getToken() {
  return localStorage.getItem('access')
}
function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  window.location.href = '#/login'
}

const {
  amount, currency, description,
  link, status, qrcanvas, makeLink
} = usePaymentIntent({ frontEndUrl, getToken, onUnauthorized: logout })

onMounted(() => {
  if (!getToken()) window.location.href = '#/login'
})
</script>

<template>
  <div class="min-h-screen flex items-start justify-center px-4 py-10">
    <div class="w-full max-w-5xl">
      <div class="flex items-start justify-between mb-8">
        <div class="text-left">
          <h1 class="text-4xl font-extrabold text-gray-900">Create Payment QR</h1>
          <p class="text-gray-600 mt-2 text-lg">Quickly generate a link or QR code your buyer can scan to pay.</p>
        </div>
        <button @click="logout" class="btn-secondary">Logout</button>
      </div>

      <div class="grid gap-8 md:grid-cols-2">
        <div class="bg-white rounded-xl shadow-lg p-6">
          <form @submit.prevent="makeLink" class="space-y-4">
            <input v-model.number="amount" type="number" step="0.01" min="0.01"
                   placeholder="Amount"
                   class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <select v-model="currency" class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option>AED</option><option>USD</option><option>EUR</option><option>INR</option>
            </select>
            <input v-model="description" placeholder="Description"
                   class="w-full border rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <button type="submit"
                    :disabled="!amount || Number(amount) <= 0"
                    class="w-full bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-white py-3 rounded-lg hover:bg-blue-700 transition">
              Create link
            </button>
          </form>
        </div>

        <div v-show="!!link" class="bg-white rounded-xl shadow-lg p-6 text-center animate-fade-in">
          <p class="text-sm mb-2">
            <strong>Link:</strong>
            <a :href="link" target="_blank" class="text-blue-600 underline break-all">{{ link }}</a>
          </p>
          <canvas ref="qrcanvas" class="mt-4 mx-auto"></canvas>

          <div class="mt-4">
            <span v-if="status === 'pending'" class="text-gray-500 text-lg animate-pulse">⏳ Status: Pending...</span>
            <span v-else-if="status === 'paid'" class="text-green-600 font-bold text-xl animate-bounce">⚡️ Payment Successful!</span>
            <span v-else-if="status === 'cancelled'" class="text-red-600 font-bold text-xl">❗ Payment Cancelled</span>
            <span v-else class="text-gray-700 text-lg">Status: {{ status }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
.animate-fade-in { animation: fadeIn .4s ease-in-out; }
</style>
