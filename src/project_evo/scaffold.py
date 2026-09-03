"""init 子命令:向目标项目安装文档骨架。

模板外置于 data/templates/(markdown 文件,受 md 标准与 mdfix 管辖);此处只做装载与变量渲染。
纪律:已有文件一律跳过不覆盖(幂等);每份文件带真实初始内容,不产空壳。
"""

from __future__ import annotations

import datetime
from pathlib import Path

DIRS = [
    "docs/proven",
    "docs/diary",
    "docs/research",
    "docs/references",
    "docs/guide",
    "docs/mistakes",
    "poc",
]

TEMPLATES = Path(__file__).parent / "data" / "templates"


def template_files() -> dict[str, str]:
    return {
        p.relative_to(TEMPLATES).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(TEMPLATES.rglob("*.md"))
    }


def generate(target: Path, name: str) -> tuple[list[str], list[str]]:
    """在 target 下生成骨架。返回 (created, skipped) 相对路径列表。幂等:已有文件跳过。"""
    date = datetime.date.today().isoformat()
    created: list[str] = []
    skipped: list[str] = []
    for d in DIRS:
        (target / d).mkdir(parents=True, exist_ok=True)
    for rel, tpl in template_files().items():
        path = target / rel
        if path.exists():
            skipped.append(rel)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(tpl.format(name=name, date=date), encoding="utf-8")
        created.append(rel)
    return created, skipped
