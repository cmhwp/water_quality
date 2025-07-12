<template>
  <div class="min-h-screen bg-base-200 flex items-center justify-center">
    <div class="card bg-base-100 shadow-2xl w-full max-w-md">
      <div class="card-body text-center">
        <div class="avatar placeholder mx-auto mb-4">
          <div class="bg-error text-error-content rounded-full w-20">
            <span class="text-4xl">🤖</span>
          </div>
        </div>
        
        <h1 class="text-6xl font-bold text-error mb-4">404</h1>
        
        <h2 class="text-2xl font-semibold text-base-content mb-2">页面未找到</h2>
        
        <p class="text-base-content/70 mb-6">
          抱歉，您访问的页面不存在或已被移除
        </p>
        
        <div class="card-actions justify-center">
          <router-link to="/" class="btn btn-primary btn-wide">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
            </svg>
            返回首页
          </router-link>
        </div>
        
        <div class="divider">或者</div>
        
        <div class="flex justify-center gap-2">
          <router-link to="/admin/login" class="btn btn-outline btn-sm">
            管理员登录
          </router-link>
          <button class="btn btn-outline btn-sm" onclick="history.back()">
            返回上页
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404 页面
</script> 