# 验证记录 · 2026-09-10

## 完成结果

- 14 个 `Glow-*.conf`，各包含独立浅/深配色，共 28 组。
- 14 份独立 CSS，源副本与 `../www/css/` 安装副本完全一致。
- 5 项 Python 单元测试通过（每项遍历所有相关主题）：结构、深浅配置、CSS 本地关联、选中选择器、减少动效支持、对比度、原文件哈希、交付文档。
- 文本、序号与选中词的配置色彩对比度检查 ≥ 4.5:1（面板渐变两端及选中渐变两端；不代表原生半透明背景叠加任何桌面后都相同）。
- Playwright WebKit 26.4 交互图册测试 19 项通过：14 套选中光效、点击与键盘切换、布局不跳动、动效类型；28 个明暗预览；28 个竖排与注释；系统减少动态效果；图册静态开关；零脚本报错、零远程资源请求。
- 使用上游真实 `generic.scss` / `macos.scss` / `macos-15.scss` / `macos-26.scss` / `common.scss` 编译后的 CSS，完成 **168 个组合**集成验证：14 主题 × macOS 15/26 两套基础样式 × 明暗 × 横排/竖排/卷轴。
  - 加载自定义 CSS 前后，面板、候选容器及候选内层的几何尺寸和位置一致。
  - 仅选中的候选获得发光与渐变。
  - 减少动态效果仍有效。
- 原来的 `wetype.conf`、当前 `webpanel.conf`、`fcitx-glow.css`、`test1.css` 均与开始时哈希相同。
- 人工查看深色、浅色与竖排截图，未发现裁字、覆盖或选中状态串色。

## 实际边界

本次**未切换用户正在使用的输入法主题**，未执行原生打字、真实卷轴分页/长词跨列或系统毛玻璃实机验收。上游 SCSS 测试是 WebKit 内的静态结构集成测试，不是运行中的 Fcitx5 窗口。图册中的点击/方向键逻辑只用于预览，不注入实际输入法。

本机 Fcitx5 `Info.plist` 标记版本为 0.3.3；配置采用本机已存在字段与枚举（例如 `Blur=System`）。候选窗 CSS 根据官方 DOM 和上游当前样式核对。

## 可复现命令

```sh
cd ~/.local/share/fcitx5/theme
python3 -m unittest discover -s glow-studio/tests -v
# 如 Node 能直接解析 playwright：
node glow-studio/tests/browser-check.cjs
# 如使用其他位置安装的 Playwright：
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node glow-studio/tests/browser-check.cjs
```

WebKit 需通过 Playwright 预先安装。此次使用已有 Playwright 模块，并补充下载其 WebKit 测试运行时，未改变系统默认浏览器。

上游集成测试输入可自行准备：

```sh
mkdir -p /tmp/fcitx-glow-native-check
for f in common generic macos macos-15 macos-26; do
  curl -fL "https://raw.githubusercontent.com/fcitx-contrib/fcitx5-webview/master/page/$f.scss" \
    -o "/tmp/fcitx-glow-native-check/$f.scss"
done
printf "@use './generic';\n@use './macos';\n@use './macos-15';\n@use './macos-26';\n" \
  > /tmp/fcitx-glow-native-check/style.scss
npx sass /tmp/fcitx-glow-native-check/style.scss /tmp/fcitx-glow-native-check/style.css --no-source-map
FCITX_BASE_CSS=/tmp/fcitx-glow-native-check/style.css node glow-studio/tests/upstream-check.cjs
```

上游文件作为测试输入保存在临时目录，未捆绑分发。此次输入内容的 SHA-256 见 `upstream-source-hashes.json`；master 后续变动可能改变测试结果。

**注意：**原配置哈希检查针对“制作过程中不修改现有配置”。你主动导入主题或修改设置后，`webpanel.conf` 哈希变化是正常的，该项审计会提示不一致，不代表主题损坏。

## 审计文件

- `browser-results.json`：WebKit 交互验证。
- `upstream-results.json`：上游 CSS 集成验证。
- `original-hashes.json`：旧文件 SHA-256。
- `screenshots/dark-gallery.png`、`light-gallery.png`、`vertical-gallery.png`：模拟图册截图。

## 验证中解决的问题

1. 自动化点击会滚动图册外层页面，因此布局稳定性改为比较 iframe 内局部坐标，避免将滚动误判为候选位移；局部坐标与尺寸实测保持一致。
2. 深色图册与默认浅色 iframe 的 color-scheme 不匹配，会让浏览器强制画不透明白色底。按 [CSS Color Adjustment 规范](https://www.w3.org/TR/css-color-adjust-1/#color-scheme-effect)统一宿主与 iframe 的色彩方案，保留透明画布；已添加回归断言。

3. 只读复核发现琥珀浅色辅助文字在面板渐变终点的对比度为 4.441:1；补上面板终点回归检查，并将辅助文字加深至 `#77603a`。无 Critical / Important 复核问题。
4. 用户追加两套后新增 `Hologram` 与 `Porcelain`，并把图册与两组浏览器测试的主题数量改为从数据源动态读取，避免后续扩展遗漏硬编码计数。
