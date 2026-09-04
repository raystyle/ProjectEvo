"""回归测试(集成约束形态四):仓内 markdown 四类禁字清零常驻回归。

来历:第十六/十七批新增文本连犯破折号禁字(各被 scan 当场抓住),按「二犯升格 +
集成约束」裁定(2026-09-04)转为 CI 常驻回归用例;规则同源 project_evo.mdfix。
"""

from pathlib import Path

import pytest

from project_evo.mdfix import SKIP_DIRS, file_violations


def test_repo_markdown_clean():
    repo = Path(__file__).resolve().parent.parent
    if not (repo / "skills" / "project-evo").is_dir():
        pytest.skip("非仓内运行(安装态),跳过")
    bad: list[str] = []
    for p in sorted(repo.rglob("*.md")):
        rel = p.relative_to(repo).parts
        if any(part in SKIP_DIRS or part.startswith(".git") for part in rel):
            continue
        for line, cats in file_violations(p.read_text(encoding="utf-8")).items():
            bad.append(f"{p.relative_to(repo).as_posix()}:{line} {'、'.join(cats)}")
    assert not bad, "markdown 禁字回归失败(集成约束形态四): " + "; ".join(bad[:10])
