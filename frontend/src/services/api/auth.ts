// @ts-ignore
/* eslint-disable */
import request from "@/utils/request";

/** 用户登录 用户登录 POST /api/v1/auth/login */
export async function loginApiV1AuthLoginPost(
  body: API.UserLogin,
  options?: { [key: string]: any }
) {
  return request<API.Token>("/api/v1/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    data: body,
    ...(options || {}),
  });
}

/** 用户退出登录 用户退出登录 POST /api/v1/auth/logout */
export async function logoutApiV1AuthLogoutPost(options?: {
  [key: string]: any;
}) {
  return request<any>("/api/v1/auth/logout", {
    method: "POST",
    ...(options || {}),
  });
}

/** 获取当前用户信息 获取当前用户信息 GET /api/v1/auth/me */
export async function getCurrentUserInfoApiV1AuthMeGet(options?: {
  [key: string]: any;
}) {
  return request<API.UserResponse>("/api/v1/auth/me", {
    method: "GET",
    ...(options || {}),
  });
}

/** 刷新令牌 刷新令牌 POST /api/v1/auth/refresh */
export async function refreshTokenApiV1AuthRefreshPost(options?: {
  [key: string]: any;
}) {
  return request<API.Token>("/api/v1/auth/refresh", {
    method: "POST",
    ...(options || {}),
  });
}
