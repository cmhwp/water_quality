// @ts-ignore
/* eslint-disable */
import request from "@/utils/request";

/** 获取水质数据列表 获取水质数据列表 GET /api/v1/water-quality/ */
export async function getWaterQualityListApiV1WaterQualityGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getWaterQualityListApiV1WaterQualityGetParams,
  options?: { [key: string]: any }
) {
  return request<API.WaterQualityListResponse>("/api/v1/water-quality/", {
    method: "GET",
    params: {
      // page has a default value: 1
      page: "1",
      // per_page has a default value: 20
      per_page: "20",

      ...params,
    },
    ...(options || {}),
  });
}

/** 创建水质数据 创建水质数据 POST /api/v1/water-quality/ */
export async function createWaterQualityApiV1WaterQualityPost(
  body: API.WaterQualityCreate,
  options?: { [key: string]: any }
) {
  return request<API.WaterQualityResponse>("/api/v1/water-quality/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    data: body,
    ...(options || {}),
  });
}

/** 获取单个水质数据 获取单个水质数据 GET /api/v1/water-quality/${param0} */
export async function getWaterQualityByIdApiV1WaterQualityWaterQualityIdGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.getWaterQualityByIdApiV1WaterQualityWaterQualityIdGetParams,
  options?: { [key: string]: any }
) {
  const { water_quality_id: param0, ...queryParams } = params;
  return request<API.WaterQualityResponse>(`/api/v1/water-quality/${param0}`, {
    method: "GET",
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** 更新水质数据 更新水质数据 PUT /api/v1/water-quality/${param0} */
export async function updateWaterQualityApiV1WaterQualityWaterQualityIdPut(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.updateWaterQualityApiV1WaterQualityWaterQualityIdPutParams,
  body: API.WaterQualityUpdate,
  options?: { [key: string]: any }
) {
  const { water_quality_id: param0, ...queryParams } = params;
  return request<API.WaterQualityResponse>(`/api/v1/water-quality/${param0}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    params: { ...queryParams },
    data: body,
    ...(options || {}),
  });
}

/** 删除水质数据 删除水质数据 DELETE /api/v1/water-quality/${param0} */
export async function deleteWaterQualityApiV1WaterQualityWaterQualityIdDelete(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.deleteWaterQualityApiV1WaterQualityWaterQualityIdDeleteParams,
  options?: { [key: string]: any }
) {
  const { water_quality_id: param0, ...queryParams } = params;
  return request<any>(`/api/v1/water-quality/${param0}`, {
    method: "DELETE",
    params: { ...queryParams },
    ...(options || {}),
  });
}

/** 获取水质等级列表 获取水质等级列表 GET /api/v1/water-quality/options/quality-levels */
export async function getQualityLevelsApiV1WaterQualityOptionsQualityLevelsGet(options?: {
  [key: string]: any;
}) {
  return request<string[]>("/api/v1/water-quality/options/quality-levels", {
    method: "GET",
    ...(options || {}),
  });
}

/** 获取河道列表 获取河道列表 GET /api/v1/water-quality/options/rivers */
export async function getRiverListApiV1WaterQualityOptionsRiversGet(options?: {
  [key: string]: any;
}) {
  return request<string[]>("/api/v1/water-quality/options/rivers", {
    method: "GET",
    ...(options || {}),
  });
}

/** 获取水质数据统计 获取水质数据统计 GET /api/v1/water-quality/statistics/overview */
export async function getWaterQualityStatisticsApiV1WaterQualityStatisticsOverviewGet(options?: {
  [key: string]: any;
}) {
  return request<any>("/api/v1/water-quality/statistics/overview", {
    method: "GET",
    ...(options || {}),
  });
}
