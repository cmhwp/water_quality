import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 大屏可视化路由（公开访问）
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { public: true }
    },
    {
      path: '/dashboard/methods',
      name: 'dashboard-methods',
      component: () => import('../views/MethodsOverview.vue'),
      meta: { public: true }
    },
    {
      path: '/dashboard/method/:method',
      name: 'dashboard-method',
      component: () => import('../views/MethodDashboard.vue'),
      meta: { public: true }
    },
    
    // 管理员路由
    {
      path: '/admin',
      redirect: '/admin/dashboard',
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('../views/admin/Login.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/admin/Dashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/water-quality',
      name: 'admin-water-quality',
      component: () => import('../views/admin/WaterQuality.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
  ],
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 如果是公开路由，直接通过
  if (to.meta.public) {
    next()
    return
  }
  
  // 初始化用户信息
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.init()
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      next('/admin/login')
      return
    }
    
    // 检查是否需要管理员权限
    if (to.meta.requiresAdmin && !authStore.isAdmin) {
      next('/admin/login')
      return
    }
  }
  
  // 检查是否需要访客权限（已登录用户不能访问登录页）
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/admin/dashboard')
    return
  }
  
  next()
})

export default router
