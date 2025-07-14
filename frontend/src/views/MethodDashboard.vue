<template>
  <div class="method-dashboard-container" ref="dashboardContainer">
    <!-- 标题 -->
    <div class="dashboard-header">
      <div class="header-left">
        <h1>{{ methodName }} - 方式细分大屏</h1>
        <div class="update-time">
          最后更新：{{ formatTime(methodDashboardData?.overview?.latest_update) }}
        </div>
      </div>
      <div class="nav-buttons">
        <a-button @click="goToMethodsOverview">
          <template #icon>
            <AppstoreOutlined />
          </template>
          方式概览
        </a-button>
        <a-button type="primary" @click="goToMainDashboard">
          <template #icon>
            <ArrowLeftOutlined />
          </template>
          返回总览
        </a-button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="dashboard-content" v-if="methodDashboardData" :style="{ transform: `scale(${scaleFactor})`, transformOrigin: 'top left' }">
      <!-- 第一行：总览统计 -->
      <div class="overview-section">
        <OverviewStats :data="adaptMethodOverviewToOverview(methodDashboardData.overview)" />
      </div>

      <!-- 第二行：图表区域 -->
      <div class="charts-section">
        <div class="chart-row">
          <!-- 河道统计饼图 -->
          <div class="chart-card">
            <h3>河道统计</h3>
            <RiverDistributionChart :data="adaptMethodRiverStatsToRiverStats(methodDashboardData.river_stats)" />
          </div>

          <!-- 水质等级分布 -->
          <div class="chart-card">
            <h3>水质等级分布</h3>
            <QualityLevelChart :data="adaptMethodQualityToQuality(methodDashboardData.quality_distribution)" />
          </div>

          <!-- 月度趋势 -->
          <div class="chart-card wide">
            <h3>月度趋势</h3>
            <MonthlyTrendChart :data="adaptMethodMonthlyToMonthly(methodDashboardData.monthly_trend)" />
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
            <WarningLevelChart :data="processWarningData(methodDashboardData.warning_data)" />
          </div>

          <!-- 最新数据 -->
          <div class="stats-card">
            <h3>最新数据</h3>
            <RecentDataTable :data="processRecentData(methodDashboardData.recent_data)" />
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-else class="loading">
      <a-spin size="large" />
      <p>正在加载{{ methodName }}的数据...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeftOutlined, AppstoreOutlined } from '@ant-design/icons-vue'
import { getMethodDashboardDataApiV1DashboardMethodMethodAllGet, getWaterQualityLevelStatisticsApiV1DashboardQualityLevelsGet } from '@/services/api/dashboard'
import OverviewStats from '@/components/dashboard/OverviewStats.vue'
import RiverDistributionChart from '@/components/dashboard/RiverDistributionChart.vue'
import QualityLevelChart from '@/components/dashboard/QualityLevelChart.vue'
import MonthlyTrendChart from '@/components/dashboard/MonthlyTrendChart.vue'
import WaterQualityLevelStats from '@/components/dashboard/WaterQualityLevelStats.vue'
import RecentDataTable from '@/components/dashboard/RecentDataTable.vue'
import WarningLevelChart from '@/components/dashboard/WarningLevelChart.vue'

const router = useRouter()
const route = useRoute()

// 响应式数据
const methodDashboardData = ref<API.MethodDashboardResponse | null>(null)
const qualityLevelStats = ref<API.WaterQualityLevelStatistics | null>(null)
const loading = ref(true)
const dashboardContainer = ref<HTMLElement>()
const scaleFactor = ref(1)
let refreshTimer: number | null = null

// 计算方式名称
const methodName = computed(() => {
  return decodeURIComponent(route.params.method as string)
})

// 获取方式大屏数据
const fetchMethodDashboardData = async () => {
  try {
    const [methodResponse, qualityLevelResponse] = await Promise.all([
      getMethodDashboardDataApiV1DashboardMethodMethodAllGet({
        method: methodName.value
      }),
      getWaterQualityLevelStatisticsApiV1DashboardQualityLevelsGet()
    ])
    
    methodDashboardData.value = methodResponse
    qualityLevelStats.value = qualityLevelResponse.data || qualityLevelResponse
    loading.value = false
    console.log('Method dashboard data loaded:', methodResponse)
    console.log('Quality level stats loaded:', qualityLevelResponse)
  } catch (error) {
    console.error('获取方式大屏数据失败:', error)
    loading.value = false
  }
}

