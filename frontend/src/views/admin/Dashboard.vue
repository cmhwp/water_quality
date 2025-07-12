<template>
  <div class="min-h-screen bg-base-200">
    <!-- 头部导航 -->
    <div class="navbar bg-base-100 shadow-lg border-b">
      <div class="flex-1">
        <a class="btn btn-ghost normal-case text-xl font-bold">
          <div class="avatar placeholder mr-2">
            <div class="bg-primary text-primary-content rounded-full w-8">
              <span class="text-xs">💧</span>
            </div>
          </div>
          水质数据管理系统
        </a>
        <div class="badge badge-secondary badge-sm ml-2">管理员</div>
      </div>
      <div class="flex-none gap-2">
        <!-- 通知 -->
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
            <div class="indicator">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5-5 5-5h-5m-6 0H4l5 5-5 5h5m6-10v10a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h7a2 2 0 012 2z"/>
              </svg>
              <span class="badge badge-xs badge-primary indicator-item">3</span>
            </div>
          </div>
          <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-80">
            <li class="menu-title">系统通知</li>
            <li><a class="text-sm">新增数据监测点 3 个</a></li>
            <li><a class="text-sm">水质异常报警 1 条</a></li>
            <li><a class="text-sm">系统维护提醒</a></li>
          </ul>
        </div>
        
        <!-- 用户头像 -->
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
            <div class="w-10 rounded-full bg-primary text-primary-content flex items-center justify-center">
              <span class="text-sm font-bold">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
            </div>
          </div>
          <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
            <li class="menu-title">{{ authStore.user?.username }}</li>
            <li><a><span class="badge badge-success badge-xs mr-2"></span>在线状态</a></li>
            <li><a>个人设置</a></li>
            <li><a>帮助中心</a></li>
            <li class="border-t mt-2 pt-2"><a @click="handleLogout" class="text-error">退出登录</a></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="container mx-auto px-4 py-8">
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="stats shadow bg-base-100">
          <div class="stat">
            <div class="stat-figure text-primary">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div class="stat-title">总数据量</div>
            <div class="stat-value text-primary">{{ statistics.total || 0 }}</div>
            <div class="stat-desc">条水质数据</div>
          </div>
        </div>
        
        <div class="stats shadow bg-base-100">
          <div class="stat">
            <div class="stat-figure text-success">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div class="stat-title">优质水质</div>
            <div class="stat-value text-success">{{ statistics.excellent || 0 }}</div>
            <div class="stat-desc">I-II类水质</div>
          </div>
        </div>
        
        <div class="stats shadow bg-base-100">
          <div class="stat">
            <div class="stat-figure text-warning">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.664-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>
            <div class="stat-title">污染水质</div>
            <div class="stat-value text-warning">{{ statistics.polluted || 0 }}</div>
            <div class="stat-desc">IV类以上</div>
          </div>
        </div>
        
        <div class="stats shadow bg-base-100">
          <div class="stat">
            <div class="stat-figure text-info">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div class="stat-title">最新更新</div>
            <div class="stat-value text-info text-sm">5分钟前</div>
            <div class="stat-desc">数据同步中</div>
          </div>
        </div>
      </div>

      <!-- 搜索和操作栏 -->
      <div class="card bg-base-100 shadow-lg mb-6">
        <div class="card-body">
          <div class="flex flex-wrap items-center gap-4 mb-4">
            <div class="form-control">
              <div class="input-group">
                <span class="bg-base-200">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                  </svg>
                </span>
                <input 
                  v-model="searchParams.river_name" 
                  type="text" 
                  placeholder="搜索河道名称" 
                  class="input input-bordered w-full max-w-xs"
                >
              </div>
            </div>
            
            <div class="form-control">
              <div class="input-group">
                <span class="bg-base-200">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"/>
                  </svg>
                </span>
                <input 
                  v-model="searchParams.code" 
                  type="text" 
                  placeholder="搜索编号" 
                  class="input input-bordered w-full max-w-xs"
                >
              </div>
            </div>
            
            <div class="form-control">
              <select v-model="searchParams.comprehensive_quality_level" class="select select-bordered w-full max-w-xs">
                <option value="">所有水质等级</option>
                <option v-for="level in qualityLevels" :key="level" :value="level">{{ level }}</option>
              </select>
            </div>
            
            <div class="flex gap-2">
              <button @click="searchData" class="btn btn-primary">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                搜索
              </button>
              <button @click="resetSearch" class="btn btn-outline">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                重置
              </button>
              <button @click="openAddModal" class="btn btn-success">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
                添加数据
              </button>
            </div>
          </div>
          
          <!-- 快速筛选 -->
          <div class="flex flex-wrap gap-2">
            <div class="badge badge-outline cursor-pointer hover:badge-primary">今日数据</div>
            <div class="badge badge-outline cursor-pointer hover:badge-primary">本周数据</div>
            <div class="badge badge-outline cursor-pointer hover:badge-primary">优质水质</div>
            <div class="badge badge-outline cursor-pointer hover:badge-primary">污染水质</div>
          </div>
        </div>
      </div>

      <!-- 数据表格 -->
      <div class="card bg-base-100 shadow-lg">
        <div class="card-body p-0">
          <!-- 表格头部 -->
          <div class="flex justify-between items-center p-6 border-b">
            <h3 class="text-lg font-semibold">
              水质数据列表
              <div class="badge badge-neutral badge-sm ml-2">{{ dataList.total }} 条</div>
            </h3>
            <div class="flex gap-2">
              <button class="btn btn-sm btn-ghost">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                导出
              </button>
              <button class="btn btn-sm btn-ghost">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
                </svg>
                导入
              </button>
            </div>
          </div>
          
          <!-- 表格内容 -->
          <div class="overflow-x-auto">
            <table class="table table-zebra">
              <thead class="bg-base-200">
                <tr>
                  <th>
                    <label>
                      <input type="checkbox" class="checkbox checkbox-sm" />
                    </label>
                  </th>
                  <th>ID</th>
                  <th>取样日期</th>
                  <th>河道名称</th>
                  <th>编号</th>
                  <th>综合水质等级</th>
                  <th>COD</th>
                  <th>氨氮</th>
                  <th>总磷</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in dataList.items" :key="item.id" class="hover">
                  <td>
                    <label>
                      <input type="checkbox" class="checkbox checkbox-sm" />
                    </label>
                  </td>
                  <td>
                    <div class="font-bold text-primary">#{{ item.id }}</div>
                  </td>
                  <td>
                    <div class="flex items-center gap-2">
                      <svg class="w-4 h-4 text-base-content/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                      </svg>
                      {{ item.sampling_date }}
                    </div>
                  </td>
                  <td>
                    <div class="font-medium">{{ item.river_name }}</div>
                  </td>
                  <td>
                    <div class="badge badge-outline badge-sm">{{ item.code || 'N/A' }}</div>
                  </td>
                  <td>
                    <div class="badge badge-lg" :class="getQualityLevelClass(item.comprehensive_quality_level)">
                      {{ item.comprehensive_quality_level || 'N/A' }}
                    </div>
                  </td>
                  <td>
                    <div class="text-sm">
                      {{ item.cod_value || 'N/A' }}
                      <span v-if="item.cod_value" class="text-xs text-base-content/50">mg/L</span>
                    </div>
                  </td>
                  <td>
                    <div class="text-sm">
                      {{ item.ammonia_nitrogen_value || 'N/A' }}
                      <span v-if="item.ammonia_nitrogen_value" class="text-xs text-base-content/50">mg/L</span>
                    </div>
                  </td>
                  <td>
                    <div class="text-sm">
                      {{ item.total_phosphorus_value || 'N/A' }}
                      <span v-if="item.total_phosphorus_value" class="text-xs text-base-content/50">mg/L</span>
                    </div>
                  </td>
                  <td>
                    <div class="flex gap-1">
                      <button @click="editItem(item)" class="btn btn-xs btn-primary tooltip" data-tip="编辑">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>
                      <button @click="deleteItem(item.id)" class="btn btn-xs btn-error tooltip" data-tip="删除">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 分页 -->
          <div class="flex justify-between items-center p-6 border-t bg-base-50">
            <div class="text-sm text-base-content/70">
              显示 {{ (currentPage - 1) * perPage + 1 }} - {{ Math.min(currentPage * perPage, dataList.total) }} 条，
              共 {{ dataList.total }} 条数据
            </div>
            <div class="flex items-center gap-2">
              <div class="join">
                <button 
                  @click="changePage(1)" 
                  :disabled="currentPage <= 1"
                  class="join-item btn btn-sm"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/>
                  </svg>
                </button>
                <button 
                  @click="changePage(currentPage - 1)" 
                  :disabled="currentPage <= 1"
                  class="join-item btn btn-sm"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                  </svg>
                </button>
                <span class="join-item btn btn-sm btn-disabled">
                  {{ currentPage }} / {{ totalPages }}
                </span>
                <button 
                  @click="changePage(currentPage + 1)" 
                  :disabled="currentPage >= totalPages"
                  class="join-item btn btn-sm"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </button>
                <button 
                  @click="changePage(totalPages)" 
                  :disabled="currentPage >= totalPages"
                  class="join-item btn btn-sm"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑模态框 -->
    <dialog ref="editModal" class="modal">
      <div class="modal-box w-11/12 max-w-3xl">
        <h3 class="font-bold text-lg mb-4">{{ editingItem ? '编辑水质数据' : '添加水质数据' }}</h3>
        
        <form @submit.prevent="saveItem" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label">
                <span class="label-text">取样日期 *</span>
              </label>
              <input 
                v-model="editForm.sampling_date" 
                type="date" 
                class="input input-bordered" 
                required
              >
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text">检测日期 *</span>
              </label>
              <input 
                v-model="editForm.detection_date" 
                type="date" 
                class="input input-bordered" 
                required
              >
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text">河道名称 *</span>
              </label>
              <input 
                v-model="editForm.river_name" 
                type="text" 
                class="input input-bordered" 
                required
              >
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text">编号</span>
              </label>
              <input 
                v-model="editForm.code" 
                type="text" 
                class="input input-bordered"
              >
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text">COD数值</span>
              </label>
              <input 
                v-model.number="editForm.cod_value" 
                type="number" 
                step="0.01"
                class="input input-bordered"
              >
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text">氨氮数值</span>
              </label>
              <input 
                v-model.number="editForm.ammonia_nitrogen_value" 
                type="number" 
                step="0.01"
                class="input input-bordered"
              >
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text">总磷数值</span>
              </label>
              <input 
                v-model.number="editForm.total_phosphorus_value" 
                type="number" 
                step="0.01"
                class="input input-bordered"
              >
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text">综合水质等级</span>
              </label>
              <select v-model="editForm.comprehensive_quality_level" class="select select-bordered">
                <option value="">请选择</option>
                <option v-for="level in qualityLevels" :key="level" :value="level">{{ level }}</option>
              </select>
            </div>
          </div>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">备注</span>
            </label>
            <textarea 
              v-model="editForm.remarks" 
              class="textarea textarea-bordered h-24"
            ></textarea>
          </div>
          
          <div class="modal-action">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? '保存中...' : '保存' }}
            </button>
            <button type="button" @click="closeModal" class="btn">取消</button>
          </div>
        </form>
      </div>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  getWaterQualityListApiV1WaterQualityGet,
  createWaterQualityApiV1WaterQualityPost,
  updateWaterQualityApiV1WaterQualityWaterQualityIdPut,
  deleteWaterQualityApiV1WaterQualityWaterQualityIdDelete,
  getQualityLevelsApiV1WaterQualityOptionsQualityLevelsGet,
  getWaterQualityStatisticsApiV1WaterQualityStatisticsOverviewGet
} from '@/services/api/waterQuality'

