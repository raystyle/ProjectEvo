# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""打印 OfficeCLI 绝对路径与 --version。退出 0 找到 / 2 未找到。"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def resolve() -> Path | None:
    env = os.environ.get("OFFICECLI_BIN")
    if env:
        p = Path(env)
        if p.is_file():
            return p
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "OfficeCLI" / "officecli.exe"
    if local.is_file():
        return local
    found = shutil.which("officecli")
    return Path(found) if found else None


def main() -> int:
    bin_path = resolve()
    if bin_path is None:
        print("officecli not found", file=sys.stderr)
        return 2
    env = os.environ.copy()
    env["OFFICECLI_SKIP_UPDATE"] = "1"
    r = subprocess.run(
        [str(bin_path), "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    ver = (r.stdout or r.stderr or "").strip().splitlines()
    print(f"{bin_path}\t{ver[0] if ver else 'unknown'}")
    return 0 if r.returncode == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
