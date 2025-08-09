#!/usr/bin/env python3
"""
ExcelSync项目的映射配置
定义API字段名与Excel单元格位置之间的映射关系
"""

# 试算表映射配置
# 将API字段名（具有业务含义）映射到Excel单元格位置
# 基于实际Excel文件中E列有值的位置

TRIAL_BALANCE_MAPPING = {
    # 流動資産部分 (流动资产) - 11项
    "cash": "D4",                              # 現金
    "ordinary_deposits": "D5",                 # 普通預金
    "cash_and_deposits_total": "D6",          # 現金及び預金合計
    "accounts_receivable": "D8",               # 売掛金
    "receivables_total": "D9",                 # 売上債権合計
    "prepaid_expenses": "D16",                 # 前払費用
    "accounts_payable_temporary": "D17",       # 仮払金
    "consumption_tax_receivable": "D18",       # 仮払消費税
    "settlement_temporary": "D19",             # 決済仮払
    "other_current_assets_total": "D21",       # その他流動資産合計
    "current_assets_total": "D22",             # 流動資産合計
    
    # 固定資産部分 (固定资产) - 4项
    "equipment_tools": "D25",                  # 工具器具備品
    "tangible_fixed_assets_total": "D26",      # 有形固定資産合計
    "investment_assets_total": "D32",          # 投資その他の資産合計
    "fixed_assets_total": "D33",               # 固定資産合計
    
    # 資産合計部分 (资产合计) - 1项
    "total_assets": "D40",                     # 資産の部合計
    
    # 流動負債部分 (流动负债) - 7项
    "short_term_loans": "D47",                 # 短期借入金
    "accounts_payable": "D48",                 # 未払金
    "deposits_received": "D50",                # 預り金
    "temporary_receipts": "D51",               # 仮受金
    "consumption_tax_payable": "D53",          # 仮受消費税
    "other_current_liabilities_total": "D54",  # その他流動負債合計
    "current_liabilities_total": "D55",        # 流動負債合計
    
    # 固定負債・負債合計部分 (固定负债和负债合计) - 2项
    "fixed_liabilities_total": "D57",          # 固定負債合計
    "total_liabilities": "D58",                # 負債の部合計
    
    # 純資産部分 (净资产) - 8项
    "capital_stock": "D62",                    # 資本金 (第1项)
    "capital_stock_duplicate": "D63",          # 資本金 (第2项)
    "capital_reserves": "D68",                 # 資本準備金
    "capital_surplus_total": "D69",            # 資本剰余金合計
    "retained_earnings": "D71",                # 繰越利益剰余金
    "retained_earnings_total": "D73",          # 利益剰余金合計
    "shareholders_equity_total": "D78",        # 株主資本合計
    "net_assets_total": "D83",                 # 純資産の部合計
    "total_liabilities_and_equity": "D84"      # 負債・純資産合計
}

# 用于文档的单元格描述
CELL_DESCRIPTIONS = {
    "D4": "現金 (现金)",
    "D5": "普通預金 (普通存款)",
    "D6": "現金及び預金合計 (现金及存款合计)",
    "D8": "売掛金 (应收账款)",
    "D9": "売上債権合計 (销售债权合计)",
    "D16": "前払費用 (预付费用)",
    "D17": "仮払金 (临时付款)",
    "D18": "仮払消費税 (应收消费税)",
    "D19": "決済仮払 (结算临时付款)",
    "D21": "その他流動資産合計 (其他流动资产合计)",
    "D22": "流動資産合計 (流动资产合计)",
    "D25": "工具器具備品 (工具器具设备)",
    "D26": "有形固定資産合計 (有形固定资产合计)",
    "D32": "投資その他の資産合計 (投资等其他资产合计)",
    "D33": "固定資産合計 (固定资产合计)",
    "D40": "資産の部合計 (资产部合计)",
    "D47": "短期借入金 (短期借款)",
    "D48": "未払金 (应付账款)",
    "D50": "預り金 (预收款)",
    "D51": "仮受金 (临时收款)",
    "D53": "仮受消費税 (应付消费税)",
    "D54": "その他流動負債合計 (其他流动负债合计)",
    "D55": "流動負債合計 (流动负债合计)",
    "D57": "固定負債合計 (固定负债合计)",
    "D58": "負債の部合計 (负债部合计)",
    "D62": "資本金 (资本金 - 第1项)",
    "D63": "資本金 (资本金 - 第2项)",
    "D68": "資本準備金 (资本公积)",
    "D69": "資本剰余金合計 (资本盈余合计)",
    "D71": "繰越利益剰余金 (留存收益)",
    "D73": "利益剰余金合計 (利润盈余合计)",
    "D78": "株主資本合計 (股东权益合计)",
    "D83": "純資産の部合計 (净资产部合计)",
    "D84": "負債・純資産合計 (负债净资产合计)"
}

# 用于验证的数据类型定义
FIELD_DATA_TYPES = {
    # 所有字段都是数值类型（可以是正数、负数或零）
    "cash": "number",
    "ordinary_deposits": "number",
    "cash_and_deposits_total": "number",
    "accounts_receivable": "number",
    "receivables_total": "number",
    "prepaid_expenses": "number",
    "accounts_payable_temporary": "number",
    "consumption_tax_receivable": "number",
    "settlement_temporary": "number",
    "other_current_assets_total": "number",
    "current_assets_total": "number",
    "equipment_tools": "number",
    "tangible_fixed_assets_total": "number",
    "investment_assets_total": "number",
    "fixed_assets_total": "number",
    "total_assets": "number",
    "short_term_loans": "number",
    "accounts_payable": "number",
    "deposits_received": "number",
    "temporary_receipts": "number",
    "consumption_tax_payable": "number",
    "other_current_liabilities_total": "number",
    "current_liabilities_total": "number",
    "fixed_liabilities_total": "number",
    "total_liabilities": "number",
    "capital_stock": "number",
    "capital_stock_duplicate": "number",
    "capital_reserves": "number",
    "capital_surplus_total": "number",
    "retained_earnings": "number",
    "retained_earnings_total": "number",
    "shareholders_equity_total": "number",
    "net_assets_total": "number",
    "total_liabilities_and_equity": "number"
}

# 将配置导出为JSON
def export_mapping_to_json(filename="mapping_config.json"):
    """将映射配置导出为JSON文件"""
    import json
    
    config = {
        "mapping": TRIAL_BALANCE_MAPPING,
        "descriptions": CELL_DESCRIPTIONS,
        "data_types": FIELD_DATA_TYPES
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"映射配置已导出到 {filename}")

if __name__ == "__main__":
    # 打印映射摘要
    print(f"总映射字段数: {len(TRIAL_BALANCE_MAPPING)}")
    print("\n映射摘要:")
    for api_field, cell in TRIAL_BALANCE_MAPPING.items():
        desc = CELL_DESCRIPTIONS.get(cell, "")
        print(f"  {api_field:<35} -> {cell:<5} {desc}")