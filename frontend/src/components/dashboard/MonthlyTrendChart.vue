<template>
  <div class="trend-chart-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'

interface TrendData {
  month: string
  total_count: number
  excellent_count: number
  excellent_rate: number
}

interface Props {
  data: TrendData[]
}

const props = defineProps<Props>()
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  
  // 准备数据
  const months = props.data.map(item => item.month)
  const totalCounts = props.data.map(item => item.total_count)
  const excellentCounts = props.data.map(item => item.excellent_count)
  const excellentRates = props.data.map(item => item.excellent_rate)
  
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
        const month = params[0].name
        const total = params[0].value
        const excellent = params[1].value
        const rate = params[2].value
        return `
          <div style="padding: 8px;">
            <div style="margin-bottom: 4px; font-weight: bold;">${month}</div>
            <div style="margin-bottom: 2px;">总数据量: ${total}</div>
            <div style="margin-bottom: 2px;">优质水质: ${excellent}</div>
            <div>达标率: ${rate}%</div>
          </div>
        `
      }
    },
    legend: {
      data: ['总数据量', '优质水质', '达标率'],
      textStyle: {
        color: '#212529',
        fontSize: 12
      },
      top: 10,
      right: 20
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: months,
      axisLabel: {
        color: '#212529',
        fontSize: 12,
        rotate: 45
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.3)'
        }
      },
      axisTick: {
        show: false
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '数量',
        position: 'left',
        axisLabel: {
          color: '#212529',
          fontSize: 12
        },
        nameTextStyle: {
          color: '#212529',
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
            color: 'rgba(0, 0, 0, 0.1)',
            type: 'dashed'
          }
        }
      },
      {
        type: 'value',
        name: '达标率(%)',
        position: 'right',
        axisLabel: {
          color: '#212529',
          fontSize: 12,
          formatter: '{value}%'
        },
        nameTextStyle: {
          color: '#212529',
          fontSize: 12
        },
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        splitLine: {
          show: false
        }
      }
    ],
    series: [
      {
        name: '总数据量',
        type: 'bar',
        data: totalCounts,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#4facfe' },
            { offset: 1, color: '#4facfe80' }
          ]),
          borderRadius: [2, 2, 0, 0]
        },
        barWidth: '30%',
        animationDelay: (idx: number) => idx * 100
      },
      {
        name: '优质水质',
        type: 'bar',
        data: excellentCounts,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#43e97b' },
            { offset: 1, color: '#43e97b80' }
          ]),
          borderRadius: [2, 2, 0, 0]
        },
        barWidth: '30%',
        animationDelay: (idx: number) => idx * 100 + 50
      },
      {
        name: '达标率',
        type: 'line',
        yAxisIndex: 1,
        data: excellentRates,
        lineStyle: {
          color: '#f093fb',
          width: 3
        },
        itemStyle: {
          color: '#f093fb',
          borderColor: '#ffffff',
          borderWidth: 2
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#f093fb30' },
            { offset: 1, color: '#f093fb10' }
          ])
        },
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        animationDelay: (idx: number) => idx * 100 + 100
      }
    ],
    animationEasing: 'elasticOut',
    animationDelayUpdate: (idx: number) => idx * 50
  }
  
  chart.setOption(option)
  
  // 添加图表交互
  chart.on('click', (params) => {
    console.log('点击了月份:', params.name)
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
.trend-chart-container {
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