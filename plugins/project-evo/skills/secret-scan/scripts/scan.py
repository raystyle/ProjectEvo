# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""scan:本地 git 仓与 GitHub 上的密钥/隐私挖掘(只报告脱敏片段,不修改仓)。

用法:
  uv run scan.py [目标项目] [--no-history] [--pii] [--json]
  uv run scan.py --github owner/repo [--clone-history]
退出码: 0 干净 / 1 有发现 / 2 出错。
白名单: SECRET_SCAN_ALLOW="正则;正则" 匹配 文件:行 规则。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from rules import (  # noqa: E402
    ASSIGN,
    ASSIGN_OK,
    ENV_FILE,
    GITHUB_CODE_QUERIES,
    LOCAL_PATH,
    PII_CN_MOBILE,
    PII_EMAIL,
    PII_EMAIL_OK,
    SECRET_RULES,
    SENSITIVE_FILE,
    SKIP_DIRS,
    SKIP_SUFFIX,
)

Finding = dict


def _mask(s: str) -> str:
    s = s.strip()
    return (s[:12] + "***") if len(s) > 15 else s[:4] + "***"


def _allow_hit(f: Finding, pats: list[re.Pattern[str]]) -> bool:
    blob = f"{f['file']}:{f['line']} {f['rule']}"
    return any(p.search(blob) for p in pats)


def secret_hits_in_line(line: str, *, pii: bool, skip_path: bool) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for name, sev, pat in SECRET_RULES:
        m = pat.search(line)
        if m:
            out.append((name, sev, m.group(0)))
    m = ASSIGN.search(line)
    if m and not ASSIGN_OK.match(m.group(2)):
        out.append(("assigned secret", "MED", f"{m.group(1)}={_mask(m.group(2))}"))
    if not skip_path and LOCAL_PATH.search(line):
        out.append(("local absolute path", "LOW", line.strip()[:40]))
    if pii:
        for em in PII_EMAIL.findall(line):
            if not PII_EMAIL_OK.search(em):
                out.append(("email", "LOW", _mask(em)))
        if PII_CN_MOBILE.search(line):
            out.append(("cn-mobile", "LOW", "1**********"))
    return out


def _walk_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).parts
        if any(part in SKIP_DIRS or part.startswith(".git") for part in rel):
            continue
        if p.suffix.lower() in SKIP_SUFFIX:
            continue
        files.append(p)
    return files


def scan_worktree(root: Path, *, pii: bool) -> list[Finding]:
    out: list[Finding] = []
    for p in _walk_files(root):
        rel = p.relative_to(root).as_posix()
        if SENSITIVE_FILE.match(rel) or ENV_FILE.match(rel):
            out.append({
                "kind": "secrets", "severity": "HIGH", "rule": "sensitive file",
                "file": rel, "line": 0, "commit": "-", "source": "worktree", "snippet": rel,
            })
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        skip_path = p.suffix.lower() == ".md"
        for i, ln in enumerate(text.splitlines(), 1):
            for name, sev, raw in secret_hits_in_line(ln, pii=pii, skip_path=skip_path):
                out.append({
                    "kind": "secrets", "severity": sev, "rule": name,
                    "file": rel, "line": i, "commit": "-", "source": "worktree",
                    "snippet": _mask(raw) if len(raw) > 16 else raw,
                })
    return out


