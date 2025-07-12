import axios from 'axios'
import type { AxiosInstance, AxiosResponse, AxiosError } from 'axios'

// API 基础配置
const API_BASE_URL = 'http://localhost:8000'
const TOKEN_KEY = 'admin_token'

// 消息提示
const showMessage = (message: string, type: 'success' | 'error' | 'warning' = 'error') => {
  console.log(`[${type.toUpperCase()}] ${message}`)
  
  // 创建 toast 元素
  const toast = document.createElement('div')
  toast.className = `alert alert-${type === 'error' ? 'error' : type === 'warning' ? 'warning' : 'success'} fixed top-4 right-4 z-50 w-80 shadow-lg`
  toast.innerHTML = `
    <div class="flex items-center">
      <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
      </svg>
      <span>${message}</span>
    </div>
  `
  
  document.body.appendChild(toast)
  
  // 3秒后自动移除
  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast)
    }
  }, 3000)
}

// 创建 axios 实例
const request: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Token 管理
export const tokenManager = {
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY)
  },
  
  setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token)
  },
  
  removeToken(): void {
    localStorage.removeItem(TOKEN_KEY)
  },
  
  isTokenValid(): boolean {
    const token = this.getToken()
    if (!token) return false
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const exp = payload.exp * 1000 // 转换为毫秒
      return Date.now() < exp
    } catch {
      return false
    }
  }
}

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = tokenManager.getToken()
    if (token && tokenManager.isTokenValid()) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError) => {
    const { response } = error
    
    if (response) {
      switch (response.status) {
        case 401:
          tokenManager.removeToken()
          showMessage('登录已过期，请重新登录')
          // 重定向到登录页面
          window.location.href = '/admin/login'
          break
        case 403:
          showMessage('没有权限访问该资源')
          break
        case 404:
          showMessage('请求的资源不存在')
          break
        case 500:
          showMessage('服务器内部错误')
          break
        default:
          if (response.data && typeof response.data === 'object' && 'message' in response.data) {
            showMessage(response.data.message as string)
          } else {
            showMessage('请求失败')
          }
      }
    } else {
      showMessage('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

export default request 