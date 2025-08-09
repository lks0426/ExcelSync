#!/usr/bin/env python3
"""
通用Markdown表格解析器
将Markdown文件中的表格转换为结构化的JSON数据
"""

import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MDParser:
    """
    通用Markdown表格解析器
    支持标准Markdown表格语法，将表格数据转换为JSON格式
    """
    
    def __init__(self):
        """初始化解析器"""
        self.table_pattern = re.compile(
            r'^\s*\|.*\|.*$', re.MULTILINE
        )
        logger.info("Markdown表格解析器初始化完成")
    
    def parse(self, content: str) -> Dict[str, Any]:
        """
        解析Markdown内容中的表格（支持Markdown和HTML格式）
        
        参数:
            content: Markdown文本内容
            
        返回:
            包含headers和rows的字典
        """
        logger.info("开始解析Markdown内容")
        
        # 首先尝试HTML表格解析
        html_result = self._parse_html_tables(content)
        if html_result and html_result.get('metadata', {}).get('has_data'):
            logger.info(f"成功解析HTML表格: {len(html_result['headers'])} 列, {len(html_result['rows'])} 行")
            return html_result
        
        # 如果没有HTML表格，尝试Markdown表格
        tables = self._extract_tables(content)
        
        if not tables:
            logger.warning("未找到有效的Markdown表格或HTML表格")
            return {
                'headers': [],
                'rows': [],
                'metadata': {
                    'table_count': 0,
                    'type': 'none',
                    'has_data': False
                }
            }
        
        # 取第一个表格（如果有多个表格，可以扩展为处理所有表格）
        table = tables[0]
        headers, rows = self._parse_table(table)
        
        logger.info(f"成功解析Markdown表格: {len(headers)} 列, {len(rows)} 行")
        
        return {
            'headers': headers,
            'rows': self._convert_rows_to_objects(headers, rows),
            'metadata': {
                'table_count': len(tables),
                'type': 'markdown_table',
                'has_data': len(rows) > 0,
                'columns': len(headers),
                'rows': len(rows)
            }
        }
    
    def _extract_tables(self, content: str) -> List[str]:
        """
        从Markdown内容中提取所有表格
        
        参数:
            content: Markdown文本内容
            
        返回:
            表格字符串列表
        """
        tables = []
        lines = content.split('\n')
        current_table = []
        in_table = False
        
        for line in lines:
            # 检查是否是表格行
            if self._is_table_row(line):
                current_table.append(line)
                in_table = True
            else:
                # 如果之前在表格中，现在不是表格行，说明表格结束
                if in_table and current_table:
                    tables.append('\n'.join(current_table))
                    current_table = []
                in_table = False
        
        # 处理文件末尾的表格
        if current_table:
            tables.append('\n'.join(current_table))
        
        logger.debug(f"提取到 {len(tables)} 个表格")
        return tables
    
    def _is_table_row(self, line: str) -> bool:
        """
        判断是否是表格行
        
        参数:
            line: 文本行
            
        返回:
            是否是表格行
        """
        line = line.strip()
        return (line.startswith('|') and line.endswith('|')) or '|' in line
    
    def _parse_table(self, table_text: str) -> Tuple[List[str], List[List[str]]]:
        """
        解析单个表格
        
        参数:
            table_text: 表格文本
            
        返回:
            (headers, rows) 元组
        """
        lines = [line.strip() for line in table_text.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return [], []
        
        # 第一行是表头
        headers = self._parse_table_row(lines[0])
        
        # 跳过分隔符行（如果存在）
        data_start_index = 1
        if len(lines) > 1 and self._is_separator_row(lines[1]):
            data_start_index = 2
        
        # 解析数据行
        rows = []
        for i in range(data_start_index, len(lines)):
            row = self._parse_table_row(lines[i])
            if row:  # 只添加非空行
                # 确保行的长度与表头一致
                while len(row) < len(headers):
                    row.append('')
                # 截断超出表头长度的列
                row = row[:len(headers)]
                rows.append(row)
        
        return headers, rows
    
    def _is_separator_row(self, line: str) -> bool:
        """
        判断是否是表格分隔符行
        
        参数:
            line: 文本行
            
        返回:
            是否是分隔符行
        """
        # 分隔符行通常包含 :---、---:、:---: 等
        separator_pattern = re.compile(r'^\s*\|?[\s\-\|:]+\|?\s*$')
        return bool(separator_pattern.match(line))
    
    def _parse_table_row(self, row_text: str) -> List[str]:
        """
        解析表格行，提取各个单元格的内容
        
        参数:
            row_text: 表格行文本
            
        返回:
            单元格内容列表
        """
        # 去除首尾的 | 符号
        row_text = row_text.strip()
        if row_text.startswith('|'):
            row_text = row_text[1:]
        if row_text.endswith('|'):
            row_text = row_text[:-1]
        
        # 分割单元格
        cells = [cell.strip() for cell in row_text.split('|')]
        
        # 处理每个单元格的内容
        processed_cells = []
        for cell in cells:
            # 去除多余的空格
            cell = cell.strip()
            
            # 尝试转换为数字
            processed_cell = self._convert_cell_value(cell)
            processed_cells.append(processed_cell)
        
        return processed_cells
    
    def _convert_cell_value(self, cell_text: str) -> Any:
        """
        转换单元格值为合适的数据类型
        
        参数:
            cell_text: 单元格文本
            
        返回:
            转换后的值
        """
        if not cell_text or cell_text == '':
            return None
        
        cell_text = cell_text.strip()
        
        # 尝试转换为数字
        try:
            # 处理带逗号的数字
            number_text = cell_text.replace(',', '').replace('，', '')
            
            # 尝试转换为整数
            if '.' not in number_text:
                return int(number_text)
            else:
                return float(number_text)
                
        except ValueError:
            pass
        
        # 处理布尔值
        if cell_text.lower() in ['true', '是', 'yes', '✓']:
            return True
        elif cell_text.lower() in ['false', '否', 'no', '✗']:
            return False
        
        # 返回原始字符串
        return cell_text
    
    def _convert_rows_to_objects(self, headers: List[str], rows: List[List[Any]]) -> List[Dict[str, Any]]:
        """
        将行数据转换为对象列表
        
        参数:
            headers: 表头列表
            rows: 数据行列表
            
        返回:
            对象列表
        """
        objects = []
        
        for row in rows:
            obj = {}
            for i, header in enumerate(headers):
                value = row[i] if i < len(row) else None
                obj[header] = value
            objects.append(obj)
        
        return objects
    
    def _parse_html_tables(self, content: str) -> Optional[Dict[str, Any]]:
        """
        解析HTML表格
        
        参数:
            content: 包含HTML表格的内容
            
        返回:
            解析结果字典或None
        """
        try:
            soup = BeautifulSoup(content, 'html.parser')
            tables = soup.find_all('table')
            
            if not tables:
                return None
            
            # 取第一个表格
            table = tables[0]
            rows = table.find_all('tr')
            
            if not rows:
                return None
            
            # 提取表头和数据行
            headers = []
            data_rows = []
            
            for i, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                if i == 0:
                    # 第一行作为表头
                    headers = cell_texts
                else:
                    # 数据行
                    if cell_texts:  # 只添加非空行
                        # 确保行的长度与表头一致
                        while len(cell_texts) < len(headers):
                            cell_texts.append('')
                        # 截断超出表头长度的列
                        cell_texts = cell_texts[:len(headers)]
                        
                        # 转换单元格值的数据类型
                        processed_row = [self._convert_cell_value(cell) for cell in cell_texts]
                        data_rows.append(processed_row)
            
            if not headers or not data_rows:
                return None
            
            logger.info(f"成功解析HTML表格: {len(headers)} 列, {len(data_rows)} 行")
            
            return {
                'headers': headers,
                'rows': self._convert_rows_to_objects(headers, data_rows),
                'metadata': {
                    'table_count': len(tables),
                    'type': 'html_table',
                    'has_data': len(data_rows) > 0,
                    'columns': len(headers),
                    'rows': len(data_rows)
                }
            }
            
        except Exception as e:
            logger.warning(f"HTML表格解析失败: {str(e)}")
            return None
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        解析Markdown文件
        
        参数:
            file_path: 文件路径
            
        返回:
            解析结果
        """
        logger.info(f"开始解析文件: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = self.parse(content)
            result['metadata']['file_path'] = file_path
            result['metadata']['file_size'] = len(content)
            
            return result
            
        except Exception as e:
            logger.error(f"解析文件失败: {str(e)}")
            raise
    
    def save_to_json(self, data: Dict[str, Any], output_path: str):
        """
        将数据保存为JSON文件
        
        参数:
            data: 要保存的数据
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据已保存到: {output_path}")


def main():
    """测试MD解析功能"""
    parser = MDParser()
    
    # 测试内容
    test_content = """
# 产品清单

## 基本信息
- 创建日期: 2024-01-15
- 部门: 销售部

## 产品列表

| 产品名称 | 型号 | 价格 | 库存 | 类别 |
|---------|------|------|------|------|
| 笔记本电脑 | XPS-15 | 12999 | 50 | 电子产品 |
| 无线鼠标 | M705 | 299 | 200 | 配件 |
| 机械键盘 | K870 | 599 | 150 | 配件 |
| 显示器 | U2720Q | 3999 | 30 | 电子产品 |
| USB集线器 | H7 | 199 | 300 | 配件 |

## 备注
以上价格为含税价格
"""
    
    try:
        result = parser.parse(test_content)
        
        print(f"\n✅ 成功解析Markdown表格")
        print(f"📊 表头: {result['headers']}")
        print(f"📄 数据行数: {len(result['rows'])}")
        print(f"📋 元数据: {result['metadata']}")
        
        # 显示前几行数据
        if result['rows']:
            print("\n📝 示例数据:")
            for i, row in enumerate(result['rows'][:3]):
                print(f"  行 {i+1}: {row}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 解析失败: {str(e)}")
        logger.error(f"解析失败: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()