def scan_history(root: Path, *, pii: bool) -> list[Finding]:
    proc = subprocess.run(
        ["git", "-C", str(root), "log", "-p", "--all", "--no-color", "--unified=0", "--diff-filter=AM"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        print(f"error: git log 失败:{proc.stderr.strip()[:200]}", file=sys.stderr)
        return []
    out: list[Finding] = []
    seen: set[tuple] = set()
    commit, fname = "-", "-"
    for ln in proc.stdout.splitlines():
        if ln.startswith("commit "):
            commit = ln.split()[1][:8]
        elif ln.startswith("+++ b/"):
            fname = ln[6:]
        elif ln.startswith("+") and not ln.startswith("+++"):
            skip_path = fname.endswith(".md")
            for name, sev, raw in secret_hits_in_line(ln[1:], pii=pii, skip_path=skip_path):
                key = (name, fname, raw[:24])
                if key in seen:
                    continue
                seen.add(key)
                out.append({
                    "kind": "secrets", "severity": sev, "rule": name,
                    "file": fname, "line": 0, "commit": commit, "source": "history",
                    "snippet": _mask(raw) if len(raw) > 16 else raw,
                })
    return out


def _gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def scan_github_alerts(repo: str) -> tuple[list[Finding], str | None]:
    proc = _gh(["api", f"repos/{repo}/secret-scanning/alerts", "--paginate"])
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        if "404" in err or "403" in err or "Not Found" in err or "secret scanning" in err.lower():
            return [], f"SKIP github alerts:{repo} 未开 secret scanning 或无 security_events 权限"
        return [], f"error github alerts:{err[:200]}"
    try:
        data = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return [], "error github alerts:非 JSON"
    if not isinstance(data, list):
        return [], "error github alerts:响应不是列表"
    out: list[Finding] = []
    for a in data:
        loc = (a.get("most_recent_instance") or {}).get("location") or {}
        path = loc.get("path") or a.get("secret_type") or "-"
        line = int(loc.get("start_line") or 0)
        commit = (str(loc.get("commit_sha") or "-"))[:8]
        stype = str(a.get("secret_type_display_name") or a.get("secret_type") or "github-alert")
        state = str(a.get("state") or "")
        out.append({
            "kind": "secrets", "severity": "HIGH", "rule": f"github-alert:{stype}",
            "file": path, "line": line, "commit": commit, "source": "github-alert",
            "snippet": f"state={state}",
        })
    return out, None


def scan_github_code(repo: str) -> list[Finding]:
    out: list[Finding] = []
    seen: set[tuple] = set()
    for q in GITHUB_CODE_QUERIES:
        proc = _gh([
            "search", "code", q, "--repo", repo, "--limit", "20",
            "--json", "path,url,sha",
        ])
        if proc.returncode != 0:
            continue
        try:
            items = json.loads(proc.stdout or "[]")
        except json.JSONDecodeError:
            continue
        if not isinstance(items, list):
            continue
        for it in items:
            path = str(it.get("path") or "-")
            sha = str(it.get("sha") or "-")[:8]
            key = (q, path, sha)
            if key in seen:
                continue
            seen.add(key)
            out.append({
                "kind": "secrets", "severity": "MED", "rule": f"github-code:{q}",
                "file": path, "line": 0, "commit": sha, "source": "github-search",
                "snippet": "code-search 命中(当前默认分支索引,非全历史)",
            })
    return out


def clone_and_scan_history(repo: str, *, pii: bool) -> tuple[list[Finding], str | None]:
    dest = Path(tempfile.gettempdir()) / "pevo-secrets" / repo.replace("/", "_")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    proc = _gh(["repo", "clone", repo, str(dest), "--", "--bare"])
    if proc.returncode != 0:
        return [], f"error clone:{ (proc.stderr or proc.stdout or '')[:200] }"
    finds = scan_history(dest, pii=pii)
    for f in finds:
        f["source"] = "github-history"
    return finds, None


def run_scan(
    root: Path | None,
    *,
    history: bool,
    pii: bool,
    github: str | None,
    clone_history: bool,
) -> tuple[list[Finding], list[str]]:
    notes: list[str] = []
    finds: list[Finding] = []
    if root is not None:
        finds.extend(scan_worktree(root, pii=pii))
        if history:
            git_dir = root / ".git"
            if git_dir.exists() or (root / "HEAD").is_file():
                finds.extend(scan_history(root, pii=pii))
            else:
                notes.append(f"SKIP history:{root} 不是 git 仓")
    if github:
        alerts, note = scan_github_alerts(github)
        finds.extend(alerts)
        if note:
            notes.append(note)
        finds.extend(scan_github_code(github))
        if clone_history:
            hist, note = clone_and_scan_history(github, pii=pii)
            finds.extend(hist)
            if note:
                notes.append(note)
    allow = os.environ.get("SECRET_SCAN_ALLOW", "")
    if allow:
        pats = [re.compile(p) for p in allow.split(";") if p.strip()]
        finds = [f for f in finds if not _allow_hit(f, pats)]
    rank = {"HIGH": 0, "MED": 1, "LOW": 2}
    finds.sort(key=lambda f: (rank.get(f["severity"], 3), f["file"], f["rule"]))
    return finds, notes


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if stream.encoding and stream.encoding.lower().replace("-", "") != "utf8":
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="scan.py", description="密钥与隐私扫描:本地工作区/git 历史/GitHub")
    parser.add_argument("path", nargs="?", help="本地项目根(默认当前目录;与 --github 可同时用)")
    parser.add_argument("--no-history", action="store_true", help="跳过本地 git 全历史")
    parser.add_argument("--pii", action="store_true", help="加扫邮箱与大陆手机号(误报多)")
    parser.add_argument("--github", metavar="owner/repo", help="GitHub 仓:alerts + code search")
    parser.add_argument("--clone-history", action="store_true", help="裸克隆 --github 仓再扫 git 历史(须同时给 --github)")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--no-cwd", action="store_true", help="不要默认扫当前目录(只跑 --github)")
    args = parser.parse_args(argv)

    if args.clone_history and not args.github:
        print("error: --clone-history 需要 --github owner/repo", file=sys.stderr)
        return 2
    if args.github and "/" not in args.github:
        print("error: --github 须为 owner/repo", file=sys.stderr)
        return 2

    root: Path | None
    if args.no_cwd and not args.path:
        root = None
    else:
        root = Path(args.path).resolve() if args.path else Path.cwd()
        if not root.is_dir():
            print(f"error: 目标目录不存在:{root}", file=sys.stderr)
            return 2

    finds, notes = run_scan(
        root, history=not args.no_history, pii=args.pii,
        github=args.github, clone_history=args.clone_history,
    )
    if args.json:
        print(json.dumps({"findings": finds, "notes": notes}, ensure_ascii=False, indent=2))
        return 0 if not finds else 1
    for n in notes:
        print(n, file=sys.stderr)
    if not finds:
        print("扫描干净:无密钥/隐私命中")
        return 0
    for f in finds:
        loc = f"{f['file']}:{f['line']}" if f["line"] else f["file"]
        print(
            f"[{f['severity']:<4}] {f['source']:<16} {f['rule']:<28} {loc:<40} "
            f"@{f['commit']}  {f['snippet']}"
        )
    high = sum(1 for f in finds if f["severity"] == "HIGH")
    print(f"共 {len(finds)} 项(HIGH {high})")
    if high:
        print("高危:视为已泄露。先轮换凭据,再考虑 git filter-repo / BFG 清史。禁止把完整密钥写进 issue 或笔记。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
