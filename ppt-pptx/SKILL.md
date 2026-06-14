---
name: ppt-pptx
description: 从 Markdown 大纲生成 PowerPoint(.pptx) —— # 作为每页标题，- 作为正文要点。触发词：生成 PPT、做个幻灯片、大纲转 PPT、导出 pptx、做演示文稿。
license: MIT
metadata:
  author: 小墨
  origin: 原创（开放 Agent Skills 格式 + python-pptx，无第三方 skill 代码）
---

# PPT 幻灯片生成

用 python-pptx 从大纲生成 .pptx，脚本在 `scripts/`。

## 约定
- `# 标题` → 新建一页，作为该页标题
- `- 要点` → 该页正文要点（可多条）
- 首页若只有标题、无要点 → 视为封面页

## 用法
`python3 scripts/pptx_build.py 大纲.md 输出.pptx`

## 依赖
`pip install python-pptx`

## 给 AI 的执行指引
1. 用户要做 PPT → 先把内容写成上述 Markdown 大纲，再调脚本。
2. 这是「快速出框架」的工具，视觉精修（配图 / 母版 / 动画）不在范围；要好看的演示稿走专门的视觉方案，别用它硬凑。
