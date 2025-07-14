"""
数据模式包
"""
from .user import (
    UserBase, UserCreate, UserUpdate, UserResponse, 
    UserLogin, Token, TokenData
)
from .water_quality import (
    WaterQualityBase, WaterQualityCreate, WaterQualityUpdate, 
    WaterQualityResponse, WaterQualityListResponse, WaterQualityQuery
)
from .dashboard import (
    OverviewStatistics,
    RiverStatistics,
    QualityLevelDistribution,
    MonthlyTrend,
    IndicatorStatistics,
    RecentWaterQuality,
    WarningWaterQuality,
    DashboardResponse,
    RiverListResponse,
    MethodStatistics,
    MethodOverviewStatistics,
    MethodRiverStatistics,
    MethodQualityDistribution,
    MethodMonthlyTrend,
    MethodIndicatorStatistics,
    MethodDashboardResponse,
    MethodListResponse,
    IndicatorLevelDistribution,
    IndicatorLevelStatistics,
    WaterQualityLevelStatistics
)

__all__ = [
    # 用户相关
    "UserBase",
    "UserCreate", 
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    # 水质相关
    "WaterQualityBase",
    "WaterQualityCreate",
    "WaterQualityUpdate",
    "WaterQualityResponse",
    "WaterQualityListResponse",
    "WaterQualityQuery",
    # 大屏相关
    "OverviewStatistics",
    "RiverStatistics",
    "QualityLevelDistribution",
    "MonthlyTrend",
    "IndicatorStatistics",
    "RecentWaterQuality",
    "WarningWaterQuality",
    "DashboardResponse",
    "RiverListResponse",
    "MethodStatistics",
    "MethodOverviewStatistics",
    "MethodRiverStatistics",
    "MethodQualityDistribution",
    "MethodMonthlyTrend",
    "MethodIndicatorStatistics",
    "MethodDashboardResponse",
    "MethodListResponse",
    "IndicatorLevelDistribution",
    "IndicatorLevelStatistics",
    "WaterQualityLevelStatistics"
] 