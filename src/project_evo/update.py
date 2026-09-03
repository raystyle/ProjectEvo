"""update 子命令:参考 browser-harness 的部署下载升级方式。

双安装模式分派:
- git 模式(仓内 checkout):工作区干净才 `git pull --ff-only`,拒绝带未提交变更升级
- installed 模式(uv tool 安装态):`uv tool install --upgrade`(或 git 源)
版本探测走 GitHub Releases API(匿名,GH_TOKEN 可注入,离线容错不阻塞)。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

from . import __version__

DEFAULT_REPO = os.environ.get("PEVO_REPO", "raystyle/ProjectEvo")
_PRE = {"a": 0, "b": 1, "rc": 2}


def version_tuple(v: str) -> tuple[int, ...]:
    """semver 近似比较:数字段 + 预发布序(无预发布 > 有)。"""
    v = v.lstrip("v")
    m = re.match(r"(\d+)\.(\d+)\.(\d+)(?:([ab]|rc)\.?(\d+)?)?", v)
    if not m:
        return (0, 0, 0, 0, 0)
    maj, mi, pa, pre, pn = m.groups()
    rank = 3 if pre is None else _PRE.get(pre, 3)
    return (int(maj), int(mi), int(pa), rank, int(pn or 0))


def latest_release_tag(repo: str, timeout: float = 6.0) -> str | None:
    """GitHub Releases latest tag;离线/未发布/限流返回 None(不阻塞升级路径)。"""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "project-evo-update",
    })
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8")).get("tag_name")
    except Exception:
        return None


def check_for_update(repo: str = DEFAULT_REPO) -> tuple[str, str | None, bool]:
    """返回 (当前版本, 最新 tag 或 None, 是否有新版)。"""
    latest = latest_release_tag(repo)
    newer = bool(latest and version_tuple(latest) > version_tuple(__version__))
    return __version__, latest, newer


def _install_mode() -> str:
    """git(本仓 checkout 运行)或 installed(uv tool 安装态)。"""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / ".git").exists() and (parent / "pyproject.toml").exists():
            try:
                rel = p.relative_to(parent)
            except ValueError:
                continue
            if rel.parts and rel.parts[0] == "src":
                return "git", parent
    return "installed", None


def _run(cmd: list[str]) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.run(cmd).returncode


def run_update(yes: bool = False, repo: str = DEFAULT_REPO) -> int:
    cur, latest, newer = check_for_update(repo)
    if cur and latest and not newer:
        print(f"project-evo 已是最新({cur})。")
        return 0
    if latest:
        print(f"升级 project-evo:{cur} -> {latest}")
    else:
        print("未能取得远端版本(离线或未发布);仍尝试升级。")

    mode, repo_dir = _install_mode()
    if mode == "git":
        assert repo_dir is not None
        status = subprocess.run(
            ["git", "-C", str(repo_dir), "status", "--porcelain"],
            capture_output=True, text=True,
        )
        if status.returncode != 0:
            print(f"error: git status 失败:{status.stderr.strip()}", file=sys.stderr)
            return 1
        if status.stdout.strip():
            print(f"error: 仓内有未提交变更,拒绝升级:{repo_dir}", file=sys.stderr)
            print("先提交或 stash,或自行 `git pull --ff-only`。", file=sys.stderr)
            return 1
        rc = _run(["git", "-C", str(repo_dir), "pull", "--ff-only"])
        if rc != 0:
            return rc
        print(f"已更新仓({repo_dir});内嵌 skill 树随源更新,重跑 `project-evo skill <项目>` 同步各项目。")
        return 0

    # installed 模式:默认 git 直装(bh 同款);PEVO_GIT 覆盖源,PEVO_INDEX=1 走包索引名
    git_src = os.environ.get("PEVO_GIT") or f"https://github.com/{repo}"
    target = "project-evo" if os.environ.get("PEVO_INDEX") else f"git+{git_src}"
    if not yes:
        try:
            ans = input(f"将以 uv tool 升级 {target},继续?[y/N] ").strip().lower()
        except EOFError:
            ans = ""
        if ans not in {"y", "yes"}:
            print("已取消。")
            return 0
    rc = _run(["uv", "tool", "install", "--upgrade", target])
    if rc != 0:
        return rc
    print("升级完成;对已装项目重跑 `project-evo skill <项目>` 同步最新 skill 树。")
    return 0
