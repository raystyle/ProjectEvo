# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""init:向目标项目安装文档骨架(幂等,不覆盖已有)。

用法: uv run init.py <目标项目> [--name 项目名]
模板外置于同 skill 的 ../assets/templates/(markdown,受写作规范管辖);此处只做装载与变量渲染。
纪律:已有文件一律跳过不覆盖(幂等);每份文件带真实初始内容,不产空壳;目标目录不存在则创建(脚手架语义,二犯升格)。
退出码: 0 成功 / 2 出错(错误走 stderr)。
"""

from __future__ import annotations

import argparse
import datetime
import sys
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

TEMPLATES = Path(__file__).resolve().parent.parent / "assets" / "templates"


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


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if stream.encoding and stream.encoding.lower().replace("-", "") != "utf8":
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="init.py", description="安装文档骨架(幂等,不覆盖已有)")
    parser.add_argument("path", help="目标项目根目录")
    parser.add_argument("--name", default="<项目名>", help="项目名(填入 AGENTS 标题)")
    args = parser.parse_args(argv)

    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)  # 脚手架语义:目标项目目录不存在则创建(同日两犯升格)
    created, skipped = generate(target, args.name)
    for rel in created:
        print(f"created  {rel}")
    for rel in skipped:
        print(f"skip     {rel}(已存在,不覆盖)")
    print(f"共新建 {len(created)} 件,跳过 {len(skipped)} 件;下一步:填 AGENTS 定位段 + GOAL 起点回指 D01")
    return 0


if __name__ == "__main__":
    sys.exit(main())
