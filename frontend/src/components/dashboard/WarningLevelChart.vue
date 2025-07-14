<template>
  <div class="warning-chart-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'

interface WarningData {
  id: number
  river_name: string
  sampling_date: string
  comprehensive_quality_level: string
  warning_level: string
  cod_value: number | null | undefined
  ammonia_nitrogen_value: number | null | undefined
  total_phosphorus_value: number | null | undefined
  potassium_permanganate_value: number | null | undefined
}

interface Props {
  data: WarningData[]
}

const props = defineProps<Props>()
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 获取警告等级颜色
const getWarningLevelColor = (level: string) => {
  const colors: Record<string, string> = {
    'poor': '#FF9800',           // Ⅴ类 - 橙色
    'very_poor': '#E91E63',      // 劣Ⅴ类 - 粉红色
    'light_polluted': '#9C27B0', // 轻度黑臭 - 紫色
    'polluted': '#795548'        // 重度黑臭 - 褐色
  }
  return colors[level] || '#667eea'
}

// 获取警告等级名称
const getWarningLevelName = (level: string) => {
  const levelMap: Record<string, string> = {
    'poor': 'Ⅴ类',
    'very_poor': '劣Ⅴ类',
    'light_polluted': '轻度黑臭',
    'polluted': '重度黑臭'
  }
  return levelMap[level] || level
}

// 处理数据
const processData = () => {
  if (!props.data || props.data.length === 0) return { rivers: [], series: [], riverDetailData: {} }
  
  // 按河道分组统计
  const riverStats: Record<string, Record<string, number>> = {}
  const riverDetailData: Record<string, Record<string, WarningData[]>> = {}
  const allWarningLevels = new Set<string>()
  
  props.data.forEach(item => {
    const river = item.river_name
    const level = item.warning_level
    
    if (!riverStats[river]) {
      riverStats[river] = {}
    }
    if (!riverDetailData[river]) {
      riverDetailData[river] = {}
    }
    if (!riverDetailData[river][level]) {
      riverDetailData[river][level] = []
    }
    
    riverStats[river][level] = (riverStats[river][level] || 0) + 1
    riverDetailData[river][level].push(item)
    allWarningLevels.add(level)
  })
  
  const rivers = Object.keys(riverStats)
  const warningLevels = Array.from(allWarningLevels).sort()
  
  // 构建系列数据
  const series = warningLevels.map(level => ({
    name: getWarningLevelName(level),
    type: 'bar',
    stack: 'warning',
    data: rivers.map(river => riverStats[river][level] || 0),
    itemStyle: {
      color: getWarningLevelColor(level)
    }
  }))
  
  return { rivers, series, riverDetailData }
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chart) return
  
  const { rivers, series, riverDetailData } = processData()
  
  // 格式化数值
  const formatValue = (value: number | null | undefined) => {
    if (value === null || value === undefined) return '--'
    return value.toFixed(2)
  }
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      backgroundColor: 'rgba(0, 0, 0, 0.9)',
      borderColor: 'rgba(255, 255, 255, 0.2)',
      borderWidth: 1,
      textStyle: {
        color: '#ffffff',
        fontSize: 12
      },
      formatter: (params: any) => {
        const riverName = params[0].axisValue
        let tooltip = `<div style="margin-bottom: 8px; font-weight: bold; font-size: 14px; color: #4facfe;">${riverName}</div>`
        let total = 0
        
        params.forEach((item: any) => {
          if (item.value > 0) {
            const levelKey = item.seriesName === 'Ⅴ类' ? 'poor' : 
                           item.seriesName === '劣Ⅴ类' ? 'very_poor' : 'polluted'
            
            tooltip += `<div style="margin: 4px 0; padding: 4px; background: rgba(255,255,255,0.05); border-radius: 4px;">
              <div style="margin-bottom: 3px;">
                <span style="display: inline-block; width: 10px; height: 10px; background-color: ${item.color}; border-radius: 50%; margin-right: 5px;"></span>
                <span style="font-weight: bold;">${item.seriesName}: ${item.value}条</span>
              </div>`
              
            // 显示该等级的详细指标信息
            if (riverDetailData[riverName] && riverDetailData[riverName][levelKey]) {
              const levelData = riverDetailData[riverName][levelKey]
              
              // 动态计算高度，每条数据约55px，最多显示12条不出现滚动条
              const maxHeight = levelData.length > 12 ? '660px' : 'auto'
              tooltip += `<div style="margin-left: 15px; font-size: 11px; color: #ccc; max-height: ${maxHeight}; overflow-y: auto;">`
              
              levelData.forEach((item, index) => {
                const date = new Date(item.sampling_date).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
                tooltip += `<div style="margin: 3px 0; padding: 3px; background: rgba(255,255,255,0.03); border-radius: 3px;">
                  <div style="font-weight: bold; color: #fff; margin-bottom: 2px;">${date} 采样数据:</div>
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2px;">
                    <div>COD: ${formatValue(item.cod_value)} mg/L</div>
                    <div>氨氮: ${formatValue(item.ammonia_nitrogen_value)} mg/L</div>
                    <div>总磷: ${formatValue(item.total_phosphorus_value)} mg/L</div>
                    <div>高锰酸钾: ${formatValue(item.potassium_permanganate_value)} mg/L</div>
                  </div>
                </div>`
              })
              
              tooltip += `</div>`
            }
            
            tooltip += `</div>`
            total += item.value
          }
        })
        
        tooltip += `<div style="margin-top: 8px; padding-top: 5px; border-top: 1px solid rgba(255,255,255,0.2); font-weight: bold; color: #ffc107;">
          总计: ${total}条警告数据
        </div>`
        
        return tooltip
      }
    },
    legend: {
      data: series.map(s => s.name),
      textStyle: {
        color: '#212529'
      },
      top: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: {
        color: '#212529',
        fontSize: 10
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.3)'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      }
    },
    yAxis: {
      type: 'category',
      data: rivers,
      axisLabel: {
        color: '#212529',
        fontSize: 10,
        interval: 0
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.3)'
        }
      }
    },
    series: series
  }
  
  chart.setOption(option)
}

// 监听数据变化
watch(() => props.data, updateChart, { deep: true })

// 监听窗口大小变化
const handleResize = () => {
  if (chart) {
    chart.resize()
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.warning-chart-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
  min-height: 200px;
}
</style> 