const router = useRouter()
const authStore = useAuthStore()

// 数据状态
const dataList = ref<API.WaterQualityListResponse>({
  total: 0,
  page: 1,
  per_page: 20,
  items: []
})

const statistics = ref<any>({})
const qualityLevels = ref<string[]>([])
const loading = ref(false)
const currentPage = ref(1)
const perPage = ref(20)

// 搜索参数
const searchParams = reactive({
  river_name: '',
  code: '',
  comprehensive_quality_level: ''
})

// 编辑相关
const editModal = ref<HTMLDialogElement>()
const editingItem = ref<API.WaterQualityResponse | null>(null)
const editForm = reactive({
  sampling_date: '',
  detection_date: '',
  river_name: '',
  code: '',
  cod_value: null as number | null,
  ammonia_nitrogen_value: null as number | null,
  total_phosphorus_value: null as number | null,
  comprehensive_quality_level: '',
  remarks: ''
})

// 计算属性
const totalPages = computed(() => {
  return Math.ceil(dataList.value.total / perPage.value)
})

// 获取水质等级样式
const getQualityLevelClass = (level: string | null) => {
  if (!level) return 'badge-neutral'
  
  if (level.includes('I') || level.includes('优')) return 'badge-success'
  if (level.includes('II')) return 'badge-info'
  if (level.includes('III')) return 'badge-warning'
  if (level.includes('IV') || level.includes('V')) return 'badge-error'
  
  return 'badge-neutral'
}

