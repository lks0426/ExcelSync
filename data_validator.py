#!/usr/bin/env python3
"""
ExcelSync项目的简化数据处理模块
只做基本的数据清理，不做业务验证
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def clean_numeric_value(value: Any) -> float:
    """
    清理并转换值为数字格式
    
    参数:
        value: 输入值（字符串、整数、浮点数等）
        
    返回:
        浮点数值
    """
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        # 移除常见格式字符
        cleaned = value.replace(',', '').replace('¥', '').replace('￥', '').strip()
        
        # 处理括号中的负值
        if cleaned.startswith('(') and cleaned.endswith(')'):
            cleaned = '-' + cleaned[1:-1]
        
        try:
            return float(cleaned)
        except ValueError:
            raise ValueError(f"无法将 '{value}' 转换为数字")
    
    raise TypeError(f"数字值类型异常: {type(value)}")


def prepare_api_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    为写入准备和清理API数据
    
    参数:
        raw_data: 原始API响应数据
        
    返回:
        清理后的数据字典
    """
    cleaned_data = {}
    
    for key, value in raw_data.items():
        try:
            if value is not None:
                cleaned_data[key] = clean_numeric_value(value)
            else:
                cleaned_data[key] = 0  # 缺失值默认为0
        except (ValueError, TypeError) as e:
            logger.warning(f"清理字段 '{key}' 时出错: {str(e)}，保留原值")
            cleaned_data[key] = value  # 如果清理失败则保留原值
    
    return cleaned_data