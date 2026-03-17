import { defineStore } from 'pinia'

const AUTH_STORAGE_KEY = 'upao_auth_session'

const defaultState = () => ({
  token: '',
  user: null
})

const loadFromStorage = () => {
  try {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY)
    if (!raw) return defaultState()
    const parsed = JSON.parse(raw)
    return {
      token: parsed.token || '',
      user: parsed.user || null
    }
  } catch {
    return defaultState()
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => loadFromStorage(),

  getters: {
    isAuthenticated: (state) => Boolean(state.token && state.user)
  },

  actions: {
    setSession({ token, user }) {
      this.token = token
      this.user = user
      this.persist()
    },
    clearSession() {
      this.token = ''
      this.user = null
      localStorage.removeItem(AUTH_STORAGE_KEY)
    },
    persist() {
      localStorage.setItem(
        AUTH_STORAGE_KEY,
        JSON.stringify({
          token: this.token,
          user: this.user
        })
      )
    }
  }
})

export { AUTH_STORAGE_KEY }
