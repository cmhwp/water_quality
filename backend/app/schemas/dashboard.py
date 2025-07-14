"""
大屏可视化数据模式
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class OverviewStatistics(BaseModel):
    """总览统计数据"""
    total_records: int = Field(..., description="总数据量")
    excellent_count: int = Field(..., description="优质水质数量(I-III类)")
    good_count: int = Field(..., description="良好水质数量(IV类)")
    poor_count: int = Field(..., description="较差水质数量(V类)")
    very_poor_count: int = Field(..., description="极差水质数量(劣V类)")
    polluted_count: int = Field(..., description="污染水质数量(轻度黑臭、重度黑臭)")
    excellent_rate: float = Field(..., description="优质水质达标率")
    latest_update: datetime = Field(..., description="最新数据更新时间")


class RiverStatistics(BaseModel):
    """河道统计数据"""
    river_name: str = Field(..., description="河道名称")
    total_count: int = Field(..., description="总数据量")
    excellent_count: int = Field(..., description="优质水质数量")
    good_count: int = Field(..., description="良好水质数量")
    poor_count: int = Field(..., description="较差水质数量")
    very_poor_count: int = Field(..., description="极差水质数量")
    polluted_count: int = Field(..., description="污染水质数量")
    excellent_rate: float = Field(..., description="优质水质达标率")
    latest_sampling_date: Optional[datetime] = Field(None, description="最新采样时间")


class QualityLevelDistribution(BaseModel):
    """水质等级分布"""
    level: str = Field(..., description="水质等级")
    count: int = Field(..., description="数量")
    percentage: float = Field(..., description="百分比")


class MonthlyTrend(BaseModel):
    """月度趋势数据"""
    month: str = Field(..., description="月份")
    total_count: int = Field(..., description="总数据量")
    excellent_count: int = Field(..., description="优质水质数量")
    excellent_rate: float = Field(..., description="优质水质达标率")


class IndicatorStatistics(BaseModel):
    """指标统计数据"""
    indicator_name: str = Field(..., description="指标名称")
    avg_value: Optional[float] = Field(None, description="平均值")
    max_value: Optional[float] = Field(None, description="最大值")
    min_value: Optional[float] = Field(None, description="最小值")
    unit: str = Field(..., description="单位")
    standard_value: Optional[float] = Field(None, description="标准值")
    exceed_rate: float = Field(..., description="超标率")


class RecentWaterQuality(BaseModel):
    """最新水质数据"""
    id: int = Field(..., description="数据ID")
    river_name: str = Field(..., description="河道名称")
    sampling_date: datetime = Field(..., description="采样日期")
    comprehensive_quality_level: str = Field(..., description="综合水质等级")
    cod_value: Optional[float] = Field(None, description="COD值")
    ammonia_nitrogen_value: Optional[float] = Field(None, description="氨氮值")
    total_phosphorus_value: Optional[float] = Field(None, description="总磷值")
    potassium_permanganate_value: Optional[float] = Field(None, description="高锰酸钾值")


class WarningWaterQuality(BaseModel):
    """警告水质数据"""
    id: int = Field(..., description="数据ID")
    river_name: str = Field(..., description="河道名称")
    sampling_date: datetime = Field(..., description="采样日期")
    comprehensive_quality_level: str = Field(..., description="综合水质等级")
    cod_value: Optional[float] = Field(None, description="COD值")
    ammonia_nitrogen_value: Optional[float] = Field(None, description="氨氮值")
    total_phosphorus_value: Optional[float] = Field(None, description="总磷值")
    potassium_permanganate_value: Optional[float] = Field(None, description="高锰酸钾值")
    warning_level: str = Field(..., description="警告等级(poor:Ⅴ类, very_poor:劣Ⅴ类, light_polluted:轻度黑臭, polluted:重度黑臭)")


class MethodStatistics(BaseModel):
    """方式统计数据"""
    method: str = Field(..., description="方式名称")
    total_count: int = Field(..., description="总数据量")
    excellent_count: int = Field(..., description="优质水质数量")
    good_count: int = Field(..., description="良好水质数量")
    poor_count: int = Field(..., description="较差水质数量")
    very_poor_count: int = Field(..., description="极差水质数量")
    polluted_count: int = Field(..., description="污染水质数量")
    excellent_rate: float = Field(..., description="优质水质达标率")
    latest_sampling_date: Optional[datetime] = Field(None, description="最新采样时间")


class MethodOverviewStatistics(BaseModel):
    """方式总览统计数据"""
    method: str = Field(..., description="方式名称")
    total_records: int = Field(..., description="总数据量")
    excellent_count: int = Field(..., description="优质水质数量(I-III类)")
    good_count: int = Field(..., description="良好水质数量(IV类)")
    poor_count: int = Field(..., description="较差水质数量(V类)")
    very_poor_count: int = Field(..., description="极差水质数量(劣V类)")
    polluted_count: int = Field(..., description="污染水质数量(轻度黑臭、重度黑臭)")
    excellent_rate: float = Field(..., description="优质水质达标率")
    latest_update: datetime = Field(..., description="最新数据更新时间")


class MethodRiverStatistics(BaseModel):
    """方式河道统计数据"""
    method: str = Field(..., description="方式名称")
    river_name: str = Field(..., description="河道名称")
    total_count: int = Field(..., description="总数据量")
    excellent_count: int = Field(..., description="优质水质数量")
    good_count: int = Field(..., description="良好水质数量")
    poor_count: int = Field(..., description="较差水质数量")
    very_poor_count: int = Field(..., description="极差水质数量")
    polluted_count: int = Field(..., description="污染水质数量")
    excellent_rate: float = Field(..., description="优质水质达标率")
    latest_sampling_date: Optional[datetime] = Field(None, description="最新采样时间")


class MethodQualityDistribution(BaseModel):
    """方式水质等级分布"""
    method: str = Field(..., description="方式名称")
    level: str = Field(..., description="水质等级")
    count: int = Field(..., description="数量")
    percentage: float = Field(..., description="百分比")


class MethodMonthlyTrend(BaseModel):
    """方式月度趋势数据"""
    method: str = Field(..., description="方式名称")
    month: str = Field(..., description="月份")
    total_count: int = Field(..., description="总数据量")
    excellent_count: int = Field(..., description="优质水质数量")
    excellent_rate: float = Field(..., description="优质水质达标率")


class MethodIndicatorStatistics(BaseModel):
    """方式指标统计数据"""
    method: str = Field(..., description="方式名称")
    indicator_name: str = Field(..., description="指标名称")
    avg_value: Optional[float] = Field(None, description="平均值")
    max_value: Optional[float] = Field(None, description="最大值")
    min_value: Optional[float] = Field(None, description="最小值")
    unit: str = Field(..., description="单位")
    standard_value: Optional[float] = Field(None, description="标准值")
    exceed_rate: float = Field(..., description="超标率")


class MethodDashboardResponse(BaseModel):
    """方式大屏数据响应"""
    method: str = Field(..., description="方式名称")
    overview: MethodOverviewStatistics = Field(..., description="总览统计")
    river_stats: List[MethodRiverStatistics] = Field(..., description="河道统计")
    quality_distribution: List[MethodQualityDistribution] = Field(..., description="水质等级分布")
    monthly_trend: List[MethodMonthlyTrend] = Field(..., description="月度趋势")
    indicator_stats: List[MethodIndicatorStatistics] = Field(..., description="指标统计")
    recent_data: List[RecentWaterQuality] = Field(..., description="最新数据(5条)")
    warning_data: List[WarningWaterQuality] = Field(..., description="警告数据(污染严重数据)")


class MethodListResponse(BaseModel):
    """方式列表响应"""
    methods: List[str] = Field(..., description="方式名称列表")
    total_count: int = Field(..., description="方式总数")


class DashboardResponse(BaseModel):
    """大屏数据总响应"""
    overview: OverviewStatistics = Field(..., description="总览统计")
    river_stats: List[RiverStatistics] = Field(..., description="河道统计")
    quality_distribution: List[QualityLevelDistribution] = Field(..., description="水质等级分布")
    monthly_trend: List[MonthlyTrend] = Field(..., description="月度趋势")
    indicator_stats: List[IndicatorStatistics] = Field(..., description="指标统计")
    recent_data: List[RecentWaterQuality] = Field(..., description="最新数据(5条)")
    warning_data: List[WarningWaterQuality] = Field(..., description="警告数据(污染严重数据)")


class RiverListResponse(BaseModel):
    """河道列表响应"""
    rivers: List[str] = Field(..., description="河道名称列表")
    total_count: int = Field(..., description="河道总数")


class IndicatorLevelDistribution(BaseModel):
    """指标等级分布"""
    level: str = Field(..., description="等级")
    count: int = Field(..., description="数量")
    percentage: float = Field(..., description="百分比")


class IndicatorLevelStatistics(BaseModel):
    """指标等级统计"""
    indicator_name: str = Field(..., description="指标名称")
    indicator_code: str = Field(..., description="指标代码")
    total_count: int = Field(..., description="总数据量")
    level_distribution: List[IndicatorLevelDistribution] = Field(..., description="等级分布")
    most_common_level: str = Field(..., description="最常见等级")
    most_common_count: int = Field(..., description="最常见等级数量")
    most_common_percentage: float = Field(..., description="最常见等级百分比")
    qualified_rate: float = Field(..., description="该指标合格率(I-III类)")
    unqualified_rate: float = Field(..., description="该指标不合格率")
    warning_rate: float = Field(..., description="该指标警告率(轻度+重度污染)")


class WaterQualityLevelStatistics(BaseModel):
    """水质等级统计"""
    cod_stats: IndicatorLevelStatistics = Field(..., description="COD等级统计")
    ammonia_nitrogen_stats: IndicatorLevelStatistics = Field(..., description="氨氮等级统计")
    total_phosphorus_stats: IndicatorLevelStatistics = Field(..., description="总磷等级统计")
    potassium_permanganate_stats: IndicatorLevelStatistics = Field(..., description="高锰酸钾等级统计")
    overall_summary: dict = Field(..., description="总体概况")
    qualified_rate: float = Field(..., description="合格率(I-III类)")
    unqualified_rate: float = Field(..., description="不合格率")
    warning_rate: float = Field(..., description="警告率(轻度+重度污染)") 