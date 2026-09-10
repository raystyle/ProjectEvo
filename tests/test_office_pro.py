"""office-pro: SKILL 面、which.py 定位、smoke.py 可选（无二进制 exit 2）。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "project-evo"
SKILL = PLUGIN / "skills" / "office-pro"
SCRIPTS = SKILL / "scripts"


def test_skill_layout():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---")
    fm = text.split("---", 2)[1]
    assert "name: office-pro" in fm
    assert "version:" not in fm
    assert len(text.splitlines()) <= 500
    for name in ("install.md", "cli.md", "edit.md", "facts.md", "README.md"):
        assert (SKILL / "references" / name).is_file(), name
    assert (SKILL / "verification" / "smoke.md").is_file()
    assert (PLUGIN / "commands" / "office-cli.md").is_file()


def test_which_and_optional_smoke():
    which = subprocess.run(
        [sys.executable, str(SCRIPTS / "which.py")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    assert which.returncode in (0, 2), which.stderr
    smoke = subprocess.run(
        [sys.executable, str(SCRIPTS / "smoke.py")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    if which.returncode == 2:
        assert smoke.returncode == 2
        return
    assert smoke.returncode == 0, smoke.stdout + smoke.stderr
    assert "PASS" in smoke.stdout
