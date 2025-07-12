<template>
  <div class="water-quality-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">水质数据管理</h1>
          <p class="page-subtitle">管理和监控水质检测数据</p>
        </div>
        <div class="header-right">
          <a-button type="primary" @click="showAddModal" size="large">
            <template #icon>
              <PlusOutlined />
            </template>
            添加水质数据
          </a-button>
        </div>
      </div>
    </div>

    <!-- 搜索和过滤区域 -->
    <div class="search-section">
      <a-card title="搜索筛选" class="search-card">
        <a-form layout="inline" :model="searchForm" @finish="handleSearch">
          <a-form-item label="河道名称">
            <a-input 
              v-model:value="searchForm.river_name" 
              placeholder="请输入河道名称"
              allow-clear
              style="width: 200px"
            />
          </a-form-item>
          
          <a-form-item label="编号">
            <a-input 
              v-model:value="searchForm.code" 
              placeholder="请输入编号"
              allow-clear
              style="width: 150px"
            />
          </a-form-item>
          
          <a-form-item label="水质等级">
            <a-select 
              v-model:value="searchForm.comprehensive_quality_level" 
              placeholder="请选择水质等级"
              allow-clear
              style="width: 150px"
            >
              <a-select-option value="I">I类</a-select-option>
              <a-select-option value="II">II类</a-select-option>
              <a-select-option value="III">III类</a-select-option>
              <a-select-option value="IV">IV类</a-select-option>
              <a-select-option value="V">V类</a-select-option>
              <a-select-option value="劣V">劣V类</a-select-option>
            </a-select>
          </a-form-item>
          
          <a-form-item label="取样日期">
            <a-range-picker 
              v-model:value="searchForm.samplingDateRange" 
              style="width: 280px"
            />
          </a-form-item>
          
          <a-form-item>
            <a-button type="primary" html-type="submit" :loading="loading">
              <template #icon>
                <SearchOutlined />
              </template>
              搜索
            </a-button>
          </a-form-item>
          
          <a-form-item>
            <a-button @click="resetSearch">
              <template #icon>
                <ReloadOutlined />
              </template>
              重置
            </a-button>
          </a-form-item>
        </a-form>
      </a-card>
    </div>

    <!-- 数据表格 -->
    <div class="table-section">
      <a-card class="table-card">
        <template #title>
          <div class="table-header">
            <span>水质数据列表 (共 {{ pagination.total }} 条)</span>
            <div class="table-actions">
              <a-button @click="exportData" size="small">
                <template #icon>
                  <DownloadOutlined />
                </template>
                导出
              </a-button>
              <a-button @click="fetchData" size="small">
                <template #icon>
                  <ReloadOutlined />
                </template>
                刷新
              </a-button>
            </div>
          </div>
        </template>
        
        <a-table
          :columns="columns"
          :data-source="dataSource"
          :pagination="paginationConfig"
          :loading="loading"
          :scroll="{ x: 1500 }"
          row-key="id"
          @change="handleTableChange"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'comprehensive_quality_level'">
              <a-tag :color="getQualityColor(record.comprehensive_quality_level)">
                {{ record.comprehensive_quality_level }}
              </a-tag>
            </template>
            
            <template v-else-if="column.key === 'sampling_date'">
              {{ formatDate(record.sampling_date) }}
            </template>
            
            <template v-else-if="column.key === 'detection_date'">
              {{ formatDate(record.detection_date) }}
            </template>
            
            <template v-else-if="column.key === 'action'">
              <a-space>
                <a-button type="text" size="small" @click="viewRecord(record)">
                  <template #icon>
                    <EyeOutlined />
                  </template>
                  查看
                </a-button>
                <a-button type="text" size="small" @click="editRecord(record)">
                  <template #icon>
                    <EditOutlined />
                  </template>
                  编辑
                </a-button>
                <a-popconfirm
                  title="确定要删除这条数据吗？"
                  ok-text="确定"
                  cancel-text="取消"
                  @confirm="deleteRecord(record.id)"
                >
                  <a-button type="text" size="small" danger>
                    <template #icon>
                      <DeleteOutlined />
                    </template>
                    删除
                  </a-button>
                </a-popconfirm>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>

    <!-- 添加/编辑模态框 -->
    <a-modal
      v-model:open="modalVisible"
      :title="isEditing ? '编辑水质数据' : '添加水质数据'"
      :width="800"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
      :confirm-loading="modalLoading"
    >
      <a-form
        ref="modalFormRef"
        :model="modalForm"
        :rules="modalRules"
        layout="vertical"
      >
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="河道名称" name="river_name">
              <a-input v-model:value="modalForm.river_name" placeholder="请输入河道名称" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="编号" name="code">
              <a-input v-model:value="modalForm.code" placeholder="请输入编号" />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="取样日期" name="sampling_date">
              <a-date-picker 
                v-model:value="modalForm.sampling_date" 
                style="width: 100%"
                placeholder="请选择取样日期"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="检测日期" name="detection_date">
              <a-date-picker 
                v-model:value="modalForm.detection_date" 
                style="width: 100%"
                placeholder="请选择检测日期"
              />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="取样时间" name="sampling_time">
              <a-time-picker 
                v-model:value="modalForm.sampling_time" 
                style="width: 100%"
                placeholder="请选择取样时间"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="检测方式" name="method">
              <a-input v-model:value="modalForm.method" placeholder="请输入检测方式" />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-divider>检测数值</a-divider>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="COD数值(mg/L)" name="cod_value">
              <a-input-number 
                v-model:value="modalForm.cod_value" 
                style="width: 100%"
                :precision="2"
                :min="0"
                placeholder="请输入COD数值"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="氨氮数值(mg/L)" name="ammonia_nitrogen_value">
              <a-input-number 
                v-model:value="modalForm.ammonia_nitrogen_value" 
                style="width: 100%"
                :precision="2"
                :min="0"
                placeholder="请输入氨氮数值"
              />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="总磷数值(mg/L)" name="total_phosphorus_value">
              <a-input-number 
                v-model:value="modalForm.total_phosphorus_value" 
                style="width: 100%"
                :precision="2"
                :min="0"
                placeholder="请输入总磷数值"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="高锰酸钾数值(mg/L)" name="potassium_permanganate_value">
              <a-input-number 
                v-model:value="modalForm.potassium_permanganate_value" 
                style="width: 100%"
                :precision="2"
                :min="0"
                placeholder="请输入高锰酸钾数值"
              />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-form-item label="综合水质等级" name="comprehensive_quality_level">
          <a-select 
            v-model:value="modalForm.comprehensive_quality_level" 
            placeholder="请选择综合水质等级"
            style="width: 100%"
          >
            <a-select-option value="I">I类</a-select-option>
            <a-select-option value="II">II类</a-select-option>
            <a-select-option value="III">III类</a-select-option>
            <a-select-option value="IV">IV类</a-select-option>
            <a-select-option value="V">V类</a-select-option>
            <a-select-option value="劣V">劣V类</a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="备注" name="remarks">
          <a-textarea 
            v-model:value="modalForm.remarks" 
            placeholder="请输入备注信息"
            :rows="3"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看详情模态框 -->
    <a-modal
      v-model:open="viewModalVisible"
      title="水质数据详情"
      :width="800"
      :footer="null"
    >
      <a-descriptions 
        v-if="viewRecordData" 
        :column="2" 
        bordered
        size="small"
      >
        <a-descriptions-item label="河道名称">
          {{ viewRecordData.river_name }}
        </a-descriptions-item>
        <a-descriptions-item label="编号">
          {{ viewRecordData.code }}
        </a-descriptions-item>
        <a-descriptions-item label="取样日期">
          {{ formatDate(viewRecordData.sampling_date) }}
        </a-descriptions-item>
        <a-descriptions-item label="检测日期">
          {{ formatDate(viewRecordData.detection_date) }}
        </a-descriptions-item>
        <a-descriptions-item label="取样时间">
          {{ viewRecordData.sampling_time }}
        </a-descriptions-item>
        <a-descriptions-item label="检测方式">
          {{ viewRecordData.method }}
        </a-descriptions-item>
        <a-descriptions-item label="COD数值">
          {{ viewRecordData.cod_value }} mg/L
        </a-descriptions-item>
        <a-descriptions-item label="氨氮数值">
          {{ viewRecordData.ammonia_nitrogen_value }} mg/L
        </a-descriptions-item>
        <a-descriptions-item label="总磷数值">
          {{ viewRecordData.total_phosphorus_value }} mg/L
        </a-descriptions-item>
        <a-descriptions-item label="高锰酸钾数值">
          {{ viewRecordData.potassium_permanganate_value }} mg/L
        </a-descriptions-item>
        <a-descriptions-item label="综合水质等级">
          <a-tag :color="getQualityColor(viewRecordData.comprehensive_quality_level)">
            {{ viewRecordData.comprehensive_quality_level }}
          </a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="备注" :span="2">
          {{ viewRecordData.remarks || '无' }}
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import dayjs from 'dayjs'
import type { FormInstance, TableColumnsType } from 'ant-design-vue'
import {
  PlusOutlined,
  SearchOutlined,
  ReloadOutlined,
  DownloadOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'
import {
  getWaterQualityListApiV1WaterQualityGet,
  createWaterQualityApiV1WaterQualityPost,
  updateWaterQualityApiV1WaterQualityWaterQualityIdPut,
  deleteWaterQualityApiV1WaterQualityWaterQualityIdDelete
} from '@/services/api/waterQuality'

// 响应式数据
const loading = ref(false)
const modalLoading = ref(false)
const modalVisible = ref(false)
const viewModalVisible = ref(false)
const isEditing = ref(false)
const currentEditId = ref<number | null>(null)
const dataSource = ref<any[]>([])
const modalFormRef = ref<FormInstance>()
const viewRecordData = ref<any>(null)

// 搜索表单
const searchForm = reactive({
  river_name: '',
  code: '',
  comprehensive_quality_level: undefined,
  samplingDateRange: undefined as any
})

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total: number) => `共 ${total} 条数据`
})

