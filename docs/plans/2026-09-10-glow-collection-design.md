# Fcitx5 macOS · Glow Collection 设计

用户已批准原先六套风格并要求增加数量，本次扩展为十二套：微信翠光、Apple 冰晶、Telegram 蓝调、Cyberpunk 霓虹、Aurora 极光、Obsidian 黑金、Sakura 樱花、Matcha 抹茶、Sunset 落日、Dracula 夜幕、Matrix 终端、Amber 琥珀。

- 每套独立 `.conf` 与 CSS，提供浅/深两组配色；系统模式跟随明暗。
- 前三套适合日常；科幻组使用呼吸或渐变动效，其余采用静态柔光。
- 仅当前选中的候选发光，不闪烁正文、不缩放移动候选、不改卷轴尺寸；响应 reduced-motion。
- 按照真实 fcitx DOM 和主题配置导入机制实现，读取本机 schema 并核对上游源代码。
- 纯本地 CSS，无远程素材/字体、无注入脚本。保留原主题、当前配置和现有 CSS。
- 提供中文使用说明、可离线浏览的候选窗效果图册（模拟，不冒充原生实测）、结构与浏览器校验。
- 本目录不是 Git 仓库，不创建仓库或提交，不为任务改造用户目录。
