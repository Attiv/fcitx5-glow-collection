#!/bin/sh

set -eu

package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
fcitx_data_dir="${XDG_DATA_HOME:-$HOME/.local/share}/fcitx5"
theme_dir="$fcitx_data_dir/theme"
css_dir="$fcitx_data_dir/www/css"

mkdir -p "$theme_dir" "$css_dir"
cp -f "$package_dir"/theme/*.conf "$theme_dir"/
cp -f "$package_dir"/www/css/*.css "$css_dir"/

printf '%s\n' "安装完成：71 套 Fcitx5 主题已复制到 $fcitx_data_dir"
printf '%s\n' "请在 Fcitx5 设置中选择用户主题；如未刷新，请重启 Fcitx5。"
