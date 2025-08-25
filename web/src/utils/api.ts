import axios from 'axios'
import toast from 'react-hot-toast'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          toast.error('Authentication required')
          localStorage.removeItem('auth_token')
          window.location.href = '/login'
          break
        case 403:
          toast.error('Access forbidden')
          break
        case 404:
          toast.error('Resource not found')
          break
        case 500:
          toast.error('Internal server error')
          break
        default:
          toast.error(data?.error || data?.message || 'An error occurred')
      }
    } else if (error.request) {
      toast.error('Network error - please check your connection')
    } else {
      toast.error('An unexpected error occurred')
    }

    return Promise.reject(error)
  }
)

export default api
