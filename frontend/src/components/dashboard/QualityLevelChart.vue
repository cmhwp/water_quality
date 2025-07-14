<template>
  <div class="quality-chart-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'

interface QualityData {
  level: string
  count: number
  percentage: number
}

interface Props {
  data: QualityData[]
}

const props = defineProps<Props>()
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 获取等级颜色
const getLevelColor = (level: string) => {
  const colors: Record<string, string> = {
    'Ⅰ类': '#43e97b',
    'Ⅱ类': '#38f9d7',
    'Ⅲ类': '#4facfe',
    'Ⅳ类': '#f093fb',
    'Ⅴ类': '#ff6b6b',
    '劣Ⅴ类': '#ee5a52',
    '轻度黑臭': '#795548',
    '重度黑臭': '#2c3e50'
  }
  return colors[level] || '#667eea'
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  
  // 准备数据
  const categories = props.data.map(item => item.level)
  const values = props.data.map(item => item.count)
  const percentages = props.data.map(item => item.percentage)
  
  // 配置项
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: 'rgba(255, 255, 255, 0.2)',
      borderWidth: 1,
      textStyle: {
        color: '#ffffff'
      },
      formatter: (params: any) => {
        const data = params[0]
        const index = data.dataIndex
        const percentage = percentages[index]
        return `
          <div style="padding: 8px;">
            <div style="margin-bottom: 4px; font-weight: bold;">${data.name}</div>
            <div style="margin-bottom: 2px;">数量: ${data.value}</div>
            <div>占比: ${percentage}%</div>
          </div>
        `
      }
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        color: '#ffffff',
        fontSize: 12,
        rotate: 45
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      axisTick: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#ffffff',
        fontSize: 12
      },
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)',
          type: 'dashed'
        }
      }
    },
    series: [
      {
        name: '水质等级分布',
        type: 'bar',
        data: values.map((value, index) => ({
          value,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: getLevelColor(categories[index]) },
              { offset: 1, color: getLevelColor(categories[index]) + '80' }
            ]),
            borderRadius: [4, 4, 0, 0]
          }
        })),
        barWidth: '60%',
        label: {
          show: true,
          position: 'top',
          color: '#ffffff',
          fontSize: 12,
          fontWeight: 'bold'
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#ffffff' },
              { offset: 1, color: '#ffffff80' }
            ])
          }
        },
        animationDelay: (idx: number) => idx * 100
      }
    ],
    animationEasing: 'elasticOut',
    animationDelayUpdate: (idx: number) => idx * 50
  }
  
  chart.setOption(option)
  
  // 添加图表交互
  chart.on('click', (params) => {
    console.log('点击了水质等级:', params.name)
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
.quality-chart-container {
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