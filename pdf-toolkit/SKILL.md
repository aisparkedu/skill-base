---
name: pdf-toolkit
description: PDF 工具箱 —— 提取文本、合并、拆分。触发词：提取 PDF 文字、PDF 转文本、合并 PDF、拆分 PDF、把几个 PDF 拼一起。
license: MIT
metadata:
  author: 小墨
  origin: 原创（开放 Agent Skills 格式 + PyMuPDF，无第三方 skill 代码）
---

# PDF 工具箱

用 PyMuPDF(fitz) 处理 PDF，脚本在 `scripts/`。

## 能力
- **提取文本**：整篇或指定页码范围。
- **合并**：多个 PDF 拼成一个。
- **拆分**：按每 N 页切成多个 PDF。

## 用法
- 提取：`python3 scripts/pdf_extract.py 文件.pdf [--pages 1-3]`
- 合并：`python3 scripts/pdf_merge.py merge 输出.pdf a.pdf b.pdf ...`
- 拆分：`python3 scripts/pdf_merge.py split 输入.pdf 前缀 [--every N]`

## 依赖
`pip install PyMuPDF`

## 给 AI 的执行指引
1. 扫描件 / 图片型 PDF 提取不到文字时，需要 OCR（本脚本不含），直说并给方案。
2. 合并前确认页序，拆分时说明每段页码范围。
