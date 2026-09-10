# 冒烟

> 验证本机 `officecli` 能建三类文件并给出 JSON 信封。参数化工作目录，不要写用户桌面。

前置：`uv run plugins/project-evo/skills/office-pro/scripts/which.py` 退出 0。

```powershell
uv run plugins/project-evo/skills/office-pro/scripts/smoke.py
```

期望：pptx / docx / xlsx 均 `validate` 通过；`get --json` 含 `"success": true`；坏路径 `/slide[99]` 退出 1、`not_found`。工作目录 `%TEMP%\pevo-office-pro-smoke\`。
