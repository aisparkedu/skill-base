# AI Spark Skill 合集（skill-base）

> 给 Claude Code / Codex / Gemini CLI 等 AI 编程智能体用的实用 Skill 合集 —— 覆盖**文档处理、内容创作、营销增长、调研分析、效率协作**五大类。**AI Spark 原创 + 精选整理自开源社区。**

🔗 配套：[AI Spark 知识库](https://github.com/aisparkedu/knowledge-base) · 一线 AI 实战者维护的开源知识库

---

## 这是什么

每个 Skill 是一个文件夹，含 `SKILL.md`（能力说明 + 触发词），部分带 `scripts/`（可执行脚本）。

Skill 是 AI 智能体的「可复用技能包」：放进智能体的 skills 目录后，遇到匹配的需求会**自动触发**，不用你每次手把手教。格式遵循 Anthropic 于 2025-12 公开的 **Agent Skills 开放标准**，兼容 Claude Code / Codex / Gemini CLI / Cursor 等主流 AI 编程工具。

## 快速使用

1. 把想用的 Skill 文件夹复制到 `~/.claude/skills/`（或对应工具的 skills 目录）。
2. 重启会话即生效，描述里的触发词命中时会自动调用。
3. 带脚本的 Skill 需先装依赖，见各自 `SKILL.md` 里的「依赖」。

---

## Skill 清单（共 31 个）

### 📄 文档处理（4）
- **word-docx** —— Markdown 一键生成带标题 / 列表 / 表格的 Word(.docx)，也能反向提取 .docx 文本。
- **excel-xlsx** —— CSV 转成带表头样式、冻结首行、自动列宽的 Excel(.xlsx)，也能读取数据与公式。
- **ppt-pptx** —— 把 Markdown 大纲（`#` 标题、`-` 要点）直接生成 PowerPoint(.pptx)。
- **pdf-toolkit** —— PDF 提取文本、合并多个 PDF、按页拆分。

### ✍️ 内容创作（8）
- **visual-deck** —— 把选题 / 大纲做成图文混合的全屏 HTML 演示稿（科普图、讲解 PPT、知识卡）。
- **content-production** —— 内容生产全流水线，一个选题从空白页做到可发布成稿。
- **storytelling-expert** —— 故事化表达：叙事结构、开场钩子、情绪弧线，把干内容讲出感染力。
- **article-optimizer** —— 针对某一篇具体文章做定向优化打磨。
- **score-optimizer** —— 按爆款维度给文章打分，并据评分迭代优化。
- **research-collector** —— 收集选题素材（YouTube 视频 + 网文），汇进 NotebookLM 做分析。
- **yt-dlp-direct** —— 用 yt-dlp 下载 / 检查在线音视频（单视频、playlist、字幕、音频提取）。
- **publisher-wechatsync** —— 成稿一键分发到知乎 / 掘金 / CSDN / 公众号等多平台。

### 📈 营销 / 增长（6）
- **x-twitter-growth** —— X/Twitter 涨粉引擎：账号诊断、对标研究、写推文 / thread、发布规划、互动追踪。
- **social-media-strategist** —— 社媒内容策略：内容日历、分平台格式、互动运营、分平台 KPI。
- **seo-optimizer** —— 站内与技术 SEO：meta 标签、结构化数据、Core Web Vitals、关键词策略。
- **growth-hacking-strategist** —— 增长黑客：按 AARRR 框架做获客 / 激活 / 留存 / 推荐 / 变现。
- **email-marketing-designer** —— 邮件营销：自动化序列、分群、A/B 测试、送达率优化。
- **app-store-optimization** —— ASO：关键词研究、对标排名分析、元数据建议、提升商店可见度。

### 🔎 调研 / 分析（4）
- **market-research** —— 市场调研：TAM/SAM/SOM 自上而下 + 自下而上双算、问卷样本量测算。
- **product-research** —— 产品 / 用户研究：按目标选方法（访谈 / 可用性 / 概念测试）、整理研究库。
- **financial-analyst** —— 财务比率分析、DCF 估值、预算差异分析、滚动预测。
- **notebooklm** —— 浏览器自动化操控 NotebookLM：开笔记本、加来源、向笔记本提问。

### ⚙️ 效率 / 协作 / 工程（9）
- **check-reset-credits** —— 安全查询 Codex 重置额度、授予时间和本地到期时间，不暴露凭证或唯一 ID。
- **meeting-summarizer** —— 会议纪要：提炼决策、待办、下一步，出完整版 + 速读版两个版本。
- **weekly-planner** —— 周计划：用艾森豪威尔矩阵排优先级 + 时间块。
- **decision-matrix** —— 决策矩阵：选项 × 加权标准打分，帮你在多个选择间做复杂取舍。
- **pitch-deck-designer** —— 融资路演 deck 设计：页面结构、关键指标、融资诉求。
- **handoff** —— 把当前对话压缩成交接文档给下一个 agent 接手，写入前自动脱敏密钥。
- **workflow-builder** —— 设计 / 编写 Claude Code 多智能体工作流脚本（`.js`）。
- **skill-tester** —— 测 Skill 质量的元技能：结构校验、脚本测试、多维度打分。
- **n8n-workflow-designer** —— 用 n8n 搭自动化工作流：节点、触发器、凭据、自托管部署。

---

## 来源与致谢

本合集包含 **AI Spark 原创 Skill**，以及**精选整理自开源社区（MIT 协议）的 Skill**。

- 每个 Skill 的**来源、原作者与协议**见其目录下的 `_SOURCE.md`。
- 第三方协议原文存档于 `_LICENSES/`，汇总见 [`NOTICE.md`](./NOTICE.md)。

感谢原作者们的开源贡献。

## 协议

- 本合集中 **AI Spark 原创部分以 MIT 协议开源**（见 [`LICENSE`](./LICENSE)）。
- 第三方 Skill **保留其原有协议**（均为 MIT），详见各 `_SOURCE.md`、`_LICENSES/` 与 `NOTICE.md`。
