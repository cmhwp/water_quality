<template>
  <div class="quality-level-stats">
    <!-- 顶部统计区域 -->
    <div class="stats-header">
      <!-- 出现频次最多的等级 -->
      <!-- <div class="most-common-level">
        <div class="level-circle">
          <div class="circle-chart">
            <svg width="80" height="80" viewBox="0 0 80 80">
              <defs>
                <linearGradient id="circleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#4facfe" />
                  <stop offset="100%" stop-color="#00f2fe" />
                </linearGradient>
              </defs>
              <circle
                cx="40"
                cy="40"
                r="32"
                fill="none"
                stroke="rgba(255, 255, 255, 0.1)"
                stroke-width="8"
              />
              <circle
                cx="40"
                cy="40"
                r="32"
                fill="none"
                stroke="url(#circleGradient)"
                stroke-width="8"
                stroke-dasharray="201"
                :stroke-dashoffset="circleOffset"
                stroke-linecap="round"
                transform="rotate(-90 40 40)"
              />
            </svg>
            <div class="circle-text">
              <div class="percentage">{{ mostCommonPercentage }}%</div>
              <div class="level-name">{{ mostCommonLevel }}</div>
            </div>
          </div>
        </div>
        <div class="level-label">出现频次最多的等级</div>
      </div> -->

      <!-- 整体指标概览 -->
      <div class="overall-rates">
        <div class="overall-item">
          <div class="overall-value qualified">{{ data?.qualified_rate || 0 }}%</div>
          <div class="overall-label">整体达标率</div>
        </div>
        <div class="overall-item">
          <div class="overall-value unqualified">{{ data?.unqualified_rate || 0 }}%</div>
          <div class="overall-label">整体不达标率</div>
        </div>
        <div class="overall-item">
          <div class="overall-value warning">{{ data?.warning_rate || 0 }}%</div>
          <div class="overall-label">整体警告率</div>
        </div>
      </div>
    </div>

    <!-- 各指标详细率统计 -->
    <div class="indicators-rates">
      <div class="indicator-rates-grid">
        <div v-for="indicator in indicators" :key="indicator.code" class="indicator-card">
          <div class="indicator-header">
            <h4 class="indicator-title">{{ indicator.name }}</h4>
            <div class="indicator-total">总计: {{ indicator.data.total_count }}</div>
          </div>
          
          <div class="rates-container">
            <div class="rate-row">
              <div class="rate-item">
                <span class="rate-label">达标率</span>
                <span class="rate-value qualified">{{ indicator.data.qualified_rate }}%</span>
              </div>
              <div class="rate-item">
                <span class="rate-label">不达标率</span>
                <span class="rate-value unqualified">{{ indicator.data.unqualified_rate }}%</span>
              </div>
              <div class="rate-item">
                <span class="rate-label">警告率</span>
                <span class="rate-value warning">{{ indicator.data.warning_rate }}%</span>
              </div>
            </div>
            
            <div class="most-common">
              <span class="most-common-label">最常见等级:</span>
              <span class="most-common-value">{{ indicator.data.most_common_level }} ({{ indicator.data.most_common_percentage }}%)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  data: API.WaterQualityLevelStatistics | null
}

const props = defineProps<Props>()

// 计算圆形图表的偏移量
const circleOffset = computed(() => {
  const percentage = mostCommonPercentage.value
  const circumference = 201 // 2 * π * 32 ≈ 201
  return circumference - (percentage / 100) * circumference
})

// 找到出现频次最多的等级
const mostCommonLevel = computed(() => {
  if (!props.data) return ''
  
  const allStats = [
    props.data.cod_stats,
    props.data.ammonia_nitrogen_stats,
    props.data.total_phosphorus_stats,
    props.data.potassium_permanganate_stats
  ]
  
  let maxCount = 0
  let mostCommon = ''
  
  allStats.forEach(stat => {
    if (stat.most_common_count > maxCount) {
      maxCount = stat.most_common_count
      mostCommon = stat.most_common_level
    }
  })
  
  return mostCommon
})

const mostCommonPercentage = computed(() => {
  if (!props.data) return 0
  
  const allStats = [
    props.data.cod_stats,
    props.data.ammonia_nitrogen_stats,
    props.data.total_phosphorus_stats,
    props.data.potassium_permanganate_stats
  ]
  
  let maxPercentage = 0
  
  allStats.forEach(stat => {
    if (stat.most_common_percentage > maxPercentage) {
      maxPercentage = stat.most_common_percentage
    }
  })
  
  return Math.round(maxPercentage)
})

// 处理指标数据
const indicators = computed(() => {
  if (!props.data) return []
  
  return [
    {
      name: 'COD',
      code: 'cod',
      data: props.data.cod_stats
    },
    {
      name: '氨氮',
      code: 'ammonia_nitrogen', 
      data: props.data.ammonia_nitrogen_stats
    },
    {
      name: '总磷',
      code: 'total_phosphorus',
      data: props.data.total_phosphorus_stats
    },
    {
      name: '高锰酸钾',
      code: 'potassium_permanganate',
      data: props.data.potassium_permanganate_stats
    }
  ]
})


</script>

<style scoped>
.quality-level-stats {
  width: 100%;
  height: 100%;
  color: #212529;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.15);
}

.most-common-level {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.level-circle {
  position: relative;
}

.circle-chart {
  position: relative;
  width: 80px;
  height: 80px;
}

.circle-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.percentage {
  font-size: 18px;
  font-weight: bold;
  color: #00f2fe;
  line-height: 1;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.level-name {
  font-size: 12px;
  color: #6c757d;
  margin-top: 2px;
}

.level-label {
  font-size: 12px;
  color: #6c757d;
  text-align: center;
}

.overall-rates {
  display: flex;
  gap: 32px;
}

.overall-item {
  text-align: center;
}

.overall-value {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 4px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.overall-value.qualified {
  background: linear-gradient(45deg, #43e97b, #38f9d7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.overall-value.unqualified {
  background: linear-gradient(45deg, #ff6b6b, #ee5a52);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.overall-value.warning {
  background: linear-gradient(45deg, #f093fb, #f5576c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.overall-label {
  font-size: 11px;
  color: #6c757d;
}

.indicators-rates {
  margin-top: 16px;
}

.indicator-rates-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.indicator-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.indicator-card:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
}

.indicator-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.indicator-title {
  font-size: 16px;
  font-weight: 600;
  color: #00f2fe;
  margin: 0;
}

.indicator-total {
  font-size: 12px;
  color: #6c757d;
}

.rates-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rate-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.rate-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.rate-label {
  font-size: 11px;
  color: #6c757d;
  margin-bottom: 4px;
}

.rate-value {
  font-size: 16px;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.rate-value.qualified {
  background: linear-gradient(45deg, #43e97b, #38f9d7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.rate-value.unqualified {
  background: linear-gradient(45deg, #ff6b6b, #ee5a52);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.rate-value.warning {
  background: linear-gradient(45deg, #f093fb, #f5576c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.most-common {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 6px;
  font-size: 12px;
}

.most-common-label {
  color: #6c757d;
}

.most-common-value {
  color: #212529;
  font-weight: 600;
}


</style> 