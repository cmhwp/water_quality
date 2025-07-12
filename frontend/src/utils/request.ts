import axios, { type AxiosInstance, type InternalAxiosRequestConfig, type AxiosResponse, type AxiosError } from 'axios'

// 创建axios实例
const request: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    // 直接返回响应数据
    return response.data
  },
  (error: AxiosError) => {
    console.error('Response error:', error)
    
    // 处理不同的错误状态码
    if (error.response) {
      const { status } = error.response
      
      switch (status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          console.error('403 Forbidden: 没有权限访问该资源')
          break
        case 404:
          console.error('404 Not Found: 请求的资源不存在')
          break
        case 500:
          console.error('500 Internal Server Error: 服务器内部错误')
          break
        default:
          console.error(`HTTP Error: ${status}`)
      }
    } else if (error.request) {
      // 网络错误
      console.error('Network error: 请求无响应')
    } else {
      // 其他错误
      console.error('Error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default request
