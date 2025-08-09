# ExcelSync 项目

ExcelSync 是一个Python项目，用于将API数据同步到Excel试算表的特定单元格。它处理34个会计字段，并将它们写入Excel文件D列中E列有值的位置。

## 功能特性

- **精确映射**: 将34个特定API字段映射到Excel单元格
- **数据验证**: 验证数据类型和会计平衡关系
- **错误处理**: 全面的错误处理和日志记录
- **备份支持**: 写入前可选择创建备份
- **批量处理**: 一次性写入所有34个字段

## 项目结构

```
ExcelSync/
├── mapping.xlsx           # 目标Excel文件，包含试算表
├── excel_writer.py        # 使用openpyxl的Excel写入引擎
├── mapping_config.py      # 34字段映射配置
├── data_validator.py      # API数据验证模块  
├── excel_sync.py          # 主要协调模块
├── sample_api_data.json   # 示例API数据
├── requirements.txt       # 依赖列表
└── README.md              # 本文件
```

## 安装依赖

```bash
# 安装必需的包
pip install pandas openpyxl
```

## 使用方法

### 命令行界面

```bash
# 生成示例API数据文件
python excel_sync.py --generate-sample

# 从JSON文件同步数据
python excel_sync.py --api-data sample_api_data.json

# 只验证数据而不写入
python excel_sync.py --api-data sample_api_data.json --validate-only

# 同步前创建备份
python excel_sync.py --api-data sample_api_data.json --backup
```

### Python API

```python
from excel_sync import ExcelSync

# 初始化
sync = ExcelSync("mapping.xlsx", "A社貼り付けBS")

# 准备API数据（需要所有34个字段）
api_data = {
    "cash": 1234567,
    "ordinary_deposits": 8765432,
    # ... 所有34个字段
}

# 同步数据
result = sync.sync_from_api(api_data)
print(result["status"])  # "success", "validation_failed" 等
```

## API数据格式

API必须提供所有34个字段，数值类型：

### 流动资产 - 11个字段
- `cash`: 現金
- `ordinary_deposits`: 普通預金
- `cash_and_deposits_total`: 現金及び預金合計
- `accounts_receivable`: 売掛金
- `receivables_total`: 売上債権合計
- `prepaid_expenses`: 前払費用
- `accounts_payable_temporary`: 仮払金
- `consumption_tax_receivable`: 仮払消費税
- `settlement_temporary`: 決済仮払
- `other_current_assets_total`: その他流動資産合計
- `current_assets_total`: 流動資産合計

### 固定资产 - 4个字段
- `equipment_tools`: 工具器具備品
- `tangible_fixed_assets_total`: 有形固定資産合計
- `investment_assets_total`: 投資その他の資産合計
- `fixed_assets_total`: 固定資産合計

### 资产合计 - 1个字段
- `total_assets`: 資産の部合計

### 流动负债 - 7个字段
- `short_term_loans`: 短期借入金
- `accounts_payable`: 未払金
- `deposits_received`: 預り金
- `temporary_receipts`: 仮受金
- `consumption_tax_payable`: 仮受消費税
- `other_current_liabilities_total`: その他流動負債合計
- `current_liabilities_total`: 流動負債合計

### 固定负债和负债合计 - 2个字段
- `fixed_liabilities_total`: 固定負債合計
- `total_liabilities`: 負債の部合計

### 净资产 - 8个字段
- `capital_stock`: 資本金
- `capital_stock_duplicate`: 資本金（重复项）
- `capital_reserves`: 資本準備金
- `capital_surplus_total`: 資本剰余金合計
- `retained_earnings`: 繰越利益剰余金
- `retained_earnings_total`: 利益剰余金合計
- `shareholders_equity_total`: 株主資本合計
- `net_assets_total`: 純資産の部合計

### 负债净资产合计 - 1个字段
- `total_liabilities_and_equity`: 負債・純資産合計

## 验证规则

系统验证：
1. **数据类型**: 所有字段必须是数值
2. **完整性**: 必须存在所有34个字段
3. **平衡关系**:
   - 現金 + 普通預金 = 現金及び預金合計
   - 総資産 = 負債・純資産合計

## 日志记录

系统将所有操作记录到：
- 控制台输出
- `excel_sync.log` 文件

日志级别：
- INFO: 正常操作
- WARNING: 非关键问题（如验证警告）
- ERROR: 阻止操作的关键错误

## 错误处理

系统处理：
- 缺失的API字段
- 无效的数据类型
- 平衡验证失败
- Excel文件访问错误
- 单元格位置错误

## API响应示例

```json
{
  "cash": 1234567,
  "ordinary_deposits": 8765432,
  "cash_and_deposits_total": 9999999,
  "accounts_receivable": 3456789,
  "receivables_total": 3456789,
  "prepaid_expenses": 234567,
  "accounts_payable_temporary": 345678,
  "consumption_tax_receivable": 456789,
  "settlement_temporary": 567890,
  "other_current_assets_total": 1604924,
  "current_assets_total": 15565380,
  "equipment_tools": 500000,
  "tangible_fixed_assets_total": 500000,
  "investment_assets_total": 1000000,
  "fixed_assets_total": 1500000,
  "total_assets": 17065380,
  "short_term_loans": 1000000,
  "accounts_payable": 2345678,
  "deposits_received": 123456,
  "temporary_receipts": 234567,
  "consumption_tax_payable": 345678,
  "other_current_liabilities_total": 1049379,
  "current_liabilities_total": 4049379,
  "fixed_liabilities_total": 0,
  "total_liabilities": 4049379,
  "capital_stock": 10000000,
  "capital_stock_duplicate": 10000000,
  "capital_reserves": 2000000,
  "capital_surplus_total": 2000000,
  "retained_earnings": 1055544,
  "retained_earnings_total": 1055544,
  "shareholders_equity_total": 13055544,
  "net_assets_total": 13055544,
  "total_liabilities_and_equity": 17065380
}
```