---
name: excel-xlsx
description: 生成和读取 Excel(.xlsx) —— 把 CSV 转成带表头样式/冻结首行/自动列宽的 Excel，或读取 xlsx 的数据与公式。触发词：生成 Excel、做个表格、CSV 转 Excel、读取 xlsx、导出 Excel。
license: MIT
metadata:
  author: 小墨
  origin: 原创（开放 Agent Skills 格式 + openpyxl，无第三方 skill 代码）
---

# Excel 表格处理

用 openpyxl 生成和读取 .xlsx，脚本在 `scripts/`。

## 能力
- **生成**：CSV → 格式化 Excel（表头加粗高亮、冻结首行、自动列宽、数字自动识别）。
- **读取**：打印各工作表数据，`--formulas` 可看公式而非计算值。

## 用法
- 生成：`python3 scripts/xlsx_build.py 输入.csv 输出.xlsx [--sheet 名称]`
- 读取：`python3 scripts/xlsx_read.py 表格.xlsx [--formulas]`

## 依赖
`pip install openpyxl`

## 给 AI 的执行指引
1. 用户要做表 → 先把数据整理成 CSV（首行表头），再调 `xlsx_build.py`。
2. 需要图表 / 透视表 / 复杂公式时，超出脚本范围就直说，按需扩展脚本。
