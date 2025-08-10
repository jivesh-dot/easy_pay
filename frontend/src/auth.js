import { jwtDecode } from 'jwt-decode'

export function isTokenValid() {
  const token = localStorage.getItem('access')
  if (!token) return false
  try {
    const { exp } = jwtDecode(token)
    return Date.now() < exp * 1000  // exp is in seconds, Date.now() in ms
  } catch {
    return false
  }
}
