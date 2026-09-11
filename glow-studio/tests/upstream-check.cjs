// Integration with freshly compiled official Fcitx5 webview SCSS.
// FCITX_BASE_CSS=/path/to/compiled/style.css PLAYWRIGHT_MODULE=... node this-file
// Official SCSS is a test input; it is not bundled with these original themes.
const {webkit}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const pack=path.resolve(__dirname,'..');
const base=fs.readFileSync(process.env.FCITX_BASE_CSS,'utf8');
const themes=JSON.parse(fs.readFileSync(path.join(pack,'palettes.json'),'utf8'));
const kebab=s=>s.replace(/([a-z])([A-Z])/g,'$1-$2').toLowerCase();
(async()=>{
 const browser=await webkit.launch();const page=await browser.newPage({viewport:{width:900,height:750},reducedMotion:'reduce'});
 let count=0;
 try{
 for(const t of themes) for(const version of ['15','26']) for(const mode of ['light','dark']) for(const layout of ['horizontal','vertical','scroll']){
  const p=t[mode],scroll=layout==='scroll';
  const vars={'border-width':'1px','border-radius':t.radius+'px','margin':'5px','middle-margin':'2.5px','highlight-radius':t.selected_radius.split(' ')[0]+'px','top-padding':'4px','bottom-padding':'4px','left-padding':'10px','right-padding':'10px','label-text-gap':'6px','vertical-min-width':'220px','cell-width':'65px','horizontal-divider-width':'0px','max-row':'6','max-column':'6','text-font-family':'"PingFang SC", sans-serif','text-font-size':'16px','label-font-size':'11px','comment-font-size':'12px','preedit-font-size':'14px','mark-opacity':'0','text-font-weight':'500'};
  for(const m of ['light','dark'])for(const [k,v] of Object.entries({'panel-color':t[m].panel,'panel-color-no-image':t[m].panel,'text-color':t[m].text,'label-color':t[m].muted,'comment-color':t[m].muted,'highlight-color':t[m].selection,'highlight-text-color':t[m].selected_text,'highlight-label-color':t[m].selected_text,'highlight-comment-color':t[m].selected_text,'preedit-color-pre-caret':t[m].text,'preedit-color-post-caret':t[m].muted,'preedit-color-caret':t[m].accent,'panel-border-color':t[m].border}))vars[m+'-'+k]=v;
  const cells=Array.from({length:scroll?18:4},(_,i)=>`<div class="fcitx-candidate fcitx-hoverable ${i===0?'fcitx-candidate-first fcitx-highlighted':''} ${i===3&&!scroll?'fcitx-candidate-last':''}" ${scroll?'style="width:130px"':''}><div class="fcitx-candidate-background"></div><div class="fcitx-candidate-inner fcitx-hoverable-inner"><div class="fcitx-label">${i+1}</div><div class="fcitx-text">${['灵感','候选词','企鹅','Apple'][i%4]}</div>${layout==='vertical'?'<div class="fcitx-comment">pinyin</div>':''}</div></div>`).join('');
  const doc=`<!doctype html><meta charset="utf-8"><style>body{background:#808080;margin:0}</style><style>${base}</style><div id="fcitx-theme" class="fcitx-macos fcitx-macos-${version} fcitx-basic fcitx-${mode} fcitx-blue" style="${Object.entries(vars).map(([k,v])=>'--'+k+':'+v.replaceAll('"','&quot;')).join(';')}"><div class="fcitx-decoration"><div class="fcitx-panel-center"><div class="fcitx-panel fcitx-horizontal-tb"><div class="fcitx-panel-blur"><div class="fcitx-header"><div class="fcitx-preedit"><div class="fcitx-pre-caret">ling'gan</div><div class="fcitx-caret fcitx-no-text"></div></div></div><div class="fcitx-hoverables fcitx-${layout==='vertical'?'vertical':'horizontal'} ${scroll?'fcitx-horizontal-scroll':''}">${scroll?'<div class="fcitx-scroll-area">'+cells+'</div>':cells}</div></div></div></div></div></div>`;
  await page.setContent(doc);
  const geometry=()=>page.locator('.fcitx-panel,.fcitx-hoverables,.fcitx-candidate,.fcitx-candidate-inner').evaluateAll(es=>es.map(e=>{const b=e.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height}}));
  const before=await geometry();
  await page.addStyleTag({content:fs.readFileSync(path.join(pack,'css','glow-'+t.id.toLowerCase()+'.css'),'utf8')});
  const after=await geometry();
  assert.deepEqual(after,before,`${t.id} macOS-${version}/${mode}/${layout}: CSS must preserve geometry`);
  const paint=await page.locator('.fcitx-candidate-inner').evaluateAll(es=>es.slice(0,2).map(e=>({shadow:getComputedStyle(e).boxShadow,bg:getComputedStyle(e).backgroundImage,anim:getComputedStyle(e).animationName})));
  assert.notEqual(paint[0].shadow,'none');assert.match(paint[0].bg,/linear-gradient/);assert.equal(paint[1].shadow,'none');assert.equal(paint[0].anim,'none');
  count++;
 }
 const result={engine:'Playwright WebKit '+browser.version(),base:'Official fcitx5-webview SCSS compiled from master (fetched 2026-09-10)',scenarios:count,variants:`${themes.length} themes × 2 macOS base styles × 2 color modes × 3 layouts`,checks:['CSS does not alter panel, candidate or scrolling geometry','Only selected candidate receives glow and gradient','Reduced motion remains honored under upstream rules'],nativeIME:false};
 fs.writeFileSync(path.join(pack,'upstream-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
