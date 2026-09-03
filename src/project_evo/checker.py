"""check 子命令:骨架合规检查(PE-01 至 PE-13 的 Python 实现)。

退出码:0 全部通过(含 SKIP)/ 1 存在 FAIL / 2 出错。检查只读,不改目标项目。
"""

from __future__ import annotations

import re
from pathlib import Path

from .mdfix import file_violations

ROOT_PRIMITIVES = ["AGENTS.md", "PRD.md", "GOAL.md", "PLAN.md", "TODO.md", "INDEX.md"]
DOC_DIRS = ["proven", "diary", "research", "references", "guide", "mistakes"]
_EMOJI = re.compile(
    "[☀-➿\U0001f000-\U0001faff✅⚠]"
)
_BAD_NAME = re.compile(r"[()\s:]")


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def check(root: Path) -> tuple[list[tuple[str, str, str]], bool]:
    """返回 (结果列表[(编号, 状态, 说明)], ok)。状态:PASS/FAIL/SKIP。"""
    r: list[tuple[str, str, str]] = []

    # PE-01 根六原语
    missing = [f for f in ROOT_PRIMITIVES if not (root / f).exists()]
    r.append(("PE-01", "FAIL" if missing else "PASS",
              f"缺失: {', '.join(missing)}" if missing else "根六原语齐全"))

    # PE-02 docs 六目录
    miss_dirs = [d for d in DOC_DIRS if not (root / "docs" / d).is_dir()]
    r.append(("PE-02", "FAIL" if miss_dirs else "PASS",
              f"缺失: {', '.join(miss_dirs)}" if miss_dirs else "docs 六目录齐全"))

    # PE-03 方案模板
    tpl = root / "docs" / "guide" / "template.md"
    r.append(("PE-03", "FAIL" if not tpl.exists() else "PASS",
              "" if tpl.exists() else "docs/guide/template.md 不存在"))

    # PE-04 CLAUDE.md 单行桥接(存在才查)
    claude = root / "CLAUDE.md"
    if not claude.exists():
        r.append(("PE-04", "SKIP", "CLAUDE.md 不存在"))
    else:
        lines = [ln for ln in _read(claude).splitlines() if ln.strip()]
        ok = len(lines) == 1 and lines[0].strip() == "@AGENTS.md"
        r.append(("PE-04", "PASS" if ok else "FAIL",
                  "" if ok else f"应仅一行 @AGENTS.md,实际 {len(lines)} 行"))

    # PE-05 编号文件名规范
    bad: list[str] = []
    if (root / "docs").is_dir():
        for p in (root / "docs").rglob("*.md"):
            if p.name == "template.md":
                continue
            if _BAD_NAME.search(p.name):
                bad.append(p.relative_to(root).as_posix())
    r.append(("PE-05", "FAIL" if bad else "PASS",
              f"命名含空格/括号/冒号: {', '.join(bad[:5])}" if bad else "编号文件名规范"))

    # PE-06 P 编号四位
    pbad = [p.name for p in (root / "docs" / "proven").glob("*.md")
            if not re.match(r"^P\d{4}-", p.name)] if (root / "docs" / "proven").is_dir() else []
    has_p = (root / "docs" / "proven").is_dir() and any((root / "docs" / "proven").glob("*.md"))
    r.append(("PE-06", "FAIL" if pbad else ("PASS" if has_p else "SKIP"),
              f"非 PNNNN 前缀: {', '.join(pbad)}" if pbad else ("P 编号四位" if has_p else "proven 空,跳过")))

    # PE-07 编号文档登记 INDEX
    index_text = _read(root / "INDEX.md")
    unreg: list[str] = []
    for sub in ("proven", "research", "references", "guide", "mistakes"):
        d = root / "docs" / sub
        if not d.is_dir():
            continue
        for p in d.glob("*.md"):
            if p.name == "template.md" or re.match(r"^\d{4}-\d{2}-\d{2}-", p.name):
                continue
            if index_text and p.name not in index_text:
                unreg.append(p.name)
    r.append(("PE-07", "FAIL" if unreg else "PASS",
              f"未登记 INDEX: {', '.join(unreg[:5])}" if unreg else "编号文档均已登记"))

    # PE-08 AGENTS 含义务表
    agents = _read(root / "AGENTS.md")
    r.append(("PE-08", "FAIL" if ("义务" not in agents) else "PASS",
              "" if "义务" in agents else "AGENTS 缺文档义务表"))

    # PE-09 PRD 与 GOAL 互指
    prd, goal = _read(root / "PRD.md"), _read(root / "GOAL.md")
    ok9 = ("D01" in prd) and (prd and goal)
    r.append(("PE-09", "FAIL" if not ok9 else "PASS",
              "" if ok9 else "PRD 未登记 D01 或 GOAL 缺失"))

    # PE-10 六态标记(research/proven 有文档时)
    mark = False
    has_docs = False
    for sub in ("research", "proven"):
        for p in (root / "docs" / sub).glob("*.md"):
            has_docs = True
            if re.search(r"\[(实证|推断|经验|记忆|假设|直觉)[:\]]", _read(p)):
                mark = True
    r.append(("PE-10", "PASS" if mark else ("SKIP" if not has_docs else "FAIL"),
              "" if mark or not has_docs else "research/proven 无六态标记"))

    # PE-11 标题禁括号(跳过围栏代码块内的 # 注释行)
    badh: list[str] = []
    cands11 = [root / f for f in (*ROOT_PRIMITIVES, "README.md")] + list((root / "docs").rglob("*.md"))
    for p in [p for p in cands11 if p.exists()]:
        in_fence = False
        for i, ln in enumerate(_read(p).splitlines(), 1):
            if ln.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence and ln.startswith("#") and "(" in ln:
                badh.append(f"{p.name}:{i}")
    r.append(("PE-11", "FAIL" if badh else "PASS",
              f"标题含括号: {', '.join(badh[:5])}" if badh else "标题无括号"))

    # PE-12 四类禁字(emoji/破折号/箭头/中文半角标点;豁免区感知,与 scan 同源)
    em: list[str] = []
    cands12 = [root / f for f in (*ROOT_PRIMITIVES, "README.md", "CHANGELOG.md", "ROADMAP.md")] + list((root / "docs").rglob("*.md"))
    for p in [p for p in cands12 if p.exists()]:
        v = file_violations(_read(p))
        if v:
            first = min(v)
            em.append(f"{p.name}:{first}({'+'.join(v[first])})")
    r.append(("PE-12", "FAIL" if em else "PASS",
              f"含禁字: {', '.join(em[:5])}" if em else "无四类禁字"))

    # PE-13 INDEX 反引号路径断链粗检
    dead: list[str] = []
    for m in re.finditer(r"`([\w\-\\/\.]+\.(?:md|py|rs|toml|ts))`", index_text):
        rel = m.group(1)
        if not (root / rel).exists():
            dead.append(rel)
    r.append(("PE-13", "FAIL" if dead else "PASS",
              f"INDEX 引用不存在: {', '.join(dead[:5])}" if dead else "INDEX 引用可达"))

    ok = all(s != "FAIL" for _, s, _ in r)
    return r, ok
