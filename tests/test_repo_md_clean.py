"""回归测试(集成约束形态四):仓内 markdown 四类禁字清零常驻回归。

来历:第十六/十七批新增文本连犯破折号禁字(各被 scan 当场抓住),按「二犯升格 +
集成约束」裁定(2026-09-04)转为 CI 常驻回归用例;规则同源 plugins 内 mdrules.py。
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
_MDRULES = REPO / "plugins" / "project-evo" / "skills" / "evo" / "scripts" / "mdrules.py"

_spec = importlib.util.spec_from_file_location("pevo_mdrules", _MDRULES)
mdrules = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mdrules)


def test_repo_markdown_clean():
    if not (REPO / "plugins" / "project-evo").is_dir():
        pytest.skip("非仓内运行(安装态),跳过")
    bad: list[str] = []
    for p in sorted(REPO.rglob("*.md")):
        rel = p.relative_to(REPO).parts
        if any(part in mdrules.SKIP_DIRS or part.startswith(".git") for part in rel):
            continue
        for line, cats in mdrules.file_violations(p.read_text(encoding="utf-8")).items():
            bad.append(f"{p.relative_to(REPO).as_posix()}:{line} {'、'.join(cats)}")
    assert not bad, "markdown 禁字回归失败(集成约束形态四): " + "; ".join(bad[:10])
