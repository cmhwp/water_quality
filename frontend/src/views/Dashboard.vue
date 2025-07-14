<template>
  <div class="dashboard-container" ref="dashboardContainer">
    <!-- 标题 -->
    <div class="dashboard-header">
      <h1>水质监测大屏</h1>
      <div class="header-right">
        <div class="nav-buttons">
          <a-button type="primary" @click="goToMethodsOverview">
            <template #icon>
              <AppstoreOutlined />
            </template>
            方式细分
          </a-button>
          <a-button type="default" @click="goToAdminPanel">
            <template #icon>
              <SettingOutlined />
            </template>
            管理后台
          </a-button>
        </div>
        <div class="update-time">
          最后更新：{{ formatTime(dashboardData?.overview?.latest_update) }}
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="dashboard-content" v-if="dashboardData" :style="{ transform: `scale(${scaleFactor})`, transformOrigin: 'top left' }">
      <!-- 第一行：总览统计 -->
      <div class="overview-section">
        <OverviewStats :data="dashboardData.overview" />
      </div>

      <!-- 第二行：图表区域 -->
      <div class="charts-section">
        <div class="chart-row">
          <!-- 河道统计饼图 -->
          <div class="chart-card">
            <h3>河道统计</h3>
            <RiverDistributionChart :data="processRiverStats(dashboardData.river_stats)" />
          </div>

          <!-- 水质等级分布 -->
          <div class="chart-card">
            <h3>水质等级分布</h3>
            <QualityLevelChart :data="dashboardData.quality_distribution" />
          </div>

          <!-- 月度趋势 -->
          <div class="chart-card wide">
            <h3>月度趋势</h3>
            <MonthlyTrendChart :data="dashboardData.monthly_trend" />
          </div>
        </div>
      </div>

      <!-- 第三行：指标统计和最新数据 -->
      <div class="bottom-section">
        <div class="stats-row">
          <!-- 水质等级统计 -->
          <div class="stats-card">
            <h3>水质等级统计</h3>
            <WaterQualityLevelStats :data="qualityLevelStats" />
          </div>

          <!-- 警告数据 -->
          <div class="stats-card">
            <h3>警告数据(top10)</h3>
            <WarningLevelChart :data="processWarningData(dashboardData.warning_data)" />
          </div>

          <!-- 最新数据 -->
          <div class="stats-card">
            <h3>最新数据</h3>
            <RecentDataTable :data="processRecentData(dashboardData.recent_data)" />
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
import { AppstoreOutlined, SettingOutlined } from '@ant-design/icons-vue'
import { getDashboardDataApiV1DashboardAllGet, getWaterQualityLevelStatisticsApiV1DashboardQualityLevelsGet } from '@/services/api/dashboard'
import OverviewStats from '@/components/dashboard/OverviewStats.vue'
import RiverDistributionChart from '@/components/dashboard/RiverDistributionChart.vue'
import QualityLevelChart from '@/components/dashboard/QualityLevelChart.vue'
import MonthlyTrendChart from '@/components/dashboard/MonthlyTrendChart.vue'
import WaterQualityLevelStats from '@/components/dashboard/WaterQualityLevelStats.vue'
import RecentDataTable from '@/components/dashboard/RecentDataTable.vue'
import WarningLevelChart from '@/components/dashboard/WarningLevelChart.vue'

const router = useRouter()

// 响应式数据
const dashboardData = ref<API.DashboardResponse | null>(null)
const qualityLevelStats = ref<API.WaterQualityLevelStatistics | null>(null)
const loading = ref(true)
const dashboardContainer = ref<HTMLElement>()
const scaleFactor = ref(1)
let refreshTimer: number | null = null

// 获取数据
const fetchDashboardData = async () => {
  try {
    const [dashboardResponse, qualityLevelResponse] = await Promise.all([
      getDashboardDataApiV1DashboardAllGet(),
      getWaterQualityLevelStatisticsApiV1DashboardQualityLevelsGet()
    ])
    
    dashboardData.value = dashboardResponse.data || dashboardResponse
    qualityLevelStats.value = qualityLevelResponse.data || qualityLevelResponse
    loading.value = false
    console.log('Dashboard data loaded:', dashboardResponse)
    console.log('Quality level stats loaded:', qualityLevelResponse)
  } catch (error) {
    console.error('获取大屏数据失败:', error)
    loading.value = false
  }
}

// 导航到方式概览
const goToMethodsOverview = () => {
  router.push('/dashboard/methods')
}

// 导航到管理后台
const goToAdminPanel = () => {
  router.push('/admin')
}

// 处理河道统计数据，确保类型兼容
const processRiverStats = (stats: API.RiverStatistics[]) => {
  return stats.map(stat => ({
    ...stat,
    latest_sampling_date: stat.latest_sampling_date || new Date().toISOString()
  }))
}



