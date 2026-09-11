#!/usr/bin/env python3
"""Build the local Fcitx5 Glow Collection. No running settings are modified.
Use --install-css to copy the generated CSS to Fcitx5's local www/css folder.
"""
import argparse
import configparser
import html
import json
from pathlib import Path

PACK = Path(__file__).resolve().parent
ROOT = PACK.parent
SIGNATURE = 'Fcitx5 Glow Collection — generated'


def rgba(value, alpha):
    return 'rgba(' + ', '.join(str(int(value[i:i+2], 16)) for i in (1, 3, 5)) + f', {alpha})'


def safe_write(path, content, signature=SIGNATURE):
    if path.exists() and signature not in path.read_text():
        raise RuntimeError(f'Refusing to overwrite an unrelated file: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def css_for(t):
    out = [f'/* {SIGNATURE}\n * {t["name"]} | {t["effect"]}\n * Only paint is customized. Native geometry and scrolling stay intact.\n * Set --gs-motion: none to keep the glow static.\n */']
    for mode in ('light', 'dark'):
        p=t[mode]
        surface=f'linear-gradient(145deg, {p["panel"]}, {p["panel_end"]})'
        ring=f'inset 0 0 0 1px {rgba(p["accent"], .45)}'
        if t['material']=='glass':
            surface=f'linear-gradient(145deg, {rgba(p["panel"], .94)}, {rgba(p["panel_end"], .90)})'
            ring=f'inset 0 1px 0 {rgba("#ffffff", .58)}, inset 0 0 0 1px {rgba(p["accent"], .6)}'
        elif t['material']=='neon':
            ring=f'inset 2px 0 0 {p["accent"]}, inset -2px 0 0 #ed68cf, inset 0 0 0 1px {rgba(p["accent"], .5)}'
        elif t['material'] in ('terminal','phosphor'):
            surface=f'repeating-linear-gradient(0deg, transparent 0px, transparent 3px, {rgba(p["accent"], .035)} 3px, {rgba(p["accent"], .035)} 4px), {surface}'
            ring=f'inset 0 -2px 0 {rgba(p["accent"], .85)}, inset 0 0 0 1px {rgba(p["accent"], .45)}'
        elif t['material']=='gold':
            ring=f'inset 0 1px 0 {rgba("#fff2bd", .65)}, inset 0 0 0 1px {rgba(p["accent"], .65)}'
        elif t['material']=='paper':
            surface=f'radial-gradient(ellipse at top left, {rgba(p["accent"], .1)}, transparent 75%), {surface}'
        elif t['material']=='vampire':
            ring=f'inset 0 -2px 0 {rgba(p["accent"], .9)}, inset 0 0 0 1px {rgba("#9ce8cc", .5)}'
        elif t['material']=='hologram':
            surface=f'radial-gradient(circle at 12% 0%, {rgba(p["accent"], .16)}, transparent 48%), radial-gradient(circle at 92% 100%, {rgba("#f681ff", .10)}, transparent 52%), {surface}'
            ring=f'inset 2px 0 0 {rgba(p["accent"], .9)}, inset -2px 0 0 {rgba("#f681ff", .85)}, inset 0 0 0 1px {rgba(p["accent"], .5)}'
        elif t['material']=='porcelain':
            surface=f'radial-gradient(ellipse at 85% 0%, {rgba(p["accent"], .10)}, transparent 58%), {surface}'
            ring=f'inset 0 0 0 1px {rgba(p["accent"], .75)}, inset 0 -2px 0 {rgba(p["accent"], .7)}'
        selected=f'linear-gradient(115deg, {p["selection"]}, {p["selection_end"]})'
        if t['motion']=='flow':
            selected=f'linear-gradient(115deg, {p["selection"]}, {p["selection_end"]}, {p["selection"]})'
        lines={
          'surface':surface, 'text':p['text'], 'muted':p['muted'], 'accent':p['accent'],
          'border':p['border'], 'selected':selected, 'selected-text':p['selected_text'],
          'ring':ring, 'glow':rgba(p['accent'], .35 if mode=='dark' else .23),
          'glow-soft':rgba(p['accent'], .21 if mode=='dark' else .13),
          'glow-strong':rgba(p['accent'], .51 if mode=='dark' else .34),
          'hover':rgba(p['accent'], .12), 'panel-shadow':rgba('#000000', .28 if mode=='dark' else .13),
        }
        selector='#fcitx-theme, #fcitx-theme.fcitx-light' if mode=='light' else '#fcitx-theme.fcitx-dark'
        out.append(selector+' {\n'+'\n'.join(f'  --gs-{k}: {v};' for k,v in lines.items())+'\n}')
    out.append('''
/* Current and older Webview versions paint the panel in different layers. */
#fcitx-theme .fcitx-panel {
  background: var(--gs-surface) !important;
  border-color: var(--gs-border) !important;
  box-shadow: 0 6px 16px var(--gs-panel-shadow), inset 0 1px 0 rgba(255,255,255,.06) !important;
}
#fcitx-theme .fcitx-candidate-background,
#fcitx-theme .fcitx-panel-blur,
#fcitx-theme .fcitx-header,
#fcitx-theme .fcitx-preedit,
#fcitx-theme .fcitx-aux-up,
#fcitx-theme .fcitx-aux-down,
#fcitx-theme .fcitx-paging,
#fcitx-theme .fcitx-divider-side,
#fcitx-theme .fcitx-hoverables.fcitx-horizontal-scroll .fcitx-divider-middle {
  background-color: transparent !important;
}
#fcitx-theme .fcitx-text { color: var(--gs-text) !important; }
#fcitx-theme .fcitx-label,
#fcitx-theme .fcitx-comment { color: var(--gs-muted) !important; }
#fcitx-theme .fcitx-text,
#fcitx-theme .fcitx-label,
#fcitx-theme .fcitx-comment { text-shadow: none; }
#fcitx-theme .fcitx-preedit,
#fcitx-theme .fcitx-aux-up,
#fcitx-theme .fcitx-aux-down { color: var(--gs-text) !important; }
#fcitx-theme .fcitx-caret.fcitx-no-text {
  background-color: var(--gs-accent) !important;
  box-shadow: 0 0 5px var(--gs-glow);
}
#fcitx-theme .fcitx-candidate-inner {
  background: transparent !important;
  box-shadow: none;
  transition: box-shadow 160ms ease, background-color 160ms ease;
}
/* Paint the selected candidate above adjacent candidate backgrounds. No movement. */
#fcitx-theme .fcitx-candidate.fcitx-highlighted { z-index: 1; }
#fcitx-theme .fcitx-candidate.fcitx-highlighted .fcitx-candidate-inner {
  background: var(--gs-selected) !important;
  background-size: 220% 100% !important;
  box-shadow: var(--gs-ring), 0 0 6px var(--gs-glow), 0 0 12px var(--gs-glow-soft);
}
#fcitx-theme .fcitx-candidate.fcitx-highlighted .fcitx-text,
#fcitx-theme .fcitx-candidate.fcitx-highlighted .fcitx-label,
#fcitx-theme .fcitx-candidate.fcitx-highlighted .fcitx-comment {
  color: var(--gs-selected-text) !important;
}
#fcitx-theme .fcitx-candidate.fcitx-highlighted .fcitx-mark.fcitx-no-text {
  background-color: var(--gs-selected-text) !important;
  box-shadow: 0 0 5px var(--gs-glow);
}
/* Mouse hover is a quiet inset outline, never a second luminous selection. */
#fcitx-theme .fcitx-mousemoved .fcitx-candidate:not(.fcitx-highlighted):hover .fcitx-candidate-inner {
  box-shadow: inset 0 0 0 1px var(--gs-border);
}
#fcitx-theme .fcitx-paging .fcitx-hoverable-inner:hover {
  background: var(--gs-hover) !important;
}
#fcitx-theme .fcitx-contextmenu {
  background: var(--gs-surface) !important;
  border-color: var(--gs-border) !important;
  color: var(--gs-text) !important;
}
#fcitx-theme .fcitx-menu-item:hover {
  background: var(--gs-selected) !important;
  color: var(--gs-selected-text) !important;
}
''')
    out.append(f'#fcitx-theme .fcitx-candidate-inner {{ border-radius: {t["selected_radius"]}px !important; }}'.replace(' '.join(t['selected_radius'].split())+'px', ' '.join(v+'px' for v in t['selected_radius'].split())))
    # Unique low-amplitude light textures, without animating text or layout.
    if t['motion']=='pulse':
        out.append('''
@keyframes gs-breathe {
  0%, 100% { box-shadow: var(--gs-ring), 0 0 5px var(--gs-glow), 0 0 10px var(--gs-glow-soft); }
  50% { box-shadow: var(--gs-ring), 0 0 8px var(--gs-glow-strong), 0 0 15px var(--gs-glow-soft); }
}
#fcitx-theme .fcitx-candidate.fcitx-highlighted .fcitx-candidate-inner {
  animation: var(--gs-motion, gs-breathe 3.8s ease-in-out infinite);
}
''')
    elif t['motion']=='flow':
        out.append('''
@keyframes gs-flow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
#fcitx-theme .fcitx-candidate.fcitx-highlighted .fcitx-candidate-inner {
  animation: var(--gs-motion, gs-flow 7s ease-in-out infinite);
}
''')
    out.append('''
/* Honor macOS Reduce Motion. The static selected glow remains. */
@media (prefers-reduced-motion: reduce) {
  #fcitx-theme .fcitx-candidate-inner {
    animation: none !important;
    transition: none !important;
  }
}
''')
    return '\n'.join(out)


def conf_for(t):
    c=configparser.ConfigParser(interpolation=None)
    c.optionxform=str
    c['Basic']={'Theme':'System'}
    for mode in ('light','dark'):
        p=t[mode]
        d={'OverrideDefault':'True'}
        if mode=='dark': d['SameWithLightMode']='False'
        d.update(dict(HighlightColor=p['selection'],HighlightHoverColor=p['selection_end'],
            HighlightTextColor=p['selected_text'],HighlightTextPressColor=p['selected_text'],
            HighlightLabelColor=p['selected_text'],HighlightCommentColor=p['selected_text'],HighlightMarkColor=p['selected_text'],
            PanelColor=p['panel'],TextColor=p['text'],LabelColor=p['muted'],CommentColor=p['muted'],
            PagingButtonColor=p['muted'],DisabledPagingButtonColor=p['muted'],AuxColor=p['text'],
            PreeditColorPreCaret=p['text'],PreeditColorCaret=p['accent'],PreeditColorPostCaret=p['muted'],
            BorderColor=p['border'],DividerColor=p['panel']))
        c[mode.title()+'Mode']=d
    c['Typography']={'Layout':'Horizontal','WritingMode':'"Horizontal top-bottom"','TypographyAwarenessForIM':'False','VerticalCommentsAlignRight':'True','PagingButtonsStyle':'Arrow'}
    c['Background']={'ImageUrl':'','KeepPanelColorWhenHasImage':'False','Blur':'System','Shadow':'True'}
    c['Font']={'TextFontSize':'16','TextFontWeight':'500','LabelFontSize':'11','LabelFontWeight':'400','CommentFontSize':'12','CommentFontWeight':'400','PreeditFontSize':'14','PreeditFontWeight':'400'}
    regular=['PingFang SC','Helvetica Neue','sans-serif']
    font=['Songti SC','PingFang SC','serif'] if t['material']=='paper' else regular
    for category,families in [('Text',font),('Label',['SF Mono','Menlo','monospace']),('Comment',regular),('Preedit',['SF Mono','PingFang SC','monospace'])]:
        c[f'Font/{category}FontFamily']={str(i):('"'+f+'"' if ' ' in f else f) for i,f in enumerate(families)}
    c['Caret']={'Style':'Blink','Text':'‸'}
    c['Highlight']={'MarkStyle':'None','MarkText':'🐧','HoverBehavior':'None'}
    c['Size']={'OverrideDefault':'True','BorderWidth':'1','BorderRadius':str(t['radius']),'Margin':'5',
        'HighlightRadius':t['selected_radius'].split()[0],'TopPadding':'4','RightPadding':'10','BottomPadding':'4','LeftPadding':'10',
        'LabelTextGap':'6','VerticalMinWidth':'220','ScrollCellWidth':'65','HorizontalDividerWidth':'0'}
    c['Advanced']={'UserCss':f'fcitx:///file/css/glow-{t["id"].lower()}.css'}
    import io
    out=io.StringIO()
    out.write(f'# {SIGNATURE}\n# {t["name"]} — {t["description"]}\n# Import via Theme Editor. CSS path is bundled; do not remove it.\n')
    c.write(out,space_around_delimiters=False)
    return out.getvalue()


def build(install_css=False):
    themes=json.loads((PACK/'palettes.json').read_text())
    for t in themes:
        css=css_for(t)
        name=f'glow-{t["id"].lower()}.css'
        safe_write(PACK/'css'/name,css)
        safe_write(ROOT/f'Glow-{t["id"]}.conf',conf_for(t))
        if install_css: safe_write(ROOT.parent/'www/css'/name,css)
    template=(PACK/'preview-template.html').read_text()
    preview=template.replace('__THEMES_JSON__',json.dumps(themes,ensure_ascii=False)).replace('__STYLES_JSON__',json.dumps({t['id']:css_for(t) for t in themes},ensure_ascii=False))
    (PACK/'preview.html').write_text(preview)
    print(f'Built {len(themes)} themes with light/dark palettes; CSS installed: {install_css}')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--install-css',action='store_true')
    build(p.parse_args().install_css)
