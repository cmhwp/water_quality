<template>
  <div class="dashboard-container">
    <!-- 头部 -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="dashboard-title">水质监测管理系统</h1>
          <p class="dashboard-subtitle">管理员控制面板</p>
        </div>
        <div class="header-right">
          <a-dropdown placement="bottomRight">
            <a-button type="text" size="large">
              <template #icon>
                <UserOutlined />
              </template>
              {{ authStore.user?.username || '管理员' }}
              <DownOutlined />
            </a-button>
            <template #overlay>
              <a-menu @click="handleMenuClick">
                <a-menu-item key="profile">
                  <UserOutlined />
                  个人资料
                </a-menu-item>
                <a-menu-item key="settings">
                  <SettingOutlined />
                  系统设置
                </a-menu-item>
                <a-menu-item key="dashboard">
                  <DashboardOutlined />
                  返回首页
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="logout">
                  <LogoutOutlined />
                  退出登录
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :sm="12" :md="6">
          <a-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon water-quality">
                <BarChartOutlined />
              </div>
              <div class="stat-info">
                <h3 class="stat-number">{{ statistics.total || 0 }}</h3>
                <p class="stat-label">水质记录总数</p>
              </div>
            </div>
          </a-card>
        </a-col>
        <a-col :xs="24" :sm="12" :md="6">
          <a-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon excellent">
                <CheckCircleOutlined />
              </div>
              <div class="stat-info">
                <h3 class="stat-number">{{ statistics.excellent || 0 }}</h3>
                <p class="stat-label">优秀水质</p>
              </div>
            </div>
          </a-card>
        </a-col>
        <a-col :xs="24" :sm="12" :md="6">
          <a-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon warning">
                <ExclamationCircleOutlined />
              </div>
              <div class="stat-info">
                <h3 class="stat-number">{{ statistics.polluted || 0 }}</h3>
                <p class="stat-label">污染记录</p>
              </div>
            </div>
          </a-card>
        </a-col>
        <a-col :xs="24" :sm="12" :md="6">
          <a-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon rivers">
                <EnvironmentOutlined />
              </div>
              <div class="stat-info">
                <h3 class="stat-number">{{ (statistics.river_stats || []).length }}</h3>
                <p class="stat-label">监测河道</p>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 图表和操作区域 -->
    <div class="content-section">
      <a-row :gutter="[16, 16]">
        <!-- 左侧图表区域 -->
        <a-col :xs="24" :lg="16">
          <a-card title="月度检测趋势" class="chart-card">
            <div ref="chartRef" class="chart-container" style="height: 400px;"></div>
          </a-card>
        </a-col>
        
        <!-- 水质等级分布图 -->
        <a-col :xs="24" :lg="8">
          <a-card title="水质等级分布" class="chart-card">
            <div ref="qualityChartRef" class="chart-container" style="height: 400px;"></div>
          </a-card>
        </a-col>
      </a-row>
      
      <a-row :gutter="[16, 16]" style="margin-top: 16px;">
        <!-- 河道检测统计 -->
        <a-col :xs="24" :lg="16">
          <a-card title="河道检测统计" class="chart-card">
            <div ref="riverChartRef" class="chart-container" style="height: 300px;"></div>
          </a-card>
        </a-col>
        
        <!-- 右侧操作区域 -->
        <a-col :xs="24" :lg="8">
          <a-card title="快速操作" class="action-card">
            <div class="action-list">
              <a-button 
                type="primary" 
                size="large" 
                block 
                class="action-button"
                @click="() => router.push('/admin/water-quality')"
              >
                <template #icon>
                  <PlusOutlined />
                </template>
                添加水质数据
              </a-button>
              
              <a-button 
                size="large" 
                block 
                class="action-button"
                @click="() => router.push('/admin/water-quality')"
              >
                <template #icon>
                  <UnorderedListOutlined />
                </template>
                查看所有数据
              </a-button>
              
              <a-button 
                size="large" 
                block 
                class="action-button"
                @click="exportData"
              >
                <template #icon>
                  <DownloadOutlined />
                </template>
                导出数据
              </a-button>
              
              <a-button 
                size="large" 
                block 
                class="action-button"
                @click="refreshData"
                :loading="loading"
              >
                <template #icon>
                  <ReloadOutlined />
                </template>
                刷新数据
              </a-button>
            </div>
          </a-card>
          
          <!-- 最近添加的数据 -->
          <a-card title="最近添加" class="recent-card">
            <div class="recent-list">
              <div 
                v-for="record in recentRecords" 
                :key="record.id"
                class="recent-item"
              >
                <div class="recent-info">
                  <h4>{{ record.river_name }}</h4>
                  <p>{{ record.sampling_date }}</p>
                </div>
                <div class="recent-status">
                  <a-tag 
                    :color="getQualityColor(record.comprehensive_quality_level)"
                  >
                    {{ record.comprehensive_quality_level }}
                  </a-tag>
                </div>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import * as echarts from 'echarts'
