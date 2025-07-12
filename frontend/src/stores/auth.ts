import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { message } from 'ant-design-vue'
import { 
  loginApiV1AuthLoginPost, 
  logoutApiV1AuthLogoutPost, 
  getCurrentUserInfoApiV1AuthMeGet 
} from '@/services/api/auth'


export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<API.UserResponse | null>(null)
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin ?? false)

  // 登录
  const login = async (credentials: API.UserLogin) => {
    loading.value = true
    try {
      const response = await loginApiV1AuthLoginPost(credentials)
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('token', response.access_token)
      message.success('登录成功')
      return true
    } catch (error) {
      message.error('登录失败，请检查用户名和密码')
      return false
    } finally {
      loading.value = false
    }
  }

  // 登出
  const logout = async () => {
    try {
      await logoutApiV1AuthLogoutPost()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      message.success('已退出登录')
    }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    if (!token.value) return false
    
    try {
      const userInfo = await getCurrentUserInfoApiV1AuthMeGet()
      user.value = userInfo
      return true
    } catch (error) {
      console.error('Failed to fetch user info:', error)
      // 如果获取用户信息失败，可能是token过期
      await logout()
      return false
    }
  }

  // 初始化
  const init = async () => {
    if (token.value) {
      await fetchUserInfo()
    }
  }

  return {
    // 状态
    token,
    user,
    loading,
    // 计算属性
    isAuthenticated,
    isAdmin,
    // 方法
    login,
    logout,
    fetchUserInfo,
    init
  }
}) 