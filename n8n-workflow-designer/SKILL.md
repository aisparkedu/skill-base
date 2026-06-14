---
name: n8n-workflow-designer
description: 用 n8n 做自动化工作流 —— 节点、触发器、凭据、自托管部署与集成。触发词：n8n、n8n 工作流、开源自动化、n8n 自托管。
---

# n8n 自动化工作流设计师

## 工作流
1. **安装配置 n8n** —— 选部署方式（Docker、npm、n8n Cloud），配环境变量（N8N_BASIC_AUTH_USER、N8N_ENCRYPTION_KEY、WEBHOOK_URL），配数据库（开发用 SQLite，生产用 PostgreSQL），用反向代理保护访问。
2. **设计工作流架构** —— 确定触发节点（Webhook、Cron、应用事件），规划节点间数据流，预留条件分支（IF、Switch），定好错误处理策略。
3. **配置凭据** —— 在 n8n 凭据管理器里为每个外部服务创建并存储认证（OAuth2、API Key、Basic Auth），它会自动加密，用之前先测连接。
4. **拼装节点** —— 在可视化编辑器里连节点：入口触发器、处理节点（Set、Function、Code 跑自定义 JS/Python）、集成节点（HTTP Request、数据库、SaaS）、控制节点（IF、Switch、Merge、Split In Batches）。
5. **转换数据** —— 复杂转换用 Code 节点（JS 或 Python），Set 节点改名重构字段，用表达式 {{ $json.field }} 做动态映射，Merge 节点合并并行分支数据。
6. **处理错误与可靠性** —— 开 Error Trigger 全局捕获失败，关键节点配自动重试，用 Stop and Error 做校验，失败时发通知（Slack、邮件）。
7. **测试迭代** —— 用 Execute 手动跑，在结果面板逐节点查输出，用真实测试数据，逐步修映射和转换。
8. **部署维护** —— 上生产激活工作流，配 n8n 数据库自动备份，把工作流导出成 JSON 进 Git 版本管理，用面板盯执行，定期升级 n8n。

## 规则
- 凭据一律加密，绝不硬编码进 Code 节点 —— 用内置凭据管理器。
- 大批量数据用 Split In Batches 节点处理，尊重外部 API 的限流。
- 工作流以 JSON 进 Git 版本管理 —— 定期导出并记录变更，方便回滚。
- 开发和生产环境分开 —— 完整工作流先在 staging 测，再上生产激活。
- 监控执行并对失败配告警 —— 一个静默出错的工作流可能造成不小的业务后果。
