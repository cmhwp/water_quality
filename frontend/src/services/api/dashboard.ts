// @ts-ignore
/* eslint-disable */
import request from "@/utils/request";

/** 获取大屏完整数据 获取大屏完整数据

一次性返回大屏所需的所有数据：
- 总览统计
- 河道统计
- 水质等级分布
- 月度趋势
- 指标统计
- 最新数据（5条）
- 警告数据 GET /api/v1/dashboard/all */
export async function getDashboardDataApiV1DashboardAllGet(options?: {
  [key: string]: any;
}) {
  return request<API.DashboardResponse>("/api/v1/dashboard/all", {
    method: "GET",
    ...(options || {}),
  });
}

/** 获取指标统计数据 获取指标统计数据

返回各指标的统计信息：
- 指标名称
- 平均值、最大值、最小值
- 超标率 GET /api/v1/dashboard/indicators */
export async function getIndicatorStatisticsApiV1DashboardIndicatorsGet(options?: {
  [key: string]: any;
}) {
  return request<API.IndicatorStatistics[]>("/api/v1/dashboard/indicators", {
    method: "GET",
    ...(options || {}),
  });
}

/** 获取方式列表 获取方式列表

返回所有方式名称列表 GET /api/v1/dashboard/method-list */
export async function getMethodListApiV1DashboardMethodListGet(options?: {
  [key: string]: any;
}) {
  return request<API.MethodListResponse>("/api/v1/dashboard/method-list", {
    method: "GET",
    ...(options || {}),
  });
}

/** 获取特定方式的大屏完整数据 获取特定方式的大屏完整数据

Args:
    method: 方式名称
    
Returns:
    MethodDashboardResponse: 方式大屏完整数据 GET /api/v1/dashboard/method/${param0}/all */
export async function getMethodDashboardDataApiV1DashboardMethodMethodAllGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMethodDashboardDataApiV1DashboardMethodMethodAllGetParams,
  options?: { [key: string]: any }
) {
  const { method: param0, ...queryParams } = params;
  return request<API.MethodDashboardResponse>(
    `/api/v1/dashboard/method/${param0}/all`,
    {
      method: "GET",
      params: { ...queryParams },
      ...(options || {}),
    }
  );
}

/** 获取特定方式的指标统计数据 获取特定方式的指标统计数据

Args:
    method: 方式名称
    
Returns:
    List[MethodIndicatorStatistics]: 方式指标统计数据列表 GET /api/v1/dashboard/method/${param0}/indicators */
export async function getMethodIndicatorStatisticsApiV1DashboardMethodMethodIndicatorsGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMethodIndicatorStatisticsApiV1DashboardMethodMethodIndicatorsGetParams,
  options?: { [key: string]: any }
) {
  const { method: param0, ...queryParams } = params;
  return request<API.MethodIndicatorStatistics[]>(
    `/api/v1/dashboard/method/${param0}/indicators`,
    {
      method: "GET",
      params: { ...queryParams },
      ...(options || {}),
    }
  );
}

/** 获取特定方式的月度趋势数据 获取特定方式的月度趋势数据

Args:
    method: 方式名称
    limit: 返回月份数量限制
    
Returns:
    List[MethodMonthlyTrend]: 方式月度趋势数据列表 GET /api/v1/dashboard/method/${param0}/monthly-trend */
export async function getMethodMonthlyTrendApiV1DashboardMethodMethodMonthlyTrendGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMethodMonthlyTrendApiV1DashboardMethodMethodMonthlyTrendGetParams,
  options?: { [key: string]: any }
) {
  const { method: param0, ...queryParams } = params;
  return request<API.MethodMonthlyTrend[]>(
    `/api/v1/dashboard/method/${param0}/monthly-trend`,
    {
      method: "GET",
      params: {
        // limit has a default value: 12
        limit: "12",
        ...queryParams,
      },
      ...(options || {}),
    }
  );
}

/** 获取特定方式的总览统计数据 获取特定方式的总览统计数据

Args:
    method: 方式名称
    
Returns:
    MethodOverviewStatistics: 方式总览统计数据 GET /api/v1/dashboard/method/${param0}/overview */
export async function getMethodOverviewStatisticsApiV1DashboardMethodMethodOverviewGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMethodOverviewStatisticsApiV1DashboardMethodMethodOverviewGetParams,
  options?: { [key: string]: any }
) {
  const { method: param0, ...queryParams } = params;
  return request<API.MethodOverviewStatistics>(
    `/api/v1/dashboard/method/${param0}/overview`,
    {
      method: "GET",
      params: { ...queryParams },
      ...(options || {}),
    }
  );
}

