"""
服务模块
"""
from app.services.water_quality_service import WaterQualityService
from app.services.user_service import UserService
from app.services.dashboard_service import DashboardService

__all__ = ["WaterQualityService", "UserService", "DashboardService"] 