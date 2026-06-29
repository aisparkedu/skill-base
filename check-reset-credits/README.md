# check-reset-credits

安全查询本机 Codex 账号的 rate-limit reset credits，并把授予时间、到期时间转换为本地时区。适合在演示或日常使用时，用一句自然语言查看还有多少张重置卡，不必在提示词里粘贴接口地址。

## 功能

- 读取本机 Codex 登录凭证并发起查询
- 汇总可用数量及每条 credit 的状态、标题、授予时间和到期时间
- 自动把 UTC 时间转换成本机时区
- 过滤令牌、Cookie、原始响应和唯一 ID
- 对 HTTP 401 给出明确的凭证或 Authorization header 提示

## 要求

- 已安装 Codex，并已在本机登录
- `~/.codex/auth.json` 中存在 `tokens.access_token`
- Python 3
- 能访问 ChatGPT 服务

## 安装

将整个目录复制到 Codex 的 Skills 目录：

```bash
cp -R check-reset-credits ~/.codex/skills/
```

新开一个 Codex 会话，让 Skill 重新加载。

## 使用示例

自然语言触发：

```text
帮我看看还有几张重置卡，什么时候到期。
```

显式触发：

```text
使用 $check-reset-credits 查询我的 Codex 重置额度。
```

也可以直接运行脚本：

```bash
python3 scripts/check_reset_credits.py
```

## 输出与安全

脚本只输出：

- `available_count`
- 每条 credit 的 `status`
- `title`
- `granted_at`
- `expires_at`

访问令牌只在进程内用于 Bearer 鉴权，不会主动打印或写入文件。脚本不会输出 refresh token、Cookie、Authorization header、原始响应或完整唯一 ID。

## 故障排查

- `HTTP 401`：本机凭证可能已失效，或 Authorization header 未正确携带；重新登录 Codex 后再试。
- 无法读取凭证：确认 Codex 已登录，且 `~/.codex/auth.json` 存在。
- 网络连接或超时：确认当前网络可以访问 ChatGPT 服务。

完整执行约束见 [SKILL.md](SKILL.md)。
