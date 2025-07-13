<template>
  <div class="methods-overview-container" ref="overviewContainer">
    <!-- 标题 -->
    <div class="dashboard-header">
      <h1>方式细分大屏</h1>
      <div class="nav-buttons">
        <a-button type="primary" @click="goToMainDashboard">
          <template #icon>
            <ArrowLeftOutlined />
          </template>
          返回总览
        </a-button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="methods-content" v-if="methodsData" :style="{ transform: `scale(${scaleFactor})`, transformOrigin: 'top left' }">
      <!-- 方式统计网格 -->
      <div class="methods-grid">
        <div 
          v-for="method in methodsData" 
          :key="method.method"
          class="method-card"
          @click="goToMethodDashboard(method.method)"
        >
          <div class="method-header">
            <h3>{{ method.method }}</h3>
            <div class="method-icon">
              <DatabaseOutlined />
            </div>
          </div>
          
          <div class="method-stats">
            <div class="stat-row">
              <span class="stat-label">总数据量</span>
              <span class="stat-value">{{ method.total_count }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">优质水质</span>
              <span class="stat-value excellent">{{ method.excellent_count }}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">达标率</span>
              <span class="stat-value" :class="getQualityClass(method.excellent_rate)">
                {{ method.excellent_rate }}%
              </span>
            </div>
          </div>
          
          <div class="method-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill excellent"
                :style="{ width: `${method.excellent_rate}%` }"
              ></div>
            </div>
          </div>
          
          <div class="method-footer">
            <span class="update-time">
              最新: {{ formatDate(method.latest_sampling_date) }}
            </span>
            <span class="view-detail">
              查看详情 <ArrowRightOutlined />
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-else class="loading">
      <a-spin size="large" />
      <p>正在加载数据...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftOutlined, ArrowRightOutlined, DatabaseOutlined } from '@ant-design/icons-vue'
import { getMethodStatisticsApiV1DashboardMethodsGet } from '@/services/api/dashboard'

const router = useRouter()

// 响应式数据
const methodsData = ref<API.MethodStatistics[] | null>(null)
const loading = ref(true)
const overviewContainer = ref<HTMLElement>()
const scaleFactor = ref(1)
let refreshTimer: number | null = null

// 获取方式统计数据
const fetchMethodsData = async () => {
  try {
    const response = await getMethodStatisticsApiV1DashboardMethodsGet()
    methodsData.value = response.data || response
    loading.value = false
    console.log('Methods data loaded:', response.data)
  } catch (error) {
    console.error('获取方式统计数据失败:', error)
    loading.value = false
  }
}

// 导航到总览大屏
const goToMainDashboard = () => {
  router.push('/dashboard')
}

// 导航到特定方式的大屏
const goToMethodDashboard = (method: string) => {
  router.push(`/dashboard/method/${encodeURIComponent(method)}`)
}

// 根据达标率获取样式类
const getQualityClass = (rate: number) => {
  if (rate >= 80) return 'excellent'
  if (rate >= 60) return 'good'
  if (rate >= 40) return 'average'
  return 'poor'
}

// 格式化日期
const formatDate = (date: string | null | undefined) => {
  if (!date) return '--'
  return new Date(date).toLocaleDateString('zh-CN')
}

// 计算自适应缩放比例
const calculateScaleFactor = () => {
  if (!overviewContainer.value) return

  const container = overviewContainer.value
  const containerWidth = container.clientWidth
  const containerHeight = container.clientHeight
  
  // 基准尺寸
  const baseWidth = 1920
  const baseHeight = 1080
  
  // 计算缩放比例
  const scaleX = containerWidth / baseWidth
  const scaleY = containerHeight / baseHeight
  
  // 使用较小的缩放比例
  const newScaleFactor = Math.min(scaleX, scaleY, 1)
  
  // 限制最小缩放比例
  scaleFactor.value = Math.max(newScaleFactor, 0.5)
}

// 处理窗口大小变化
const handleResize = () => {
  calculateScaleFactor()
}

// 组件挂载
onMounted(async () => {
  await fetchMethodsData()
  
  // 等待DOM更新后计算缩放比例
  await nextTick()
  calculateScaleFactor()
  
  // 每30秒刷新一次数据
  refreshTimer = window.setInterval(fetchMethodsData, 30000)
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

// 组件卸载
onBeforeUnmount(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.methods-overview-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
  color: #ffffff;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  overflow: hidden;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 10;
}

.dashboard-header h1 {
  font-size: 32px;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(45deg, #4facfe, #00f2fe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-buttons {
  display: flex;
  gap: 12px;
}

.methods-content {
  padding: 40px;
  width: 1920px;
  height: calc(1080px - 80px);
  position: relative;
  transition: transform 0.3s ease;
}

.methods-grid {
  display: flex;
  flex-direction: row;
  gap: 30px;
  max-width: 1600px;
  margin: 0 auto;
  justify-content: center;
  align-items: stretch;
}

.method-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  border-radius: 16px;
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  flex: 1;
  min-width: 300px;
  max-width: 400px;
}

.method-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(79, 172, 254, 0.5);
}

.method-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4facfe, #00f2fe);
}

.method-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.method-header h3 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  color: #ffffff;
}

.method-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #ffffff;
}

.method-stats {
  margin-bottom: 24px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.stat-label {
  font-size: 14px;
  color: #a0a0a0;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}

.stat-value.excellent {
  color: #52c41a;
}

.stat-value.good {
  color: #1890ff;
}

.stat-value.average {
  color: #faad14;
}

.stat-value.poor {
  color: #ff4d4f;
}

.method-progress {
  margin-bottom: 24px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-fill.excellent {
  background: linear-gradient(90deg, #52c41a, #73d13d);
}

.method-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.update-time {
  color: #a0a0a0;
}

.view-detail {
  color: #4facfe;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #ffffff;
}

.loading p {
  margin-top: 16px;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .methods-grid {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .method-card {
    min-width: 280px;
    max-width: 350px;
  }
}

@media (max-width: 768px) {
  .methods-grid {
    flex-direction: column;
    align-items: center;
  }
  
  .method-card {
    padding: 20px;
    min-width: 100%;
    max-width: 100%;
  }
  
  .dashboard-header {
    padding: 15px 20px;
  }
  
  .dashboard-header h1 {
    font-size: 24px;
  }
  
  .methods-content {
    padding: 20px;
  }
}
</style> 