<template>
  <div class="overview-stats">
    <div class="stats-grid">
      <!-- 总数据量 -->
      <div class="stat-card primary">
        <div class="stat-icon">
          <i class="icon-database"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ data.total_records }}</div>
          <div class="stat-label">总数据量</div>
        </div>
      </div>

      <!-- 优质水质数量 -->
      <div class="stat-card success">
        <div class="stat-icon">
          <i class="icon-water-drop"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ data.excellent_count }}</div>
          <div class="stat-label">优质水质 (I-III类)</div>
        </div>
      </div>

      <!-- 优质水质达标率 -->
      <div class="stat-card info">
        <div class="stat-icon">
          <i class="icon-percentage"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ data.excellent_rate }}%</div>
          <div class="stat-label">优质水质达标率</div>
        </div>
      </div>

      <!-- 良好水质 -->
      <div class="stat-card warning">
        <div class="stat-icon">
          <i class="icon-check"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ data.good_count }}</div>
          <div class="stat-label">良好水质 (IV类)</div>
        </div>
      </div>

      <!-- 较差水质 -->
      <div class="stat-card danger">
        <div class="stat-icon">
          <i class="icon-warning"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ data.poor_count }}</div>
          <div class="stat-label">较差水质 (V类)</div>
        </div>
      </div>

      <!-- 极差水质 -->
      <div class="stat-card error">
        <div class="stat-icon">
          <i class="icon-alert"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ data.very_poor_count }}</div>
          <div class="stat-label">极差水质 (劣V类)</div>
        </div>
      </div>

      <!-- 污染水质 -->
      <div class="stat-card dark">
        <div class="stat-icon">
          <i class="icon-pollution"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ data.polluted_count }}</div>
          <div class="stat-label">污染水质 (重度黑臭)</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  data: {
    total_records: number
    excellent_count: number
    good_count: number
    poor_count: number
    very_poor_count: number
    polluted_count: number
    excellent_rate: number
    latest_update: string
  }
}

defineProps<Props>()
</script>

<style scoped>
.overview-stats {
  width: 100%;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  background: rgba(255, 255, 255, 0.1);
  font-size: 20px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.stat-label {
  font-size: 14px;
  color: #b0b0b0;
  font-weight: 400;
}

/* 不同状态的颜色 */
.stat-card.primary {
  --color-primary: #4facfe;
  --color-secondary: #00f2fe;
}

.stat-card.success {
  --color-primary: #43e97b;
  --color-secondary: #38f9d7;
}

.stat-card.info {
  --color-primary: #667eea;
  --color-secondary: #764ba2;
}

.stat-card.warning {
  --color-primary: #f093fb;
  --color-secondary: #f5576c;
}

.stat-card.danger {
  --color-primary: #ff6b6b;
  --color-secondary: #ee5a52;
}

.stat-card.error {
  --color-primary: #c94b4b;
  --color-secondary: #4b134f;
}

.stat-card.dark {
  --color-primary: #2c3e50;
  --color-secondary: #34495e;
}

/* 图标样式 */
.icon-database::before { content: '📊'; }
.icon-water-drop::before { content: '💧'; }
.icon-percentage::before { content: '📈'; }
.icon-check::before { content: '✅'; }
.icon-warning::before { content: '⚠️'; }
.icon-alert::before { content: '🚨'; }
.icon-pollution::before { content: '🚫'; }

/* 响应式设计 */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
  }
  
  .stat-card {
    padding: 15px;
  }
  
  .stat-value {
    font-size: 24px;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .stat-card {
    padding: 12px;
    flex-direction: column;
    text-align: center;
  }
  
  .stat-icon {
    margin-right: 0;
    margin-bottom: 10px;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .stat-label {
    font-size: 12px;
  }
}
</style> 