"""
水质数据API路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.water_quality import (
    WaterQualityResponse, 
    WaterQualityCreate, 
    WaterQualityUpdate, 
    WaterQualityListResponse,
    WaterQualityQuery
)
from app.services.water_quality_service import WaterQualityService
from app.core.deps import get_current_admin_user, get_current_user
from app.utils.common import parse_datetime
from config import settings

router = APIRouter()


@router.get("/", response_model=WaterQualityListResponse, summary="获取水质数据列表")
def get_water_quality_list(
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(20, ge=1, le=100, description="每页数量"),
    river_name: str = Query(None, description="河道名称"),
    code: str = Query(None, description="编号"),
    comprehensive_quality_level: str = Query(None, description="综合水质等级"),
    sampling_date_start: str = Query(None, description="取样开始日期"),
    sampling_date_end: str = Query(None, description="取样结束日期"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取水质数据列表"""
    water_quality_service = WaterQualityService(db)
    
    # 解析日期参数
    parsed_start_date = None
    parsed_end_date = None
    
    if sampling_date_start:
        try:
            parsed_start_date = parse_datetime(sampling_date_start)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="取样开始日期格式错误"
            )
    
    if sampling_date_end:
        try:
            parsed_end_date = parse_datetime(sampling_date_end)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="取样结束日期格式错误"
            )
    
    # 构建查询参数
    query = WaterQualityQuery(
        page=page,
        per_page=per_page,
        river_name=river_name,
        code=code,
        comprehensive_quality_level=comprehensive_quality_level,
        sampling_date_start=parsed_start_date,
        sampling_date_end=parsed_end_date
    )
    
    # 获取数据
    items, total = water_quality_service.get_water_quality_list(query)
    
    return WaterQualityListResponse(
        total=total,
        page=page,
        per_page=per_page,
        items=[WaterQualityResponse.from_orm(item) for item in items]
    )


@router.get("/{water_quality_id}", response_model=WaterQualityResponse, summary="获取单个水质数据")
def get_water_quality_by_id(
    water_quality_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取单个水质数据"""
    water_quality_service = WaterQualityService(db)
    
    water_quality = water_quality_service.get_water_quality_by_id(water_quality_id)
    if not water_quality:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="水质数据不存在"
        )
    
    return WaterQualityResponse.from_orm(water_quality)


@router.post("/", response_model=WaterQualityResponse, summary="创建水质数据")
def create_water_quality(
    water_quality_data: WaterQualityCreate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """创建水质数据"""
    water_quality_service = WaterQualityService(db)
    
    try:
        water_quality = water_quality_service.create_water_quality(water_quality_data)
        return WaterQualityResponse.from_orm(water_quality)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建水质数据失败: {str(e)}"
        )


@router.put("/{water_quality_id}", response_model=WaterQualityResponse, summary="更新水质数据")
def update_water_quality(
    water_quality_id: int,
    water_quality_data: WaterQualityUpdate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """更新水质数据"""
    water_quality_service = WaterQualityService(db)
    
    water_quality = water_quality_service.update_water_quality(water_quality_id, water_quality_data)
    if not water_quality:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="水质数据不存在"
        )
    
    return WaterQualityResponse.from_orm(water_quality)


@router.delete("/{water_quality_id}", summary="删除水质数据")
def delete_water_quality(
    water_quality_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """删除水质数据"""
    water_quality_service = WaterQualityService(db)
    
    if not water_quality_service.delete_water_quality(water_quality_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="水质数据不存在"
        )
    
    return {"message": "水质数据删除成功"}


@router.get("/statistics/overview", summary="获取水质数据统计")
def get_water_quality_statistics(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取水质数据统计"""
    water_quality_service = WaterQualityService(db)
    
    return water_quality_service.get_water_quality_statistics()


@router.get("/options/rivers", response_model=List[str], summary="获取河道列表")
def get_river_list(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取河道列表"""
    water_quality_service = WaterQualityService(db)
    
    return water_quality_service.get_river_list()


@router.get("/options/quality-levels", response_model=List[str], summary="获取水质等级列表")
def get_quality_levels(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取水质等级列表"""
    water_quality_service = WaterQualityService(db)
    
    return water_quality_service.get_quality_levels() 