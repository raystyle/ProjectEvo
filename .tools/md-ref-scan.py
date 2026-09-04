# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""md-ref-scan: skills 树内 markdown 交叉引用断链扫描。

用法: uv run .tools/md-ref-scan.py [根目录,默认 skills/project-evo]
退出码: 0 无断链 / 1 有断链 / 2 出错。
规则: 提取 <路径前缀/ ><名>.md 引用,按「本文件目录、根、根/references」三级解析;
目标项目的固定文件名(CLAUDE/AGENTS/template 等)与命令示例(notes.md/a.md)跳过。
"""

from __future__ import annotations

import sys
from pathlib import Path
import re

SKIP = {
    "CLAUDE.md", "README.md", "SKILL.md", "AGENTS.md", "PRD.md", "GOAL.md",
    "PLAN.md", "TODO.md", "INDEX.md", "CHANGELOG.md", "ROADMAP.md",
    "template.md", "MISTAKES.md", "notes.md", "A.md", "a.md", "b.md", "2.md",
}
REF = re.compile(r"((?:[A-Za-z0-9_\-]+[/\\])*[A-Za-z0-9_\-]+\.md)")


def scan(root: Path) -> list[str]:
    bad: list[str] = []
    for p in sorted(root.rglob("*.md")):
        for m in REF.finditer(p.read_text(encoding="utf-8")):
            ref = m.group(1).replace("\\", "/")
            if Path(ref).name in SKIP:
                continue
            cands = [p.parent / ref, root / ref, root / "references" / Path(ref).name]
            if not any(c.exists() for c in cands):
                bad.append(f"{p.relative_to(root)} -> {ref}")
    return sorted(set(bad))


def main(argv: list[str]) -> int:
    root = Path(argv[0]) if argv else Path("skills/project-evo")
    if not root.is_dir():
        print(f"md-ref-scan: 目录不存在 {root}", file=sys.stderr)
        return 2
    bad = scan(root)
    if bad:
        print(f"断链 {len(bad)} 处:", file=sys.stderr)
        for b in bad:
            print(f"  {b}", file=sys.stderr)
        return 1
    print("断链 0:skills 树交叉引用全部可达")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