/** 获取特定方式的水质等级分布 获取特定方式的水质等级分布

Args:
    method: 方式名称
    
Returns:
    List[MethodQualityDistribution]: 方式水质等级分布列表 GET /api/v1/dashboard/method/${param0}/quality-distribution */
export async function getMethodQualityDistributionApiV1DashboardMethodMethodQualityDistributionGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMethodQualityDistributionApiV1DashboardMethodMethodQualityDistributionGetParams,
  options?: { [key: string]: any }
) {
  const { method: param0, ...queryParams } = params;
  return request<API.MethodQualityDistribution[]>(
    `/api/v1/dashboard/method/${param0}/quality-distribution`,
    {
      method: "GET",
      params: { ...queryParams },
      ...(options || {}),
    }
  );
}

/** 获取特定方式的最新水质数据 获取特定方式的最新水质数据

Args:
    method: 方式名称
    limit: 返回数据条数限制
    
Returns:
    List[RecentWaterQuality]: 最新水质数据列表 GET /api/v1/dashboard/method/${param0}/recent-data */
export async function getMethodRecentWaterQualityApiV1DashboardMethodMethodRecentDataGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMethodRecentWaterQualityApiV1DashboardMethodMethodRecentDataGetParams,
  options?: { [key: string]: any }
) {
  const { method: param0, ...queryParams } = params;
  return request<API.RecentWaterQuality[]>(
    `/api/v1/dashboard/method/${param0}/recent-data`,
    {
      method: "GET",
      params: {
        // limit has a default value: 5
        limit: "5",
        ...queryParams,
      },
      ...(options || {}),
    }
  );
}

/** 获取特定方式的河道统计数据 获取特定方式的河道统计数据

Args:
    method: 方式名称
    limit: 返回数据条数限制
    
Returns:
    List[MethodRiverStatistics]: 方式河道统计数据列表 GET /api/v1/dashboard/method/${param0}/rivers */
export async function getMethodRiverStatisticsApiV1DashboardMethodMethodRiversGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMethodRiverStatisticsApiV1DashboardMethodMethodRiversGetParams,
  options?: { [key: string]: any }
) {
  const { method: param0, ...queryParams } = params;
  return request<API.MethodRiverStatistics[]>(
    `/api/v1/dashboard/method/${param0}/rivers`,
    {
      method: "GET",
      params: {
        // limit has a default value: 20
        limit: "20",
        ...queryParams,
      },
      ...(options || {}),
    }
  );
}

/** 获取特定方式的警告水质数据 获取特定方式的警告水质数据

Args:
    method: 方式名称
    limit: 返回数据条数限制
    
Returns:
    List[WarningWaterQuality]: 警告水质数据列表 GET /api/v1/dashboard/method/${param0}/warning-data */
export async function getMethodWarningWaterQualityApiV1DashboardMethodMethodWarningDataGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMethodWarningWaterQualityApiV1DashboardMethodMethodWarningDataGetParams,
  options?: { [key: string]: any }
) {
  const { method: param0, ...queryParams } = params;
  return request<API.WarningWaterQuality[]>(
    `/api/v1/dashboard/method/${param0}/warning-data`,
    {
      method: "GET",
      params: {
        // limit has a default value: 20
        limit: "20",
        ...queryParams,
      },
      ...(options || {}),
    }
  );
}

/** 获取方式统计数据 获取方式统计数据

返回各方式的统计信息 GET /api/v1/dashboard/methods */
export async function getMethodStatisticsApiV1DashboardMethodsGet(options?: {
  [key: string]: any;
}) {
  return request<API.MethodStatistics[]>("/api/v1/dashboard/methods", {
    method: "GET",
    ...(options || {}),
  });
}

/** 获取月度趋势数据 获取月度趋势数据

返回各月份的水质趋势：
- 月份
- 总数据量
- 优质水质数量
- 优质水质达标率 GET /api/v1/dashboard/monthly-trend */
export async function getMonthlyTrendApiV1DashboardMonthlyTrendGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getMonthlyTrendApiV1DashboardMonthlyTrendGetParams,
  options?: { [key: string]: any }
) {
  return request<API.MonthlyTrend[]>("/api/v1/dashboard/monthly-trend", {
    method: "GET",
    params: {
      // limit has a default value: 12
      limit: "12",
      ...params,
    },
    ...(options || {}),
  });
}

