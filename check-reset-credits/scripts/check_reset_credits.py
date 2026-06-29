#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime


AUTH_PATH = os.path.expanduser("~/.codex/auth.json")
ENDPOINT = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits"


def fail(message):
    print(message)
    raise SystemExit(1)


def to_local_time(value):
    if value is None:
        return None
    if not isinstance(value, str):
        return "无法解析"

    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        return datetime.fromisoformat(normalized).astimezone().isoformat(timespec="seconds")
    except ValueError:
        return "无法解析"


try:
    with open(AUTH_PATH, encoding="utf-8") as auth_file:
        access_token = json.load(auth_file)["tokens"]["access_token"]
except (OSError, json.JSONDecodeError, KeyError, TypeError):
    fail("无法从本机 Codex 凭证读取 access_token。")

request = urllib.request.Request(
    ENDPOINT,
    headers={
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    },
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        status = response.status
        payload = json.load(response)
except urllib.error.HTTPError as error:
    if error.code == 401:
        fail("HTTP 401：凭证已失效，或 Authorization header 未正确携带。")
    fail(f"请求失败：HTTP {error.code}。")
except (urllib.error.URLError, TimeoutError):
    fail("请求失败：网络连接或请求超时。")
except (json.JSONDecodeError, UnicodeDecodeError):
    fail("请求成功，但响应不是有效 JSON。")

if status != 200:
    fail(f"请求失败：HTTP {status}。")
if not isinstance(payload, dict):
    fail("请求成功，但响应格式不符合预期。")

credits = payload.get("credits", [])
if not isinstance(credits, list):
    credits = []

safe_summary = {
    "available_count": payload.get("available_count"),
    "credits": [
        {
            "status": credit.get("status"),
            "title": credit.get("title"),
            "granted_at": to_local_time(credit.get("granted_at")),
            "expires_at": to_local_time(credit.get("expires_at")),
        }
        for credit in credits
        if isinstance(credit, dict)
    ],
}

print(json.dumps(safe_summary, ensure_ascii=False, indent=2))
