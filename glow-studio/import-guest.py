#!/usr/bin/env python3
"""Import the third-party Fcitx5 theme collection into this repository.

The source pack lives in fcitx5-custom-theme-collection/ and ships 71 themes
plus a matching CSS file per theme. This script flattens it into the repository
layout used by the Glow Collection:

  fcitx5-custom-theme-collection/theme/<Name>.conf
      -> Guest-<Name>.conf                      (repository root)
  fcitx5-custom-theme-collection/www/css/<name>.css
      -> glow-studio/css/guest-<name>.css       (packaged source of truth)
      -> ~/.local/share/fcitx5/www/css/guest-<name>.css  (--install-css only)

Only the [Advanced] UserCss path and the header comment are rewritten. Every
other key is copied verbatim so the upstream styling is preserved exactly.

Run with --install-css to also copy the CSS into the live Fcitx5 folder.
"""
import argparse
import configparser
import io
import re
from pathlib import Path

PACK = Path(__file__).resolve().parent
ROOT = PACK.parent
SOURCE = ROOT / 'fcitx5-custom-theme-collection'
SIGNATURE = 'Fcitx5 Guest Collection — imported'
ORIGIN = 'from fcitx5-custom-theme-collection (third-party)'
PREFIX = 'Guest-'


def conf_text(name, description, uri):
    return (
        f'# {SIGNATURE}\n'
        f'# {description}\n'
        f'# {ORIGIN}. Vertical layout, paging buttons hidden.\n'
        f'# CSS path is bundled; do not remove it.\n'
    )


def rewrite_conf(src, css_name, description):
    """Copy a source conf, retargeting UserCss and the banner comment."""
    c = configparser.ConfigParser(interpolation=None)
    c.optionxform = str
    c.read(src)
    c['Advanced']['UserCss'] = f'fcitx:///file/css/{css_name}'
    out = io.StringIO()
    out.write(conf_text(src.stem, description, css_name))
    c.write(out, space_around_delimiters=False)
    return out.getvalue()


def description_of(conf_path):
    """Pull the human-readable line from the upstream banner, if present."""
    for line in conf_path.read_text().splitlines()[:4]:
        if line.startswith('#') and '·' in line:
            return line.lstrip('# ').strip()
        if line.startswith('#') and '—' in line and 'generated' not in line:
            return line.lstrip('# ').strip()
    return conf_path.stem


def main(install_css=False):
    confs = sorted(SOURCE.glob('theme/*.conf'))
    if not confs:
        raise SystemExit(f'No source themes found under {SOURCE}')
    css_src_dir = SOURCE / 'www/css'
    out_css = PACK / 'css'
    out_css.mkdir(parents=True, exist_ok=True)
    installed = 0
    written = []
    for conf in confs:
        stem = conf.stem                       # e.g. Dopamine-Citrus
        # The source pack does not derive the CSS name from the conf name
        # (e.g. ArtDeco-EmeraldGold -> signature-artdeco-emeraldgold.css), so
        # honour each conf's own UserCss instead of guessing.
        src = configparser.ConfigParser(interpolation=None)
        src.optionxform = str
        src.read(conf)
        upstream_css = src['Advanced']['UserCss'].rsplit('/', 1)[-1]
        src_css = css_src_dir / upstream_css
        if not src_css.is_file():
            raise SystemExit(f'Missing CSS for {conf.name}: expected {src_css.name}')
        css_name = f'guest-{stem.lower()}.css'
        text = rewrite_conf(conf, css_name, description_of(conf))
        (ROOT / f'{PREFIX}{stem}.conf').write_text(text)
        (out_css / css_name).write_text(src_css.read_text())
        written.append((stem, css_name))
        if install_css:
            live = ROOT.parent / 'www/css' / css_name
            live.write_text(src_css.read_text())
            installed += 1
    print(f'Imported {len(written)} guest themes; CSS installed: {installed}')
    return written


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--install-css', action='store_true',
                   help='also copy CSS into ~/.local/share/fcitx5/www/css/')
    p.add_argument('--list', action='store_true', help='print imported themes')
    args = p.parse_args()
    for stem, css in main(install_css=args.install_css):
        if args.list:
            print(f'{PREFIX}{stem}.conf  ->  {css}')
