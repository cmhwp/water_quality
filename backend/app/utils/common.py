"""
通用工具函数
"""
from datetime import datetime
from typing import Optional, Union
import re


def parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """解析日期时间字符串"""
    if not date_str:
        return None
    
    # 支持多种日期格式
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"无效的日期格式: {date_str}")


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    return dt.strftime(fmt)


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_string(value: Optional[str]) -> Optional[str]:
    """清理字符串"""
    if not value:
        return None
    
    # 移除首尾空白
    value = value.strip()
    
    # 如果是空字符串，返回None
    if not value:
        return None
    
    return value


def safe_float(value: Union[str, float, int, None]) -> Optional[float]:
    """安全转换为浮点数"""
    if value is None:
        return None
    
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        
        try:
            return float(value)
        except ValueError:
            return None
    
    return None


def safe_int(value: Union[str, int, float, None]) -> Optional[int]:
    """安全转换为整数"""
    if value is None:
        return None
    
    if isinstance(value, int):
        return value
    
    if isinstance(value, float):
        return int(value)
    
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        
        try:
            return int(float(value))
        except ValueError:
            return None
    
    return None


def normalize_river_name(name: str) -> str:
    """规范化河道名称"""
    if not name:
        return ""
    
    # 移除多余空格
    name = ' '.join(name.split())
    
    # 转换为标准格式
    name = name.strip()
    
    return name


def create_response(success: bool = True, message: str = "", data: any = None, **kwargs) -> dict:
    """创建标准响应格式"""
    response = {
        "success": success,
        "message": message,
        "data": data
    }
    
    # 添加额外字段
    response.update(kwargs)
    
    return response


def create_error_response(message: str, error_code: int = 400, **kwargs) -> dict:
    """创建错误响应格式"""
    return create_response(
        success=False,
        message=message,
        error_code=error_code,
        **kwargs
    )


def create_success_response(message: str = "操作成功", data: any = None, **kwargs) -> dict:
    """创建成功响应格式"""
    return create_response(
        success=True,
        message=message,
        data=data,
        **kwargs
    ) 