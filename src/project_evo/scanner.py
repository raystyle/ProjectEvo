"""scan 子命令:git 隐私安全扫描 + markdown 规范告警。

- secrets:工作区与 git 全历史中的 token/密钥/隐私(高危:令牌与私钥;中危:赋值型与敏感文件;低危:本机路径)
- md:四类禁字与半角标点可修正项,告警并提示用 `project-evo fix` 修正
报告片段脱敏(仅示前缀);退出码 0 干净 / 1 有发现 / 2 出错。
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from .mdfix import SKIP_DIRS, file_violations

SECRET_RULES: list[tuple[str, str, re.Pattern]] = [
    ("GitHub token", "HIGH", re.compile(r"gh[pousr]_[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{20,}")),
    ("OpenAI/Anthropic key", "HIGH", re.compile(r"sk-(?:ant-)?[A-Za-z0-9_\-]{20,}")),
    ("AWS access key", "HIGH", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google API key", "HIGH", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Slack token", "HIGH", re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}")),
    ("private key block", "HIGH", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JWT", "HIGH", re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.")),
    ("URL embedded credentials", "HIGH", re.compile(r"https?://[^\s/:@]+:[^\s/@]{6,}@")),
]
_ASSIGN = re.compile(
    r"(?i)\b(password|passwd|secret|token|api[_-]?key|access[_-]?key|client[_-]?secret)\b[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_\-./+=]{10,})"
)
_ASSIGN_OK = re.compile(r"(?i)^(x+i*x*|<[^>]+>|\$\{|…+|example|placeholder|changeme|your[_-])")
SENSITIVE_FILE = re.compile(
    r"(^|/)(\.env|id_rsa[^/]*|.*\.pem|.*\.key|.*\.p12|credentials\.json|secrets?\.(json|ya?ml|toml))$", re.I
)
ENV_FILE = re.compile(r"(^|/)\.env(\.[^/]+)?$", re.I)
LOCAL_PATH = re.compile(r"[A-Z]:\\Users\\|[A-Z]:\\[A-Za-z][^\\/:*?\"<>|\s]*")

Finding = dict  # {kind,severity,rule,file,line,commit,snippet}


def _mask(s: str) -> str:
    return (s[:12] + "***") if len(s) > 15 else s[:4] + "***"


def _secret_findings_in_line(line: str, low_rules: bool = True) -> list[tuple[str, str, str]]:
    out = []
    for name, sev, pat in SECRET_RULES:
        m = pat.search(line)
        if m:
            out.append((name, sev, m.group(0)))
    m = _ASSIGN.search(line)
    if m and not _ASSIGN_OK.match(m.group(2)):
        out.append(("assigned secret", "MED", f"{m.group(1)}={_mask(m.group(2))}"))
    if low_rules and LOCAL_PATH.search(line):
        out.append(("local absolute path", "LOW", line.strip()[:40]))
    return out


def _walk_files(root: Path) -> list[Path]:
    files = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).parts
        if any(part in SKIP_DIRS or part.startswith(".git") for part in rel):
            continue
        if p.suffix.lower() in {".png", ".jpg", ".zip", ".pdf", ".exe", ".dll", ".whl", ".lock"}:
            continue
        files.append(p)
    return files


def scan_worktree_secrets(root: Path) -> list[Finding]:
    out: list[Finding] = []
    for p in _walk_files(root):
        rel = p.relative_to(root).as_posix()
        if SENSITIVE_FILE.match(rel) or ENV_FILE.match(rel):
            out.append({"kind": "secrets", "severity": "HIGH", "rule": "sensitive file",
                        "file": rel, "line": 0, "commit": "-", "snippet": rel})
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        is_md = p.suffix.lower() == ".md"
        for i, ln in enumerate(text.splitlines(), 1):
            for name, sev, raw in _secret_findings_in_line(ln, low_rules=not is_md):
                out.append({"kind": "secrets", "severity": sev, "rule": name,
                            "file": rel, "line": i, "commit": "-",
                            "snippet": _mask(raw) if len(raw) > 16 else raw})
    return out


def scan_history_secrets(root: Path) -> list[Finding]:
    """git 全历史新增行扫描(git log -p --all),按(规则,文件,片段)去重保留首见提交。"""
    proc = subprocess.run(
        ["git", "-C", str(root), "log", "-p", "--all", "--no-color", "--unified=0",
         "--diff-filter=AM"],
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
            for name, sev, raw in _secret_findings_in_line(ln[1:], low_rules=not fname.endswith(".md")):
                key = (name, fname, raw[:24])
                if key in seen:
                    continue
                seen.add(key)
                out.append({"kind": "secrets", "severity": sev, "rule": name,
                            "file": fname, "line": 0, "commit": commit,
                            "snippet": _mask(raw) if len(raw) > 16 else raw})
    return out


def scan_md(root: Path) -> list[Finding]:
    """markdown 禁字逐行告警(标注文件与行号;不修改,修正由人工/编辑器完成)。"""
    out: list[Finding] = []
    for p in _walk_files(root):
        if p.suffix.lower() != ".md":
            continue
        rel = p.relative_to(root).as_posix()
        for line_no, cats in file_violations(p.read_text(encoding="utf-8")).items():
            out.append({"kind": "md", "severity": "MED", "rule": "、".join(cats),
                        "file": rel, "line": line_no, "commit": "-",
                        "snippet": "按《字符与标点硬禁令》修正(替代写法:冒号/括号/拆句;箭头改文字)"})
    return out


def run_scan(root: Path, history: bool = True) -> tuple[list[Finding], bool]:
    import os
    finds = scan_worktree_secrets(root) + (scan_history_secrets(root) if history else []) + scan_md(root)
    allow = os.environ.get("PEVO_SCAN_ALLOW", "")
    if allow:
        pats = [re.compile(p) for p in allow.split(";") if p.strip()]
        finds = [f for f in finds if not any(p.search(f"{f['file']}:{f['line']} {f['rule']}") for p in pats)]
    rank = {"HIGH": 0, "MED": 1, "LOW": 2}
    finds.sort(key=lambda f: (rank.get(f["severity"], 3), f["file"]))
    return finds, not finds
