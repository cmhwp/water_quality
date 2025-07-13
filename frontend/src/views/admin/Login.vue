<template>
  <div class="login-container">
    <div class="login-background">
      <div class="bg-pattern"></div>
    </div>
    
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">水质监测系统</h1>
        <p class="login-subtitle">管理员登录</p>
      </div>
      
      <a-form
        ref="formRef"
        :model="formState"
        :rules="rules"
        layout="vertical"
        @finish="handleLogin"
        class="login-form"
      >
        <a-form-item name="username" label="用户名">
          <a-input
            v-model:value="formState.username"
            size="large"
            placeholder="请输入用户名或邮箱"
            prefix-icon="user"
          >
            <template #prefix>
              <UserOutlined />
            </template>
          </a-input>
        </a-form-item>
        
        <a-form-item name="password" label="密码">
          <a-input-password
            v-model:value="formState.password"
            size="large"
            placeholder="请输入密码"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>
        
        <a-form-item>
          <a-checkbox v-model:checked="formState.rememberMe">
            记住我
          </a-checkbox>
        </a-form-item>
        
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            block
            :loading="loading"
            class="login-button"
          >
            登录
          </a-button>
        </a-form-item>
      </a-form>
      
      <div class="login-footer">
        <a-divider>
          <span class="divider-text">水质监测管理系统</span>
        </a-divider>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance } from 'ant-design-vue'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const formState = reactive({
  username: '',
  password: '',
  rememberMe: false
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少3个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  loading.value = true
  
  try {
    const success = await authStore.login({
      username: formState.username,
      password: formState.password
    })
    
    if (success) {
      // 登录成功，跳转到管理员dashboard
      router.push('/admin/dashboard')
    }
  } catch (error) {
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background-image: linear-gradient( 109.6deg,  rgba(75,228,255,1) 11.2%, rgba(188,204,251,1) 100.6% );
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.bg-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(75, 228, 255, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(188, 204, 251, 0.2) 0%, transparent 50%);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.login-card {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.login-subtitle {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

.login-form {
  margin-top: 24px;
}

.login-button {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
  background: linear-gradient(109.6deg, rgba(75,228,255,1) 11.2%, rgba(188,204,251,1) 100.6%);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(75, 228, 255, 0.3);
}

.login-footer {
  margin-top: 24px;
}

.divider-text {
  color: #9ca3af;
  font-size: 14px;
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
  color: #374151;
}

:deep(.ant-input-affix-wrapper) {
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

:deep(.ant-input-affix-wrapper:focus) {
  border-color: #4be4ff;
  box-shadow: 0 0 0 2px rgba(75, 228, 255, 0.2);
}

:deep(.ant-checkbox-wrapper) {
  color: #6b7280;
}
</style> 