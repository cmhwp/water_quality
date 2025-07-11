"""
数据模式模块
"""
from app.schemas.water_quality import (
    WaterQualityBase,
    WaterQualityCreate,
    WaterQualityUpdate,
    WaterQualityResponse,
    WaterQualityListResponse,
    WaterQualityQuery
)
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData
)

__all__ = [
    "WaterQualityBase",
    "WaterQualityCreate", 
    "WaterQualityUpdate",
    "WaterQualityResponse",
    "WaterQualityListResponse", 
    "WaterQualityQuery",
    "UserBase",
    "UserCreate",
    "UserUpdate", 
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData"
] 