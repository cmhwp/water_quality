"""
大屏可视化服务层
"""
from typing import List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_
from app.models.water_quality import WaterQuality
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


class DashboardService:
    """大屏可视化服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _classify_water_quality(self, level: str) -> str:
        """分类水质等级"""
        if not level:
            return "unknown"
        
        if level in ["Ⅰ类", "Ⅱ类", "Ⅲ类"]:
            return "excellent"
        elif level in ["Ⅳ类"]:
            return "good"
        elif level in ["Ⅴ类"]:
            return "poor"
        elif level in ["劣Ⅴ类"]:
            return "very_poor"
        elif level in ["重度黑臭"]:
            return "polluted"
        else:
            return "unknown"
    
    def get_overview_statistics(self) -> OverviewStatistics:
        """获取总览统计数据"""
        # 获取所有数据的水质等级分布
        quality_stats = self.db.query(
            WaterQuality.comprehensive_quality_level,
            func.count(WaterQuality.id).label('count')
        ).group_by(WaterQuality.comprehensive_quality_level).all()
        
        # 统计各个等级的数量
        total_records = 0
        excellent_count = 0
        good_count = 0
        poor_count = 0
        very_poor_count = 0
        polluted_count = 0
        
        for level, count in quality_stats:
            total_records += count
            classification = self._classify_water_quality(level)
            
            if classification == "excellent":
                excellent_count += count
            elif classification == "good":
                good_count += count
            elif classification == "poor":
                poor_count += count
            elif classification == "very_poor":
                very_poor_count += count
            elif classification == "polluted":
                polluted_count += count
        
        # 计算优质水质达标率 (I-III类)
        excellent_rate = (excellent_count / total_records * 100) if total_records > 0 else 0
        
        # 获取最新数据更新时间
        latest_data = self.db.query(WaterQuality).order_by(WaterQuality.sampling_date.desc()).first()
        latest_update = latest_data.sampling_date if latest_data else datetime.now()
        
        return OverviewStatistics(
            total_records=total_records,
            excellent_count=excellent_count,
            good_count=good_count,
            poor_count=poor_count,
            very_poor_count=very_poor_count,
            polluted_count=polluted_count,
            excellent_rate=round(excellent_rate, 2),
            latest_update=latest_update
        )
    
    def get_river_statistics(self, limit: int = 20) -> List[RiverStatistics]:
        """获取河道统计数据"""
        # 获取每个河道的数据统计
        river_stats = self.db.query(
            WaterQuality.river_name,
            func.count(WaterQuality.id).label('total_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level.in_(["Ⅰ类", "Ⅱ类", "Ⅲ类"]), 1),
                else_=0
            )).label('excellent_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "Ⅳ类", 1),
                else_=0
            )).label('good_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "Ⅴ类", 1),
                else_=0
            )).label('poor_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "劣Ⅴ类", 1),
                else_=0
            )).label('very_poor_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "重度黑臭", 1),
                else_=0
            )).label('polluted_count'),
            func.max(WaterQuality.sampling_date).label('latest_sampling_date')
        ).group_by(WaterQuality.river_name)\
         .order_by(func.count(WaterQuality.id).desc())\
         .limit(limit).all()
        
        result = []
        for stat in river_stats:
            excellent_rate = (stat.excellent_count / stat.total_count * 100) if stat.total_count > 0 else 0
            
            result.append(RiverStatistics(
                river_name=stat.river_name,
                total_count=stat.total_count,
                excellent_count=stat.excellent_count,
                good_count=stat.good_count,
                poor_count=stat.poor_count,
                very_poor_count=stat.very_poor_count,
                polluted_count=stat.polluted_count,
                excellent_rate=round(excellent_rate, 2),
                latest_sampling_date=stat.latest_sampling_date
            ))
        
        return result
    
    def get_quality_distribution(self) -> List[QualityLevelDistribution]:
        """获取水质等级分布"""
        # 获取水质等级分布
        quality_stats = self.db.query(
            WaterQuality.comprehensive_quality_level,
            func.count(WaterQuality.id).label('count')
        ).group_by(WaterQuality.comprehensive_quality_level).all()
        
        total_count = sum(stat.count for stat in quality_stats)
        
        result = []
        for stat in quality_stats:
            percentage = (stat.count / total_count * 100) if total_count > 0 else 0
            result.append(QualityLevelDistribution(
                level=stat.comprehensive_quality_level or "未知",
                count=stat.count,
                percentage=round(percentage, 2)
            ))
        
        return result
    
    def get_monthly_trend(self, limit: int = 12) -> List[MonthlyTrend]:
        """获取月度趋势数据"""
        # 获取月度趋势数据
        monthly_stats = self.db.query(
            func.strftime('%Y-%m', WaterQuality.sampling_date).label('month'),
            func.count(WaterQuality.id).label('total_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level.in_(["Ⅰ类", "Ⅱ类", "Ⅲ类"]), 1),
                else_=0
            )).label('excellent_count')
        ).group_by(func.strftime('%Y-%m', WaterQuality.sampling_date))\
         .order_by(func.strftime('%Y-%m', WaterQuality.sampling_date).desc())\
         .limit(limit).all()
        
        result = []
        for stat in monthly_stats:
            excellent_rate = (stat.excellent_count / stat.total_count * 100) if stat.total_count > 0 else 0
            result.append(MonthlyTrend(
                month=stat.month,
                total_count=stat.total_count,
                excellent_count=stat.excellent_count,
                excellent_rate=round(excellent_rate, 2)
            ))
        
        return result
    
    def get_indicator_statistics(self) -> List[IndicatorStatistics]:
        """获取指标统计数据"""
        indicators = [
            ("COD", "cod_value", "mg/L", 20.0),
            ("氨氮", "ammonia_nitrogen_value", "mg/L", 1.0),
            ("总磷", "total_phosphorus_value", "mg/L", 0.2),
            ("高锰酸钾", "potassium_permanganate_value", "mg/L", 6.0)
        ]
        
        result = []
        for indicator_name, column_name, unit, standard_value in indicators:
            # 获取指标统计数据
            stats = self.db.query(
                func.avg(getattr(WaterQuality, column_name)).label('avg_value'),
                func.max(getattr(WaterQuality, column_name)).label('max_value'),
                func.min(getattr(WaterQuality, column_name)).label('min_value'),
                func.count(case(
                    (getattr(WaterQuality, column_name) > standard_value, 1)
                )).label('exceed_count'),
                func.count(getattr(WaterQuality, column_name)).label('total_count')
            ).filter(getattr(WaterQuality, column_name).is_not(None)).first()
            
            if stats and stats.total_count > 0:
                exceed_rate = (stats.exceed_count / stats.total_count * 100) if stats.total_count > 0 else 0
                
                result.append(IndicatorStatistics(
                    indicator_name=indicator_name,
                    avg_value=round(stats.avg_value, 2) if stats.avg_value else None,
                    max_value=round(stats.max_value, 2) if stats.max_value else None,
                    min_value=round(stats.min_value, 2) if stats.min_value else None,
                    unit=unit,
                    standard_value=standard_value,
                    exceed_rate=round(exceed_rate, 2)
                ))
        
        return result
    
    def get_recent_water_quality(self, limit: int = 10) -> List[RecentWaterQuality]:
        """获取最新水质数据"""
        recent_data = self.db.query(WaterQuality)\
            .order_by(WaterQuality.sampling_date.desc())\
            .limit(limit).all()
        
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
    
    def get_dashboard_data(self) -> DashboardResponse:
        """获取大屏完整数据"""
        return DashboardResponse(
            overview=self.get_overview_statistics(),
            river_stats=self.get_river_statistics(),
            quality_distribution=self.get_quality_distribution(),
            monthly_trend=self.get_monthly_trend(),
            indicator_stats=self.get_indicator_statistics(),
            recent_data=self.get_recent_water_quality()
        )
    
    def get_river_list(self) -> RiverListResponse:
        """获取河道列表"""
        rivers = self.db.query(WaterQuality.river_name)\
            .distinct()\
            .order_by(WaterQuality.river_name)\
            .all()
        
        river_names = [river[0] for river in rivers if river[0]]
        
        return RiverListResponse(
            rivers=river_names,
            total_count=len(river_names)
        )
    
    # 新增方式细分相关方法
    def get_method_list(self) -> MethodListResponse:
        """获取方式列表"""
        methods = self.db.query(WaterQuality.method)\
            .distinct()\
            .filter(WaterQuality.method.is_not(None))\
            .filter(WaterQuality.method != "")\
            .order_by(WaterQuality.method)\
            .all()
        
        method_names = [method[0] for method in methods if method[0]]
        
        return MethodListResponse(
            methods=method_names,
            total_count=len(method_names)
        )
    
    def get_method_statistics(self) -> List[MethodStatistics]:
        """获取方式统计数据"""
        method_stats = self.db.query(
            WaterQuality.method,
            func.count(WaterQuality.id).label('total_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level.in_(["Ⅰ类", "Ⅱ类", "Ⅲ类"]), 1),
                else_=0
            )).label('excellent_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "Ⅳ类", 1),
                else_=0
            )).label('good_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "Ⅴ类", 1),
                else_=0
            )).label('poor_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "劣Ⅴ类", 1),
                else_=0
            )).label('very_poor_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "重度黑臭", 1),
                else_=0
            )).label('polluted_count'),
            func.max(WaterQuality.sampling_date).label('latest_sampling_date')
        ).filter(WaterQuality.method.is_not(None))\
         .filter(WaterQuality.method != "")\
         .group_by(WaterQuality.method)\
         .order_by(func.count(WaterQuality.id).desc())\
         .all()
        
        result = []
        for stat in method_stats:
            excellent_rate = (stat.excellent_count / stat.total_count * 100) if stat.total_count > 0 else 0
            
            result.append(MethodStatistics(
                method=stat.method,
                total_count=stat.total_count,
                excellent_count=stat.excellent_count,
                good_count=stat.good_count,
                poor_count=stat.poor_count,
                very_poor_count=stat.very_poor_count,
                polluted_count=stat.polluted_count,
                excellent_rate=round(excellent_rate, 2),
                latest_sampling_date=stat.latest_sampling_date
            ))
        
        return result
    
    def get_method_overview_statistics(self, method: str) -> MethodOverviewStatistics:
        """获取特定方式的总览统计数据"""
        quality_stats = self.db.query(
            WaterQuality.comprehensive_quality_level,
            func.count(WaterQuality.id).label('count')
        ).filter(WaterQuality.method == method)\
         .group_by(WaterQuality.comprehensive_quality_level).all()
        
        # 统计各个等级的数量
        total_records = 0
        excellent_count = 0
        good_count = 0
        poor_count = 0
        very_poor_count = 0
        polluted_count = 0
        
        for level, count in quality_stats:
            total_records += count
            classification = self._classify_water_quality(level)
            
            if classification == "excellent":
                excellent_count += count
            elif classification == "good":
                good_count += count
            elif classification == "poor":
                poor_count += count
            elif classification == "very_poor":
                very_poor_count += count
            elif classification == "polluted":
                polluted_count += count
        
        # 计算优质水质达标率
        excellent_rate = (excellent_count / total_records * 100) if total_records > 0 else 0
        
        # 获取最新数据更新时间
        latest_data = self.db.query(WaterQuality)\
            .filter(WaterQuality.method == method)\
            .order_by(WaterQuality.sampling_date.desc()).first()
        latest_update = latest_data.sampling_date if latest_data else datetime.now()
        
        return MethodOverviewStatistics(
            method=method,
            total_records=total_records,
            excellent_count=excellent_count,
            good_count=good_count,
            poor_count=poor_count,
            very_poor_count=very_poor_count,
            polluted_count=polluted_count,
            excellent_rate=round(excellent_rate, 2),
            latest_update=latest_update
        )
    
    def get_method_river_statistics(self, method: str, limit: int = 20) -> List[MethodRiverStatistics]:
        """获取特定方式的河道统计数据"""
        river_stats = self.db.query(
            WaterQuality.river_name,
            func.count(WaterQuality.id).label('total_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level.in_(["Ⅰ类", "Ⅱ类", "Ⅲ类"]), 1),
                else_=0
            )).label('excellent_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "Ⅳ类", 1),
                else_=0
            )).label('good_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "Ⅴ类", 1),
                else_=0
            )).label('poor_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "劣Ⅴ类", 1),
                else_=0
            )).label('very_poor_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level == "重度黑臭", 1),
                else_=0
            )).label('polluted_count'),
            func.max(WaterQuality.sampling_date).label('latest_sampling_date')
        ).filter(WaterQuality.method == method)\
         .group_by(WaterQuality.river_name)\
         .order_by(func.count(WaterQuality.id).desc())\
         .limit(limit).all()
        
        result = []
        for stat in river_stats:
            excellent_rate = (stat.excellent_count / stat.total_count * 100) if stat.total_count > 0 else 0
            
            result.append(MethodRiverStatistics(
                method=method,
                river_name=stat.river_name,
                total_count=stat.total_count,
                excellent_count=stat.excellent_count,
                good_count=stat.good_count,
                poor_count=stat.poor_count,
                very_poor_count=stat.very_poor_count,
                polluted_count=stat.polluted_count,
                excellent_rate=round(excellent_rate, 2),
                latest_sampling_date=stat.latest_sampling_date
            ))
        
        return result
    
    def get_method_quality_distribution(self, method: str) -> List[MethodQualityDistribution]:
        """获取特定方式的水质等级分布"""
        quality_stats = self.db.query(
            WaterQuality.comprehensive_quality_level,
            func.count(WaterQuality.id).label('count')
        ).filter(WaterQuality.method == method)\
         .group_by(WaterQuality.comprehensive_quality_level).all()
        
        total_count = sum(stat.count for stat in quality_stats)
        
        result = []
        for stat in quality_stats:
            percentage = (stat.count / total_count * 100) if total_count > 0 else 0
            result.append(MethodQualityDistribution(
                method=method,
                level=stat.comprehensive_quality_level or "未知",
                count=stat.count,
                percentage=round(percentage, 2)
            ))
        
        return result
    
    def get_method_monthly_trend(self, method: str, limit: int = 12) -> List[MethodMonthlyTrend]:
        """获取特定方式的月度趋势数据"""
        monthly_stats = self.db.query(
            func.strftime('%Y-%m', WaterQuality.sampling_date).label('month'),
            func.count(WaterQuality.id).label('total_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level.in_(["Ⅰ类", "Ⅱ类", "Ⅲ类"]), 1),
                else_=0
            )).label('excellent_count')
        ).filter(WaterQuality.method == method)\
         .group_by(func.strftime('%Y-%m', WaterQuality.sampling_date))\
         .order_by(func.strftime('%Y-%m', WaterQuality.sampling_date).desc())\
         .limit(limit).all()
        
        result = []
        for stat in monthly_stats:
            excellent_rate = (stat.excellent_count / stat.total_count * 100) if stat.total_count > 0 else 0
            result.append(MethodMonthlyTrend(
                method=method,
                month=stat.month,
                total_count=stat.total_count,
                excellent_count=stat.excellent_count,
                excellent_rate=round(excellent_rate, 2)
            ))
        
        return result
    
    def get_method_indicator_statistics(self, method: str) -> List[MethodIndicatorStatistics]:
        """获取特定方式的指标统计数据"""
        indicators = [
            ("COD", "cod_value", "mg/L", 20.0),
            ("氨氮", "ammonia_nitrogen_value", "mg/L", 1.0),
            ("总磷", "total_phosphorus_value", "mg/L", 0.2),
            ("高锰酸钾", "potassium_permanganate_value", "mg/L", 6.0)
        ]
        
        result = []
        for indicator_name, column_name, unit, standard_value in indicators:
            # 获取指标统计数据
            stats = self.db.query(
                func.avg(getattr(WaterQuality, column_name)).label('avg_value'),
                func.max(getattr(WaterQuality, column_name)).label('max_value'),
                func.min(getattr(WaterQuality, column_name)).label('min_value'),
                func.count(case(
                    (getattr(WaterQuality, column_name) > standard_value, 1)
                )).label('exceed_count'),
                func.count(getattr(WaterQuality, column_name)).label('total_count')
            ).filter(WaterQuality.method == method)\
             .filter(getattr(WaterQuality, column_name).is_not(None)).first()
            
            if stats and stats.total_count > 0:
                exceed_rate = (stats.exceed_count / stats.total_count * 100) if stats.total_count > 0 else 0
                
                result.append(MethodIndicatorStatistics(
                    method=method,
                    indicator_name=indicator_name,
                    avg_value=round(stats.avg_value, 2) if stats.avg_value else None,
                    max_value=round(stats.max_value, 2) if stats.max_value else None,
                    min_value=round(stats.min_value, 2) if stats.min_value else None,
                    unit=unit,
                    standard_value=standard_value,
                    exceed_rate=round(exceed_rate, 2)
                ))
        
        return result
    
    def get_method_recent_water_quality(self, method: str, limit: int = 10) -> List[RecentWaterQuality]:
        """获取特定方式的最新水质数据"""
        recent_data = self.db.query(WaterQuality)\
            .filter(WaterQuality.method == method)\
            .order_by(WaterQuality.sampling_date.desc())\
            .limit(limit).all()
        
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
    
    def get_method_dashboard_data(self, method: str) -> MethodDashboardResponse:
        """获取特定方式的大屏完整数据"""
        return MethodDashboardResponse(
            method=method,
            overview=self.get_method_overview_statistics(method),
            river_stats=self.get_method_river_statistics(method),
            quality_distribution=self.get_method_quality_distribution(method),
            monthly_trend=self.get_method_monthly_trend(method),
            indicator_stats=self.get_method_indicator_statistics(method),
            recent_data=self.get_method_recent_water_quality(method)
        ) 