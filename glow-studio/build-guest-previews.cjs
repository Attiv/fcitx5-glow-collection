#!/usr/bin/env node
// Render preview galleries for the imported Guest Collection.
//
// Reuses the same Fcitx5 candidate-panel DOM as the Glow preview so the shots
// reflect the real stylesheet behaviour. Outputs:
//
//   screenshots/guest-dark.png         one tall contact sheet, dark mode
//   screenshots/guest-light.png        one tall contact sheet, light mode
//   screenshots/families/<family>.png  per-style-family strip (linked from README)
//
// Run trim-previews.py afterwards to crop the surrounding whitespace and shrink
// the files; raw Playwright output is ~4x larger.
//
// Run:  PLAYWRIGHT_MODULE=/path/to/playwright node build-guest-previews.cjs
const { webkit } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');

const PACK = __dirname;                       // glow-studio/
const ROOT = path.resolve(PACK, '..');        // repository root
const CSS_DIR = path.join(PACK, 'css');
const OUT = path.join(PACK, 'screenshots');

// Guest themes are vertical, 15px, paging hidden, with a "●" mark style.
const CANDIDATES = [
  ['灵感', 'líng gǎn'],
  ['灵光', 'líng guāng'],
  ['灵动', 'líng dòng'],
  ['灵巧', 'líng qiǎo'],
];

