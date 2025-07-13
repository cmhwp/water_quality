"""
大屏可视化API路由
"""
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.dashboard import (
    OverviewStatistics,
    RiverStatistics, 
    QualityLevelDistribution,
    MonthlyTrend,
    IndicatorStatistics,
    RecentWaterQuality,
    DashboardResponse,
    RiverListResponse,
    MethodStatistics,
    MethodOverviewStatistics,
    MethodRiverStatistics,
    MethodQualityDistribution,
    MethodMonthlyTrend,
    MethodIndicatorStatistics,
    MethodDashboardResponse,
    MethodListResponse
)
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/overview", response_model=OverviewStatistics, summary="获取总览统计数据")
def get_overview_statistics(
    db: Session = Depends(get_db)
):
    """
    获取总览统计数据
    
    返回水质数据的总体统计信息：
    - 总数据量
    - 各等级水质数量
    - 优质水质达标率
    - 最新数据更新时间
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_overview_statistics()


@router.get("/rivers", response_model=List[RiverStatistics], summary="获取河道统计数据")
def get_river_statistics(
    limit: int = Query(20, ge=1, le=100, description="返回河道数量限制"),
    db: Session = Depends(get_db)
):
    """
    获取河道统计数据
    
    返回各河道的水质统计信息：
    - 河道名称
    - 数据总量
    - 各等级水质数量
    - 优质水质达标率
    - 最新采样时间
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_river_statistics(limit)


@router.get("/quality-distribution", response_model=List[QualityLevelDistribution], summary="获取水质等级分布")
def get_quality_distribution(
    db: Session = Depends(get_db)
):
    """
    获取水质等级分布
    
    返回各水质等级的数量和百分比分布：
    - 水质等级
    - 数量
    - 百分比
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_quality_distribution()


@router.get("/monthly-trend", response_model=List[MonthlyTrend], summary="获取月度趋势数据")
def get_monthly_trend(
    limit: int = Query(12, ge=1, le=24, description="返回月份数量限制"),
    db: Session = Depends(get_db)
):
    """
    获取月度趋势数据
    
    返回按月份统计的水质趋势：
    - 月份
    - 总数据量
    - 优质水质数量
    - 优质水质达标率
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_monthly_trend(limit)


@router.get("/indicators", response_model=List[IndicatorStatistics], summary="获取指标统计数据")
def get_indicator_statistics(
    db: Session = Depends(get_db)
):
    """
    获取指标统计数据
    
    返回各水质指标的统计信息：
    - 指标名称
    - 平均值、最大值、最小值
    - 单位
    - 标准值
    - 超标率
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_indicator_statistics()


@router.get("/recent-data", response_model=List[RecentWaterQuality], summary="获取最新水质数据")
def get_recent_water_quality(
    limit: int = Query(10, ge=1, le=50, description="返回数据条数限制"),
    db: Session = Depends(get_db)
):
    """
    获取最新水质数据
    
    返回最近的水质检测数据：
    - 河道名称
    - 采样日期
    - 综合水质等级
    - 各项指标值
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_recent_water_quality(limit)


@router.get("/all", response_model=DashboardResponse, summary="获取大屏完整数据")
def get_dashboard_data(
    db: Session = Depends(get_db)
):
    """
    获取大屏完整数据
    
    一次性返回大屏所需的所有统计数据：
    - 总览统计
    - 河道统计
    - 水质等级分布
    - 月度趋势
    - 指标统计
    - 最新数据
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_dashboard_data()


@router.get("/river-list", response_model=RiverListResponse, summary="获取河道列表")
def get_river_list(
    db: Session = Depends(get_db)
):
    """
    获取河道列表
    
    返回所有河道名称列表：
    - 河道名称数组
    - 河道总数
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_river_list()


@router.get("/river/{river_name}", response_model=List[RecentWaterQuality], summary="获取特定河道数据")
def get_river_data(
    river_name: str,
    limit: int = Query(20, ge=1, le=100, description="返回数据条数限制"),
    db: Session = Depends(get_db)
):
    """
    获取特定河道的水质数据
    
    返回指定河道的最新水质数据：
    - 河道名称
    - 采样日期
    - 综合水质等级
    - 各项指标值
    """
    dashboard_service = DashboardService(db)
    
    # 查询特定河道的数据
    from app.models.water_quality import WaterQuality
    river_data = db.query(WaterQuality)\
        .filter(WaterQuality.river_name == river_name)\
        .order_by(WaterQuality.sampling_date.desc())\
        .limit(limit).all()
    
    result = []
    for data in river_data:
        result.append(RecentWaterQuality(
            id=data.id,
            river_name=data.river_name,
            sampling_date=data.sampling_date,
            comprehensive_quality_level=data.comprehensive_quality_level or "未知",
            cod_value=data.cod_value,
            ammonia_nitrogen_value=data.ammonia_nitrogen_value,
            total_phosphorus_value=data.total_phosphorus_value,
            potassium_permanganate_value=data.potassium_permanganate_value
        ))
    
    return result


# 新增方式细分相关的API端点
@router.get("/method-list", response_model=MethodListResponse, summary="获取方式列表")
def get_method_list(
    db: Session = Depends(get_db)
):
    """
    获取方式列表
    
    返回所有方式名称列表：
    - 方式名称数组
    - 方式总数
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_method_list()


@router.get("/methods", response_model=List[MethodStatistics], summary="获取方式统计数据")
def get_method_statistics(
    db: Session = Depends(get_db)
):
    """
    获取方式统计数据
    
    返回各方式的水质统计信息：
    - 方式名称
    - 数据总量
    - 各等级水质数量
    - 优质水质达标率
    - 最新采样时间
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_method_statistics()


