<template>
  <div class="river-chart-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'

interface RiverData {
  river_name: string
  total_count: number
  excellent_count: number
  excellent_rate: number
  latest_sampling_date: string | null | undefined
}

interface Props {
  data: RiverData[]
}

const props = defineProps<Props>()
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  
  // 准备数据
  const chartData = props.data.slice(0, 10).map(item => ({
    name: item.river_name,
    value: item.total_count,
    excellentCount: item.excellent_count,
    excellentRate: item.excellent_rate
  }))
  
  // 配置项
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: 'rgba(255, 255, 255, 0.2)',
      borderWidth: 1,
      textStyle: {
        color: '#ffffff'
      },
      formatter: (params: any) => {
        const data = params.data
        return `
          <div style="padding: 8px;">
            <div style="margin-bottom: 4px; font-weight: bold;">${data.name}</div>
            <div style="margin-bottom: 2px;">总数据量: ${data.value}</div>
            <div style="margin-bottom: 2px;">优质水质: ${data.excellentCount}</div>
            <div>达标率: ${data.excellentRate}%</div>
          </div>
        `
      }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 20,
      bottom: 20,
      textStyle: {
        color: '#ffffff',
        fontSize: 12
      },
      itemWidth: 12,
      itemHeight: 12,
      formatter: (name: string) => {
        const item = chartData.find(d => d.name === name)
        return `${name} (${item?.value || 0})`
      }
    },
    series: [
      {
        name: '河道分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
            color: '#ffffff'
          },
          scale: true,
          scaleSize: 10
        },
        labelLine: {
          show: false
        },
        data: chartData,
        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: (idx: number) => idx * 100
      }
    ],
    color: [
      '#4facfe', '#00f2fe', '#43e97b', '#38f9d7', '#667eea',
      '#764ba2', '#f093fb', '#f5576c', '#ff6b6b', '#ee5a52'
    ]
  }
  
  chart.setOption(option)
  
  // 添加图表交互
  chart.on('click', (params) => {
    console.log('点击了河道:', params.name)
    // 可以在这里添加点击事件处理
  })
}

// 更新图表大小
const resizeChart = () => {
  if (chart) {
    chart.resize()
  }
}

// 监听数据变化
watch(() => props.data, () => {
  if (chart) {
    initChart()
  }
}, { deep: true })

onMounted(() => {
  initChart()
  window.addEventListener('resize', resizeChart)
})

onBeforeUnmount(() => {
  if (chart) {
    chart.dispose()
  }
  window.removeEventListener('resize', resizeChart)
})
</script>

<style scoped>
.river-chart-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart {
  width: 100%;
  height: 350px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chart {
    height: 300px;
  }
}
</style> 