// 表格列配置
const columns: TableColumnsType = [
  {
    title: '河道名称',
    dataIndex: 'river_name',
    key: 'river_name',
    width: 120,
    fixed: 'left'
  },
  {
    title: '编号',
    dataIndex: 'code',
    key: 'code',
    width: 100
  },
  {
    title: '取样日期',
    dataIndex: 'sampling_date',
    key: 'sampling_date',
    width: 120
  },
  {
    title: '检测日期',
    dataIndex: 'detection_date',
    key: 'detection_date',
    width: 120
  },
  {
    title: 'COD(mg/L)',
    dataIndex: 'cod_value',
    key: 'cod_value',
    width: 100,
    align: 'right'
  },
  {
    title: '氨氮(mg/L)',
    dataIndex: 'ammonia_nitrogen_value',
    key: 'ammonia_nitrogen_value',
    width: 100,
    align: 'right'
  },
  {
    title: '总磷(mg/L)',
    dataIndex: 'total_phosphorus_value',
    key: 'total_phosphorus_value',
    width: 100,
    align: 'right'
  },
  {
    title: '高锰酸钾(mg/L)',
    dataIndex: 'potassium_permanganate_value',
    key: 'potassium_permanganate_value',
    width: 120,
    align: 'right'
  },
  {
    title: '综合水质等级',
    dataIndex: 'comprehensive_quality_level',
    key: 'comprehensive_quality_level',
    width: 120,
    align: 'center'
  },
  {
    title: '操作',
    key: 'action',
    width: 180,
    fixed: 'right',
    align: 'center'
  }
]

