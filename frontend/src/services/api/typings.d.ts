declare namespace API {
  type DashboardResponse = {
    /** 总览统计 */
    overview: OverviewStatistics;
    /** River Stats 河道统计 */
    river_stats: RiverStatistics[];
    /** Quality Distribution 水质等级分布 */
    quality_distribution: QualityLevelDistribution[];
    /** Monthly Trend 月度趋势 */
    monthly_trend: MonthlyTrend[];
    /** Indicator Stats 指标统计 */
    indicator_stats: IndicatorStatistics[];
    /** Recent Data 最新数据 */
    recent_data: RecentWaterQuality[];
  };

  type deleteWaterQualityApiV1WaterQualityWaterQualityIdDeleteParams = {
    water_quality_id: number;
  };

  type getMethodDashboardDataApiV1DashboardMethodMethodAllGetParams = {
    method: string;
  };

  type getMethodIndicatorStatisticsApiV1DashboardMethodMethodIndicatorsGetParams =
    {
      method: string;
    };

  type getMethodMonthlyTrendApiV1DashboardMethodMethodMonthlyTrendGetParams = {
    method: string;
    /** 返回月份数量限制 */
    limit?: number;
  };

  type getMethodOverviewStatisticsApiV1DashboardMethodMethodOverviewGetParams =
    {
      method: string;
    };

  type getMethodQualityDistributionApiV1DashboardMethodMethodQualityDistributionGetParams =
    {
      method: string;
    };

  type getMethodRecentWaterQualityApiV1DashboardMethodMethodRecentDataGetParams =
    {
      method: string;
      /** 返回数据条数限制 */
      limit?: number;
    };

  type getMethodRiverStatisticsApiV1DashboardMethodMethodRiversGetParams = {
    method: string;
    /** 返回河道数量限制 */
    limit?: number;
  };

  type getMonthlyTrendApiV1DashboardMonthlyTrendGetParams = {
    /** 返回月份数量限制 */
    limit?: number;
  };

  type getRecentWaterQualityApiV1DashboardRecentDataGetParams = {
    /** 返回数据条数限制 */
    limit?: number;
  };

  type getRiverDataApiV1DashboardRiverRiverNameGetParams = {
    river_name: string;
    /** 返回数据条数限制 */
    limit?: number;
  };

  type getRiverStatisticsApiV1DashboardRiversGetParams = {
    /** 返回河道数量限制 */
    limit?: number;
  };

  type getWaterQualityByIdApiV1WaterQualityWaterQualityIdGetParams = {
    water_quality_id: number;
  };

  type getWaterQualityListApiV1WaterQualityGetParams = {
    /** 页码 */
    page?: number;
    /** 每页数量 */
    per_page?: number;
    /** 河道名称 */
    river_name?: string;
    /** 编号 */
    code?: string;
    /** 综合水质等级 */
    comprehensive_quality_level?: string;
    /** 取样开始日期 */
    sampling_date_start?: string;
    /** 取样结束日期 */
    sampling_date_end?: string;
  };

  type HTTPValidationError = {
    /** Detail */
    detail?: ValidationError[];
  };

  type IndicatorStatistics = {
    /** Indicator Name 指标名称 */
    indicator_name: string;
    /** Avg Value 平均值 */
    avg_value?: number | null;
    /** Max Value 最大值 */
    max_value?: number | null;
    /** Min Value 最小值 */
    min_value?: number | null;
    /** Unit 单位 */
    unit: string;
    /** Standard Value 标准值 */
    standard_value?: number | null;
    /** Exceed Rate 超标率 */
    exceed_rate: number;
  };

  type MethodDashboardResponse = {
    /** Method 方式名称 */
    method: string;
    /** 总览统计 */
    overview: MethodOverviewStatistics;
    /** River Stats 河道统计 */
    river_stats: MethodRiverStatistics[];
    /** Quality Distribution 水质等级分布 */
    quality_distribution: MethodQualityDistribution[];
    /** Monthly Trend 月度趋势 */
    monthly_trend: MethodMonthlyTrend[];
    /** Indicator Stats 指标统计 */
    indicator_stats: MethodIndicatorStatistics[];
    /** Recent Data 最新数据 */
    recent_data: RecentWaterQuality[];
  };

  type MethodIndicatorStatistics = {
    /** Method 方式名称 */
    method: string;
    /** Indicator Name 指标名称 */
    indicator_name: string;
    /** Avg Value 平均值 */
    avg_value?: number | null;
    /** Max Value 最大值 */
    max_value?: number | null;
    /** Min Value 最小值 */
    min_value?: number | null;
    /** Unit 单位 */
    unit: string;
    /** Standard Value 标准值 */
    standard_value?: number | null;
    /** Exceed Rate 超标率 */
    exceed_rate: number;
  };

  type MethodListResponse = {
    /** Methods 方式名称列表 */
    methods: string[];
    /** Total Count 方式总数 */
    total_count: number;
  };

  type MethodMonthlyTrend = {
    /** Method 方式名称 */
    method: string;
    /** Month 月份 */
    month: string;
    /** Total Count 总数据量 */
    total_count: number;
    /** Excellent Count 优质水质数量 */
    excellent_count: number;
    /** Excellent Rate 优质水质达标率 */
    excellent_rate: number;
  };

  type MethodOverviewStatistics = {
    /** Method 方式名称 */
    method: string;
    /** Total Records 总数据量 */
    total_records: number;
    /** Excellent Count 优质水质数量(I-III类) */
    excellent_count: number;
    /** Good Count 良好水质数量(IV类) */
    good_count: number;
    /** Poor Count 较差水质数量(V类) */
    poor_count: number;
    /** Very Poor Count 极差水质数量(劣V类) */
    very_poor_count: number;
    /** Polluted Count 污染水质数量(重度黑臭) */
    polluted_count: number;
    /** Excellent Rate 优质水质达标率 */
    excellent_rate: number;
    /** Latest Update 最新数据更新时间 */
    latest_update: string;
  };

  type MethodQualityDistribution = {
    /** Method 方式名称 */
    method: string;
    /** Level 水质等级 */
    level: string;
    /** Count 数量 */
    count: number;
    /** Percentage 百分比 */
    percentage: number;
  };

  type MethodRiverStatistics = {
    /** Method 方式名称 */
    method: string;
    /** River Name 河道名称 */
    river_name: string;
    /** Total Count 总数据量 */
    total_count: number;
    /** Excellent Count 优质水质数量 */
    excellent_count: number;
    /** Good Count 良好水质数量 */
    good_count: number;
    /** Poor Count 较差水质数量 */
    poor_count: number;
    /** Very Poor Count 极差水质数量 */
    very_poor_count: number;
    /** Polluted Count 污染水质数量 */
    polluted_count: number;
    /** Excellent Rate 优质水质达标率 */
    excellent_rate: number;
    /** Latest Sampling Date 最新采样时间 */
    latest_sampling_date?: string | null;
  };

  type MethodStatistics = {
    /** Method 方式名称 */
    method: string;
    /** Total Count 总数据量 */
    total_count: number;
    /** Excellent Count 优质水质数量 */
    excellent_count: number;
    /** Good Count 良好水质数量 */
    good_count: number;
    /** Poor Count 较差水质数量 */
    poor_count: number;
    /** Very Poor Count 极差水质数量 */
    very_poor_count: number;
    /** Polluted Count 污染水质数量 */
    polluted_count: number;
    /** Excellent Rate 优质水质达标率 */
    excellent_rate: number;
    /** Latest Sampling Date 最新采样时间 */
    latest_sampling_date?: string | null;
  };

  type MonthlyTrend = {
    /** Month 月份 */
    month: string;
    /** Total Count 总数据量 */
    total_count: number;
    /** Excellent Count 优质水质数量 */
    excellent_count: number;
    /** Excellent Rate 优质水质达标率 */
    excellent_rate: number;
  };

  type OverviewStatistics = {
    /** Total Records 总数据量 */
    total_records: number;
    /** Excellent Count 优质水质数量(I-III类) */
    excellent_count: number;
    /** Good Count 良好水质数量(IV类) */
    good_count: number;
    /** Poor Count 较差水质数量(V类) */
    poor_count: number;
    /** Very Poor Count 极差水质数量(劣V类) */
    very_poor_count: number;
    /** Polluted Count 污染水质数量(重度黑臭) */
    polluted_count: number;
    /** Excellent Rate 优质水质达标率 */
    excellent_rate: number;
    /** Latest Update 最新数据更新时间 */
    latest_update: string;
  };

  type QualityLevelDistribution = {
    /** Level 水质等级 */
    level: string;
    /** Count 数量 */
    count: number;
    /** Percentage 百分比 */
    percentage: number;
  };

  type RecentWaterQuality = {
    /** Id 数据ID */
    id: number;
    /** River Name 河道名称 */
    river_name: string;
    /** Sampling Date 采样日期 */
    sampling_date: string;
    /** Comprehensive Quality Level 综合水质等级 */
    comprehensive_quality_level: string;
    /** Cod Value COD值 */
    cod_value?: number | null;
    /** Ammonia Nitrogen Value 氨氮值 */
    ammonia_nitrogen_value?: number | null;
    /** Total Phosphorus Value 总磷值 */
    total_phosphorus_value?: number | null;
    /** Potassium Permanganate Value 高锰酸钾值 */
    potassium_permanganate_value?: number | null;
  };

  type RiverListResponse = {
    /** Rivers 河道名称列表 */
    rivers: string[];
    /** Total Count 河道总数 */
    total_count: number;
  };

  type RiverStatistics = {
    /** River Name 河道名称 */
    river_name: string;
    /** Total Count 总数据量 */
    total_count: number;
    /** Excellent Count 优质水质数量 */
    excellent_count: number;
    /** Good Count 良好水质数量 */
    good_count: number;
    /** Poor Count 较差水质数量 */
    poor_count: number;
    /** Very Poor Count 极差水质数量 */
    very_poor_count: number;
    /** Polluted Count 污染水质数量 */
    polluted_count: number;
    /** Excellent Rate 优质水质达标率 */
    excellent_rate: number;
    /** Latest Sampling Date 最新采样时间 */
    latest_sampling_date?: string | null;
  };

  type Token = {
    /** Access Token 访问令牌 */
    access_token: string;
    /** Token Type 令牌类型 */
    token_type?: string;
    /** Expires In 过期时间（秒） */
    expires_in: number;
    /** 用户信息 */
    user: UserResponse;
  };

  type updateWaterQualityApiV1WaterQualityWaterQualityIdPutParams = {
    water_quality_id: number;
  };

  type UserLogin = {
    /** Username 用户名或邮箱 */
    username: string;
    /** Password 密码 */
    password: string;
  };

  type UserResponse = {
    /** Email 邮箱 */
    email: string;
    /** Username 用户名 */
    username: string;
    /** Full Name 全名 */
    full_name?: string | null;
    /** Is Active 是否激活 */
    is_active?: boolean;
    /** Is Admin 是否管理员 */
    is_admin?: boolean;
    /** Id 用户ID */
    id: number;
    /** Created At 创建时间 */
    created_at: string;
    /** Updated At 更新时间 */
    updated_at: string;
    /** Last Login 最后登录时间 */
    last_login?: string | null;
  };

  type ValidationError = {
    /** Location */
    loc: (string | number)[];
    /** Message */
    msg: string;
    /** Error Type */
    type: string;
  };

  type WaterQualityCreate = {
    /** Sampling Date 取样日期 */
    sampling_date: string;
    /** Sampling Time 取样时间 */
    sampling_time?: string | null;
    /** Detection Date 检测日期 */
    detection_date: string;
    /** Code 编号 */
    code?: string | null;
    /** River Name 河道名称 */
    river_name: string;
    /** Method 方式 */
    method?: string | null;
    /** Cod Value COD数值 */
    cod_value?: number | null;
    /** Ammonia Nitrogen Value 氨氮数值 */
    ammonia_nitrogen_value?: number | null;
    /** Total Phosphorus Value 总磷数值 */
    total_phosphorus_value?: number | null;
    /** Potassium Permanganate Value 高锰酸钾数值 */
    potassium_permanganate_value?: number | null;
    /** Cod Level COD等级 */
    cod_level?: string | null;
    /** Ammonia Nitrogen Level 氨氮等级 */
    ammonia_nitrogen_level?: string | null;
    /** Total Phosphorus Level 总磷等级 */
    total_phosphorus_level?: string | null;
    /** Potassium Permanganate Level 高锰酸钾等级 */
    potassium_permanganate_level?: string | null;
    /** Comprehensive Quality Level 综合水质等级 */
    comprehensive_quality_level?: string | null;
    /** Comprehensive Level Number 综合等级数 */
    comprehensive_level_number?: number | null;
    /** Remarks 备注 */
    remarks?: string | null;
  };

  type WaterQualityListResponse = {
    /** Total 总数 */
    total: number;
    /** Page 当前页码 */
    page: number;
    /** Per Page 每页数量 */
    per_page: number;
    /** Items 数据列表 */
    items: WaterQualityResponse[];
  };

  type WaterQualityResponse = {
    /** Sampling Date 取样日期 */
    sampling_date: string;
    /** Sampling Time 取样时间 */
    sampling_time?: string | null;
    /** Detection Date 检测日期 */
    detection_date: string;
    /** Code 编号 */
    code?: string | null;
    /** River Name 河道名称 */
    river_name: string;
    /** Method 方式 */
    method?: string | null;
    /** Cod Value COD数值 */
    cod_value?: number | null;
    /** Ammonia Nitrogen Value 氨氮数值 */
    ammonia_nitrogen_value?: number | null;
    /** Total Phosphorus Value 总磷数值 */
    total_phosphorus_value?: number | null;
    /** Potassium Permanganate Value 高锰酸钾数值 */
    potassium_permanganate_value?: number | null;
    /** Cod Level COD等级 */
    cod_level?: string | null;
    /** Ammonia Nitrogen Level 氨氮等级 */
    ammonia_nitrogen_level?: string | null;
    /** Total Phosphorus Level 总磷等级 */
    total_phosphorus_level?: string | null;
    /** Potassium Permanganate Level 高锰酸钾等级 */
    potassium_permanganate_level?: string | null;
    /** Comprehensive Quality Level 综合水质等级 */
    comprehensive_quality_level?: string | null;
    /** Comprehensive Level Number 综合等级数 */
    comprehensive_level_number?: number | null;
    /** Remarks 备注 */
    remarks?: string | null;
    /** Id 数据ID */
    id: number;
    /** Created At 创建时间 */
    created_at: string;
    /** Updated At 更新时间 */
    updated_at: string;
  };

  type WaterQualityUpdate = {
    /** Sampling Date 取样日期 */
    sampling_date?: string | null;
    /** Sampling Time 取样时间 */
    sampling_time?: string | null;
    /** Detection Date 检测日期 */
    detection_date?: string | null;
    /** Code 编号 */
    code?: string | null;
    /** River Name 河道名称 */
    river_name?: string | null;
    /** Method 方式 */
    method?: string | null;
    /** Cod Value COD数值 */
    cod_value?: number | null;
    /** Ammonia Nitrogen Value 氨氮数值 */
    ammonia_nitrogen_value?: number | null;
    /** Total Phosphorus Value 总磷数值 */
    total_phosphorus_value?: number | null;
    /** Potassium Permanganate Value 高锰酸钾数值 */
    potassium_permanganate_value?: number | null;
    /** Cod Level COD等级 */
    cod_level?: string | null;
    /** Ammonia Nitrogen Level 氨氮等级 */
    ammonia_nitrogen_level?: string | null;
    /** Total Phosphorus Level 总磷等级 */
    total_phosphorus_level?: string | null;
    /** Potassium Permanganate Level 高锰酸钾等级 */
    potassium_permanganate_level?: string | null;
    /** Comprehensive Quality Level 综合水质等级 */
    comprehensive_quality_level?: string | null;
    /** Comprehensive Level Number 综合等级数 */
    comprehensive_level_number?: number | null;
    /** Remarks 备注 */
    remarks?: string | null;
  };
}
