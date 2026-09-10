"""project-evo 脚本与插件面测试。

脚本为 PEP 723 零依赖形态,从 plugins/ 树按文件路径加载(无安装态包,单源无副本)。
覆盖:init 幂等、check 抓违(PE-01/PE-11/围栏感知)、scan 历史泄漏与 md 告警、
退出码、市场清单与双 manifest 一致性守卫(改一面须同步另一面)。
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "project-evo"
SCRIPTS = PLUGIN / "skills" / "docs-evo" / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"pevo_{name}", SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


init_mod = _load("init")
check_mod = _load("check")
scan_mod = _load("scan")


def test_scaffold_creates_and_idempotent(tmp_path: Path):
    created, skipped = init_mod.generate(tmp_path, "demo")
    assert len(created) >= 11, "骨架文件不少于 11 件"
    assert (tmp_path / "PRD.md").exists()
    assert (tmp_path / "docs" / "guide" / "template.md").exists()
    assert "D01" in (tmp_path / "PRD.md").read_text(encoding="utf-8"), "PRD 带真实初始内容"
    # 幂等:二次生成全跳过,内容不变
    before = (tmp_path / "PRD.md").read_text(encoding="utf-8")
    created2, skipped2 = init_mod.generate(tmp_path, "demo")
    assert not created2 and len(skipped2) == len(created)
    assert (tmp_path / "PRD.md").read_text(encoding="utf-8") == before, "已有文件不被覆盖"


def test_check_passes_on_scaffold(tmp_path: Path):
    init_mod.generate(tmp_path, "demo")
    results, ok = check_mod.check(tmp_path)
    assert ok, [r for r in results if r[1] == "FAIL"]


def test_check_catches_violations(tmp_path: Path):
    init_mod.generate(tmp_path, "demo")
    (tmp_path / "INDEX.md").unlink()  # PE-01 是六原语含 INDEX
    results, ok = check_mod.check(tmp_path)
    assert not ok
    assert "PE-01" in {r[0] for r in results if r[1] == "FAIL"}, "缺 INDEX 应被 PE-01 抓住"


def test_check_title_bracket(tmp_path: Path):
    init_mod.generate(tmp_path, "demo")
    (tmp_path / "docs" / "guide" / "G001-文档标准细则.md").write_text(
        "# G001:文档标准细则\n\n## 一、命名(详版)\n", encoding="utf-8"
    )
    _, ok = check_mod.check(tmp_path)
    assert not ok, "标题带括号应被 PE-11 抓住"


def test_check_ignores_fenced_code_comments(tmp_path: Path):
    """代码块内的 # 注释带括号不算标题违规(PE-11 围栏感知)。"""
    init_mod.generate(tmp_path, "demo")
    (tmp_path / "docs" / "guide" / "G001-文档标准细则.md").write_text(
        "# G001:文档标准细则\n\n## 命名\n\n```powershell\n"
        "# 1. 看 skill 本体(意图路由入口)\nGet-Content SKILL.md\n```\n",
        encoding="utf-8",
    )
    _, ok = check_mod.check(tmp_path)
    assert ok, "围栏内 # 注释不应触发 PE-11"


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True,
                   env={**__import__("os").environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def test_scan_finds_secret_in_history(tmp_path: Path):
    _git(tmp_path, "init", "-b", "main")
    (tmp_path / "cfg.txt").write_text("token = ghp_0123456789abcdefghijklmnop\n", encoding="utf-8")
    _git(tmp_path, "add", "-A"); _git(tmp_path, "commit", "-m", "leak")
    (tmp_path / "cfg.txt").unlink()
    _git(tmp_path, "add", "-A"); _git(tmp_path, "commit", "-m", "remove")
    finds = scan_mod.scan_history_secrets(tmp_path)
    assert any(f["rule"] == "GitHub token" for f in finds), "历史中的 token 应被抓到"
    _, clean = scan_mod.run_scan(tmp_path)
    assert not clean
    # 报告脱敏:不回显完整 token
    joined = " ".join(f["snippet"] for f in finds)
    assert "ghp_0123456789abcdefghijklmnop" not in joined


def test_scan_md_reports_file_and_line(tmp_path: Path):
    (tmp_path / "A.md").write_text(
        "# 标题\n\n规则:登记到立项——执行“完”\n\n```text\n# 注释(豁免)—— →\n```\n",
        encoding="utf-8",
    )
    finds, clean = scan_mod.run_scan(tmp_path, history=False)
    assert not clean
    md = [f for f in finds if f["kind"] == "md"]
    assert md and md[0]["file"] == "A.md" and md[0]["line"] == 3, "标注文件与行号"
    assert any("破折号" in f["rule"] for f in md) and any("智能引号" in f["rule"] for f in md)
    assert all(f["line"] != 6 for f in md), "围栏内豁免"


def test_init_creates_missing_target(tmp_path: Path):
    """脚手架语义:目标目录不存在则创建(同日两犯升格:本地 e2e 与 CI 冒烟各踩一次)。"""
    target = tmp_path / "nested" / "demo"
    r = subprocess.run([sys.executable, str(SCRIPTS / "init.py"), str(target), "--name", "demo"],
                       capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    assert (target / "PRD.md").is_file()


def test_check_script_exit_codes(tmp_path: Path):
    """子进程直跑:PEP 723 零依赖,系统 python 即可;退出码 0/1。"""
    init_mod.generate(tmp_path, "demo")
    r_ok = subprocess.run([sys.executable, str(SCRIPTS / "check.py"), str(tmp_path)],
                          capture_output=True, text=True, encoding="utf-8")
    assert r_ok.returncode == 0, r_ok.stdout + r_ok.stderr
    (tmp_path / "PRD.md").unlink()
    r_bad = subprocess.run([sys.executable, str(SCRIPTS / "check.py"), str(tmp_path)],
                           capture_output=True, text=True, encoding="utf-8")
    assert r_bad.returncode == 1


def test_marketplace_catalog_consistency():
    """清单守卫:市场只收一个插件、双清单一致、双 manifest 与市场版本同步、四 skill 与命令面在位。"""
    claude_mkt = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    codex_mkt = json.loads((REPO / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    claude_man = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    codex_man = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))

    names_c = {p["name"] for p in claude_mkt["plugins"]}
    names_x = {p["name"] for p in codex_mkt["plugins"]}
    assert names_c == names_x == {"project-evo"}, "市场只收一个插件 project-evo(四 skill 同装同版)"
    for p in claude_mkt["plugins"]:
        assert (REPO / p["source"].removeprefix("./")).is_dir(), f"Claude source 不可达: {p['source']}"
    for p in codex_mkt["plugins"]:
        assert (REPO / p["source"]["path"].removeprefix("./")).is_dir(), "Codex source 不可达"

    for k in ("name", "version", "description"):
        assert claude_man[k] == codex_man[k], f"{k} 双 manifest 漂移,须同步改两面"
    entry = next(p for p in claude_mkt["plugins"] if p["name"] == "project-evo")
    assert entry["version"] == claude_man["version"], "市场清单版本与 manifest 漂移"

    skills = PLUGIN / "skills"
    dirs = sorted(d.name for d in skills.iterdir() if d.is_dir())
    assert dirs == ["docs-evo", "office-pro", "secret-scan", "super-research"], f"四 skill 须齐备: {dirs}"
    for name in dirs:
        text = (skills / name / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---\n"), f"{name}/SKILL.md 缺 frontmatter"
        head = text.split("---")[1]
        declared = next(l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("name:"))
        assert declared == name, f"frontmatter name({declared}) 须与目录名({name})一致"

    docs = skills / "docs-evo"
    assert (docs / "references").is_dir() and (docs / "assets" / "templates").is_dir()
    for s in ("init.py", "check.py", "scan.py", "mdrules.py", "md-guard.py"):
        assert (docs / "scripts" / s).is_file(), f"脚本缺失: {s}"
    for name in dirs:
        assert (skills / name / "references").is_dir(), f"参考目录缺失: {name}"
    assert (skills / "secret-scan" / "scripts" / "scan.py").is_file()
    assert (skills / "secret-scan" / "scripts" / "ab.py").is_file()
    assert (skills / "office-pro" / "scripts" / "which.py").is_file()
    assert (skills / "office-pro" / "scripts" / "smoke.py").is_file()
    for c in ("init.md", "check.md", "scan.md", "secret-scan-cli.md", "office-cli.md"):
        assert (PLUGIN / "commands" / c).is_file(), f"斜杠命令缺失: {c}"
    json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8")), "hooks.json 须为合法 JSON"


def _run_md_guard(payload: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "md-guard.py")],
        input=payload, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=env,
    )


def test_md_guard_hook_tolerates_alien_payload(tmp_path: Path):
    """Codex apply_patch 面载荷宽容:tool_input 是对象但无 file_path,或整体不是对象,均放行 0。"""
    codex_shape = json.dumps({
        "hook_event_name": "PostToolUse",
        "tool_name": "apply_patch",
        "tool_input": {"command": "*** Begin Patch\n*** Update File: note.md\n+x\n*** End Patch\n"},
        "tool_response": "Success. Updated files.",
    })
    assert _run_md_guard(codex_shape).returncode == 0
    alien_shape = json.dumps({"hook_event_name": "PostToolUse", "tool_input": "*** Begin Patch"})
    assert _run_md_guard(alien_shape).returncode == 0
    assert _run_md_guard("not json at all").returncode == 0


def test_md_guard_hook_flags_forbidden_chars(tmp_path: Path):
    """Claude 面判据不回退:file_path 指向含禁字的 .md 时退出 2 并写 stderr。"""
    bad = tmp_path / "bad.md"
    bad.write_text("正常一行\n带破折号 \u2014 的一行\n", encoding="utf-8")
    bad_payload = json.dumps({"hook_event_name": "PostToolUse", "tool_input": {"file_path": str(bad)}})
    r = _run_md_guard(bad_payload)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "禁字" in r.stderr
    clean = tmp_path / "ok.md"
    clean.write_text("干净一行\n", encoding="utf-8")
    ok_payload = json.dumps({"hook_event_name": "PostToolUse", "tool_input": {"file_path": str(clean)}})
    assert _run_md_guard(ok_payload).returncode == 0


def test_plugin_hooks_use_braced_plugin_root():
    """hook 命令须写 ${CLAUDE_PLUGIN_ROOT}。

    Codex 只替换花括号形态(codex-rs/hooks/src/engine/discovery.rs: fold replace "${key}"),
    且在 Windows 用 cmd.exe /C 执行(command_runner.rs: COMSPEC 兜底 cmd.exe /C)。
    故裸 $VAR 与 PowerShell 的 $env: 在 Windows 面都不展开,脚本路径必失效。
    """
    hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    handlers = [h for g in hooks["hooks"]["PostToolUse"] for h in g["hooks"]]
    assert handlers, "hooks.json 须有 PostToolUse 处理器"
    for h in handlers:
        for field in ("command", "commandWindows"):
            cmd = h.get(field)
            assert cmd, f"hooks.json 缺 {field}"
            assert "${CLAUDE_PLUGIN_ROOT}" in cmd, f"{field} 须用花括号形态(Codex 只替换 ${{VAR}})"
            assert "$env:" not in cmd, f"{field} 禁 PowerShell 语法:Windows 走 cmd.exe /C"
