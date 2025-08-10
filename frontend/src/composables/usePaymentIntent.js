// src/composables/usePaymentIntent.js
import { ref, watch, onBeforeUnmount } from 'vue'
import QRCode from 'qrcode'
import { api } from '../api'
import { usePolling } from './usePolling'

export function usePaymentIntent({ frontEndUrl, getToken, onUnauthorized } = {}) {
  const amount = ref(111)
  const currency = ref('AED')
  const description = ref('Demo item')

  const id = ref('')
  const status = ref('')
  const link = ref('')
  const qrcanvas = ref(null)

  async function refresh() {
    if (!id.value) return
    try {
      const res = await api.get(`/payment-intents/${id.value}/`)
      const data = res.data?.data ?? res.data
      status.value = data.status
      if (['paid', 'cancelled'].includes(String(status.value).toLowerCase())) {
        polling.stop()
      }
    } catch (err) {
      if (err?.response?.status === 401 && typeof onUnauthorized === 'function') {
        polling.stop()
        onUnauthorized()
      }
    }
  }

  const polling = usePolling(refresh, 1000)

  watch(link, async (val) => {
    if (!val || !qrcanvas.value) return
    try {
      await QRCode.toCanvas(qrcanvas.value, val, { width: 220, margin: 2, errorCorrectionLevel: 'M' })
      polling.start()
    } catch (e) {
      console.error('QR render failed:', e)
    }
  }, { flush: 'post' }) 

  async function makeLink() {
    id.value = ''
    status.value = ''
    link.value = ''

    try {
      const res = await api.post(
        '/payment-intents/',
        { amount: Number(amount.value), currency: currency.value, description: description.value },
        { headers: { Authorization: `Bearer ${getToken?.()}` } }
      )

      const data = res.data?.data ?? res.data
      id.value = data.id
      status.value = data.status

      const fe = frontEndUrl || `${location.protocol}//${location.host}`
      link.value = `${fe}/#/pay/${id.value}`
    } catch (err) {
      if (err?.response?.status === 401 && typeof onUnauthorized === 'function') {
        onUnauthorized()
        return
      }
      console.error('PaymentIntent creation failed:', err)
      throw err
    }
  }

  onBeforeUnmount(() => {
    polling.stop()
  })

  return {
    amount, currency, description,
    id, status, link, qrcanvas,
    makeLink, refresh,
    startPolling: polling.start,
    stopPolling: polling.stop,
  }
}