import {
  UserOutlined,
  DownOutlined,
  SettingOutlined,
  LogoutOutlined,
  BarChartOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  EnvironmentOutlined,
  PlusOutlined,
  UnorderedListOutlined,
  DownloadOutlined,
  ReloadOutlined,
  DashboardOutlined
} from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { 
  getWaterQualityStatisticsApiV1WaterQualityStatisticsOverviewGet,
  getWaterQualityListApiV1WaterQualityGet 
} from '@/services/api/waterQuality'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const chartRef = ref<HTMLElement>()
const qualityChartRef = ref<HTMLElement>()
const riverChartRef = ref<HTMLElement>()
const statistics = ref<any>({})
const recentRecords = ref<any[]>([])

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const data = await getWaterQualityStatisticsApiV1WaterQualityStatisticsOverviewGet()
    statistics.value = data
  } catch (error) {
    console.error('Failed to fetch statistics:', error)
  }
}

// 获取最近数据
const fetchRecentRecords = async () => {
  try {
    const data = await getWaterQualityListApiV1WaterQualityGet({
      page: 1,
      per_page: 5
    }) as any
    recentRecords.value = data.items || []
  } catch (error) {
    console.error('Failed to fetch recent records:', error)
  }
}

// 初始化月度趋势图表
const initChart = () => {
  if (!chartRef.value || !statistics.value.monthly_stats) return

  const chart = echarts.init(chartRef.value)
  
  const monthlyData = statistics.value.monthly_stats || []
  const months = monthlyData.map((item: any) => item.month.substring(5) + '月')
  const counts = monthlyData.map((item: any) => item.count)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c} 条记录'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: months,
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value',
      name: '检测记录数'
    },
    series: [
      {
        name: '检测记录',
        type: 'bar',
        data: counts,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#2378f7' },
              { offset: 0.7, color: '#2378f7' },
              { offset: 1, color: '#83bff6' }
            ])
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 初始化水质等级分布图表
const initQualityChart = () => {
  if (!qualityChartRef.value || !statistics.value.quality_stats) return

  const chart = echarts.init(qualityChartRef.value)
  
  const qualityData = statistics.value.quality_stats || []
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '水质等级',
        type: 'pie',
        radius: '50%',
        data: qualityData.map((item: any) => ({
          value: item.count,
          name: item.level
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 初始化河道统计图表
const initRiverChart = () => {
  if (!riverChartRef.value || !statistics.value.river_stats) return

  const chart = echarts.init(riverChartRef.value)
  
  const riverData = statistics.value.river_stats || []
  const rivers = riverData.map((item: any) => item.river_name)
  const counts = riverData.map((item: any) => item.count)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: rivers,
      axisLabel: {
        interval: 0,
        rotate: 0
      }
    },
    series: [
      {
        name: '检测次数',
        type: 'bar',
        data: counts,
        itemStyle: {
          color: '#52c41a'
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 获取水质等级颜色
const getQualityColor = (level: string) => {
  const colorMap: Record<string, string> = {
    'I': 'green',
    'II': 'blue',
    'III': 'yellow',
    'IV': 'orange',
    'V': 'red',
    '劣V': 'purple'
  }
  return colorMap[level] || 'default'
}

// 刷新数据
const refreshData = async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchStatistics(),
      fetchRecentRecords()
    ])
    
    // 重新初始化图表
    nextTick(() => {
      initChart()
      initQualityChart()
      initRiverChart()
    })
    
    message.success('数据刷新成功')
  } catch (error) {
    message.error('数据刷新失败')
  } finally {
    loading.value = false
  }
}

// 导出数据
const exportData = () => {
  message.info('导出功能开发中...')
}

// 菜单点击处理
const handleMenuClick = async ({ key }: { key: string }) => {
  switch (key) {
    case 'profile':
      message.info('个人资料功能开发中...')
      break
    case 'settings':
      message.info('系统设置功能开发中...')
      break
    case 'logout':
      await authStore.logout()
      router.push('/admin/login')
      break
    case 'dashboard':
      router.push('/dashboard')
      break
  }
}

// 初始化
onMounted(async () => {
  await Promise.all([
    fetchStatistics(),
    fetchRecentRecords()
  ])
  
  nextTick(() => {
    initChart()
    initQualityChart()
    initRiverChart()
  })
})
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.dashboard-header {
  background: white;
  padding: 16px 24px;
  border-bottom: 1px solid #e8e8e8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.dashboard-subtitle {
  color: #6b7280;
  margin: 0;
  font-size: 14px;
}

.stats-section {
  padding: 24px;
}

.stat-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.water-quality {
  background: linear-gradient(135deg, #1890ff, #40a9ff);
}

.stat-icon.excellent {
  background: linear-gradient(135deg, #52c41a, #73d13d);
}

.stat-icon.warning {
  background: linear-gradient(135deg, #faad14, #ffc53d);
}

.stat-icon.rivers {
  background: linear-gradient(135deg, #722ed1, #9254de);
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.stat-label {
  color: #6b7280;
  margin: 0;
  font-size: 14px;
}

.content-section {
  padding: 0 24px 24px;
}

.chart-card,
.action-card,
.recent-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 16px;
}

.chart-container {
  width: 100%;
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-button {
  height: 48px;
  border-radius: 8px;
  font-weight: 500;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 6px;
}

.recent-info h4 {
  margin: 0;
  font-size: 14px;
  color: #1f2937;
}

.recent-info p {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 12px 16px;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .stats-section,
  .content-section {
    padding: 16px;
  }
  
  .dashboard-title {
    font-size: 20px;
  }
}
</style> 