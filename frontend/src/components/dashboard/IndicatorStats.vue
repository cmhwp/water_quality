<template>
  <div class="indicator-stats">
    <div class="indicators-grid">
      <div 
        v-for="indicator in data" 
        :key="indicator.indicator_name"
        class="indicator-card"
        :class="{ 'exceeded': indicator.exceed_rate > 10 }"
      >
        <div class="indicator-header">
          <h4>{{ indicator.indicator_name }}</h4>
          <span class="unit">({{ indicator.unit }})</span>
        </div>
        
        <div class="indicator-values">
          <div class="value-item">
            <span class="label">平均值</span>
            <span class="value">{{ formatValue(indicator.avg_value) }}</span>
          </div>
          
          <div class="value-item">
            <span class="label">最大值</span>
            <span class="value max">{{ formatValue(indicator.max_value) }}</span>
          </div>
          
          <div class="value-item">
            <span class="label">最小值</span>
            <span class="value min">{{ formatValue(indicator.min_value) }}</span>
          </div>
          
          <div class="value-item">
            <span class="label">标准值</span>
            <span class="value standard">{{ formatValue(indicator.standard_value) }}</span>
          </div>
        </div>
        
        <div class="exceed-rate">
          <div class="exceed-label">超标率</div>
          <div class="exceed-value" :class="getExceedRateClass(indicator.exceed_rate)">
            {{ indicator.exceed_rate }}%
          </div>
          <div class="exceed-bar">
            <div 
              class="exceed-progress" 
              :style="{ width: `${Math.min(indicator.exceed_rate, 100)}%` }"
              :class="getExceedRateClass(indicator.exceed_rate)"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface IndicatorData {
  indicator_name: string
  avg_value: number | null | undefined
  max_value: number | null | undefined
  min_value: number | null | undefined
  unit: string
  standard_value: number | null | undefined
  exceed_rate: number
}

interface Props {
  data: IndicatorData[]
}

defineProps<Props>()

// 格式化数值
const formatValue = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return '--'
  return value.toFixed(2)
}

// 获取超标率样式类
const getExceedRateClass = (rate: number): string => {
  if (rate >= 30) return 'high'
  if (rate >= 10) return 'medium'
  return 'low'
}
</script>

<style scoped>
.indicator-stats {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.indicators-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  padding: 5px;
}

.indicator-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
}

.indicator-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.indicator-card.exceeded {
  border-color: rgba(255, 107, 107, 0.5);
  background: rgba(255, 107, 107, 0.1);
}

.indicator-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.indicator-header h4 {
  margin: 0;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
}

.unit {
  color: #a0a0a0;
  font-size: 12px;
}

.indicator-values {
  margin-bottom: 12px;
}

.value-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.value-item:last-child {
  margin-bottom: 0;
}

.label {
  font-size: 12px;
  color: #b0b0b0;
}

.value {
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
}

.value.max {
  color: #ff6b6b;
}

.value.min {
  color: #43e97b;
}

.value.standard {
  color: #4facfe;
}

.exceed-rate {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.exceed-label {
  font-size: 12px;
  color: #b0b0b0;
  margin-bottom: 4px;
}

.exceed-value {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 6px;
  text-align: center;
}

.exceed-value.low {
  color: #43e97b;
}

.exceed-value.medium {
  color: #f093fb;
}

.exceed-value.high {
  color: #ff6b6b;
}

.exceed-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.exceed-progress {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.exceed-progress.low {
  background: linear-gradient(90deg, #43e97b, #38f9d7);
}

.exceed-progress.medium {
  background: linear-gradient(90deg, #f093fb, #f5576c);
}

.exceed-progress.high {
  background: linear-gradient(90deg, #ff6b6b, #ee5a52);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .indicators-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
  }
  
  .indicator-card {
    padding: 12px;
  }
  
  .indicator-header h4 {
    font-size: 12px;
  }
  
  .value-item {
    margin-bottom: 4px;
  }
  
  .label, .value {
    font-size: 11px;
  }
  
  .exceed-value {
    font-size: 14px;
  }
}
</style> 