// 导航到总览大屏
const goToMainDashboard = () => {
  router.push('/dashboard')
}

// 导航到方式概览
const goToMethodsOverview = () => {
  router.push('/dashboard/methods')
}

// 适配器函数：将方式总览统计转换为总览统计格式
const adaptMethodOverviewToOverview = (methodOverview: API.MethodOverviewStatistics): API.OverviewStatistics => {
  return {
    total_records: methodOverview.total_records,
    excellent_count: methodOverview.excellent_count,
    good_count: methodOverview.good_count,
    poor_count: methodOverview.poor_count,
    very_poor_count: methodOverview.very_poor_count,
    polluted_count: methodOverview.polluted_count,
    excellent_rate: methodOverview.excellent_rate,
    latest_update: methodOverview.latest_update
  }
}

// 适配器函数：将方式河道统计转换为河道统计格式
const adaptMethodRiverStatsToRiverStats = (methodRiverStats: API.MethodRiverStatistics[]): API.RiverStatistics[] => {
  return methodRiverStats.map(stat => ({
    river_name: stat.river_name,
    total_count: stat.total_count,
    excellent_count: stat.excellent_count,
    good_count: stat.good_count,
    poor_count: stat.poor_count,
    very_poor_count: stat.very_poor_count,
    polluted_count: stat.polluted_count,
    excellent_rate: stat.excellent_rate,
    latest_sampling_date: stat.latest_sampling_date || new Date().toISOString()
  }))
}

// 适配器函数：将方式水质等级分布转换为水质等级分布格式
const adaptMethodQualityToQuality = (methodQualityDist: API.MethodQualityDistribution[]): API.QualityLevelDistribution[] => {
  return methodQualityDist.map(dist => ({
    level: dist.level,
    count: dist.count,
    percentage: dist.percentage
  }))
}

// 适配器函数：将方式月度趋势转换为月度趋势格式
const adaptMethodMonthlyToMonthly = (methodMonthlyTrend: API.MethodMonthlyTrend[]): API.MonthlyTrend[] => {
  return methodMonthlyTrend.map(trend => ({
    month: trend.month,
    total_count: trend.total_count,
    excellent_count: trend.excellent_count,
    excellent_rate: trend.excellent_rate
  }))
}



// 处理最新数据
const processRecentData = (data: API.RecentWaterQuality[]) => {
  return data.map(item => ({
    ...item,
    cod_value: item.cod_value ?? null,
    ammonia_nitrogen_value: item.ammonia_nitrogen_value ?? null,
    total_phosphorus_value: item.total_phosphorus_value ?? null,
    potassium_permanganate_value: item.potassium_permanganate_value ?? null
  }))
}

// 处理警告数据
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
  await fetchMethodDashboardData()
  
  // 等待DOM更新后计算缩放比例
  await nextTick()
  calculateScaleFactor()
  
  // 每30秒刷新一次数据
  refreshTimer = window.setInterval(fetchMethodDashboardData, 30000)
  
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
.method-dashboard-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  color: #212529;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  overflow: hidden;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
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

.update-time {
  font-size: 14px;
  color: #6c757d;
}

.nav-buttons {
  display: flex;
  gap: 12px;
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
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  min-height: 300px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-card.wide {
  grid-column: span 1;
}

.chart-card h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #212529;
  text-align: center;
}

.bottom-section {
  margin-bottom: 20px;
}

.stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 15px;
}

.stats-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  min-height: 250px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stats-card h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #212529;
  text-align: center;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #212529;
}

.loading p {
  margin-top: 16px;
  font-size: 16px;
}

/* 响应式设计 */
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
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  
  .chart-card {
    min-height: 250px;
    padding: 12px;
  }
  
  .chart-card.wide {
    grid-column: span 2;
  }
  
  /* 在中等屏幕上将三列改为两列 */
  .stats-row {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  
  .stats-card {
    min-height: 200px;
    padding: 12px;
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
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .chart-card {
    min-height: 200px;
    padding: 10px;
  }
  
  .chart-card.wide {
    grid-column: span 1;
  }
  
  .chart-card h3,
  .stats-card h3 {
    font-size: 14px;
    margin: 0 0 8px 0;
  }
  
  /* 在小屏幕上改为单列布局 */
  .stats-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .stats-card {
    min-height: 150px;
    padding: 10px;
  }
  
  .stats-card:first-child {
    grid-column: 1;
  }
}
</style> 