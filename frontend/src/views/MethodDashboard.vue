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
          <!-- 指标统计 -->
          <div class="stats-card">
            <h3>指标统计</h3>
            <IndicatorStats :data="adaptMethodIndicatorToIndicator(methodDashboardData.indicator_stats)" />
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
import { getMethodDashboardDataApiV1DashboardMethodMethodAllGet } from '@/services/api/dashboard'
import OverviewStats from '@/components/dashboard/OverviewStats.vue'
import RiverDistributionChart from '@/components/dashboard/RiverDistributionChart.vue'
import QualityLevelChart from '@/components/dashboard/QualityLevelChart.vue'
import MonthlyTrendChart from '@/components/dashboard/MonthlyTrendChart.vue'
import IndicatorStats from '@/components/dashboard/IndicatorStats.vue'
import RecentDataTable from '@/components/dashboard/RecentDataTable.vue'

const router = useRouter()
const route = useRoute()

// 响应式数据
const methodDashboardData = ref<API.MethodDashboardResponse | null>(null)
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
    const response = await getMethodDashboardDataApiV1DashboardMethodMethodAllGet({
      method: methodName.value
    })
    methodDashboardData.value = response
    loading.value = false
    console.log('Method dashboard data loaded:', response)
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

// 适配器函数：将方式指标统计转换为指标统计格式
const adaptMethodIndicatorToIndicator = (methodIndicatorStats: API.MethodIndicatorStatistics[]): API.IndicatorStatistics[] => {
  return methodIndicatorStats.map(stat => ({
    indicator_name: stat.indicator_name,
    avg_value: stat.avg_value ?? null,
    max_value: stat.max_value ?? null,
    min_value: stat.min_value ?? null,
    unit: stat.unit,
    standard_value: stat.standard_value ?? null,
    exceed_rate: stat.exceed_rate
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
  color: #a0a0a0;
}

.nav-buttons {
  display: flex;
  gap: 12px;
}

.dashboard-content {
  padding: 20px 40px;
  width: 1920px;
  height: calc(1080px - 80px);
  position: relative;
  transition: transform 0.3s ease;
}

.overview-section {
  margin-bottom: 30px;
}

.charts-section {
  margin-bottom: 30px;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.chart-card.wide {
  grid-column: span 1;
}

.chart-card h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}

.bottom-section {
  margin-bottom: 30px;
}

.stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.stats-card {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stats-card h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
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
  .chart-row {
    grid-template-columns: 1fr 1fr;
  }
  
  .chart-card.wide {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .chart-row {
    grid-template-columns: 1fr;
  }
  
  .chart-card.wide {
    grid-column: span 1;
  }
  
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header {
    padding: 15px 20px;
    flex-direction: column;
    gap: 16px;
  }
  
  .dashboard-header h1 {
    font-size: 24px;
  }
  
  .dashboard-content {
    padding: 20px;
  }
}
</style> 