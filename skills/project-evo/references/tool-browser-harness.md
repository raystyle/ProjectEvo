# browser-harness — 浏览器直控操作指南

> 定位:**搜索引擎与网页抓取**(用户裁定):google_search/bing_search 走真实浏览器搜引擎,web-fetch/extract 抓正文;亦覆盖自动化、JS 渲染、登录态页面。**普通 HTTP 能拿到的页面不要用它**(fetch/curl 优先)。本机 CLI v0.6.8 [实证: 2026-09-03 `browser-harness --version`]。

## 零、搜索与抓取(首要场景)

```python
# 搜索引擎(真实浏览器会话,复用各自 tab)
google_search("rust web framework", limit=5)     # -> [{title, url}, ...]
bing_search("rust web framework", limit=5)
```

```powershell
# 网页正文抓取(命令行)
browser-harness web-fetch "https://example.com/article"           # markdown
browser-harness web-fetch "https://example.com/a" --text --json   # 纯文本/全元数据
browser-harness web-fetch "https://x.com/home" --browser          # 需会话/JS 的页面
```

搜索引擎被 bot 墙、结果要 JS 渲染、或页面要登录态时,它取代 WebSearch/WebFetch/curl。

## 零点五、脚本 helper 面(源码实证)

管道脚本预导入的函数面(实证自 `浏览器工具仓\src\browser_harness\helpers.py` def 清单,2026-09-03):

| 类别 | 函数 |
| --- | --- |
| 导航/标签 | `new_tab` `goto_url` `wait_for_load` `list_tabs` `current_tab` `switch_tab` `activate_tab` `ensure_real_tab` |
| 页面读写 | `page_info` `js` `cdp` `click_at_xy` `capture_screenshot` |
| 抓取/搜索 | `extract_url_content` `extract_page_content` `web_fetch` `google_search` `bing_search` `http_get`(agent_helpers) |
| 工程桥 | `run_app`(子命令桥) `setup_browser_apps` `start_recording`/`stop_recording` |

## 一、健康检查与连接模型

```powershell
browser-harness doctor --json    # daemon.alive / daemon.browser_ready / chrome_running
browser-harness browsers         # 实例列表(agent/user 标记、tab 绑定)
browser-harness current          # 当前 attach 的目标
```

- 默认 daemon 钉在**隔离 agent Chrome**(端口 9223,标题带马形标记),永不碰用户自己的 Chrome [实证: 2026-09-03 browsers 输出确认隔离]
- agent Chrome 未起时 `ensure_daemon` 自动拉起;**冷启动首条命令可能 5s 超时**,等 `browser_ready: true` 后重试即成功 [实证: 2026-09-03 实测]

## 二、脚本模式(管道喂 Python)

```powershell
# Windows / 已装 pwsh 的平台:here-string
@'
info = new_tab("https://example.com")   # 任务首个导航用 new_tab
wait_for_load()
print(page_info())
print(js("document.querySelector('h1').innerText"))
'@ | browser-harness
```

```bash
# Linux / macOS:heredoc
browser-harness <<'EOF'
info = new_tab("https://example.com")
wait_for_load()
print(page_info())
EOF
```

[实证: bh SKILL 双形态约定]

- helpers 预导入;后续导航用 `goto_url`,不要每次 `new_tab`
- 一任务一工作 tab;先 `list_tabs()`/`switch_tab()` 复用,不开重复 tab

## 三、元素定位与点击(标准工作流)

**优先无障碍树,不优先截图**:

```python
nodes = cdp("Accessibility.getFullAXTree")["nodes"]   # 过滤后再打印,数千节点
# role/name 取值要归一化(value 可能是 dict 套 dict)
m = cdp("DOM.getBoxModel", backendNodeId=n["backendDOMNodeId"])["model"]["content"]
x, y = sum(m[0::2])/4, sum(m[1::2])/4                 # 盒中心,viewport 坐标
click_at_xy(x, y)
```

点击后必须用 `page_info()`/`js(...)` 定向验证效果。

## 四、内容提取与截图

```python
extract_page_content(markdown=True)                 # 当前 tab 正文(defuddle 引擎)
extract_url_content(url, markdown=True)             # 纯 HTTP
extract_url_content(url, markdown=True, use_browser=True)  # 需会话/JS 的页面
capture_screenshot()                                # 返回 PNG 路径(非 base64)
```

命令行等价:`browser-harness web-fetch <url> [--text|--json|--browser|--current]`。

## 五、坑(全部本机踩过)

| 症状 | 根因 | 处理 | 状态 |
| --- | --- | --- | --- |
| 首条命令 `_IPCResponseTimeout` | agent Chrome 冷启动中 | 查 doctor,`browser_ready: true` 后重试一次 | [实证: 2026-09-03] |
| 隐藏 tab 上 `click_at_xy` 无效果 | 后台 tab 渲染暂停 | `activate_tab(current_tab())` 后重试同一点击 | [实证: 2026-09-03] |
| `Runtime.evaluate` 超时 | 页面正在跳转 | 属正常瞬态;稍后重读 `page_info()` | [实证: 2026-09-03] |
| AX 树 role/name 取不到 | 字段是 property object,嵌套随版本变 | 用归一化函数逐层取 value | [实证: 2026-09-03] |

## 六、生态位

- skill 双入口:仓库 SKILL.md + `browser-harness --llms` 紧凑索引 [实证: 2026-09-03]
- 长驻监控(X 抓推等)走 rmux 会话(`browser-harness rmux ...`),不占前台
- Chrome 144+ 首连可能有「允许远程调试」弹窗:提示用户点 Allow,勿轮询重试

## 七、复验命令

```powershell
browser-harness --version
browser-harness doctor --json     # browser_ready 应为 true(Chrome 在跑时)
```
