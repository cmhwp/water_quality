"""
水质数据服务层
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.water_quality import WaterQuality
from app.schemas.water_quality import WaterQualityCreate, WaterQualityUpdate, WaterQualityQuery
from app.utils.water_quality_calculator import WaterQualityCalculator
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
        """创建水质数据，自动计算等级"""
        # 创建数据字典
        data_dict = water_quality_data.dict()
        
        # 自动计算等级
        levels = WaterQualityCalculator.calculate_all_levels(
            cod_value=data_dict.get('cod_value'),
            ammonia_nitrogen_value=data_dict.get('ammonia_nitrogen_value'),
            total_phosphorus_value=data_dict.get('total_phosphorus_value'),
            potassium_permanganate_value=data_dict.get('potassium_permanganate_value')
        )
        
        # 更新计算得到的等级（如果用户没有手动设置）
        if data_dict.get('cod_level') is None:
            data_dict['cod_level'] = levels['cod_level']
        if data_dict.get('ammonia_nitrogen_level') is None:
            data_dict['ammonia_nitrogen_level'] = levels['ammonia_nitrogen_level']
        if data_dict.get('total_phosphorus_level') is None:
            data_dict['total_phosphorus_level'] = levels['total_phosphorus_level']
        if data_dict.get('potassium_permanganate_level') is None:
            data_dict['potassium_permanganate_level'] = levels['potassium_permanganate_level']
        if data_dict.get('comprehensive_quality_level') is None:
            data_dict['comprehensive_quality_level'] = levels['comprehensive_quality_level']
        if data_dict.get('comprehensive_level_number') is None:
            data_dict['comprehensive_level_number'] = levels['comprehensive_level_number']
        
        # 创建数据库对象
        db_water_quality = WaterQuality(**data_dict)
        self.db.add(db_water_quality)
        self.db.commit()
        self.db.refresh(db_water_quality)
        return db_water_quality
    
    def update_water_quality(self, water_quality_id: int, water_quality_data: WaterQualityUpdate) -> Optional[WaterQuality]:
        """更新水质数据，自动重新计算等级"""
        db_water_quality = self.get_water_quality_by_id(water_quality_id)
        if not db_water_quality:
            return None
        
        # 更新数据
        update_data = water_quality_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_water_quality, key, value)
        
        # 检查是否有水质指标数值更新，如果有则重新计算等级
        indicator_values_updated = any(key in update_data for key in [
            'cod_value', 'ammonia_nitrogen_value', 'total_phosphorus_value', 'potassium_permanganate_value'
        ])
        
        if indicator_values_updated:
            # 重新计算等级
            levels = WaterQualityCalculator.calculate_all_levels(
                cod_value=db_water_quality.cod_value,
                ammonia_nitrogen_value=db_water_quality.ammonia_nitrogen_value,
                total_phosphorus_value=db_water_quality.total_phosphorus_value,
                potassium_permanganate_value=db_water_quality.potassium_permanganate_value
            )
            
            # 更新等级（如果用户没有手动设置）
            if 'cod_level' not in update_data:
                db_water_quality.cod_level = levels['cod_level']
            if 'ammonia_nitrogen_level' not in update_data:
                db_water_quality.ammonia_nitrogen_level = levels['ammonia_nitrogen_level']
            if 'total_phosphorus_level' not in update_data:
                db_water_quality.total_phosphorus_level = levels['total_phosphorus_level']
            if 'potassium_permanganate_level' not in update_data:
                db_water_quality.potassium_permanganate_level = levels['potassium_permanganate_level']
            if 'comprehensive_quality_level' not in update_data:
                db_water_quality.comprehensive_quality_level = levels['comprehensive_quality_level']
            if 'comprehensive_level_number' not in update_data:
                db_water_quality.comprehensive_level_number = levels['comprehensive_level_number']
        
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
            func.count(WaterQuality.id).label('count')
        ).group_by(WaterQuality.river_name).all()
        
        # 按水质等级统计
        quality_stats = self.db.query(
            WaterQuality.comprehensive_quality_level,
            func.count(WaterQuality.id).label('count')
        ).group_by(WaterQuality.comprehensive_quality_level).all()
        
        # 按月份统计
        monthly_stats = self.db.query(
            func.strftime('%Y-%m', WaterQuality.sampling_date).label('month'),
            func.count(WaterQuality.id).label('count')
        ).group_by('month').order_by('month').all()
        
        # 计算优质水质(I-III类)和污染水质(IV-V类)数量
        excellent_count = 0
        polluted_count = 0
        
        for level, count in quality_stats:
            if level and ('Ⅰ类' in level or 'Ⅱ类' in level or 'Ⅲ类' in level):
                excellent_count += count
            elif level and ('Ⅳ类' in level or 'Ⅴ类' in level or '劣Ⅴ类' in level or '轻度黑臭' in level or '重度黑臭' in level):
                polluted_count += count
        
        return {
            'total': total_count,
            'excellent': excellent_count,
            'polluted': polluted_count,
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
    
    def recalculate_all_levels(self) -> int:
        """重新计算所有水质数据的等级"""
        # 获取所有水质数据
        all_water_quality = self.db.query(WaterQuality).all()
        updated_count = 0
        
        for water_quality in all_water_quality:
            # 重新计算等级
            levels = WaterQualityCalculator.calculate_all_levels(
                cod_value=water_quality.cod_value,
                ammonia_nitrogen_value=water_quality.ammonia_nitrogen_value,
                total_phosphorus_value=water_quality.total_phosphorus_value,
                potassium_permanganate_value=water_quality.potassium_permanganate_value
            )
            
            # 更新等级
            water_quality.cod_level = levels['cod_level']
            water_quality.ammonia_nitrogen_level = levels['ammonia_nitrogen_level']
            water_quality.total_phosphorus_level = levels['total_phosphorus_level']
            water_quality.potassium_permanganate_level = levels['potassium_permanganate_level']
            water_quality.comprehensive_quality_level = levels['comprehensive_quality_level']
            water_quality.comprehensive_level_number = levels['comprehensive_level_number']
            
            updated_count += 1
        
        # 批量提交
        self.db.commit()
        return updated_count 