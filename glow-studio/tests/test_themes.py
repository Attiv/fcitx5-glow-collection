import configparser
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'glow-studio'

class ThemeTests(unittest.TestCase):
    def themes(self):
        files = sorted(ROOT.glob('Glow-*.conf'))
        self.assertEqual(len(files), 14, 'Fourteen importable themes must exist')
        return files

    def test_fourteen_themes_with_two_modes(self):
        self.assertEqual({'Hologram', 'Porcelain'} - {f.stem.removeprefix('Glow-') for f in self.themes()}, set())
        for f in self.themes():
            c = configparser.ConfigParser(interpolation=None)
            c.read(f)
            for mode in ('LightMode', 'DarkMode'):
                self.assertEqual(c[mode]['OverrideDefault'], 'True')
                for key in ('PanelColor', 'HighlightColor', 'HighlightTextColor', 'TextColor', 'LabelColor'):
                    self.assertRegex(c[mode][key], r'^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$')
            self.assertEqual(c['DarkMode']['SameWithLightMode'], 'False')
            self.assertEqual(c['Basic']['Theme'], 'System')
            self.assertEqual(c['Background']['Blur'], 'System')
            self.assertNotIn('ScrollMode', c)

    def test_css_is_installed_and_self_contained(self):
        for f in self.themes():
            c = configparser.ConfigParser(interpolation=None)
            c.read(f)
            uri = c['Advanced']['UserCss']
            self.assertTrue(uri.startswith('fcitx:///file/css/glow-'))
            name = uri.rsplit('/', 1)[-1]
            css = (PACK / 'css' / name).read_text()
            self.assertEqual(css, (ROOT.parent / 'www/css' / name).read_text())
            self.assertNotRegex(css, r'@import|url\(|:selected|\.fcitx-candidate-list')
            self.assertIn('.fcitx-candidate.fcitx-highlighted', css)
            self.assertIn('box-shadow:', css)
            self.assertIn('prefers-reduced-motion: reduce', css)
            self.assertNotRegex(css, r'(?m)^\s*(width|height|min-width|max-width|transform|padding|margin)\s*:')
            self.assertEqual(css.count('{'), css.count('}'))

    def test_original_files_unchanged(self):
        for path, sha in json.loads((PACK / 'original-hashes.json').read_text()).items():
            resolved = Path(path).expanduser()
            self.assertTrue(resolved.is_file(), f'{path} is missing')
            self.assertEqual(hashlib.sha256(resolved.read_bytes()).hexdigest(), sha, path)

    def test_palette_contrast(self):
        source = PACK / 'palettes.json'
        self.assertTrue(source.exists(), 'Theme palette data must exist')
        def luminance(color):
            rgb = [int(color[i:i+2],16)/255 for i in (1,3,5)]
            rgb = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
            return sum(a*b for a,b in zip(rgb,[.2126,.7152,.0722]))
        def ratio(a,b):
            x,y=sorted([luminance(a),luminance(b)])
            return (y+.05)/(x+.05)
        for theme in json.loads(source.read_text()):
            for mode in ('light', 'dark'):
                p=theme[mode]
                for fg,bg in ((p['text'],p['panel']),(p['muted'],p['panel']), (p['text'],p['panel_end']), (p['muted'],p['panel_end']), (p['selected_text'],p['selection']), (p['selected_text'],p['selection_end'])):
                    self.assertGreaterEqual(ratio(fg,bg),4.5, (theme['id'],mode,fg,bg))

    def test_preview_and_instructions_exist(self):
        self.assertTrue((PACK / 'preview.html').is_file(), 'Offline preview must exist')
        self.assertTrue((ROOT / 'README-Glow.md').is_file(), 'Chinese instructions must exist')

if __name__ == '__main__':
    unittest.main()
