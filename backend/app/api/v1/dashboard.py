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
    WaterQualityLevelStatistics
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
    - 各等级水质数量
    - 优质水质达标率
    - 最新采样时间
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_river_statistics(limit=limit)


@router.get("/quality-distribution", response_model=List[QualityLevelDistribution], summary="获取水质等级分布")
def get_quality_distribution(
    db: Session = Depends(get_db)
):
    """
    获取水质等级分布
    
    返回各水质等级的分布情况：
    - 水质等级
    - 数量
    - 占比百分比
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
    
    返回各月份的水质趋势：
    - 月份
    - 总数据量
    - 优质水质数量
    - 优质水质达标率
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_monthly_trend(limit=limit)


@router.get("/indicators", response_model=List[IndicatorStatistics], summary="获取指标统计数据")
def get_indicator_statistics(
    db: Session = Depends(get_db)
):
    """
    获取指标统计数据
    
    返回各指标的统计信息：
    - 指标名称
    - 平均值、最大值、最小值
    - 超标率
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_indicator_statistics()


@router.get("/recent-data", response_model=List[RecentWaterQuality], summary="获取最新水质数据")
def get_recent_water_quality(
    limit: int = Query(5, ge=1, le=20, description="返回数据条数限制"),
    db: Session = Depends(get_db)
):
    """
    获取最新水质数据
    
    返回最新的水质监测数据：
    - 河道名称
    - 采样日期
    - 水质等级
    - 各指标数值
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_recent_water_quality(limit=limit)


@router.get("/warning-data", response_model=List[WarningWaterQuality], summary="获取警告水质数据")
def get_warning_water_quality(
    limit: int = Query(20, ge=1, le=50, description="返回数据条数限制"),
    db: Session = Depends(get_db)
):
    """
    获取警告水质数据
    
    返回污染严重的水质监测数据（Ⅴ类、劣Ⅴ类、轻度黑臭、重度黑臭）：
    - 河道名称
    - 采样日期
    - 水质等级
    - 各指标数值
    - 警告等级
    
    数据按污染严重程度排序，优先展示重度污染数据
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_warning_water_quality(limit=limit)


@router.get("/all", response_model=DashboardResponse, summary="获取大屏完整数据")
def get_dashboard_data(
    db: Session = Depends(get_db)
):
    """
    获取大屏完整数据
    
    一次性返回大屏所需的所有数据：
    - 总览统计
    - 河道统计
    - 水质等级分布
    - 月度趋势
    - 指标统计
    - 最新数据（5条）
    - 警告数据
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_dashboard_data()


@router.get("/river-list", response_model=RiverListResponse, summary="获取河道列表")
def get_river_list(
    db: Session = Depends(get_db)
):
    """
    获取河道列表
    
    返回所有河道名称列表
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
    获取特定河道数据
    
    返回指定河道的水质监测数据
    """
    dashboard_service = DashboardService(db)
    
    # 构建查询条件
    from app.models.water_quality import WaterQuality
    recent_data = dashboard_service.db.query(WaterQuality)\
        .filter(WaterQuality.river_name == river_name)\
        .order_by(WaterQuality.sampling_date.desc())\
        .limit(limit).all()
    
    if not recent_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"河道'{river_name}'未找到数据"
        )
    
    result = []
    for data in recent_data:
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


@router.get("/method-list", response_model=MethodListResponse, summary="获取方式列表")
def get_method_list(
    db: Session = Depends(get_db)
):
    """
    获取方式列表
    
    返回所有方式名称列表
    """
    dashboard_service = DashboardService(db)
    return dashboard_service.get_method_list()


@router.get("/methods", response_model=List[MethodStatistics], summary="获取方式统计数据")
def get_method_statistics(
    db: Session = Depends(get_db)
):
    """
    获取方式统计数据
    
    返回各方式的统计信息
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
    
    Args:
        method: 方式名称
        
    Returns:
        MethodOverviewStatistics: 方式总览统计数据
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_method_overview_statistics(method)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方式'{method}'总览统计数据失败: {str(e)}"
        )


