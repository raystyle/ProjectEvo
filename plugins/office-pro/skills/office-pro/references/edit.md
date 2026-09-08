# 既有稿：探查到截图核

> 本文件 = 改别人已经做好的 pptx/docx/xlsx。禁止用 pptxgenjs 重做模板。大文件（百 MB）优先 officecli set，不要整包 unpack。

## 循环

```text
备份 → outline/text/query → 对照邻页几何 → native 截图 → set/remove → 再截图 → close → rg 残留
```

1. 备份到同目录旁路名。只读则 `attrib -R`。锁则改 `*-work.pptx`，最后再覆盖。
2. `view outline`、`view text --page N`、`query '*' --find '关键词' --compact` 定位页。
3. 取一页已对齐的邻居做网格：标题 `x`/`y`、页眉线、内容区顶边、左右边距。`get /slide[N] --json --depth 1` 与 `query '/slide[N] > *' --compact --fields x,y,width,height,name`。
4. `view screenshot --page N --render native -o sN.png`。`-o` 必须是文件路径，目录会被拒。html 渲染缺无头浏览器会失败；Windows 用 native。[实证: 2026-09-08]
5. 偏位典型：截图盖住页眉、左右边距差一截、标题 `xfrm` 偏离版式、组 `x` 抖动、图片 `srcRect` 裁顶、残留连接线（宽过画布、微旋转、低透明度）。
6. `set` 坐标；图片按原 `width/height` 比缩放。不要为「好看」拉伸。
7. 只重截改过的页。一处 set 常带出新重叠。
8. `close`。覆盖原文件前确认 PowerPoint 已关。

## 换文案

`set --prop text=`。多段用 `\n`。表格单元格路径 `/slide[N]/table[@id=ID]/tr[R]/tc[C]`。

单元格窄、字号小：先看截图溢出，再缩短文案，不要堆无法核验的长句。

## 探查 XML（可选）

officecli 读不出 `srcRect` / `chOff` / `rot` 时，用 Python `zipfile` 读 `ppt/slides/slideN.xml`，不要 sed。
