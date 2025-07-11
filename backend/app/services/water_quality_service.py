"""
水质数据服务层
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.water_quality import WaterQuality
from app.schemas.water_quality import WaterQualityCreate, WaterQualityUpdate, WaterQualityQuery
from config import settings


class WaterQualityService:
    """水质数据服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_water_quality_by_id(self, water_quality_id: int) -> Optional[WaterQuality]:
        """根据ID获取水质数据"""
        return self.db.query(WaterQuality).filter(WaterQuality.id == water_quality_id).first()
    
    def get_water_quality_list(self, query: WaterQualityQuery) -> tuple[List[WaterQuality], int]:
        """获取水质数据列表"""
        # 构建查询条件
        conditions = []
        
        if query.river_name:
            conditions.append(WaterQuality.river_name.like(f"%{query.river_name}%"))
        
        if query.code:
            conditions.append(WaterQuality.code.like(f"%{query.code}%"))
        
        if query.comprehensive_quality_level:
            conditions.append(WaterQuality.comprehensive_quality_level == query.comprehensive_quality_level)
        
        if query.sampling_date_start:
            conditions.append(WaterQuality.sampling_date >= query.sampling_date_start)
        
        if query.sampling_date_end:
            conditions.append(WaterQuality.sampling_date <= query.sampling_date_end)
        
        # 构建查询
        base_query = self.db.query(WaterQuality)
        if conditions:
            base_query = base_query.filter(and_(*conditions))
        
        # 获取总数
        total = base_query.count()
        
        # 分页查询
        offset = (query.page - 1) * query.per_page
        items = base_query.order_by(WaterQuality.sampling_date.desc()).offset(offset).limit(query.per_page).all()
        
        return items, total
    
    def create_water_quality(self, water_quality_data: WaterQualityCreate) -> WaterQuality:
        """创建水质数据"""
        db_water_quality = WaterQuality(**water_quality_data.dict())
        self.db.add(db_water_quality)
        self.db.commit()
        self.db.refresh(db_water_quality)
        return db_water_quality
    
    def update_water_quality(self, water_quality_id: int, water_quality_data: WaterQualityUpdate) -> Optional[WaterQuality]:
        """更新水质数据"""
        db_water_quality = self.get_water_quality_by_id(water_quality_id)
        if not db_water_quality:
            return None
        
        # 更新数据
        update_data = water_quality_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_water_quality, key, value)
        
        db_water_quality.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(db_water_quality)
        return db_water_quality
    
    def delete_water_quality(self, water_quality_id: int) -> bool:
        """删除水质数据"""
        db_water_quality = self.get_water_quality_by_id(water_quality_id)
        if not db_water_quality:
            return False
        
        self.db.delete(db_water_quality)
        self.db.commit()
        return True
    
    def get_water_quality_statistics(self) -> dict:
        """获取水质数据统计"""
        total_count = self.db.query(WaterQuality).count()
        
        # 按河道统计
        river_stats = self.db.query(
            WaterQuality.river_name,
            self.db.func.count(WaterQuality.id).label('count')
        ).group_by(WaterQuality.river_name).all()
        
        # 按水质等级统计
        quality_stats = self.db.query(
            WaterQuality.comprehensive_quality_level,
            self.db.func.count(WaterQuality.id).label('count')
        ).group_by(WaterQuality.comprehensive_quality_level).all()
        
        # 按月份统计
        monthly_stats = self.db.query(
            self.db.func.date_format(WaterQuality.sampling_date, '%Y-%m').label('month'),
            self.db.func.count(WaterQuality.id).label('count')
        ).group_by('month').order_by('month').all()
        
        return {
            'total_count': total_count,
            'river_stats': [{'river_name': r[0], 'count': r[1]} for r in river_stats],
            'quality_stats': [{'level': q[0], 'count': q[1]} for q in quality_stats],
            'monthly_stats': [{'month': m[0], 'count': m[1]} for m in monthly_stats]
        }
    
    def get_river_list(self) -> List[str]:
        """获取河道列表"""
        rivers = self.db.query(WaterQuality.river_name).distinct().all()
        return [river[0] for river in rivers if river[0]]
    
    def get_quality_levels(self) -> List[str]:
        """获取水质等级列表"""
        levels = self.db.query(WaterQuality.comprehensive_quality_level).distinct().all()
        return [level[0] for level in levels if level[0]] 