/** 获取总览统计数据 获取总览统计数据

返回水质数据的总体统计信息：
- 总数据量
- 各等级水质数量
- 优质水质达标率
- 最新数据更新时间 GET /api/v1/dashboard/overview */
export async function getOverviewStatisticsApiV1DashboardOverviewGet(options?: {
  [key: string]: any;
}) {
  return request<API.OverviewStatistics>("/api/v1/dashboard/overview", {
    method: "GET",
    ...(options || {}),
  });
}

/** 获取水质等级分布 获取水质等级分布

返回各水质等级的分布情况：
- 水质等级
- 数量
- 占比百分比 GET /api/v1/dashboard/quality-distribution */
export async function getQualityDistributionApiV1DashboardQualityDistributionGet(options?: {
  [key: string]: any;
}) {
  return request<API.QualityLevelDistribution[]>(
    "/api/v1/dashboard/quality-distribution",
    {
      method: "GET",
      ...(options || {}),
    }
  );
}

/** 获取水质等级统计数据 获取水质等级统计数据

Returns:
    WaterQualityLevelStatistics: 水质等级统计数据 GET /api/v1/dashboard/quality-levels */
export async function getWaterQualityLevelStatisticsApiV1DashboardQualityLevelsGet(options?: {
  [key: string]: any;
}) {
  return request<API.WaterQualityLevelStatistics>(
    "/api/v1/dashboard/quality-levels",
    {
      method: "GET",
      ...(options || {}),
    }
  );
}

/** 获取最新水质数据 获取最新水质数据

返回最新的水质监测数据：
- 河道名称
- 采样日期
- 水质等级
- 各指标数值 GET /api/v1/dashboard/recent-data */
export async function getRecentWaterQualityApiV1DashboardRecentDataGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getRecentWaterQualityApiV1DashboardRecentDataGetParams,
  options?: { [key: string]: any }
) {
  return request<API.RecentWaterQuality[]>("/api/v1/dashboard/recent-data", {
    method: "GET",
    params: {
      // limit has a default value: 5
      limit: "5",
      ...params,
    },
    ...(options || {}),
  });
}

/** 获取河道列表 获取河道列表

返回所有河道名称列表 GET /api/v1/dashboard/river-list */
export async function getRiverListApiV1DashboardRiverListGet(options?: {
  [key: string]: any;
}) {
  return request<API.RiverListResponse>("/api/v1/dashboard/river-list", {
    method: "GET",
    ...(options || {}),
  });
}

/** 获取特定河道数据 获取特定河道数据

返回指定河道的水质监测数据 GET /api/v1/dashboard/river/${param0} */
export async function getRiverDataApiV1DashboardRiverRiverNameGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getRiverDataApiV1DashboardRiverRiverNameGetParams,
  options?: { [key: string]: any }
) {
  const { river_name: param0, ...queryParams } = params;
  return request<API.RecentWaterQuality[]>(
    `/api/v1/dashboard/river/${param0}`,
    {
      method: "GET",
      params: {
        // limit has a default value: 20
        limit: "20",
        ...queryParams,
      },
      ...(options || {}),
    }
  );
}

/** 获取河道统计数据 获取河道统计数据

返回各河道的水质统计信息：
- 河道名称
- 各等级水质数量
- 优质水质达标率
- 最新采样时间 GET /api/v1/dashboard/rivers */
export async function getRiverStatisticsApiV1DashboardRiversGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getRiverStatisticsApiV1DashboardRiversGetParams,
  options?: { [key: string]: any }
) {
  return request<API.RiverStatistics[]>("/api/v1/dashboard/rivers", {
    method: "GET",
    params: {
      // limit has a default value: 20
      limit: "20",
      ...params,
    },
    ...(options || {}),
  });
}

/** 获取警告水质数据 获取警告水质数据

返回污染严重的水质监测数据（Ⅴ类、劣Ⅴ类、轻度黑臭、重度黑臭）：
- 河道名称
- 采样日期
- 水质等级
- 各指标数值
- 警告等级

数据按污染严重程度排序，优先展示重度污染数据 GET /api/v1/dashboard/warning-data */
export async function getWarningWaterQualityApiV1DashboardWarningDataGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getWarningWaterQualityApiV1DashboardWarningDataGetParams,
  options?: { [key: string]: any }
) {
  return request<API.WarningWaterQuality[]>("/api/v1/dashboard/warning-data", {
    method: "GET",
    params: {
      // limit has a default value: 20
      limit: "20",
      ...params,
    },
    ...(options || {}),
  });
}