// 处理最新数据，确保类型兼容
const processRecentData = (data: API.RecentWaterQuality[]) => {
  return data.map(item => ({
    ...item,
    cod_value: item.cod_value ?? null,
    ammonia_nitrogen_value: item.ammonia_nitrogen_value ?? null,
    total_phosphorus_value: item.total_phosphorus_value ?? null,
    potassium_permanganate_value: item.potassium_permanganate_value ?? null
  }))
}

// 处理警告数据，确保类型兼容
const processWarningData = (data: API.WarningWaterQuality[]) => {
  return data.map(item => ({
    ...item,
    cod_value: item.cod_value ?? null,
    ammonia_nitrogen_value: item.ammonia_nitrogen_value ?? null,
    total_phosphorus_value: item.total_phosphorus_value ?? null,
    potassium_permanganate_value: item.potassium_permanganate_value ?? null
  }))
}

// 计算自适应缩放比例
const calculateScaleFactor = () => {
  if (!dashboardContainer.value) return

  const container = dashboardContainer.value
  const containerWidth = container.clientWidth
  const containerHeight = container.clientHeight
  
  // 基准尺寸（设计稿尺寸）
  const baseWidth = 1920
  const baseHeight = 1080
  
  // 计算缩放比例
  const scaleX = containerWidth / baseWidth
  const scaleY = containerHeight / baseHeight
  
  // 使用较小的缩放比例以确保内容完全显示
  const newScaleFactor = Math.min(scaleX, scaleY, 1)
  
  // 限制最小缩放比例
  scaleFactor.value = Math.max(newScaleFactor, 0.5)
}

// 处理窗口大小变化
const handleResize = () => {
  calculateScaleFactor()
}

// 格式化时间
const formatTime = (date: string | undefined) => {
  if (!date) return '--'
  return new Date(date).toLocaleString('zh-CN')
}

// 组件挂载
onMounted(async () => {
  await fetchDashboardData()
  
  // 等待DOM更新后计算缩放比例
  await nextTick()
  calculateScaleFactor()
  
  // 每30秒刷新一次数据
  refreshTimer = window.setInterval(fetchDashboardData, 30000)
  
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
.dashboard-container {
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

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-buttons {
  display: flex;
  gap: 12px;
}

.update-time {
  font-size: 14px;
  color: #a0a0a0;
}

.dashboard-content {
  padding: 15px 30px;
  width: 1920px;
  height: calc(1080px - 80px);
  position: relative;
  transition: transform 0.3s ease;
}

.overview-section {
  margin-bottom: 20px;
}

.charts-section {
  margin-bottom: 20px;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr;
  gap: 15px;
  margin-bottom: 15px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 300px;
}

.chart-card.wide {
  grid-column: span 1;
}

.chart-card h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #ffffff;
  text-align: center;
}

.bottom-section {
  margin-top: 20px;
}

.stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 15px;
}

.stats-card {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 250px;
}

.stats-card h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #ffffff;
  text-align: center;
}

.loading {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  font-size: 16px;
  color: #a0a0a0;
}

.loading p {
  margin-top: 16px;
}

/* 小屏幕响应式处理 */
@media (max-width: 1400px) {
  .dashboard-header {
    padding: 12px 25px;
  }
  
  .dashboard-header h1 {
    font-size: 28px;
  }
  
  .dashboard-content {
    padding: 12px 25px;
  }
  
  .chart-row {
    gap: 12px;
  }
  
  .stats-row {
    gap: 12px;
  }
  
  .chart-card {
    min-height: 250px;
    padding: 12px;
  }
  
  .stats-card {
    min-height: 200px;
    padding: 12px;
  }
  
  /* 在中等屏幕上将三列改为两列 */
  .stats-row {
    grid-template-columns: 1fr 1fr;
  }
  
  /* 水质等级统计占整行 */
  .stats-card:first-child {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 10px 15px;
    flex-direction: column;
    gap: 8px;
  }
  
  .dashboard-header h1 {
    font-size: 24px;
  }
  
  .dashboard-content {
    padding: 10px 15px;
  }
  
  .chart-row {
    gap: 10px;
  }
  
  .stats-row {
    gap: 10px;
  }
  
  .chart-card {
    min-height: 200px;
    padding: 10px;
  }
  
  .stats-card {
    min-height: 150px;
    padding: 10px;
  }
  
  .chart-card h3,
  .stats-card h3 {
    font-size: 14px;
    margin: 0 0 8px 0;
  }
  
  /* 在小屏幕上改为单列布局 */
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .stats-card:first-child {
    grid-column: 1;
  }
}

/* 全屏适配 */
@media (min-width: 1920px) {
  .dashboard-container {
    overflow: auto;
  }
}

/* 超宽屏适配 */
@media (min-width: 2560px) {
  .dashboard-content {
    transform-origin: top center;
  }
}
</style> 