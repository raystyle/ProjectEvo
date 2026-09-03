"""project-evo 测试:脚手架幂等、检查器抓违、llms 版本、SKILL 双漂移守卫。"""

from __future__ import annotations

from pathlib import Path

import pytest

from project_evo import __version__
from project_evo.checker import check
from project_evo.cli import LLMS, main
from project_evo.scaffold import generate


def test_scaffold_creates_and_idempotent(tmp_path: Path):
    created, skipped = generate(tmp_path, "demo")
    assert len(created) >= 11, "骨架文件不少于 11 件"
    assert (tmp_path / "PRD.md").exists()
    assert (tmp_path / "docs" / "guide" / "template.md").exists()
    assert "D01" in (tmp_path / "PRD.md").read_text(encoding="utf-8"), "PRD 带真实初始内容"
    # 幂等:二次生成全跳过,内容不变
    before = (tmp_path / "PRD.md").read_text(encoding="utf-8")
    created2, skipped2 = generate(tmp_path, "demo")
    assert not created2 and len(skipped2) == len(created)
    assert (tmp_path / "PRD.md").read_text(encoding="utf-8") == before, "已有文件不被覆盖"


def test_check_passes_on_scaffold(tmp_path: Path):
    generate(tmp_path, "demo")
    results, ok = check(tmp_path)
    assert ok, [r for r in results if r[1] == "FAIL"]
    fails = [r for r in results if r[1] == "FAIL"]
    assert not fails


def test_check_catches_violations(tmp_path: Path):
    generate(tmp_path, "demo")
    (tmp_path / "INDEX.md").unlink()  # 抽走索引:PE-01? 不,PE-01 是六原语含 INDEX
    results, ok = check(tmp_path)
    assert not ok
    ids = {r[0] for r in results if r[1] == "FAIL"}
    assert "PE-01" in ids, "缺 INDEX 应被 PE-01 抓住"


def test_check_title_bracket(tmp_path: Path):
    generate(tmp_path, "demo")
    (tmp_path / "docs" / "guide" / "G001-文档标准细则.md").write_text(
        "# G001:文档标准细则\n\n## 一、命名(详版)\n", encoding="utf-8"
    )
    _, ok = check(tmp_path)
    assert not ok, "标题带括号应被 PE-11 抓住"


def test_llms_has_version():
    assert __version__ in LLMS
    assert "init" in LLMS and "check" in LLMS


def test_skill_drift_guard():
    """双漂移守卫:内嵌 skill 全树与仓内 skills/project-evo/ 逐文件一致。"""
    repo = Path(__file__).resolve().parents[1] / "skills" / "project-evo"
    embedded = Path(__file__).resolve().parents[1] / "src" / "project_evo" / "data" / "skill"
    if not (repo.is_dir() and embedded.is_dir()):
        pytest.skip("非仓内运行(安装态),跳过漂移守卫")
    repo_files = {p.relative_to(repo).as_posix(): p.read_text(encoding="utf-8") for p in repo.rglob("*") if p.is_file()}
    emb_files = {p.relative_to(embedded).as_posix(): p.read_text(encoding="utf-8") for p in embedded.rglob("*") if p.is_file()}
    assert set(repo_files) == set(emb_files), f"文件集漂移: 仅仓内 {set(repo_files) - set(emb_files)} / 仅内嵌 {set(emb_files) - set(repo_files)}"
    diff = [k for k in repo_files if repo_files[k] != emb_files[k]]
    assert not diff, f"内容漂移: {diff};须同步 src/project_evo/data/skill/ 与 skills/project-evo/"