// 获取数据列表
const fetchDataList = async () => {
  loading.value = true
  
  try {
    const response = await getWaterQualityListApiV1WaterQualityGet({
      page: currentPage.value,
      per_page: perPage.value,
      ...searchParams
    })
    console.log(response)
    if (response.data) {
      dataList.value = response.data
    }
  } catch (error) {
    console.error('获取数据列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const response = await getWaterQualityStatisticsApiV1WaterQualityStatisticsOverviewGet()
    if (response.data) {
      statistics.value = response.data
    }
    console.log(statistics.value)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取水质等级选项
const fetchQualityLevels = async () => {
  try {
    const response = await getQualityLevelsApiV1WaterQualityOptionsQualityLevelsGet()
    if (response.data) {
      qualityLevels.value = response.data
    }
  } catch (error) {
    console.error('获取水质等级失败:', error)
  }
}

// 搜索数据
const searchData = () => {
  currentPage.value = 1
  fetchDataList()
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchParams, {
    river_name: '',
    code: '',
    comprehensive_quality_level: ''
  })
  searchData()
}

// 切换页面
const changePage = (page: number) => {
  currentPage.value = page
  fetchDataList()
}

// 打开添加模态框
const openAddModal = () => {
  editingItem.value = null
  resetEditForm()
  editModal.value?.showModal()
}

// 编辑项目
const editItem = (item: API.WaterQualityResponse) => {
  editingItem.value = item
  Object.assign(editForm, {
    sampling_date: item.sampling_date,
    detection_date: item.detection_date,
    river_name: item.river_name,
    code: item.code || '',
    cod_value: item.cod_value,
    ammonia_nitrogen_value: item.ammonia_nitrogen_value,
    total_phosphorus_value: item.total_phosphorus_value,
    comprehensive_quality_level: item.comprehensive_quality_level || '',
    remarks: item.remarks || ''
  })
  editModal.value?.showModal()
}

// 保存项目
const saveItem = async () => {
  loading.value = true
  
  try {
    if (editingItem.value) {
      // 更新
      await updateWaterQualityApiV1WaterQualityWaterQualityIdPut(
        { water_quality_id: editingItem.value.id },
        editForm
      )
    } else {
      // 创建
      await createWaterQualityApiV1WaterQualityPost(editForm)
    }
    
    closeModal()
    fetchDataList()
    fetchStatistics()
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    loading.value = false
  }
}

// 删除项目
const deleteItem = async (id: number) => {
  if (!confirm('确定要删除这条数据吗？')) {
    return
  }
  
  try {
    await deleteWaterQualityApiV1WaterQualityWaterQualityIdDelete({ water_quality_id: id })
    fetchDataList()
    fetchStatistics()
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 关闭模态框
const closeModal = () => {
  editModal.value?.close()
  resetEditForm()
}

// 重置编辑表单
const resetEditForm = () => {
  Object.assign(editForm, {
    sampling_date: '',
    detection_date: '',
    river_name: '',
    code: '',
    cod_value: null,
    ammonia_nitrogen_value: null,
    total_phosphorus_value: null,
    comprehensive_quality_level: '',
    remarks: ''
  })
}

// 退出登录
const handleLogout = () => {
  authStore.logout()
  router.push('/admin/login')
}

// 初始化
onMounted(async () => {
  await authStore.initAuth()
  
  if (!authStore.isAuthenticated || !authStore.isAdmin) {
    router.push('/admin/login')
    return
  }
  
  await Promise.all([
    fetchDataList(),
    fetchStatistics(),
    fetchQualityLevels()
  ])
})
</script>

<style scoped>
.stat {
  padding: 2rem;
}
</style> 