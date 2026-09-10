# Glow Collection · 小企鹅 macOS 发光主题

**14 套独立主题，28 组深浅配色。** 默认横排；所有主题均为当前选中的候选提供光晕。仅使用本地 CSS，无远程素材、字体下载或 JavaScript 插件。

## 先看效果

**深色模式**

![深色图册](glow-studio/screenshots/dark-gallery.png)

**浅色模式**

![浅色图册](glow-studio/screenshots/light-gallery.png)

> 以上为复用主题 CSS 的模拟预览，不是原生输入法截图。双击打开 [交互图册](glow-studio/preview.html) 可切换深浅、横竖排，点击候选体验选中高亮。

## 使用方法

主题配置已经放在本机 `~/.local/share/fcitx5/theme/`，CSS 已放在 `~/.local/share/fcitx5/www/css/`。**未替换你正在使用的主题或 CSS，也未重启输入法。**

1. 打开小企鹅的 **主题编辑器 → 基础**。
2. 建议先导出当前配色，并记下“高级 → 用户 CSS”的现有路径。你当前的路径为 `fcitx:///file/css/fcitx-glow.css`；原文件保留不动。
3. 点击 **选择/导入主题**，选择下面任意一个 `Glow-*.conf`。如文件选择器没在主题目录，按 `⌘⇧G` 输入 `~/.local/share/fcitx5/theme/`。
4. 新主题配置包含 `[Advanced] UserCss`，按上游导入实现会一并加载对应 CSS。导入后检查 **高级 → 用户 CSS** 是否是该主题的 `glow-xxx.css`。
5. 如果只有配色、没有光效，在 **高级 → 用户 CSS** 手动选取 `~/.local/share/fcitx5/www/css/glow-xxx.css`。若界面是文本字段，可填表中的 `fcitx:///file/css/` 前缀加文件名。
6. 新主题设置为 `System` 跟随系统明暗。想固定深色/浅色，在 **基础 → 主题** 中选择 `Dark` / `Light`。

> 导入主题会改变外观（配色、字体、间距、横排等），但本套件不包含输入方案、词库、热键或插件配置。

## 主题目录

| 主题文件 | 风格 | 选中效果 | 对应 CSS |
|---|---|---|---|
| `Glow-WeChat.conf` | 微信 · 翠光，日常清爽 | 静态翡翠柔光 | `glow-wechat.css` |
| `Glow-Apple.conf` | Apple · 冰晶，冰蓝玻璃质感 | 静态冰光＋细高光 | `glow-apple.css` |
| `Glow-Telegram.conf` | Telegram · 蓝调，气泡轮廓 | 静态天蓝光晕 | `glow-telegram.css` |
| `Glow-Cyberpunk.conf` | Cyberpunk · 霓虹，青色/洋红双边 | 3.8 秒霓虹呼吸 | `glow-cyberpunk.css` |
| `Glow-Aurora.conf` | Aurora · 极光，蓝绿渐变 | 7 秒背景流光 | `glow-aurora.css` |
| `Glow-Obsidian.conf` | Obsidian · 黑金，香槟细边 | 静态金辉 | `glow-obsidian.css` |
| `Glow-Sakura.conf` | Sakura · 樱花，花瓣圆角 | 静态樱粉柔光 | `glow-sakura.css` |
| `Glow-Matcha.conf` | Matcha · 抹茶，和纸底、宋体字 | 静态苔绿微光 | `glow-matcha.css` |
| `Glow-Sunset.conf` | Sunset · 落日，杏橙莓果 | 7 秒暮色流光 | `glow-sunset.css` |
| `Glow-Dracula.conf` | Dracula · 夜幕，紫夜薄荷边 | 3.8 秒紫电呼吸 | `glow-dracula.css` |
| `Glow-Matrix.conf` | Matrix · 终端，扫描细纹 | 3.8 秒荧光呼吸 | `glow-matrix.css` |
| `Glow-Amber.conf` | Amber · 琥珀，复古暖屏 | 静态琥珀光晕 | `glow-amber.css` |
| `Glow-Hologram.conf` | Hologram · 全息棱镜，深海青紫 | 7 秒青紫粉棱镜流光 | `glow-hologram.css` |
| `Glow-Porcelain.conf` | Porcelain · 青花瓷，瓷白靛青 | 静态蓝釉柔光 | `glow-porcelain.css` |

