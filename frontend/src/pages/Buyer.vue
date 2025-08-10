<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api.js'

const route = useRoute()
const intent = ref(null)
const processing = ref(false)

async function fetchOne() {
  intent.value = (await api.get(`/payment-intents/${route.params.id}/`)).data.data
}

async function pay() {
  processing.value = true
  intent.value = (await api.patch(`/payment-intents/`, {
    identifier: intent.value.id,
    status: 'paid'
  })).data.data
  console.debug(`#buyer#pay intent.value=${intent.value}`)
  processing.value = false
}

onMounted(fetchOne)
</script>

<template>
  <div class="mx-auto max-w-md">
    <div class="card">
      <div v-if="!intent">Loading…</div>
      <div v-else>
        <h2 class="text-xl font-bold">{{ intent.description }}</h2>
        <p class="subtle mt-1">{{ intent.currency }} {{ intent.amount }}</p>
        <p class="mt-2">Status: <span class="font-medium">{{ intent.status }}</span></p>

        <div v-if="intent.status === 'pending'" class="mt-4">
          <button @click="pay" :disabled="processing" class="btn-primary w-full">
            {{ processing ? 'Processing…' : 'Pay now' }}
          </button>
        </div>
        <div v-else-if="intent.status === 'paid'" class="mt-4 text-green-600 font-semibold">
          Payment successful
        </div>
        <div v-else-if="intent.status === 'cancelled'" class="mt-4 text-red-600 font-semibold">
          Payment cancelled
        </div>
      </div>
    </div>
  </div>
</template>
