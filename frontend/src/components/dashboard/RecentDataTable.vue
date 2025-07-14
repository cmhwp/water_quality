<template>
  <div class="recent-data-table">
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>河道名称</th>
            <th>采样日期</th>
            <th>水质等级</th>
            <th>COD</th>
            <th>氨氮</th>
            <th>总磷</th>
            <th>高锰酸钾</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in data" :key="item.id" class="data-row">
            <td class="river-name">{{ item.river_name }}</td>
            <td class="date">{{ formatDate(item.sampling_date) }}</td>
            <td class="quality-level">
              <span :class="getQualityClass(item.comprehensive_quality_level)">
                {{ item.comprehensive_quality_level }}
              </span>
            </td>
            <td class="value">{{ formatValue(item.cod_value) }}</td>
            <td class="value">{{ formatValue(item.ammonia_nitrogen_value) }}</td>
            <td class="value">{{ formatValue(item.total_phosphorus_value) }}</td>
            <td class="value">{{ formatValue(item.potassium_permanganate_value) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
interface RecentData {
  id: number
  river_name: string
  sampling_date: string
  comprehensive_quality_level: string
  cod_value: number | null | undefined
  ammonia_nitrogen_value: number | null | undefined
  total_phosphorus_value: number | null | undefined
  potassium_permanganate_value: number | null | undefined
}

interface Props {
  data: RecentData[]
}

defineProps<Props>()

// 格式化日期
const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  })
}

// 格式化数值
const formatValue = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return '--'
  return value.toFixed(2)
}

// 获取水质等级样式类
const getQualityClass = (level: string): string => {
  const classes: Record<string, string> = {
    'Ⅰ类': 'excellent',
    'Ⅱ类': 'excellent',
    'Ⅲ类': 'good',
    'Ⅳ类': 'fair',
    'Ⅴ类': 'poor',
    '劣Ⅴ类': 'very-poor',
    '轻度黑臭': 'light-polluted',
    '重度黑臭': 'polluted'
  }
  return classes[level] || 'unknown'
}
</script>

<style scoped>
.recent-data-table {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.table-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.data-table th {
  background: rgba(0, 0, 0, 0.05);
  color: #212529;
  padding: 8px 6px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 10;
}

.data-table td {
  padding: 8px 6px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  color: #212529;
}

.data-row {
  transition: background-color 0.3s ease;
}

.data-row:hover {
  background: rgba(0, 0, 0, 0.05);
}

.river-name {
  font-weight: 600;
  color: #4facfe !important;
  min-width: 80px;
}

.date {
  color: #6c757d !important;
  font-size: 11px;
  min-width: 60px;
}

.quality-level {
  min-width: 70px;
}

.quality-level span {
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-align: center;
  display: inline-block;
  min-width: 50px;
}

.quality-level .excellent {
  background: rgba(67, 233, 123, 0.2);
  color: #43e97b;
  border: 1px solid rgba(67, 233, 123, 0.3);
}

.quality-level .good {
  background: rgba(79, 172, 254, 0.2);
  color: #4facfe;
  border: 1px solid rgba(79, 172, 254, 0.3);
}

.quality-level .fair {
  background: rgba(240, 147, 251, 0.2);
  color: #f093fb;
  border: 1px solid rgba(240, 147, 251, 0.3);
}

.quality-level .poor {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
  border: 1px solid rgba(255, 107, 107, 0.3);
}

.quality-level .very-poor {
  background: rgba(201, 75, 75, 0.2);
  color: #c94b4b;
  border: 1px solid rgba(201, 75, 75, 0.3);
}

.quality-level .light-polluted {
  background: rgba(121, 85, 72, 0.2);
  color: #795548;
  border: 1px solid rgba(121, 85, 72, 0.3);
}

.quality-level .polluted {
  background: rgba(44, 62, 80, 0.2);
  color: #2c3e50;
  border: 1px solid rgba(44, 62, 80, 0.3);
}

.quality-level .unknown {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.3);
}

.value {
  text-align: right;
  font-family: 'Courier New', monospace;
  min-width: 50px;
}

/* 滚动条样式 */
.table-container::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.table-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .data-table {
    font-size: 10px;
  }
  
  .data-table th,
  .data-table td {
    padding: 6px 4px;
  }
  
  .quality-level span {
    font-size: 9px;
    padding: 1px 4px;
    min-width: 40px;
  }
  
  .river-name {
    min-width: 60px;
  }
  
  .date {
    min-width: 50px;
  }
  
  .quality-level {
    min-width: 60px;
  }
  
  .value {
    min-width: 40px;
  }
}
</style> 