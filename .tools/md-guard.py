"""md-guard:markdown 四类禁字门禁(集成约束形态二,uv 运行时脚本)。

两种入口:
- Claude Code PostToolUse hook(形态一调度):stdin 收工具事件 JSON,取 tool_input.file_path,
  是 .md 则检四类禁字;有违规 exit 2(stderr 回传 agent 提醒修正),干净 exit 0
- git pre-commit(形态三调度):--staged 检查暂存区 .md;有违规 exit 1 挡提交

规则唯一权威在 project_evo.mdfix(与 scan/check PE-12 同源);本脚本只是薄适配,
故不带 PEP 723 头(需项目环境导入 project_evo),仓外复用等价命令:`project-evo scan <path>`。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from project_evo.mdfix import file_violations


def check_file(path: Path) -> list[str]:
    """返回该 md 文件的违规行描述;空列表 = 干净。"""
    v = file_violations(path.read_text(encoding="utf-8"))
    return [f"{path}:{line} {'、'.join(cats)}" for line, cats in sorted(v.items())]


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--staged":
        proc = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if proc.returncode != 0:
            print("md-guard: git diff 失败", file=sys.stderr)
            return 2
        bad: list[str] = []
        for name in proc.stdout.splitlines():
            p = Path(name)
            if p.suffix.lower() != ".md" or not p.exists():
                continue
            bad += check_file(p)
        if bad:
            print("md 禁字挡板(集成约束):以下暂存文件含四类禁字,修正后再提交:", file=sys.stderr)
            for b in bad:
                print(f"  {b}", file=sys.stderr)
            return 1
        return 0

    # hook 模式:stdin JSON
    try:
        event = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    fp = (event.get("tool_input") or {}).get("file_path") or ""
    p = Path(fp) if fp else None
    if not p or p.suffix.lower() != ".md" or not p.exists():
        return 0
    bad = check_file(p)
    if bad:
        print(f"md 禁字提醒(集成约束):{p.name} 有 {len(bad)} 行含四类禁字,请按写作规范修正:",
              file=sys.stderr)
        for b in bad:
            print(f"  {b}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
