# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""三类文件 create/add/set/view/get/validate/close。缺二进制退出 2。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from which import resolve  # noqa: E402


def run(bin_path: Path, cwd: Path, oc_args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["OFFICECLI_SKIP_UPDATE"] = "1"
    return subprocess.run(
        [str(bin_path), *oc_args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


def main() -> int:
    bin_path = resolve()
    if bin_path is None:
        print("SKIP: officecli not found", file=sys.stderr)
        return 2
    work = Path(tempfile.mkdtemp(prefix="pevo-office-pro-smoke-"))
    fails: list[str] = []

    def check(title: str, oc_args: list[str], expect_code: int = 0) -> str:
        r = run(bin_path, work, oc_args)
        if r.returncode != expect_code:
            fails.append(f"{title} exit {r.returncode} want {expect_code}")
        return r.stdout or ""

    check("create pptx", ["create", "deck.pptx"])
    check("add slide", ["add", "deck.pptx", "/", "--type", "slide", "--prop", "title=Hello Agent"])
    check("view outline", ["view", "deck.pptx", "outline"])
    out = check("get json", ["get", "deck.pptx", "/slide[1]", "--json", "--depth", "1"])
    try:
        if not json.loads(out, strict=False).get("success"):
            fails.append("pptx get success false")
    except json.JSONDecodeError:
        fails.append("pptx get not json")
    check("validate pptx", ["validate", "deck.pptx"])
    check("close pptx", ["close", "deck.pptx"])

    check("create docx", ["create", "report.docx"])
    check(
        "add p",
        ["add", "report.docx", "/body", "--type", "paragraph", "--prop", "text=smoke"],
    )
    check("validate docx", ["validate", "report.docx"])
    check("close docx", ["close", "report.docx"])

    check("create xlsx", ["create", "data.xlsx"])
    check("set B1", ["set", "data.xlsx", "/Sheet1/B1", "--prop", "value=10"])
    check("set B2", ["set", "data.xlsx", "/Sheet1/B2", "--prop", "formula=SUM(B1,5)"])
    out = check("get B2", ["get", "data.xlsx", "/Sheet1/B2", "--json"])
    try:
        data = json.loads(out, strict=False)
        cv = ((data.get("data") or {}).get("results") or [{}])[0].get("format", {}).get(
            "computedValue"
        )
        if str(cv) != "15":
            fails.append(f"xlsx computedValue {cv!r}")
    except json.JSONDecodeError:
        fails.append("xlsx get not json")
    check("validate xlsx", ["validate", "data.xlsx"])
    check("close xlsx", ["close", "data.xlsx"])

    check("bad path", ["get", "deck.pptx", "/slide[99]", "--json"], expect_code=1)

    if fails:
        print("FAIL")
        for f in fails:
            print(f)
        return 1
    print(f"PASS {work}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
