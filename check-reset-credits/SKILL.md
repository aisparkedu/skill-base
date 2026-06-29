---
name: check-reset-credits
description: Safely query and summarize Codex rate-limit reset credits using the local Codex credential. Use when the user asks to query, check, view, or count Codex reset credits, reset cards, rate-limit credits, remaining resets, or their grant and expiration times, including Chinese requests such as “查询重置额度”, “看看还有几张重置卡”, or “重置卡什么时候到期”.
---

# Check Reset Credits

Run:

```bash
python3 scripts/check_reset_credits.py
```

If the current directory is not this skill directory, resolve the script path relative to this `SKILL.md`.

Return the script output as the answer. Keep these safeguards:

- Never print or expose access tokens, refresh tokens, cookies, Authorization headers, raw responses, or unique IDs.
- Report only `available_count` and each credit's `status`, `title`, `granted_at`, and `expires_at`.
- Preserve the local timezone shown by the script.
- If the script reports HTTP 401, explain that the credential is invalid/expired or the Authorization header was not sent correctly.
- Do not reproduce the endpoint URL in the user-facing response.
