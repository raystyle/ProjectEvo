"""project-evo CLI:init / check / scan / skill / update / llms。

针对项目目录:结构安装、合规诊断、安全与规范扫描(只告警标注文件与行号)、项目级 SKILL 安装、自升级。
退出码:0 成功 / 1 诊断或扫描有发现 / 2 出错(错误走 stderr)。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from . import __version__
from .checker import check
from .scanner import run_scan
from .scaffold import generate
from .update import DEFAULT_REPO, run_update

DATA = Path(__file__).parent / "data"

LLMS = f"""project-evo v{__version__} — 项目进化:结构安装、诊断、安全扫描与 SKILL 安装
project-evo init <path> [--name 名]    安装文档骨架(已有文件跳过不覆盖,幂等)
project-evo check [path]               诊断骨架合规 PE-01 至 PE-13(只读)
project-evo scan [path] [--no-history] 安全与规范扫描:token/密钥/隐私(工作区+git 全历史)+ markdown 禁字,告警提示修改
project-evo skill <path>               项目级安装 SKILL 到 .claude/skills/ 与 .agents/skills/ 双落位(重装即更新)
project-evo update [-y] [--repo o/r]   升级(git 模式 ff-only pull;安装态默认 uv tool install git+ 源)
project-evo llms                       本索引
白名单: PEVO_SCAN_ALLOW="正则;正则" 豁免测试夹具等已知项(匹配 文件:行 规则)
退出码: 0 成功 / 1 诊断或扫描有发现 / 2 出错(stderr)
"""


def _target(path: str | None) -> Path:
    p = (Path(path).resolve() if path else Path.cwd())
    if not p.is_dir():
        print(f"error: 目标目录不存在:{p}", file=sys.stderr)
        raise SystemExit(2)
    return p


def _cmd_init(args: argparse.Namespace) -> int:
    target = _target(args.path)
    created, skipped = generate(target, args.name)
    for rel in created:
        print(f"created  {rel}")
    for rel in skipped:
        print(f"skip     {rel}(已存在,不覆盖)")
    print(f"共新建 {len(created)} 件,跳过 {len(skipped)} 件;下一步:填 AGENTS 定位段 + GOAL 起点回指 D01")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    root = _target(args.path)
    results, ok = check(root)
    for pid, status, note in results:
        print(f"{status:<5} {pid}  {note}".rstrip())
    print(f"{'合规: 全部通过' if ok else '不合规: 存在 FAIL'}(PASS {sum(1 for _, s, _ in results if s == 'PASS')}"
          f" / FAIL {sum(1 for _, s, _ in results if s == 'FAIL')}"
          f" / SKIP {sum(1 for _, s, _ in results if s == 'SKIP')})")
    return 0 if ok else 1


def _cmd_scan(args: argparse.Namespace) -> int:
    root = _target(args.path)
    finds, clean = run_scan(root, history=not args.no_history)
    if clean:
        print("扫描干净:无 secrets、无 markdown 禁字")
        return 0
    for f in finds:
        loc = f"{f['file']}:{f['line']}" if f["line"] else f["file"]
        print(f"[{f['severity']:<4}] {f['kind']:<7} {f['rule']:<24} {loc:<40} @{f['commit']}  {f['snippet']}")
    high = sum(1 for f in finds if f["severity"] == "HIGH")
    md = sum(1 for f in finds if f["kind"] == "md")
    print(f"共 {len(finds)} 项发现(HIGH {high}):")
    if high:
        print("  高危:密钥疑似入库。轮换该凭据(视为已泄露),再用 git filter-repo / BFG 清史。")
    if md:
        print(f"  markdown 禁字 {md} 行:按告警逐行修正(破折号用冒号/括号/拆句,箭头改文字,中文语境转全角)。")
    return 1


def _cmd_skill(args: argparse.Namespace) -> int:
    target = _target(args.path)
    src = DATA / "skill"
    if not src.is_dir():
        print("error: 内嵌 skill 树缺失", file=sys.stderr)
        return 2
    dests = [
        target / ".claude" / "skills" / "project-evo",
        target / ".agents" / "skills" / "project-evo",
    ]
    n = 0
    for dest in dests:
        shutil.copytree(src, dest, dirs_exist_ok=True)
        n = sum(1 for p in dest.rglob("*") if p.is_file())
        print(f"installed  {dest.relative_to(target)}({n} 件;重装即更新)")
    gi = target / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    added = [d for d in (".claude/", ".agents/") if d not in text]
    if added:
        entry = "# agent 运行时目录(project-evo skill 安装位)\n" + "".join(f"{d}\n" for d in added)
        gi.write_text(text.rstrip("\n") + ("\n" if text else "") + entry, encoding="utf-8")
        print("gitignore +" + " +".join(added) + "(agent 目录不入库惯例;需要入库自行删行)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="project-evo", description="项目进化:结构安装、诊断、安全扫描与 SKILL 安装"
    )
    parser.add_argument("--version", action="version", version=f"project-evo {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="安装文档骨架(幂等,不覆盖已有)")
    p.add_argument("path")
    p.add_argument("--name", default="<项目名>", help="项目名(填入 AGENTS 标题)")
    p.set_defaults(func=_cmd_init)

    p = sub.add_parser("check", help="诊断骨架合规(只读;退出码 0/1/2)")
    p.add_argument("path", nargs="?", help="目标项目根目录(默认当前目录)")
    p.set_defaults(func=_cmd_check)

    p = sub.add_parser("scan", help="安全与规范扫描:secrets(工作区+git 历史)+ markdown 禁字,告警提示修改")
    p.add_argument("path", nargs="?")
    p.add_argument("--no-history", action="store_true", help="跳过 git 全历史扫描(只扫工作区)")
    p.set_defaults(func=_cmd_scan)

    p = sub.add_parser("skill", help="项目级安装 SKILL:Claude 目录 + 通用 Agent 目录双落位(重装即更新)")
    p.add_argument("path")
    p.set_defaults(func=_cmd_skill)

    p = sub.add_parser("update", help="升级到最新版(git 模式干净仓 ff-only;安装态 uv tool;--repo 覆盖目标仓库)")
    p.add_argument("-y", action="store_true", help="免确认(agents 传)")
    p.add_argument("--repo", default=None, help="GitHub 仓库 owner/repo")
    p.set_defaults(func=lambda a: run_update(yes=a.y, repo=a.repo or DEFAULT_REPO))

    p = sub.add_parser("llms", help="输出紧凑命令索引")
    p.set_defaults(func=lambda a: (print(LLMS, end=""), 0)[1])

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
