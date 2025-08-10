import { api } from '../api'

export function createPaymentIntent(payload, token) {
  return api.post('/payment-intents/', payload, {
    headers: { Authorization: `Bearer ${token}` }
  })
}
export function getPaymentIntent(id) {
  return api.get(`/payment-intents/${id}/`)
}
export function patchPaymentIntent(body) {
  // for your merged PATCH endpoint { identifier, status }
  return api.patch('/payment-intents/', body)
}