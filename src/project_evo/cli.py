"""project-evo CLI:init / check / skill / llms。

只针对项目目录做三件事:文档结构安装(init)、诊断(check)、项目级 SKILL 安装(skill)。
退出码:0 成功 / 1 诊断发现违规 / 2 出错(错误走 stderr)。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from . import __version__
from .checker import check
from .scaffold import generate
from .update import DEFAULT_REPO, run_update

DATA = Path(__file__).parent / "data"

LLMS = f"""project-evo v{__version__} — 项目进化:项目目录的文档结构安装、诊断与项目级 SKILL 安装
project-evo init <path> [--name 名]    安装文档骨架(已有文件跳过不覆盖,幂等)
project-evo check [path]               诊断骨架合规 PE-01 至 PE-13(只读)
project-evo skill <path>               项目级安装 SKILL 到 .claude/skills/ 与 .agents/skills/ 双落位(重装即更新;agent 目录按惯例 gitignore)
project-evo update [-y] [--repo o/r]    升级(git 模式 ff-only pull;安装态默认 uv tool install git+ 源,PEVO_INDEX=1 走包索引;版本探测离线容错)
project-evo llms                       本索引
退出码: 0 成功 / 1 诊断发现违规 / 2 出错(stderr)
骨架面: AGENTS/CLAUDE/PRD/GOAL/PLAN/TODO/INDEX + CHANGELOG/ROADMAP + docs 六目录 + guide/template + G001
诊断面: 原语齐全/目录齐全/模板在位/CLAUDE 单行/命名规范/P 四位/INDEX 登记/义务表/PRD-GOAL 互指/六态/标题括号/emoji/断链
安装面: 内嵌 skill 全树(SKILL.md + references 17 篇 + verification),双漂移守卫与仓内源一致
"""


def _cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    if not target.is_dir():
        print(f"error: 目标目录不存在: {target}", file=sys.stderr)
        return 2
    created, skipped = generate(target, args.name)
    for rel in created:
        print(f"created  {rel}")
    for rel in skipped:
        print(f"skip     {rel} (已存在,不覆盖)")
    print(f"共新建 {len(created)} 件,跳过 {len(skipped)} 件;下一步:填 AGENTS 定位段 + GOAL 起点回指 D01")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve() if args.path else Path.cwd()
    if not root.is_dir():
        print(f"error: 目标目录不存在: {root}", file=sys.stderr)
        return 2
    results, ok = check(root)
    for pid, status, note in results:
        print(f"{status:<5} {pid}  {note}".rstrip())
    print(f"{'合规: 全部通过' if ok else '不合规: 存在 FAIL'}(PASS {sum(1 for _, s, _ in results if s == 'PASS')}"
          f" / FAIL {sum(1 for _, s, _ in results if s == 'FAIL')}"
          f" / SKIP {sum(1 for _, s, _ in results if s == 'SKIP')})")
    return 0 if ok else 1


def _cmd_skill(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    if not target.is_dir():
        print(f"error: 目标目录不存在: {target}", file=sys.stderr)
        return 2
    src = DATA / "skill"
    if not src.is_dir():
        print("error: 内嵌 skill 树缺失", file=sys.stderr)
        return 2
    # 双落位:Claude Code 约定目录 + 通用 Agent 共享目录(ohmyagents 惯例)
    dests = [
        target / ".claude" / "skills" / "project-evo",
        target / ".agents" / "skills" / "project-evo",
    ]
    n = 0
    for dest in dests:
        shutil.copytree(src, dest, dirs_exist_ok=True)  # 重装即更新(骨架是用户资产不覆盖;skill 是工具资产同步最新)
        n = sum(1 for p in dest.rglob("*") if p.is_file())
        print(f"installed  {dest.relative_to(target)} ({n} 件;重装即更新)")
    # agent 目录按惯例 gitignore(ohmypwsh/ohmyagents 同款)
    gi = target / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    added = [d for d in (".claude/", ".agents/") if d not in text]
    if added:
        entry = "# agent 运行时目录(project-evo skill 安装位)\n" + "".join(f"{d}\n" for d in added)
        gi.write_text(text.rstrip("\n") + ("\n" if text else "") + entry, encoding="utf-8")
        print("gitignore +" + " +".join(added) + "  (agent 目录不入库惯例;需要入库自行删行)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="project-evo", description="项目进化:文档结构安装、诊断与项目级 SKILL 安装"
    )
    parser.add_argument("--version", action="version", version=f"project-evo {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="安装文档骨架(幂等,不覆盖已有)")
    p_init.add_argument("path", help="目标项目根目录")
    p_init.add_argument("--name", default="<项目名>", help="项目名(填入 AGENTS 标题)")
    p_init.set_defaults(func=_cmd_init)

    p_check = sub.add_parser("check", help="诊断骨架合规(只读;退出码 0/1/2)")
    p_check.add_argument("path", nargs="?", help="目标项目根目录(默认当前目录)")
    p_check.set_defaults(func=_cmd_check)

    p_skill = sub.add_parser("skill", help="项目级安装 SKILL:Claude 目录 + 通用 Agent 目录双落位(重装即更新)")
    p_skill.add_argument("path", help="目标项目根目录")
    p_skill.set_defaults(func=_cmd_skill)

    p_upd = sub.add_parser("update", help="升级到最新版(git 模式干净仓 ff-only;安装态 uv tool;--repo 覆盖目标仓库)")
    p_upd.add_argument("-y", action="store_true", help="免确认(agents 传)")
    p_upd.add_argument("--repo", default=None, help="GitHub 仓库 owner/repo(默认 PEVO_REPO 环境变量)")
    p_upd.set_defaults(func=lambda a: run_update(yes=a.y, repo=a.repo or DEFAULT_REPO))

    p_llms = sub.add_parser("llms", help="输出紧凑命令索引")
    p_llms.set_defaults(func=lambda a: (print(LLMS, end=""), 0)[1])

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
