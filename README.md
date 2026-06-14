# AI Spark Skill 合集

> 给 Claude Code / Codex / Gemini CLI 等 AI 编程智能体用的实用 Skill 合集 —— 覆盖文档处理、内容创作、营销增长、调研分析、效率协作。**AI Spark 原创 + 精选整理自开源社区。**

🔗 配套：[AI Spark 知识库](https://github.com/aisparkedu/knowledge-base) · 一线 AI 实战者维护的开源知识库

---

## 这是什么

每个 Skill 是一个文件夹，含 `SKILL.md`（能力说明 + 触发词），部分带 `scripts/`（可执行脚本）。放进 AI 编程智能体的 skills 目录即可按需自动触发。

Skill 格式遵循 Anthropic 2025-12 开源的 **Agent Skills 开放标准**。

## Skill 目录（按用途）

### 📄 文档处理
`word-docx` · `excel-xlsx` · `ppt-pptx` · `pdf-toolkit`
> Word / Excel / PPT / PDF 的生成、读取、合并、拆分。

### ✍️ 内容创作
`visual-deck` · `content-production` · `storytelling-expert` · `article-optimizer` · `score-optimizer` · `research-collector` · `yt-dlp-direct` · `publisher-wechatsync`
> 从选题、素材收集、成稿、打磨到多平台分发，以及图文演示稿、音视频下载。

### 📈 营销 / 增长
`x-twitter-growth` · `social-media-strategist` · `seo-optimizer` · `growth-hacking-strategist` · `email-marketing-designer` · `app-store-optimization`
> 社媒策略、X 涨粉、SEO、增长黑客、邮件营销、ASO。

### 🔎 调研 / 分析
`market-research` · `product-research` · `financial-analyst` · `notebooklm`
> 市场 / 产品 / 财务调研，NotebookLM 自动化。

### ⚙️ 效率 / 协作 / 工程
`meeting-summarizer` · `weekly-planner` · `decision-matrix` · `pitch-deck-designer` · `handoff` · `workflow-builder` · `skill-tester` · `n8n-workflow-designer`
> 会议纪要、周计划、决策矩阵、路演 deck、对话交接、工作流编写、skill 测试、n8n 自动化。

## 使用

把想用的 Skill 文件夹复制到 `~/.claude/skills/`（或对应智能体的 skills 目录），重启会话即生效。带脚本的 Skill 需安装对应依赖，见各自 `SKILL.md`。

## 来源与致谢

本合集包含 **AI Spark 原创 Skill**，以及**精选整理自开源社区（MIT 协议）的 Skill**。

- 每个 Skill 的**来源、原作者与协议**见其目录下的 `_SOURCE.md`。
- 第三方协议原文存档于 `_LICENSES/`，汇总见 [`NOTICE.md`](./NOTICE.md)。

感谢原作者们的开源贡献。

## 协议

- 本合集中 **AI Spark 原创部分以 MIT 协议开源**（见 [`LICENSE`](./LICENSE)）。
- 第三方 Skill **保留其原有协议**（均为 MIT），详见各 `_SOURCE.md`、`_LICENSES/` 与 `NOTICE.md`。
