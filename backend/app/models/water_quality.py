"""
水质数据模型
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func

from app.db.base import Base


class WaterQuality(Base):
    """水质数据模型"""
    
    __tablename__ = "water_quality"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 时间信息
    sampling_date = Column(DateTime, nullable=False, comment="取样日期")
    sampling_time = Column(String(20), nullable=True, comment="取样时间")
    detection_date = Column(DateTime, nullable=False, comment="检测日期")
    
    # 基本信息
    code = Column(String(50), nullable=True, index=True, comment="编号")
    river_name = Column(String(100), nullable=False, index=True, comment="河道名称")
    method = Column(String(50), nullable=True, comment="方式")
    
    # 水质指标数值
    cod_value = Column(Float, nullable=True, comment="COD数值")
    ammonia_nitrogen_value = Column(Float, nullable=True, comment="氨氮数值")
    total_phosphorus_value = Column(Float, nullable=True, comment="总磷数值")
    potassium_permanganate_value = Column(Float, nullable=True, comment="高锰酸钾数值")
    
    # 水质指标等级
    cod_level = Column(String(20), nullable=True, comment="COD等级")
    ammonia_nitrogen_level = Column(String(20), nullable=True, comment="氨氮等级")
    total_phosphorus_level = Column(String(20), nullable=True, comment="总磷等级")
    potassium_permanganate_level = Column(String(20), nullable=True, comment="高锰酸钾等级")
    
    # 综合评价
    comprehensive_quality_level = Column(String(20), nullable=True, comment="综合水质等级")
    comprehensive_level_number = Column(Integer, nullable=True, comment="综合等级数")
    
    # 系统字段
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    remarks = Column(Text, nullable=True, comment="备注")
    
    def __repr__(self):
        return f"<WaterQuality(id={self.id}, river_name='{self.river_name}', sampling_date='{self.sampling_date}')>" 