推荐先试 **Apple / WeChat / Telegram / Porcelain** 做日常，再试 **Cyberpunk / Aurora / Hologram / Matrix 深色**看炫酷效果。均为风格致敬，不是相关产品的官方主题。

## 微调

- **竖排：**主题编辑器 → 版式 → 布局 → Vertical。本套主题将“输入法感知版式”设为 False，使布局选择生效；有需要可重新开启。CSS 不限制横竖排。
- **字体：**默认苹方；抹茶使用宋体，序号使用 SF Mono / Menlo。均有本地后备字体。
- **取消动效、保留发光：**macOS 辅助功能 → 显示 → 减少动态效果；或在对应 CSS 末尾加：

  ```css
  #fcitx-theme { --gs-motion: none; }
  ```

- **减弱发光：**在对应 CSS 最后加（不影响选中底色）：

  ```css
  #fcitx-theme.fcitx-light,
  #fcitx-theme.fcitx-dark {
    --gs-glow: rgba(120, 160, 160, 0.12);
    --gs-glow-soft: transparent;
    --gs-glow-strong: rgba(120, 160, 160, 0.18);
  }
  ```

- **毛玻璃：**`Background/Blur=System`；macOS 背景模糊由原生窗口控制，CSS 只控制颜色与玻璃高光。不承诺复刻 Apple Liquid Glass 的折射。
- 选中效果使用真实 `.fcitx-highlighted` 状态；悬浮只加细线，不额外制造一个发光选中。正文不闪烁、不缩放。光晕边缘可能被原生候选窗裁切，这是为保持圆角、卷轴和点击区域正常，不强行改变 overflow。
- 未改卷轴的单元格 CSS 尺寸、滚动容器或候选定位；保留 `ScrollCellWidth=65`。开启卷轴后仍需在实际输入法中确认长词和候选注释显示。

## 再次导出 / 迁移

上游当前实现导出主题时会移除 `Basic`、`ScrollMode` 和 `Advanced`，因此**输入法重新导出的 `.conf` 不包含用户 CSS 引用**。迁移时请同时带上原始 `Glow-*.conf` 与对应 `glow-*.css`，将 CSS 放到另一台机器的 `~/.local/share/fcitx5/www/css/`，再导入；或在新机器手动重新选择 CSS。

`glow-studio/css/` 保存了本次 CSS 源副本；实际输入法读取的是 `www/css/` 中的安装副本。修改安装副本后重新选择 CSS 使其刷新。

## 还原

- 当前 `wetype.conf`、`webpanel.conf`、`fcitx-glow.css`、`test1.css` 均保留，校验哈希记录于 `glow-studio/original-hashes.json`。
- 要恢复导入前外观，导入你在步骤 2 导出的主题，并恢复原 CSS 路径。原始 `wetype.conf` 不一定等于你后来微调过的当前外观，不能代替你自己的导出备份。
- 切回普通主题后，如果还有新光效，在 **高级 → 用户 CSS** 清空或选回原文件。
- 删除套件前先切换走，再删除 `Glow-*.conf` 与对应 `www/css/glow-*.css`；不要删除原来的 `wetype.conf` 和 `fcitx-glow.css`（命名不同）。

## 维护与验证

```sh
cd ~/.local/share/fcitx5/theme
python3 -m unittest discover -s glow-studio/tests -v
# 修改 palettes.json 或 build.py 后重新生成；会更新本套件生成文件，覆盖其手工改动：
python3 glow-studio/build.py --install-css
```

生成器拒绝覆盖没有本套件标记的同名文件，不读取或写入当前运行配置。测试涵盖 14 套主题、28 组配色对比度、CSS 安装一致性、关键选中选择器和旧文件保持不变。浏览器验证结果另见 `glow-studio/verification.md`；未自动切换到原生输入法做实机输入测试。

参考：[官方 CSS 文档](https://fcitx-contrib.github.io/docs/theme/css.html)、[官方导入/导出说明](https://fcitx-contrib.github.io/docs/theme/import.html)、[主题集合格式](https://github.com/fcitx-contrib/fcitx5-theme-collection)、[导入/导出实现](https://github.com/fcitx-contrib/fcitx5-macos/blob/master/webpanel/webpanel.cpp)。本套件为原创 CSS 和配色，没有复制仓库主题文件。
