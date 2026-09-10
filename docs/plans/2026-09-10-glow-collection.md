# Glow Collection Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在当前主题目录制作 12 套可导入的 macOS 小企鹅主题，选中发光且不影响现有设置。

**Architecture:** 配色和外观参数作为 JSON 源数据，Python 标准库生成 conf 与独立 CSS。CSS 同时保存于套件和 `../www/css` 可加载目录。主题文件按实际支持的导入字段关联 CSS；若导入不携带 CSS，说明手动选择。效果图册复用生成 CSS，独立布局仅用于模拟展示。

**Tech Stack:** Fcitx5 config / CSS / Python unittest / browser rendering.

---

### Task 1: 确认协议与建立失败校验
- 检查本机 webpanel 配置与 upstream 导入代码，确定 UserCss 是否导入及路径解析。
- Create: `glow-studio/tests/test_themes.py`，校验 12 个主题、深浅配置、CSS 关联、selected glow、reduced-motion、不改滚动尺寸。
- Run: `python3 -m unittest discover -s glow-studio/tests -v`，应因缺少交付物失败。

### Task 2: 生成可安装主题
- Create: `glow-studio/palettes.json`, `glow-studio/build.py`, `glow-studio/css/*.css`。
- Create: 顶层 `Glow-*.conf`，仅创建新文件；安装对应独立 CSS 至 `../www/css/glow-*.css`。
- 写静态与动效样式，使用 fcitx-highlighted，不使用不存在的 selected 伪类。
- Run: 同上测试，全部通过；校验原文件哈希不变。

### Task 3: 图册、文档与渲染核验
- Create: `glow-studio/preview.html`, `README-Glow.md`。
- 图册复用真实 CSS，展示 24 种配色，可切换横竖布局、点击候选预览高亮、关闭动效。
- 使用浏览器检查横排/竖排、选中态、reduced-motion；保留截图与校验结果。
- 使用说明准确列出导入/选择 CSS 流程，以及备份、还原、未原生实测的边界。
- 最后重新运行全套校验，不修改当前运行主题。

## 执行结果

- [x] Task 1：上游导入会加载 Advanced/UserCss，导出会移除；失败测试已观察。
- [x] Task 2：12 套 conf/CSS 生成并安装，24 组对比度通过，原文件哈希不变。
- [x] Task 3：离线图册、中文说明、WebKit 17 项测试、上游 CSS 144 场景测试和截图已完成。
- 无 Git 仓库，因此 worktree、分支收尾、提交不适用；只创建请求范围内主题和配套交付文件。

## 追加交付 · 2026-09-10

- [x] 新增 Hologram · 全息棱镜与 Porcelain · 青花瓷。
- [x] 图册、测试、文档改为 14 套 / 28 配色；浏览器与上游 CSS 集成重新全量验证。