// 模态框表单
const modalForm = reactive({
  river_name: '',
  code: '',
  sampling_date: null as any,
  detection_date: null as any,
  sampling_time: null as any,
  method: '',
  cod_value: null as number | null,
  ammonia_nitrogen_value: null as number | null,
  total_phosphorus_value: null as number | null,
  potassium_permanganate_value: null as number | null,
  comprehensive_quality_level: '',
  remarks: ''
})

// 表单验证规则
const modalRules = {
  river_name: [
    { required: true, message: '请输入河道名称', trigger: 'blur' }
  ],
  sampling_date: [
    { required: true, message: '请选择取样日期', trigger: 'change' }
  ],
  detection_date: [
    { required: true, message: '请选择检测日期', trigger: 'change' }
  ]
}

// 分页配置
const paginationConfig = {
  current: pagination.current,
  pageSize: pagination.pageSize,
  total: pagination.total,
  showSizeChanger: pagination.showSizeChanger,
  showQuickJumper: pagination.showQuickJumper,
  showTotal: pagination.showTotal
}

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: any = {
      page: pagination.current,
      per_page: pagination.pageSize
    }
    
    // 添加搜索条件
    if (searchForm.river_name) params.river_name = searchForm.river_name
    if (searchForm.code) params.code = searchForm.code
    if (searchForm.comprehensive_quality_level) params.comprehensive_quality_level = searchForm.comprehensive_quality_level
    if (searchForm.samplingDateRange && searchForm.samplingDateRange.length === 2) {
      params.sampling_date_start = searchForm.samplingDateRange[0].format('YYYY-MM-DD')
      params.sampling_date_end = searchForm.samplingDateRange[1].format('YYYY-MM-DD')
    }
    
    const response = await getWaterQualityListApiV1WaterQualityGet(params) as any
    dataSource.value = response.items || []
    pagination.total = response.total || 0
  } catch (error) {
    console.error('Failed to fetch data:', error)
    message.error('获取数据失败')
  } finally {
    loading.value = false
  }
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

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD')
}