function panelHTML(css, mode, { compact }) {
  const items = CANDIDATES.map(([word, pinyin], i) => {
    const sel = i === 0 ? ' fcitx-highlighted' : '';
    return `<div class="fcitx-candidate${sel}" role="option" aria-selected="${i === 0}">
      <div class="fcitx-candidate-background"></div>
      <div class="fcitx-candidate-inner">
        <div class="fcitx-label">${i + 1}</div>
        <div class="fcitx-text">${word}</div>
        <div class="fcitx-comment">${pinyin}</div>
      </div></div>`;
  }).join('');
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>
  html{color-scheme:${mode}}
  html,body{margin:0;background:transparent}
  body{display:flex;align-items:center;justify-content:center;padding:${compact ? 10 : 22}px;box-sizing:border-box;
       font-family:"PingFang SC","Helvetica Neue",sans-serif}
  #fcitx-theme{font-size:15px}
  .fcitx-panel{border:1px solid #0000;border-radius:10px;overflow:hidden;width:fit-content}
  .fcitx-panel-blur,.fcitx-header{background:transparent}
  .fcitx-preedit{font:13px "SF Mono",Menlo,monospace;display:flex;align-items:center;min-height:24px;
                 margin:5px;padding:4px 10px}
  .fcitx-caret{width:1px;height:14px;margin:0 2px}
  .fcitx-hoverables{display:flex;flex-direction:column}
  .fcitx-candidate{position:relative;min-width:${compact ? 190 : 250}px}
  .fcitx-candidate-background{position:absolute;width:100%;height:100%}
  .fcitx-candidate-inner{position:relative;box-sizing:content-box;display:flex;align-items:center;
                         min-height:24px;line-height:16px;margin:5px;padding:4px 10px;gap:5px;
                         white-space:pre-wrap;border-radius:5px}
  .fcitx-text{font:400 15px "PingFang SC",sans-serif}
  .fcitx-label{font:400 10px "SF Mono",Menlo,monospace}
  .fcitx-comment{font:400 11px "PingFang SC",sans-serif;margin-left:auto}
  .fcitx-mark{font-size:10px}
  </style><style>${css}</style></head><body>
  <div id="fcitx-theme" class="fcitx-macos fcitx-macos-15 fcitx-basic fcitx-${mode}">
    <div class="fcitx-panel"><div class="fcitx-panel-blur">
      <div class="fcitx-header"><div class="fcitx-preedit">
        <div class="fcitx-pre-caret">ling'gan</div>
        <div class="fcitx-caret fcitx-no-text"></div>
      </div></div>
      <div class="fcitx-hoverables fcitx-vertical" role="listbox">${items}</div>
    </div></div>
  </div></body></html>`;
}

function guestThemes() {
  return fs.readdirSync(CSS_DIR)
    .filter(f => f.startsWith('guest-') && f.endsWith('.css'))
    .sort()
    .map(f => {
      const name = path.basename(f, '.css');            // guest-dopamine-citrus
      const stem = name.slice('guest-'.length);          // dopamine-citrus
      const conf = path.join(ROOT, `Guest-${stem}.conf`);
      const parts = stem.split('-');
      const label = parts.slice(1).join(' ') || parts[0];
      return {
        id: stem,
        name,
        family: parts[0],
        label: label.replace(/\b\w/g, c => c.toUpperCase()),
        css: fs.readFileSync(path.join(CSS_DIR, f), 'utf8'),
      };
    });
}

function contactSheet(themes, mode) {
  const cards = themes.map(t => `
    <figure class="card">
      <div class="shot"><iframe srcdoc="${escapeAttr(panelHTML(t.css, mode, { compact: true }))}"></iframe></div>
      <figcaption><b>${t.label}</b><span>${t.family}</span></figcaption>
    </figure>`).join('');
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>
  *{box-sizing:border-box}
  body{margin:0;background:${mode === 'dark' ? '#141614' : '#eef0ea'};
       font-family:"PingFang SC","Helvetica Neue",sans-serif;
       color:${mode === 'dark' ? '#e9eadf' : '#22261f'}}
  .sheet{padding:36px 40px 44px}
  .head{display:flex;align-items:baseline;gap:14px;border-bottom:1px solid ${mode === 'dark' ? '#333a31' : '#ccd2c4'};padding-bottom:16px;margin-bottom:26px}
  .head h1{font-size:19px;margin:0;font-weight:600;letter-spacing:.2px}
  .head span{font-size:12px;opacity:.6}
  .grid{display:grid;grid-template-columns:repeat(5,1fr);gap:18px 16px}
  .card{margin:0;background:${mode === 'dark' ? '#1c1f1b' : '#ffffff'};
        border:1px solid ${mode === 'dark' ? '#2c322a' : '#dde1d6'};border-radius:10px;
        padding:12px 10px 9px;display:flex;flex-direction:column;gap:9px}
  .shot{display:flex;align-items:center;justify-content:center;min-height:186px}
  iframe{border:0;width:100%;height:186px;background:transparent}
  figcaption{display:flex;justify-content:space-between;align-items:baseline;gap:6px;font-size:10.5px}
  figcaption b{font-weight:600}
  figcaption span{opacity:.5;font-family:"SF Mono",Menlo,monospace;font-size:9.5px}
  </style></head><body><div class="sheet">
  <div class="head"><h1>Guest Collection · 71 套</h1><span>${mode === 'dark' ? 'DARK' : 'LIGHT'} · 纵排 · 静态低对比背景 · 隐藏翻页按钮</span></div>
  <div class="grid">${cards}</div></div></body></html>`;
}

function familyStrip(themes, family, mode) {
  const cards = themes.map(t => `
    <figure class="card">
      <div class="shot"><iframe srcdoc="${escapeAttr(panelHTML(t.css, mode, { compact: false }))}"></iframe></div>
      <figcaption>${t.label}</figcaption>
    </figure>`).join('');
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>
  *{box-sizing:border-box}
  body{margin:0;background:${mode === 'dark' ? '#141614' : '#eef0ea'};
       font-family:"PingFang SC","Helvetica Neue",sans-serif;color:${mode === 'dark' ? '#e9eadf' : '#22261f'}}
  .strip{padding:22px 24px 24px}
  .grid{display:grid;grid-template-columns:repeat(${Math.min(themes.length, 4)},1fr);gap:16px}
  .card{margin:0;display:flex;flex-direction:column;gap:9px}
  .shot{display:flex;align-items:center;justify-content:center;min-height:196px;
        background:${mode === 'dark' ? '#1c1f1b' : '#ffffff'};
        border:1px solid ${mode === 'dark' ? '#2c322a' : '#dde1d6'};border-radius:10px;padding:8px}
  iframe{border:0;width:100%;height:196px;background:transparent}
  figcaption{font-size:11.5px;font-weight:600;text-align:center}
  </style></head><body><div class="strip"><div class="grid">${cards}</div></div></body></html>`;
}

function escapeAttr(s) {
  return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
}

(async () => {
  const only = process.argv[2] && process.argv[2].toLowerCase();   // optional family filter
  const themes = guestThemes().filter(t => !only || t.family === only);
  const browser = await webkit.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 2 });
  const problems = [];
  page.on('pageerror', e => problems.push(e.message));

  async function shoot(html, file, opts = {}) {
    await page.setContent(html, { waitUntil: 'load' });
    await page.waitForFunction(n => document.querySelectorAll('iframe').length === n,
      (html.match(/<iframe/g) || []).length);
    const frames = page.frames().filter(f => f !== page.mainFrame());
    for (const f of frames) {
      await f.waitForSelector('.fcitx-highlighted .fcitx-candidate-inner');
      const ok = await f.evaluate(() => {
        const i = document.querySelector('.fcitx-highlighted .fcitx-candidate-inner');
        const bg = getComputedStyle(i).backgroundImage || getComputedStyle(i).backgroundColor;
        return bg && bg !== 'none';
      });
      if (!ok) problems.push('unpainted frame in ' + file);
    }
    fs.mkdirSync(path.dirname(file), { recursive: true });
    await page.screenshot({ path: file, fullPage: true });
    return frames.length;
  }

  const results = { dark: 0, light: 0, families: [] };

  if (!only) {
    results.dark = await shoot(contactSheet(themes, 'dark'), path.join(OUT, 'guest-dark.png'));
    results.light = await shoot(contactSheet(themes, 'light'), path.join(OUT, 'guest-light.png'));
  }

  const fams = [...new Set(themes.map(t => t.family))].sort();
  for (const fam of fams) {
    const group = themes.filter(t => t.family === fam);
    const n = await shoot(familyStrip(group, fam, 'dark'),
      path.join(OUT, 'families', `${fam.toLowerCase()}.png`));
    results.families.push([fam, n]);
  }

  await browser.close();
  console.log(JSON.stringify({ ...results, problems }, null, 1));
})();
