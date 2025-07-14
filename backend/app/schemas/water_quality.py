"""
水质数据模式
"""
from datetime import datetime, date
from typing import Optional, Union
from pydantic import BaseModel, Field, validator
from app.utils.water_quality_calculator import WaterQualityCalculator


class WaterQualityBase(BaseModel):
    """水质数据基础模式"""
    
    sampling_date: Union[datetime, date] = Field(..., description="取样日期")
    sampling_time: Optional[str] = Field(None, description="取样时间")
    detection_date: Union[datetime, date] = Field(..., description="检测日期")
    code: Optional[str] = Field(None, description="编号")
    river_name: str = Field(..., description="河道名称")
    method: Optional[str] = Field(None, description="方式")
    
    # 水质指标数值
    cod_value: Optional[float] = Field(None, description="COD数值")
    ammonia_nitrogen_value: Optional[float] = Field(None, description="氨氮数值")
    total_phosphorus_value: Optional[float] = Field(None, description="总磷数值")
    potassium_permanganate_value: Optional[float] = Field(None, description="高锰酸钾数值")
    
    # 水质指标等级
    cod_level: Optional[str] = Field(None, description="COD等级")
    ammonia_nitrogen_level: Optional[str] = Field(None, description="氨氮等级")
    total_phosphorus_level: Optional[str] = Field(None, description="总磷等级")
    potassium_permanganate_level: Optional[str] = Field(None, description="高锰酸钾等级")
    
    # 综合评价
    comprehensive_quality_level: Optional[str] = Field(None, description="综合水质等级")
    comprehensive_level_number: Optional[int] = Field(None, description="综合等级数")
    
    # 备注
    remarks: Optional[str] = Field(None, description="备注")
    
    @validator('sampling_date', 'detection_date', pre=True)
    def parse_date(cls, v):
        """解析日期字符串"""
        if v is None:
            return v
        if isinstance(v, (datetime, date)):
            return v
        if isinstance(v, str):
            try:
                # 尝试解析为日期
                return datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                try:
                    # 尝试解析为日期时间
                    return datetime.fromisoformat(v)
                except ValueError:
                    raise ValueError(f"Invalid date format: {v}")
        return v
    
    @validator('cod_value', 'ammonia_nitrogen_value', 'total_phosphorus_value', 'potassium_permanganate_value')
    def validate_positive_values(cls, v):
        """验证水质指标数值必须为正数"""
        if v is not None and v < 0:
            raise ValueError("水质指标数值必须为正数")
        return v
    
    @validator('comprehensive_level_number')
    def validate_level_number(cls, v):
        """验证等级数范围"""
        if v is not None and (v < 0 or v > 6):
            raise ValueError("等级数必须在0-6之间")
        return v


class WaterQualityCreate(WaterQualityBase):
    """创建水质数据模式"""
    pass


class WaterQualityUpdate(BaseModel):
    """更新水质数据模式"""
    
    sampling_date: Optional[Union[datetime, date]] = Field(None, description="取样日期")
    sampling_time: Optional[str] = Field(None, description="取样时间")
    detection_date: Optional[Union[datetime, date]] = Field(None, description="检测日期")
    code: Optional[str] = Field(None, description="编号")
    river_name: Optional[str] = Field(None, description="河道名称")
    method: Optional[str] = Field(None, description="方式")
    
    # 水质指标数值
    cod_value: Optional[float] = Field(None, description="COD数值")
    ammonia_nitrogen_value: Optional[float] = Field(None, description="氨氮数值")
    total_phosphorus_value: Optional[float] = Field(None, description="总磷数值")
    potassium_permanganate_value: Optional[float] = Field(None, description="高锰酸钾数值")
    
    # 水质指标等级
    cod_level: Optional[str] = Field(None, description="COD等级")
    ammonia_nitrogen_level: Optional[str] = Field(None, description="氨氮等级")
    total_phosphorus_level: Optional[str] = Field(None, description="总磷等级")
    potassium_permanganate_level: Optional[str] = Field(None, description="高锰酸钾等级")
    
    # 综合评价
    comprehensive_quality_level: Optional[str] = Field(None, description="综合水质等级")
    comprehensive_level_number: Optional[int] = Field(None, description="综合等级数")
    
    # 备注
    remarks: Optional[str] = Field(None, description="备注")
    
    @validator('sampling_date', 'detection_date', pre=True)
    def parse_date(cls, v):
        """解析日期字符串"""
        if v is None:
            return v
        if isinstance(v, (datetime, date)):
            return v
        if isinstance(v, str):
            try:
                # 尝试解析为日期
                return datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                try:
                    # 尝试解析为日期时间
                    return datetime.fromisoformat(v)
                except ValueError:
                    raise ValueError(f"Invalid date format: {v}")
        return v


class WaterQualityResponse(WaterQualityBase):
    """水质数据响应模式"""
    
    id: int = Field(..., description="数据ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class WaterQualityListResponse(BaseModel):
    """水质数据列表响应模式"""
    
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页码")
    per_page: int = Field(..., description="每页数量")
    items: list[WaterQualityResponse] = Field(..., description="数据列表")


class WaterQualityQuery(BaseModel):
    """水质数据查询模式"""
    
    page: int = Field(1, ge=1, description="页码")
    per_page: int = Field(20, ge=1, le=100, description="每页数量")
    river_name: Optional[str] = Field(None, description="河道名称")
    sampling_date_start: Optional[datetime] = Field(None, description="取样开始日期")
    sampling_date_end: Optional[datetime] = Field(None, description="取样结束日期")
    comprehensive_quality_level: Optional[str] = Field(None, description="综合水质等级")
    code: Optional[str] = Field(None, description="编号")
    
    @validator('sampling_date_end')
    def validate_date_range(cls, v, values):
        """验证日期范围"""
        if v and values.get('sampling_date_start') and v < values['sampling_date_start']:
            raise ValueError('结束日期不能早于开始日期')
        return v 