@router.get("/method/{method}/overview", response_model=MethodOverviewStatistics, summary="获取特定方式的总览统计数据")
def get_method_overview_statistics(
    method: str,
    db: Session = Depends(get_db)
):
    """
    获取特定方式的总览统计数据
    
    返回指定方式的水质数据总体统计信息：
    - 方式名称
    - 总数据量
    - 各等级水质数量
    - 优质水质达标率
    - 最新数据更新时间
    """
    dashboard_service = DashboardService(db)
    
    # 验证方式是否存在
    method_list = dashboard_service.get_method_list()
    if method not in method_list.methods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"方式 '{method}' 不存在"
        )
    
    return dashboard_service.get_method_overview_statistics(method)


@router.get("/method/{method}/rivers", response_model=List[MethodRiverStatistics], summary="获取特定方式的河道统计数据")
def get_method_river_statistics(
    method: str,
    limit: int = Query(20, ge=1, le=100, description="返回河道数量限制"),
    db: Session = Depends(get_db)
):
    """
    获取特定方式的河道统计数据
    
    返回指定方式各河道的水质统计信息：
    - 方式名称
    - 河道名称
    - 数据总量
    - 各等级水质数量
    - 优质水质达标率
    - 最新采样时间
    """
    dashboard_service = DashboardService(db)
    
    # 验证方式是否存在
    method_list = dashboard_service.get_method_list()
    if method not in method_list.methods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"方式 '{method}' 不存在"
        )
    
    return dashboard_service.get_method_river_statistics(method, limit)


@router.get("/method/{method}/quality-distribution", response_model=List[MethodQualityDistribution], summary="获取特定方式的水质等级分布")
def get_method_quality_distribution(
    method: str,
    db: Session = Depends(get_db)
):
    """
    获取特定方式的水质等级分布
    
    返回指定方式各水质等级的数量和百分比分布：
    - 方式名称
    - 水质等级
    - 数量
    - 百分比
    """
    dashboard_service = DashboardService(db)
    
    # 验证方式是否存在
    method_list = dashboard_service.get_method_list()
    if method not in method_list.methods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"方式 '{method}' 不存在"
        )
    
    return dashboard_service.get_method_quality_distribution(method)


@router.get("/method/{method}/monthly-trend", response_model=List[MethodMonthlyTrend], summary="获取特定方式的月度趋势数据")
def get_method_monthly_trend(
    method: str,
    limit: int = Query(12, ge=1, le=24, description="返回月份数量限制"),
    db: Session = Depends(get_db)
):
    """
    获取特定方式的月度趋势数据
    
    返回指定方式按月份统计的水质趋势：
    - 方式名称
    - 月份
    - 总数据量
    - 优质水质数量
    - 优质水质达标率
    """
    dashboard_service = DashboardService(db)
    
    # 验证方式是否存在
    method_list = dashboard_service.get_method_list()
    if method not in method_list.methods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"方式 '{method}' 不存在"
        )
    
    return dashboard_service.get_method_monthly_trend(method, limit)


@router.get("/method/{method}/indicators", response_model=List[MethodIndicatorStatistics], summary="获取特定方式的指标统计数据")
def get_method_indicator_statistics(
    method: str,
    db: Session = Depends(get_db)
):
    """
    获取特定方式的指标统计数据
    
    返回指定方式各水质指标的统计信息：
    - 方式名称
    - 指标名称
    - 平均值、最大值、最小值
    - 单位
    - 标准值
    - 超标率
    """
    dashboard_service = DashboardService(db)
    
    # 验证方式是否存在
    method_list = dashboard_service.get_method_list()
    if method not in method_list.methods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"方式 '{method}' 不存在"
        )
    
    return dashboard_service.get_method_indicator_statistics(method)


@router.get("/method/{method}/recent-data", response_model=List[RecentWaterQuality], summary="获取特定方式的最新水质数据")
def get_method_recent_water_quality(
    method: str,
    limit: int = Query(10, ge=1, le=50, description="返回数据条数限制"),
    db: Session = Depends(get_db)
):
    """
    获取特定方式的最新水质数据
    
    返回指定方式最近的水质检测数据：
    - 河道名称
    - 采样日期
    - 综合水质等级
    - 各项指标值
    """
    dashboard_service = DashboardService(db)
    
    # 验证方式是否存在
    method_list = dashboard_service.get_method_list()
    if method not in method_list.methods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"方式 '{method}' 不存在"
        )
    
    return dashboard_service.get_method_recent_water_quality(method, limit)


@router.get("/method/{method}/all", response_model=MethodDashboardResponse, summary="获取特定方式的大屏完整数据")
def get_method_dashboard_data(
    method: str,
    db: Session = Depends(get_db)
):
    """
    获取特定方式的大屏完整数据
    
    一次性返回指定方式大屏所需的所有统计数据：
    - 方式名称
    - 总览统计
    - 河道统计
    - 水质等级分布
    - 月度趋势
    - 指标统计
    - 最新数据
    """
    dashboard_service = DashboardService(db)
    
    # 验证方式是否存在
    method_list = dashboard_service.get_method_list()
    if method not in method_list.methods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"方式 '{method}' 不存在"
        )
    
    return dashboard_service.get_method_dashboard_data(method) 