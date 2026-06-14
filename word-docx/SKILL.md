---
name: word-docx
description: 生成和读取 Word(.docx) 文档 —— 从 Markdown 一键生成带标题/列表/表格/加粗的 Word，或提取 .docx 文本。触发词：生成 Word、做个 docx、导出 Word、读取 Word、把内容转成 Word。
license: MIT
metadata:
  author: 小墨
  origin: 原创（开放 Agent Skills 格式 + python-docx，无第三方 skill 代码）
---

# Word 文档处理

用 python-docx 生成和解析 .docx，脚本在 `scripts/`。

## 能力
- **生成**：把 Markdown（# 标题、- / 1. 列表、| 表格 |、**加粗**）转成排版好的 Word。
- **读取**：提取 .docx 的段落和表格文本。

## 用法
- 生成：`python3 scripts/docx_create.py 输入.md 输出.docx`（输入用 `-` 从 stdin 读）
- 读取：`python3 scripts/docx_read.py 文档.docx`

## 依赖
`pip install python-docx`

## 给 AI 的执行指引
1. 用户要做 Word → 先把内容整理成 Markdown，再调 `docx_create.py`。
2. 用户给 .docx 要内容 → 调 `docx_read.py` 提取后再处理。
3. 页眉页脚、复杂样式超出脚本范围时，直说做不了并给替代方案，别假装能做。
