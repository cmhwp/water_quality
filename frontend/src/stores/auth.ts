import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginApiV1AuthLoginPost, getCurrentUserInfoApiV1AuthMeGet } from '@/services/api/auth'
import { tokenManager } from '@/utils/request'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<API.UserResponse | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const isAuthenticated = computed(() => {
    return !!user.value && tokenManager.isTokenValid()
  })

  const isAdmin = computed(() => {
    return user.value?.is_admin ?? false
  })

  // 登录
  const login = async (username: string, password: string) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await loginApiV1AuthLoginPost({
        username,
        password
      })
      
      if (response.data) {
        // 保存 token
        tokenManager.setToken(response.data.access_token)
        
        // 保存用户信息
        user.value = response.data.user
        
        return true
      }
      
      return false
    } catch (err: any) {
      error.value = err.response?.data?.message || '登录失败'
      return false
    } finally {
      loading.value = false
    }
  }

  // 退出登录
  const logout = () => {
    tokenManager.removeToken()
    user.value = null
    error.value = null
  }

  // 获取当前用户信息
  const getCurrentUser = async () => {
    if (!tokenManager.isTokenValid()) {
      logout()
      return false
    }

    loading.value = true
    
    try {
      const response = await getCurrentUserInfoApiV1AuthMeGet()
      
      if (response.data) {
        user.value = response.data
        return true
      }
      
      return false
    } catch (err: any) {
      console.error('获取用户信息失败:', err)
      logout()
      return false
    } finally {
      loading.value = false
    }
  }

  // 初始化认证状态
  const initAuth = async () => {
    if (tokenManager.isTokenValid()) {
      await getCurrentUser()
    }
  }

  return {
    // 状态
    user,
    loading,
    error,
    
    // 计算属性
    isAuthenticated,
    isAdmin,
    
    // 方法
    login,
    logout,
    getCurrentUser,
    initAuth
  }
}) 