"""
大屏可视化服务层
"""
from typing import List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_, desc
from app.models.water_quality import WaterQuality
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
    WaterQualityLevelStatistics, 
    IndicatorLevelStatistics, 
    IndicatorLevelDistribution
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
        elif level in ["轻度黑臭", "重度黑臭"]:
            return "polluted"
        else:
            return "unknown"
    
    def _get_warning_level(self, comprehensive_level: str) -> str:
        """获取警告等级"""
        if comprehensive_level == "Ⅴ类":
            return "poor"
        elif comprehensive_level == "劣Ⅴ类":
            return "very_poor"
        elif comprehensive_level == "轻度黑臭":
            return "light_polluted"
        elif comprehensive_level == "重度黑臭":
            return "polluted"
        else:
            return "unknown"
    
    def _normalize_method(self, method: str) -> str:
        """标准化方式名称，将空白方式设定为'其他'"""
        if not method or method.strip() == "":
            return "其他"
        return method.strip()
    
    def _filter_by_method(self, query, method: str):
        """根据方式过滤查询，处理'其他'方式"""
        if method == "其他":
            return query.filter(
                func.coalesce(WaterQuality.method, "") == ""
            )
        else:
            return query.filter(WaterQuality.method == method)
    
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
                (WaterQuality.comprehensive_quality_level.in_(["轻度黑臭", "重度黑臭"]), 1),
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
    
    def get_warning_water_quality(self, limit: int = 20) -> List[WarningWaterQuality]:
        """获取警告水质数据，优先展示污染严重的数据"""
        # 定义污染严重程度排序（数字越小越严重）
        pollution_order = case(
            (WaterQuality.comprehensive_quality_level == "重度黑臭", 1),
            (WaterQuality.comprehensive_quality_level == "轻度黑臭", 2),
            (WaterQuality.comprehensive_quality_level == "劣Ⅴ类", 3),
            (WaterQuality.comprehensive_quality_level == "Ⅴ类", 4),
            else_=5
        )
        
        # 获取警告数据，按污染严重程度和时间排序
        warning_data = self.db.query(WaterQuality)\
            .filter(WaterQuality.comprehensive_quality_level.in_(["Ⅴ类", "劣Ⅴ类", "轻度黑臭", "重度黑臭"]))\
            .order_by(pollution_order, desc(WaterQuality.sampling_date))\
            .limit(limit).all()
        
        result = []
        for data in warning_data:
            result.append(WarningWaterQuality(
                id=data.id,
                river_name=data.river_name,
                sampling_date=data.sampling_date,
                comprehensive_quality_level=data.comprehensive_quality_level or "未知",
                cod_value=data.cod_value,
                ammonia_nitrogen_value=data.ammonia_nitrogen_value,
                total_phosphorus_value=data.total_phosphorus_value,
                potassium_permanganate_value=data.potassium_permanganate_value,
                warning_level=self._get_warning_level(data.comprehensive_quality_level)
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
            recent_data=self.get_recent_water_quality(limit=10),
            warning_data=self.get_warning_water_quality(limit=10)
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
            .all()
        
        # 使用集合来去重，因为空白方式都会被标准化为"其他"
        method_names = set()
        for method in methods:
            normalized_method = self._normalize_method(method[0])
            method_names.add(normalized_method)
        
        # 转换为列表并排序
        method_names_list = sorted(list(method_names))
        
        return MethodListResponse(
            methods=method_names_list,
            total_count=len(method_names_list)
        )
    
    def get_method_statistics(self) -> List[MethodStatistics]:
        """获取方式统计数据"""
        # 使用case语句将空白方式转换为"其他"
        normalized_method = case(
            (func.coalesce(WaterQuality.method, "") == "", "其他"),
            else_=func.coalesce(WaterQuality.method, "其他")
        )
        
        method_stats = self.db.query(
            normalized_method.label('method'),
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
                (WaterQuality.comprehensive_quality_level.in_(["轻度黑臭", "重度黑臭"]), 1),
                else_=0
            )).label('polluted_count'),
            func.max(WaterQuality.sampling_date).label('latest_sampling_date')
        ).group_by(normalized_method)\
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
        query = self.db.query(
            WaterQuality.comprehensive_quality_level,
            func.count(WaterQuality.id).label('count')
        )
        query = self._filter_by_method(query, method)
        quality_stats = query.group_by(WaterQuality.comprehensive_quality_level).all()
        
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
        latest_query = self.db.query(WaterQuality)
        latest_query = self._filter_by_method(latest_query, method)
        latest_data = latest_query.order_by(WaterQuality.sampling_date.desc()).first()
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
        query = self.db.query(
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
                (WaterQuality.comprehensive_quality_level.in_(["轻度黑臭", "重度黑臭"]), 1),
                else_=0
            )).label('polluted_count'),
            func.max(WaterQuality.sampling_date).label('latest_sampling_date')
        )
        query = self._filter_by_method(query, method)
        river_stats = query.group_by(WaterQuality.river_name)\
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
        query = self.db.query(
            WaterQuality.comprehensive_quality_level,
            func.count(WaterQuality.id).label('count')
        )
        query = self._filter_by_method(query, method)
        quality_stats = query.group_by(WaterQuality.comprehensive_quality_level).all()
        
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
        query = self.db.query(
            func.strftime('%Y-%m', WaterQuality.sampling_date).label('month'),
            func.count(WaterQuality.id).label('total_count'),
            func.sum(case(
                (WaterQuality.comprehensive_quality_level.in_(["Ⅰ类", "Ⅱ类", "Ⅲ类"]), 1),
                else_=0
            )).label('excellent_count')
        )
        query = self._filter_by_method(query, method)
        monthly_stats = query.group_by(func.strftime('%Y-%m', WaterQuality.sampling_date))\
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
            query = self.db.query(
                func.avg(getattr(WaterQuality, column_name)).label('avg_value'),
                func.max(getattr(WaterQuality, column_name)).label('max_value'),
                func.min(getattr(WaterQuality, column_name)).label('min_value'),
                func.count(case(
                    (getattr(WaterQuality, column_name) > standard_value, 1)
                )).label('exceed_count'),
                func.count(getattr(WaterQuality, column_name)).label('total_count')
            )
            query = self._filter_by_method(query, method)
            stats = query.filter(getattr(WaterQuality, column_name).is_not(None)).first()
            
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
        query = self.db.query(WaterQuality)
        query = self._filter_by_method(query, method)
        recent_data = query.order_by(WaterQuality.sampling_date.desc()).limit(limit).all()
        
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
    
    def get_method_warning_water_quality(self, method: str, limit: int = 20) -> List[WarningWaterQuality]:
        """获取特定方式的警告水质数据"""
        # 定义污染严重程度排序
        pollution_order = case(
            (WaterQuality.comprehensive_quality_level == "重度黑臭", 1),
            (WaterQuality.comprehensive_quality_level == "轻度黑臭", 2),
            (WaterQuality.comprehensive_quality_level == "劣Ⅴ类", 3),
            (WaterQuality.comprehensive_quality_level == "Ⅴ类", 4),
            else_=5
        )
        
        query = self.db.query(WaterQuality)
        query = self._filter_by_method(query, method)
        warning_data = query.filter(
            WaterQuality.comprehensive_quality_level.in_(["Ⅴ类", "劣Ⅴ类", "轻度黑臭", "重度黑臭"])
        ).order_by(pollution_order, desc(WaterQuality.sampling_date)).limit(limit).all()
        
        result = []
        for data in warning_data:
            result.append(WarningWaterQuality(
                id=data.id,
                river_name=data.river_name,
                sampling_date=data.sampling_date,
                comprehensive_quality_level=data.comprehensive_quality_level or "未知",
                cod_value=data.cod_value,
                ammonia_nitrogen_value=data.ammonia_nitrogen_value,
                total_phosphorus_value=data.total_phosphorus_value,
                potassium_permanganate_value=data.potassium_permanganate_value,
                warning_level=self._get_warning_level(data.comprehensive_quality_level)
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
            recent_data=self.get_method_recent_water_quality(method, limit=10),
            warning_data=self.get_method_warning_water_quality(method, limit=10)
        ) 
    
    def get_water_quality_level_statistics(self) -> WaterQualityLevelStatistics:
        """获取水质等级统计数据"""
        
        # 获取各指标的等级统计
        cod_stats = self._get_indicator_level_statistics(
            'cod_level', 'COD', 'cod'
        )
        ammonia_nitrogen_stats = self._get_indicator_level_statistics(
            'ammonia_nitrogen_level', '氨氮', 'ammonia_nitrogen'
        )
        total_phosphorus_stats = self._get_indicator_level_statistics(
            'total_phosphorus_level', '总磷', 'total_phosphorus'
        )
        potassium_permanganate_stats = self._get_indicator_level_statistics(
            'potassium_permanganate_level', '高锰酸钾', 'potassium_permanganate'
        )
        
        # 计算总体概况
        overall_summary = self._calculate_overall_level_summary([
            cod_stats, ammonia_nitrogen_stats, 
            total_phosphorus_stats, potassium_permanganate_stats
        ])
        
        # 计算合格率、不合格率和警告率
        qualified_rate, unqualified_rate, warning_rate = self._calculate_quality_rates(overall_summary)
        
        return WaterQualityLevelStatistics(
            cod_stats=cod_stats,
            ammonia_nitrogen_stats=ammonia_nitrogen_stats,
            total_phosphorus_stats=total_phosphorus_stats,
            potassium_permanganate_stats=potassium_permanganate_stats,
            overall_summary=overall_summary,
            qualified_rate=qualified_rate,
            unqualified_rate=unqualified_rate,
            warning_rate=warning_rate
        )
    
    def _get_indicator_level_statistics(self, level_field: str, indicator_name: str, indicator_code: str) -> IndicatorLevelStatistics:
        """获取单个指标的等级统计"""
        
        # 获取指标等级分布
        level_stats = self.db.query(
            getattr(WaterQuality, level_field).label('level'),
            func.count(WaterQuality.id).label('count')
        ).filter(
            getattr(WaterQuality, level_field).is_not(None),
            getattr(WaterQuality, level_field) != ""
        ).group_by(getattr(WaterQuality, level_field)).all()
        
        # 计算总数
        total_count = sum(count for _, count in level_stats)
        
        # 构建等级分布
        level_distribution = []
        most_common_level = ""
        most_common_count = 0
        most_common_percentage = 0.0
        
        # 计算各等级统计
        qualified_count = 0  # I-III类
        warning_count = 0    # IV类、V类、劣V类、重度黑臭
        
        for level, count in level_stats:
            percentage = (count / total_count * 100) if total_count > 0 else 0
            
            level_distribution.append(IndicatorLevelDistribution(
                level=level or "未知",
                count=count,
                percentage=round(percentage, 2)
            ))
            
            # 记录最常见等级
            if count > most_common_count:
                most_common_count = count
                most_common_level = level or "未知"
                most_common_percentage = round(percentage, 2)
            
            # 计算合格和警告数量
            if level and level in ["Ⅰ类", "Ⅱ类", "Ⅲ类"]:
                qualified_count += count
            elif level and level in ["Ⅴ类", "劣Ⅴ类", "轻度黑臭", "重度黑臭"]:
                warning_count += count
        
        # 按数量排序
        level_distribution.sort(key=lambda x: x.count, reverse=True)
        
        # 计算各项比率
        qualified_rate = (qualified_count / total_count * 100) if total_count > 0 else 0
        unqualified_rate = 100 - qualified_rate
        warning_rate = (warning_count / total_count * 100) if total_count > 0 else 0
        
        return IndicatorLevelStatistics(
            indicator_name=indicator_name,
            indicator_code=indicator_code,
            total_count=total_count,
            level_distribution=level_distribution,
            most_common_level=most_common_level,
            most_common_count=most_common_count,
            most_common_percentage=most_common_percentage,
            qualified_rate=round(qualified_rate, 2),
            unqualified_rate=round(unqualified_rate, 2),
            warning_rate=round(warning_rate, 2)
        )
    
    def _calculate_overall_level_summary(self, indicator_stats: List[IndicatorLevelStatistics]) -> dict:
        """计算总体等级概况"""
        total_records = sum(stat.total_count for stat in indicator_stats)
        
        # 统计各等级的整体情况
        level_summary = {}
        for stat in indicator_stats:
            for level_dist in stat.level_distribution:
                if level_dist.level not in level_summary:
                    level_summary[level_dist.level] = {
                        'count': 0,
                        'indicators': []
                    }
                level_summary[level_dist.level]['count'] += level_dist.count
                level_summary[level_dist.level]['indicators'].append({
                    'name': stat.indicator_name,
                    'count': level_dist.count,
                    'percentage': level_dist.percentage
                })
        
        # 计算整体百分比
        for level in level_summary:
            level_summary[level]['percentage'] = round(
                level_summary[level]['count'] / total_records * 100, 2
            ) if total_records > 0 else 0
        
        return {
            'total_records': total_records,
            'level_summary': level_summary,
            'indicator_count': len(indicator_stats)
        } 

    def _calculate_quality_rates(self, overall_summary: dict) -> Tuple[float, float, float]:
        """
        计算水质合格率、不合格率和警告率。
        合格率：水质等级为"Ⅰ类"、"Ⅱ类"、"Ⅲ类"的总数占比。
        不合格率：1-合格率。
        警告率：轻度污染(Ⅳ类、Ⅴ类)和重度污染(劣Ⅴ类、重度黑臭)的总数占比。
        """
        total_records = overall_summary['total_records']
        level_summary = overall_summary['level_summary']

        # 合格率：一类二类三类的占比
        qualified_count = sum(level_summary.get(level, {}).get('count', 0) for level in ["Ⅰ类", "Ⅱ类", "Ⅲ类"])
        qualified_rate = (qualified_count / total_records * 100) if total_records > 0 else 0
        
        # 不合格率：1-合格率
        unqualified_rate = 100 - qualified_rate
        
        # 警告率：轻度污染和重度污染占比
        warning_count = sum(level_summary.get(level, {}).get('count', 0) for level in ["Ⅴ类", "劣Ⅴ类", "轻度黑臭", "重度黑臭"])
        warning_rate = (warning_count / total_records * 100) if total_records > 0 else 0

        return round(qualified_rate, 2), round(unqualified_rate, 2), round(warning_rate, 2) 