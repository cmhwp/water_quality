// @ts-ignore
/* eslint-disable */
import request from "@/utils/request";

/** 健康检查 健康检查端点 GET /health */
export async function healthCheckHealthGet(options?: { [key: string]: any }) {
  return request<any>("/health", {
    method: "GET",
    ...(options || {}),
  });
}