@router.get("/method/{method}/rivers", response_model=List[MethodRiverStatistics], summary="获取特定方式的河道统计数据")
def get_method_river_statistics(
    method: str,
    limit: int = Query(20, ge=1, le=100, description="返回河道数量限制"),
    db: Session = Depends(get_db)
):
    """
    获取特定方式的河道统计数据
    
    Args:
        method: 方式名称
        limit: 返回数据条数限制
        
    Returns:
        List[MethodRiverStatistics]: 方式河道统计数据列表
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_method_river_statistics(method, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方式'{method}'河道统计数据失败: {str(e)}"
        )


@router.get("/method/{method}/quality-distribution", response_model=List[MethodQualityDistribution], summary="获取特定方式的水质等级分布")
def get_method_quality_distribution(
    method: str,
    db: Session = Depends(get_db)
):
    """
    获取特定方式的水质等级分布
    
    Args:
        method: 方式名称
        
    Returns:
        List[MethodQualityDistribution]: 方式水质等级分布列表
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_method_quality_distribution(method)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方式'{method}'水质等级分布失败: {str(e)}"
        )


@router.get("/method/{method}/monthly-trend", response_model=List[MethodMonthlyTrend], summary="获取特定方式的月度趋势数据")
def get_method_monthly_trend(
    method: str,
    limit: int = Query(12, ge=1, le=24, description="返回月份数量限制"),
    db: Session = Depends(get_db)
):
    """
    获取特定方式的月度趋势数据
    
    Args:
        method: 方式名称
        limit: 返回月份数量限制
        
    Returns:
        List[MethodMonthlyTrend]: 方式月度趋势数据列表
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_method_monthly_trend(method, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方式'{method}'月度趋势数据失败: {str(e)}"
        )


@router.get("/method/{method}/indicators", response_model=List[MethodIndicatorStatistics], summary="获取特定方式的指标统计数据")
def get_method_indicator_statistics(
    method: str,
    db: Session = Depends(get_db)
):
    """
    获取特定方式的指标统计数据
    
    Args:
        method: 方式名称
        
    Returns:
        List[MethodIndicatorStatistics]: 方式指标统计数据列表
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_method_indicator_statistics(method)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方式'{method}'指标统计数据失败: {str(e)}"
        )


@router.get("/method/{method}/recent-data", response_model=List[RecentWaterQuality], summary="获取特定方式的最新水质数据")
def get_method_recent_water_quality(
    method: str,
    limit: int = Query(5, ge=1, le=20, description="返回数据条数限制"),
    db: Session = Depends(get_db)
):
    """
    获取特定方式的最新水质数据
    
    Args:
        method: 方式名称
        limit: 返回数据条数限制
        
    Returns:
        List[RecentWaterQuality]: 最新水质数据列表
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_method_recent_water_quality(method, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方式'{method}'最新水质数据失败: {str(e)}"
        )


@router.get("/method/{method}/warning-data", response_model=List[WarningWaterQuality], summary="获取特定方式的警告水质数据")
def get_method_warning_water_quality(
    method: str,
    limit: int = Query(20, ge=1, le=50, description="返回数据条数限制"),
    db: Session = Depends(get_db)
):
    """
    获取特定方式的警告水质数据
    
    Args:
        method: 方式名称
        limit: 返回数据条数限制
        
    Returns:
        List[WarningWaterQuality]: 警告水质数据列表
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_method_warning_water_quality(method, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方式'{method}'警告水质数据失败: {str(e)}"
        )


@router.get("/method/{method}/all", response_model=MethodDashboardResponse, summary="获取特定方式的大屏完整数据")
def get_method_dashboard_data(
    method: str,
    db: Session = Depends(get_db)
):
    """
    获取特定方式的大屏完整数据
    
    Args:
        method: 方式名称
        
    Returns:
        MethodDashboardResponse: 方式大屏完整数据
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_method_dashboard_data(method)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方式'{method}'大屏数据失败: {str(e)}"
        )


@router.get("/quality-levels", response_model=WaterQualityLevelStatistics, summary="获取水质等级统计数据")
def get_water_quality_level_statistics(
    db: Session = Depends(get_db)
):
    """
    获取水质等级统计数据
    
    Returns:
        WaterQualityLevelStatistics: 水质等级统计数据
    """
    dashboard_service = DashboardService(db)
    try:
        return dashboard_service.get_water_quality_level_statistics()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取水质等级统计数据失败: {str(e)}"
        ) 