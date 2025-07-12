<template>
  <div class="min-h-screen bg-base-200">
    <!-- 头部导航 -->
    <div class="navbar bg-base-100 shadow-lg">
      <div class="flex-1">
        <a class="btn btn-ghost normal-case text-xl font-bold">
          <div class="avatar placeholder mr-2">
            <div class="bg-primary text-primary-content rounded-full w-8">
              <span class="text-xs">💧</span>
            </div>
          </div>
          水质数据管理系统
        </a>
      </div>
      <div class="flex-none gap-2">
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-ghost">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            关于
          </div>
          <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
            <li><a>系统简介</a></li>
            <li><a>技术支持</a></li>
            <li><a>联系我们</a></li>
          </ul>
        </div>
        <router-link to="/admin/login" class="btn btn-primary">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          管理员登录
        </router-link>
      </div>
    </div>

    <!-- 主内容 -->
    <div class="container mx-auto px-4 py-8">
      <!-- 欢迎区域 -->
      <div class="hero min-h-96 bg-gradient-to-br from-primary to-secondary rounded-3xl mb-8 text-primary-content">
        <div class="hero-content text-center">
          <div class="max-w-3xl">
            <div class="text-6xl mb-4">🌊</div>
            <h1 class="text-5xl font-bold mb-4">水质数据可视化大屏</h1>
            <p class="text-xl opacity-90 mb-8">实时监控和分析水质数据，保护水环境，建设美丽中国</p>
            <div class="flex justify-center gap-4">
              <button class="btn btn-lg btn-accent">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                数据大屏
              </button>
              <button class="btn btn-lg btn-outline btn-accent">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                技术文档
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能预览卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300 border border-primary/20">
          <div class="card-body text-center">
            <div class="avatar placeholder mx-auto mb-4">
              <div class="bg-primary text-primary-content rounded-full w-16">
                <span class="text-2xl">📊</span>
              </div>
            </div>
            <h2 class="card-title justify-center text-primary">数据统计</h2>
            <p class="text-base-content/70">实时水质数据统计分析，多维度展示环境状况</p>
            <div class="card-actions justify-center mt-4">
              <button class="btn btn-primary btn-sm">查看详情</button>
            </div>
          </div>
        </div>
        
        <div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300 border border-secondary/20">
          <div class="card-body text-center">
            <div class="avatar placeholder mx-auto mb-4">
              <div class="bg-secondary text-secondary-content rounded-full w-16">
                <span class="text-2xl">🗺️</span>
              </div>
            </div>
            <h2 class="card-title justify-center text-secondary">地理分布</h2>
            <p class="text-base-content/70">各河道水质地理分布图，直观展示污染源</p>
            <div class="card-actions justify-center mt-4">
              <button class="btn btn-secondary btn-sm">查看详情</button>
            </div>
          </div>
        </div>
        
        <div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300 border border-accent/20">
          <div class="card-body text-center">
            <div class="avatar placeholder mx-auto mb-4">
              <div class="bg-accent text-accent-content rounded-full w-16">
                <span class="text-2xl">📈</span>
              </div>
            </div>
            <h2 class="card-title justify-center text-accent">趋势分析</h2>
            <p class="text-base-content/70">水质变化趋势分析，预测环境发展动向</p>
            <div class="card-actions justify-center mt-4">
              <button class="btn btn-accent btn-sm">查看详情</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据展示区域 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 实时数据 -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">
              <div class="badge badge-success badge-sm mr-2">实时</div>
              监测数据
            </h2>
            <div class="stats shadow">
              <div class="stat">
                <div class="stat-title">监测点</div>
                <div class="stat-value text-primary">437</div>
                <div class="stat-desc">个活跃监测点</div>
              </div>
              <div class="stat">
                <div class="stat-title">数据更新</div>
                <div class="stat-value text-secondary">5分钟</div>
                <div class="stat-desc">前最后更新</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 水质等级分布 -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">水质等级分布</h2>
            <div class="flex flex-col gap-2">
              <div class="flex justify-between items-center">
                <span class="badge badge-success">I类</span>
                <progress class="progress progress-success w-20" value="30" max="100"></progress>
                <span class="text-sm">30%</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="badge badge-info">II类</span>
                <progress class="progress progress-info w-20" value="25" max="100"></progress>
                <span class="text-sm">25%</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="badge badge-warning">III类</span>
                <progress class="progress progress-warning w-20" value="20" max="100"></progress>
                <span class="text-sm">20%</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="badge badge-error">IV类</span>
                <progress class="progress progress-error w-20" value="15" max="100"></progress>
                <span class="text-sm">15%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 占位符大屏 -->
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title text-center justify-center text-2xl mb-8">
            <span class="loading loading-ring loading-lg text-primary mr-2"></span>
            数据可视化大屏
          </h2>
          <div class="hero min-h-96 bg-base-200 rounded-2xl">
            <div class="hero-content text-center">
              <div class="max-w-md">
                <div class="text-6xl mb-4">🚧</div>
                <h3 class="text-2xl font-bold text-base-content mb-4">功能开发中</h3>
                <p class="text-base-content/70 mb-6">数据可视化大屏正在开发中，敬请期待...</p>
                <div class="flex justify-center gap-2">
                  <div class="badge badge-primary">实时监控</div>
                  <div class="badge badge-secondary">数据分析</div>
                  <div class="badge badge-accent">趋势预测</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部 -->
    <footer class="footer footer-center p-10 bg-primary text-primary-content rounded-t-3xl mt-16">
      <div>
        <div class="avatar placeholder mb-4">
          <div class="bg-primary-content text-primary rounded-full w-12">
            <span class="text-xl">💧</span>
          </div>
        </div>
        <p class="font-bold text-xl">水质数据管理系统</p>
        <p class="opacity-90">保护水环境，从数据监测开始</p>
      </div>
      <div>
        <div class="grid grid-flow-col gap-4">
          <a class="link link-hover">关于我们</a>
          <a class="link link-hover">联系方式</a>
          <a class="link link-hover">隐私政策</a>
          <a class="link link-hover">使用条款</a>
        </div>
      </div>
      <div>
        <p class="opacity-75">© 2024 水质数据管理系统 - 技术支持</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 暂时空白，后续可以添加统计数据获取逻辑
</script>

<style scoped>
.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}
</style> 