// 搜索处理
const handleSearch = () => {
  pagination.current = 1
  fetchData()
}

// 重置搜索
const resetSearch = () => {
  searchForm.river_name = ''
  searchForm.code = ''
  searchForm.comprehensive_quality_level = undefined
  searchForm.samplingDateRange = undefined
  pagination.current = 1
  fetchData()
}

// 表格变化处理
const handleTableChange = (pag: any) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchData()
}

// 显示添加模态框
const showAddModal = () => {
  isEditing.value = false
  currentEditId.value = null
  resetModalForm()
  modalVisible.value = true
}

// 编辑记录
const editRecord = (record: any) => {
  isEditing.value = true
  currentEditId.value = record.id
  
  // 填充表单数据
  modalForm.river_name = record.river_name || ''
  modalForm.code = record.code || ''
  modalForm.sampling_date = record.sampling_date ? dayjs(record.sampling_date) : null
  modalForm.detection_date = record.detection_date ? dayjs(record.detection_date) : null
  modalForm.sampling_time = record.sampling_time ? dayjs(record.sampling_time, 'HH:mm:ss') : null
  modalForm.method = record.method || ''
  modalForm.cod_value = record.cod_value || null
  modalForm.ammonia_nitrogen_value = record.ammonia_nitrogen_value || null
  modalForm.total_phosphorus_value = record.total_phosphorus_value || null
  modalForm.potassium_permanganate_value = record.potassium_permanganate_value || null
  modalForm.comprehensive_quality_level = record.comprehensive_quality_level || ''
  modalForm.remarks = record.remarks || ''
  
  modalVisible.value = true
}

// 查看记录
const viewRecord = (record: any) => {
  viewRecordData.value = record
  viewModalVisible.value = true
}

// 删除记录
const deleteRecord = async (id: number) => {
  try {
    await deleteWaterQualityApiV1WaterQualityWaterQualityIdDelete({ water_quality_id: id })
    message.success('删除成功')
    fetchData()
  } catch (error) {
    console.error('Failed to delete record:', error)
    message.error('删除失败')
  }
}

// 重置模态框表单
const resetModalForm = () => {
  modalForm.river_name = ''
  modalForm.code = ''
  modalForm.sampling_date = null
  modalForm.detection_date = null
  modalForm.sampling_time = null
  modalForm.method = ''
  modalForm.cod_value = null
  modalForm.ammonia_nitrogen_value = null
  modalForm.total_phosphorus_value = null
  modalForm.potassium_permanganate_value = null
  modalForm.comprehensive_quality_level = ''
  modalForm.remarks = ''
}

// 模态框确认
const handleModalOk = async () => {
  try {
    await modalFormRef.value?.validate()
    
    modalLoading.value = true
    
    const formData = {
      ...modalForm,
      sampling_date: modalForm.sampling_date?.format('YYYY-MM-DD'),
      detection_date: modalForm.detection_date?.format('YYYY-MM-DD'),
      sampling_time: modalForm.sampling_time?.format('HH:mm:ss')
    }
    
    if (isEditing.value && currentEditId.value) {
      await updateWaterQualityApiV1WaterQualityWaterQualityIdPut(
        { water_quality_id: currentEditId.value },
        formData
      )
      message.success('更新成功')
    } else {
      await createWaterQualityApiV1WaterQualityPost(formData)
      message.success('添加成功')
    }
    
    modalVisible.value = false
    fetchData()
  } catch (error) {
    console.error('Failed to save data:', error)
    message.error('保存失败')
  } finally {
    modalLoading.value = false
  }
}

// 模态框取消
const handleModalCancel = () => {
  modalVisible.value = false
  resetModalForm()
}

// 导出数据
const exportData = () => {
  message.info('导出功能开发中...')
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.water-quality-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.page-header {
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

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.page-subtitle {
  color: #6b7280;
  margin: 0;
  font-size: 14px;
}

.search-section {
  padding: 16px 24px;
}

.search-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.table-section {
  padding: 0 24px 24px;
}

.table-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-actions {
  display: flex;
  gap: 8px;
}

:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  font-weight: 600;
}

:deep(.ant-table-tbody > tr:hover > td) {
  background: #f0f9ff;
}

@media (max-width: 768px) {
  .page-header {
    padding: 12px 16px;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .search-section,
  .table-section {
    padding: 16px;
  }
  
  .page-title {
    font-size: 20px;
  }
  
  :deep(.ant-form-inline .ant-form-item) {
    margin-right: 0;
    margin-bottom: 16px;
  }
}
</style> 