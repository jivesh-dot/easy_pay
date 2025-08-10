// Generic polling you can reuse anywhere
import { onBeforeUnmount } from 'vue'

export function usePolling(callback, intervalMs = 1000) {
  let timer = null

  function start() {
    stop()
    timer = setInterval(() => {
      try { callback() } catch (e) {  }
    }, intervalMs)
  }

  function stop() {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  onBeforeUnmount(stop)
  return { start, stop }
}
