<template>
  <div class="min-h-screen bg-base-200">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20"></div>
    
    <!-- 返回首页按钮 -->
    <div class="absolute top-4 left-4 z-10">
      <router-link to="/" class="btn btn-ghost btn-sm">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        返回首页
      </router-link>
    </div>

    <div class="relative flex items-center justify-center min-h-screen p-4">
      <div class="w-full max-w-md">
        <!-- 登录卡片 -->
        <div class="card bg-base-100 shadow-2xl">
          <div class="card-body">
            <!-- 标题区域 -->
            <div class="text-center mb-8">
              <div class="avatar placeholder mx-auto mb-4">
                <div class="bg-primary text-primary-content rounded-full w-16">
                  <span class="text-2xl">🔐</span>
                </div>
              </div>
              <h2 class="text-3xl font-bold text-primary mb-2">管理员登录</h2>
              <p class="text-base-content/70">水质数据管理系统</p>
            </div>
            
            <!-- 错误提示 -->
            <div v-if="authStore.error" class="alert alert-error mb-6">
              <svg class="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
              </svg>
              <span>{{ authStore.error }}</span>
            </div>
            
            <form @submit.prevent="handleLogin" class="space-y-6">
              <!-- 用户名输入 -->
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-medium">用户名或邮箱</span>
                </label>
                <div class="relative">
                  <input 
                    v-model="form.username" 
                    type="text" 
                    placeholder="请输入用户名或邮箱" 
                    class="input input-bordered w-full pl-10"
                    :class="{ 'input-error': errors.username }"
                    required
                  >
                  <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-base-content/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <label v-if="errors.username" class="label">
                  <span class="label-text-alt text-error">{{ errors.username }}</span>
                </label>
              </div>
              
              <!-- 密码输入 -->
              <div class="form-control">
                <label class="label">
                  <span class="label-text font-medium">密码</span>
                </label>
                <div class="relative">
                  <input 
                    v-model="form.password" 
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="请输入密码" 
                    class="input input-bordered w-full pl-10 pr-10"
                    :class="{ 'input-error': errors.password }"
                    required
                  >
                  <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-base-content/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                  <button 
                    type="button" 
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-base-content/50 hover:text-base-content transition-colors"
                  >
                    <svg v-if="showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                    </svg>
                  </button>
                </div>
                <label v-if="errors.password" class="label">
                  <span class="label-text-alt text-error">{{ errors.password }}</span>
                </label>
              </div>
              
              <!-- 记住密码 -->
              <div class="form-control">
                <label class="label cursor-pointer justify-start">
                  <input type="checkbox" class="checkbox checkbox-primary checkbox-sm mr-2" />
                  <span class="label-text">记住我</span>
                </label>
              </div>
              
              <!-- 登录按钮 -->
              <div class="form-control mt-8">
                <button 
                  type="submit" 
                  class="btn btn-primary w-full"
                  :class="{ 'loading': authStore.loading }"
                  :disabled="authStore.loading"
                >
                  <svg v-if="!authStore.loading" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
                  </svg>
                  {{ authStore.loading ? '登录中...' : '登录' }}
                </button>
              </div>
            </form>
            
            <!-- 分割线 -->
            <div class="divider">默认账户信息</div>
            
            <!-- 默认账户信息 -->
            <div class="bg-base-200 rounded-lg p-4 text-center">
              <div class="text-sm text-base-content/70 mb-2">
                <div class="badge badge-outline badge-sm mr-2">邮箱</div>
                admin@waterquality.com
              </div>
              <div class="text-sm text-base-content/70">
                <div class="badge badge-outline badge-sm mr-2">密码</div>
                admin123
              </div>
            </div>
            
            <!-- 快速填充按钮 -->
            <div class="form-control mt-4">
              <button 
                type="button" 
                @click="fillDefaultAccount"
                class="btn btn-outline btn-sm"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                快速填充
              </button>
            </div>
          </div>
        </div>
        
        <!-- 额外信息 -->
        <div class="text-center mt-6">
          <p class="text-sm text-base-content/60">
            如有技术问题，请联系系统管理员
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 表单数据
const form = reactive({
  username: '',
  password: ''
})

// 表单验证错误
const errors = ref<{ username?: string; password?: string }>({})

// 密码显示控制
const showPassword = ref(false)

// 验证表单
const validateForm = () => {
  errors.value = {}
  
  if (!form.username.trim()) {
    errors.value.username = '请输入用户名或邮箱'
  }
  
  if (!form.password.trim()) {
    errors.value.password = '请输入密码'
  }
  
  return Object.keys(errors.value).length === 0
}

// 处理登录
const handleLogin = async () => {
  if (!validateForm()) {
    return
  }
  
  const success = await authStore.login(form.username, form.password)
  
  if (success) {
    router.push('/admin/dashboard')
  }
}

// 快速填充默认账户
const fillDefaultAccount = () => {
  form.username = 'admin@waterquality.com'
  form.password = 'admin123'
  errors.value = {}
}

// 检查登录状态
onMounted(async () => {
  await authStore.initAuth()
  
  if (authStore.isAuthenticated && authStore.isAdmin) {
    router.push('/admin/dashboard')
  }
})
</script>

<style scoped>
.card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}
</style> 