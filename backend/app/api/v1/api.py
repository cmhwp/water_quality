"""
API v1 路由整合
"""
from fastapi import APIRouter
from app.api.v1 import auth, water_quality

api_router = APIRouter()

# 认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# 水质数据相关路由
api_router.include_router(water_quality.router, prefix="/water-quality", tags=["water-quality"]) 