"""
水质等级计算工具
基于中国地表水环境质量标准（GB3838-2002）
"""
from typing import Optional, Dict, Any


class WaterQualityCalculator:
    """水质等级计算器"""
    
    # 水质指标阈值标准（mg/L）
    QUALITY_STANDARDS = {
        'cod': {
            'Ⅰ类': 15,
            'Ⅱ类': 15,
            'Ⅲ类': 20,
            'Ⅳ类': 30,
            'Ⅴ类': 40
        },
        'ammonia_nitrogen': {
            'Ⅰ类': 0.15,
            'Ⅱ类': 0.5,
            'Ⅲ类': 1.0,
            'Ⅳ类': 1.5,
            'Ⅴ类': 2.0
        },
        'total_phosphorus': {
            'Ⅰ类': 0.02,
            'Ⅱ类': 0.1,
            'Ⅲ类': 0.2,
            'Ⅳ类': 0.3,
            'Ⅴ类': 0.4
        },
        'potassium_permanganate': {
            'Ⅰ类': 2,
            'Ⅱ类': 4,
            'Ⅲ类': 6,
            'Ⅳ类': 10,
            'Ⅴ类': 15
        }
    }
    
    # 等级优先级（数值越小，等级越差）
    LEVEL_PRIORITY = {
        '重度黑臭': 0,
        '轻度黑臭': 0.5,
        '劣Ⅴ类': 1,
        'Ⅴ类': 2,
        'Ⅳ类': 3,
        'Ⅲ类': 4,
        'Ⅱ类': 5,
        'Ⅰ类': 6
    }
    
    @classmethod
    def calculate_indicator_level(cls, indicator_type: str, value: Optional[float]) -> Optional[str]:
        """
        计算单个指标的等级
        
        Args:
            indicator_type: 指标类型 (cod, ammonia_nitrogen, total_phosphorus, potassium_permanganate)
            value: 指标数值
            
        Returns:
            等级字符串或None
        """
        if value is None:
            return None
            
        if indicator_type not in cls.QUALITY_STANDARDS:
            return None
            
        standards = cls.QUALITY_STANDARDS[indicator_type]
        
        # 检查是否超过Ⅴ类标准
        if value > standards['Ⅴ类']:
            return '劣Ⅴ类'
        
        # 特殊处理COD：Ⅰ类和Ⅱ类标准相同，当值等于15时判断为Ⅱ类
        if indicator_type == 'cod' and value == 15:
            return 'Ⅱ类'
        
        # 从最好的等级开始检查
        for level in ['Ⅰ类', 'Ⅱ类', 'Ⅲ类', 'Ⅳ类', 'Ⅴ类']:
            if value <= standards[level]:
                return level
        
        return '劣Ⅴ类'
    
    @classmethod
    def calculate_comprehensive_level(cls, cod_level: Optional[str], 
                                    ammonia_nitrogen_level: Optional[str],
                                    total_phosphorus_level: Optional[str],
                                    potassium_permanganate_level: Optional[str]) -> tuple[Optional[str], Optional[int]]:
        """
        计算综合水质等级（取最差等级）
        
        Args:
            cod_level: COD等级
            ammonia_nitrogen_level: 氨氮等级
            total_phosphorus_level: 总磷等级
            potassium_permanganate_level: 高锰酸钾等级
            
        Returns:
            (综合等级, 等级数)
        """
        levels = [cod_level, ammonia_nitrogen_level, total_phosphorus_level, potassium_permanganate_level]
        valid_levels = [level for level in levels if level is not None]
        
        if not valid_levels:
            return None, None
        
        # 找到最差等级（优先级最低）
        worst_level = min(valid_levels, key=lambda x: cls.LEVEL_PRIORITY.get(x, 99))
        
        # 等级数映射
        level_number_map = {
            '重度黑臭': 0,
            '轻度黑臭': 0,
            '劣Ⅴ类': 6,
            'Ⅴ类': 5,
            'Ⅳ类': 4,
            'Ⅲ类': 3,
            'Ⅱ类': 2,
            'Ⅰ类': 1
        }
        
        level_number = level_number_map.get(worst_level, None)
        
        return worst_level, level_number
    
    @classmethod
    def calculate_all_levels(cls, cod_value: Optional[float],
                           ammonia_nitrogen_value: Optional[float],
                           total_phosphorus_value: Optional[float],
                           potassium_permanganate_value: Optional[float]) -> Dict[str, Any]:
        """
        计算所有等级
        
        Args:
            cod_value: COD数值
            ammonia_nitrogen_value: 氨氮数值
            total_phosphorus_value: 总磷数值
            potassium_permanganate_value: 高锰酸钾数值
            
        Returns:
            包含所有等级的字典
        """
        # 计算各指标等级
        cod_level = cls.calculate_indicator_level('cod', cod_value)
        ammonia_nitrogen_level = cls.calculate_indicator_level('ammonia_nitrogen', ammonia_nitrogen_value)
        total_phosphorus_level = cls.calculate_indicator_level('total_phosphorus', total_phosphorus_value)
        potassium_permanganate_level = cls.calculate_indicator_level('potassium_permanganate', potassium_permanganate_value)
        
        # 计算综合等级
        comprehensive_level, level_number = cls.calculate_comprehensive_level(
            cod_level, ammonia_nitrogen_level, total_phosphorus_level, potassium_permanganate_level
        )
        
        return {
            'cod_level': cod_level,
            'ammonia_nitrogen_level': ammonia_nitrogen_level,
            'total_phosphorus_level': total_phosphorus_level,
            'potassium_permanganate_level': potassium_permanganate_level,
            'comprehensive_quality_level': comprehensive_level,
            'comprehensive_level_number': level_number
        }
    
    @classmethod
    def is_warning_level(cls, level: Optional[str]) -> bool:
        """
        判断是否为警告等级
        
        Args:
            level: 水质等级
            
        Returns:
            是否为警告等级
        """
        if not level:
            return False
        
        warning_levels = ['Ⅴ类', '劣Ⅴ类', '轻度黑臭', '重度黑臭']
        return level in warning_levels
    
    @classmethod
    def is_qualified_level(cls, level: Optional[str]) -> bool:
        """
        判断是否为合格等级（I-III类）
        
        Args:
            level: 水质等级
            
        Returns:
            是否为合格等级
        """
        if not level:
            return False
        
        qualified_levels = ['Ⅰ类', 'Ⅱ类', 'Ⅲ类']
        return level in qualified_levels 