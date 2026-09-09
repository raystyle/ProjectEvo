# super-research

超级研究插件。核心 skill 为 `research`（显示 `super-research:research`）。

把 gh、Google、Medium、X 本地库、reader、aria2c 串成一条资料检索管线。evo 只管项目文档骨架，本插件管检索与下载。

## 安装

市场已加 `raystyle/ProjectEvo` 后：

```text
/plugin install super-research@projectevo
```

Codex：`codex plugin add super-research@projectevo`；Grok：`grok plugin install super-research@projectevo --trust`；Kimi（无市场）：拷 `skills/research/` 整目录至 `~/.kimi/skills/`。

## 用法

技能按意图路由自动触发（搜论文、Google、Medium、X、GitHub、电子书、种子、aria2c）。入口 `skills/research/SKILL.md`。
