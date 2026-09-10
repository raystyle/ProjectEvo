# 命令契约

> 本文件 = 日常增删改查怎么调。schema 细节以本机 `officecli help <format> <verb> <element>` 为准。

## 分层

| 层 | 命令 | 用途 |
| --- | --- | --- |
| L1 | `view` `validate` | 读。`view` 第二参必填 mode：`text` `outline` `stats` `issues` `screenshot` |
| L2 | `get` `query` `set` `add` `remove` `move` `swap` | DOM 路径，1-based |
| L3 | `raw` `raw-set` `add-part` | 生 XML，L2 够不到时 |

路径例：`/slide[1]/shape[@id=2]`、`/body/p[1]`、`/Sheet1/B2`。方括号在 PowerShell 里给路径加引号。

`--json` 成功 `{success, data}`；失败 `{success:false, error:{error,code,suggestion}}`，坏路径常见 `not_found`、退出 1。[实证: S007 `/slide[99]`]

## 常驻

`create` / `open` 会保持 named pipe。officecli 自己的后续读能看见内存中的改；Word、python-docx、资源管理器读盘前必须 `save` 或 `close`。活常驻空闲 2 至 10 秒也会 flush（`OFFICECLI_RESIDENT_FLUSH`）。

改完一批：`close <file>`。

## 实证过的坑

| 坑 | 正确做法 |
| --- | --- |
| PowerShell 函数参数 `$args` | 改名 `$ocArgs`，`& $bin @ocArgs` |
| xlsx `value=SUM(D1,5)` | 存成字符串。公式用 `formula=SUM(D1,5)` 或 `value==SUM(D1,5)` |
| docx `style=Heading1` | 默认样式部件可能没有该样式，告警仍写入，validate 仍过；Word 里是否生效未用 Word 核 |
| `view file` 缺 mode | 打 help，不是默读全文 |
| 图片只改宽或高 | 按原比例算另一边，或只动 `x`/`y` |

## 改几何

```powershell
& $bin help pptx set shape
& $bin help pptx set picture
& $bin help pptx set group
& $bin set $file '/slide[N]/picture[@id=ID]' --prop 'x=144pt' --prop 'y=92pt' --prop 'width=672pt' --prop 'height=420pt'
& $bin remove $file '/slide[N]/connector[@id=5]' --json
```

`query --compact --fields x,y,width,height,name` 比整棵 JSON 好扫。组的 `x`/`y` 可 set；`chOff`/`srcRect` 裁剪若 officecli 设不了，再 unzip 读 XML，禁止 sed。
