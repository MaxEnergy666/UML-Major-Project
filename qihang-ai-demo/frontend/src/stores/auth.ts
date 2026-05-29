import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

interface User {
  id: number
  username: string
  phone: string
  name: string
  role: string
  is_verified: boolean
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(username: string, password: string) {
    const res = await api.post('/auth/login/', { username, password })
    token.value = res.data.token
    localStorage.setItem('token', res.data.token)
    await fetchUser()
  }

  async function fetchUser() {
    try {
      const res = await api.get('/auth/me/')
      user.value = res.data
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { token, user, isAuthenticated, isAdmin, login, fetchUser, logout }
})
