"""密钥与隐私正则。scan.py 唯一规则源。片段由调用方脱敏。"""

from __future__ import annotations

import re

# (name, severity, pattern)
SECRET_RULES: list[tuple[str, str, re.Pattern[str]]] = [
    ("GitHub token", "HIGH", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}")),
    ("GitLab token", "HIGH", re.compile(r"glpat-[A-Za-z0-9_\-]{20,}")),
    ("OpenAI/Anthropic key", "HIGH", re.compile(r"sk-(?:ant-)?[A-Za-z0-9_\-]{20,}")),
    ("AWS access key", "HIGH", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google API key", "HIGH", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Slack token", "HIGH", re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}")),
    ("Stripe key", "HIGH", re.compile(r"sk_live_[A-Za-z0-9]{20,}")),
    ("npm token", "HIGH", re.compile(r"npm_[A-Za-z0-9]{36}")),
    ("PyPI token", "HIGH", re.compile(r"pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_\-]{20,}")),
    ("Telegram bot", "HIGH", re.compile(r"\d{8,}:[A-Za-z0-9_\-]{35}")),
    ("private key block", "HIGH", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("JWT", "HIGH", re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.")),
    ("URL embedded credentials", "HIGH", re.compile(r"https?://[^\s/:@]+:[^\s/@]{6,}@")),
]

ASSIGN = re.compile(
    r"(?i)\b(password|passwd|secret|token|api[_-]?key|access[_-]?key|client[_-]?secret|"
    r"private[_-]?key|auth[_-]?token)\b[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_\-./+=]{10,})"
)
ASSIGN_OK = re.compile(
    r"(?i)^(x+i*x*|<[^>]+>|\$\{|\.+|example|placeholder|changeme|your[_-]|dummy|fake|test[_-]?key)"
)
SENSITIVE_FILE = re.compile(
    r"(^|/)(\.env|id_rsa[^/]*|.*\.pem|.*\.key|.*\.p12|credentials\.json|secrets?\.(json|ya?ml|toml))$",
    re.I,
)
ENV_FILE = re.compile(r"(^|/)\.env(\.[^/]+)?$", re.I)
LOCAL_PATH = re.compile(r"[A-Z]:\\Users\\|[A-Z]:\\[A-Za-z][^\\/:*?\"<>|\s]*")

PII_EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
PII_EMAIL_OK = re.compile(r"(?i)@(example\.com|example\.org|localhost|test\.|invalid)$")
PII_CN_MOBILE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__",
    ".tox", ".mypy_cache", ".pytest_cache",
}
SKIP_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".pdf", ".exe", ".dll", ".whl", ".lock", ".woff", ".woff2"}

GITHUB_CODE_QUERIES = (
    "ghp_",
    "github_pat_",
    "glpat-",
    "sk-ant-",
    "AKIA",
    "AIza",
    "xoxb-",
    "sk_live_",
    "BEGIN PRIVATE",
)
