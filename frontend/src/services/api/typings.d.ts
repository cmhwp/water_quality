declare namespace API {
  type deleteWaterQualityApiV1WaterQualityWaterQualityIdDeleteParams = {
    water_quality_id: number;
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