def test_skill_install_project_scope(tmp_path: Path):
    generate(tmp_path, "demo")
    assert main(["skill", str(tmp_path)]) == 0
    for dest in (tmp_path / ".claude" / "skills" / "project-evo", tmp_path / ".agents" / "skills" / "project-evo"):
        assert (dest / "SKILL.md").exists(), f"{dest} 应随装"
        assert any(dest.rglob("base-primitives.md")), "references 全树随装"
    gi = (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert ".claude/" in gi and ".agents/" in gi, "双 agent 目录按惯例 gitignore"
    # 重装即更新(不报错、不重复追加 gitignore)
    assert main(["skill", str(tmp_path)]) == 0
    gi2 = (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert gi2.count(".claude/") == 1 and gi2.count(".agents/") == 1


def test_check_ignores_fenced_code_comments(tmp_path: Path):
    """代码块内的 # 注释带括号不算标题违规(PE-11 围栏感知)。"""
    generate(tmp_path, "demo")
    gi = tmp_path / "docs" / "guide" / "G001-文档标准细则.md"
    gi.write_text(
        "# G001:文档标准细则\n\n## 命名\n\n```powershell\n"
        "# 1. 看 skill 本体(意图路由入口)\nGet-Content SKILL.md\n```\n",
        encoding="utf-8",
    )
    _, ok = check(tmp_path)
    assert ok, "围栏内 # 注释不应触发 PE-11"


def test_version_tuple_ordering():
    from project_evo.update import version_tuple as vt
    assert vt("0.2.0") > vt("0.1.0")
    assert vt("v0.1.1") > vt("0.1.0")
    assert vt("0.1.0") > vt("0.1.0rc1") > vt("0.1.0b2") > vt("0.1.0a1")
    assert vt("垃圾") == (0, 0, 0, 0, 0)


def test_latest_release_offline_returns_none(monkeypatch):
    from project_evo import update
    monkeypatch.setattr(update, "latest_release_tag", lambda repo, timeout=6.0: None)
    cur, latest, newer = update.check_for_update("x/y")
    assert cur == __version__ and latest is None and newer is False


def _git(cwd: Path, *args: str) -> None:
    import subprocess
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True,
                   env={**__import__("os").environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def test_scan_finds_secret_in_history(tmp_path: Path):
    from project_evo.scanner import run_scan, scan_history_secrets
    _git(tmp_path, "init", "-b", "main")
    (tmp_path / "cfg.txt").write_text("token = ghp_0123456789abcdefghijklmnop\n", encoding="utf-8")
    _git(tmp_path, "add", "-A"); _git(tmp_path, "commit", "-m", "leak")
    (tmp_path / "cfg.txt").unlink()
    _git(tmp_path, "add", "-A"); _git(tmp_path, "commit", "-m", "remove")
    finds = scan_history_secrets(tmp_path)
    assert any(f["rule"] == "GitHub token" for f in finds), "历史中的 token 应被抓到"
    _, clean = run_scan(tmp_path)
    assert not clean
    # 报告脱敏:不回显完整 token
    joined = " ".join(f["snippet"] for f in finds)
    assert "ghp_0123456789abcdefghijklmnop" not in joined


def test_scan_md_reports_file_and_line(tmp_path: Path):
    from project_evo.scanner import run_scan
    (tmp_path / "A.md").write_text(
        "# 标题\n\n规则:登记到立项——执行“完”\n\n```text\n# 注释(豁免)—— →\n```\n",
        encoding="utf-8",
    )
    finds, clean = run_scan(tmp_path, history=False)
    assert not clean
    md = [f for f in finds if f["kind"] == "md"]
    assert md and md[0]["file"] == "A.md" and md[0]["line"] == 3, "标注文件与行号"
    assert any("破折号" in f["rule"] for f in md) and any("智能引号" in f["rule"] for f in md)
    assert all(f["line"] != 6 for f in md), "围栏内豁免"


def test_cli_check_exit_codes(tmp_path: Path, capsys):
    generate(tmp_path, "demo")
    assert main(["check", str(tmp_path)]) == 0
    (tmp_path / "PRD.md").unlink()
    assert main(["check", str(tmp_path)]) == 1
