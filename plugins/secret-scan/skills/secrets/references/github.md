# GitHub 面

> `--github owner/repo` 的三层覆盖与失败形态。规则仍在 `scripts/rules.py`。

## 一、告警

```powershell
gh api repos/owner/repo/secret-scanning/alerts --paginate
```

需要:仓库已开 Secret Scanning;token 具备 `security_events`(私有仓还要 admin 或 security manager)。404/403 脚本打 SKIP,不当成扫描失败。

告警对象含提交 sha 与路径,是 GitHub 已确认的泄露,优先于 code search。

## 二、当前树检索

对 `rules.GITHUB_CODE_QUERIES` 逐条:

```powershell
gh search code "ghp_" --repo owner/repo --limit 20 --json path,url,sha
```

只覆盖默认分支**当前索引**,删掉的文件与历史提交不在此。命中标 MED,需打开该文件人工看(脚本不回显匹配原文)。

匿名限流 403:先 `gh auth status`。

## 三、完整历史

```powershell
gh repo clone owner/repo %TEMP%\pevo-secrets\owner_repo -- --bare
uv run scan.py %TEMP%\pevo-secrets\owner_repo
```

skill 的 `--clone-history` 即此。裸仓可用 `git log -p --all`。仓体积与时间随对象库涨,须用户显式打开。

已有本地 clone:

```powershell
git -C <本地仓> fetch --all
uv run scan.py <本地仓>
```

## 四、不要做的

- 不把 `gh search code` 当全历史
- 不默认镜像克隆
- 不调用第三方验证接口探测密钥是否仍有效
