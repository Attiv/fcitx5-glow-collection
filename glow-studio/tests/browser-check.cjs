// Run with PLAYWRIGHT_MODULE pointing to an installed playwright module if needed.
const { webkit } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const pack = path.resolve(__dirname, '..');
const themes = JSON.parse(fs.readFileSync(path.join(pack, 'palettes.json'), 'utf8'));

(async () => {
  const browser = await webkit.launch({ headless: true });
  const page = await browser.newPage({ viewport: {width:1440, height:1050}, deviceScaleFactor:2 });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  const external=[];
  page.on('request', r => {if(/^https?:/.test(r.url())) external.push(r.url())});
  const checks=[];
  async function framesReady(count) {
    await page.waitForFunction(n=>document.querySelectorAll('iframe').length===n,count);
    const frames=page.frames().filter(f=>f!==page.mainFrame());
    assert.equal(frames.length,count);
    for(const f of frames) await f.locator('.fcitx-highlighted .fcitx-candidate-inner').waitFor();
    return frames;
  }
  const paint = f => f.locator('.fcitx-candidate-inner').evaluateAll(es=>es.map(e=>({background:getComputedStyle(e).backgroundImage,shadow:getComputedStyle(e).boxShadow,animation:getComputedStyle(e).animationName,radius:getComputedStyle(e).borderRadius})));
  try {
    await page.goto(pathToFileURL(path.join(pack, 'preview.html')).href);
    const n=themes.length;
    let frames=await framesReady(n);
    for(let i=0;i<frames.length;i++) {
      const f=frames[i];
      assert.equal(await f.evaluate(()=>getComputedStyle(document.documentElement).colorScheme), 'dark', 'Preview iframe color scheme must match its host to keep the canvas transparent');
      let style=await paint(f);
      assert.notEqual(style[0].shadow,'none',themes[i].id+' selected glow');
      assert.match(style[0].background,/linear-gradient/);
      assert.equal(style[1].shadow,'none',themes[i].id+' unselected does not glow');
      assert.equal(style[0].animation, themes[i].motion==='pulse'?'gs-breathe':themes[i].motion==='flow'?'gs-flow':'none');
      const before=await f.locator('.fcitx-panel').evaluate(e=>{const b=e.getBoundingClientRect();return {x:b.x,y:b.y,width:b.width,height:b.height}});
      await f.locator('.fcitx-candidate').nth(1).click();
      await f.waitForFunction(()=>document.querySelectorAll('.fcitx-highlighted').length===1 && document.querySelectorAll('.fcitx-candidate')[1].classList.contains('fcitx-highlighted'));
      // End shadow transition before validating deselection.
      await f.waitForFunction(()=>getComputedStyle(document.querySelector('.fcitx-candidate-inner')).boxShadow==='none');
      style=await paint(f);
      assert.notEqual(style[1].shadow,'none');
      assert.equal(style[0].shadow,'none');
      const after=await f.locator('.fcitx-panel').evaluate(e=>{const b=e.getBoundingClientRect();return {x:b.x,y:b.y,width:b.width,height:b.height}});
      assert.deepEqual(after,before,themes[i].id+' selection must not move/resize panel');
      await f.locator('.fcitx-candidate').nth(1).press('ArrowRight');
      assert.equal(await f.locator('.fcitx-candidate').nth(2).getAttribute('aria-selected'),'true');
      checks.push(themes[i].id+': selected-only glow, keyboard navigation, stable geometry, correct animation');
    }
    await page.locator('#reset').click(); await framesReady(n);
    await page.screenshot({path:path.join(pack,'screenshots','dark-gallery.png'),fullPage:true});
    await page.selectOption('#mode','light'); await framesReady(n);
    await page.screenshot({path:path.join(pack,'screenshots','light-gallery.png'),fullPage:true});
    await page.selectOption('#mode','both'); frames=await framesReady(n*2);
    for(const f of frames) {
      const result=await f.evaluate(()=>({dark:document.querySelector('#fcitx-theme').classList.contains('fcitx-dark'),s:getComputedStyle(document.querySelector('.fcitx-highlighted .fcitx-text')).color,overflow:document.documentElement.scrollWidth>innerWidth}));
      assert.equal(result.overflow,false,'horizontal candidates fit the preview frame');
    }
    checks.push(`${n*2} light/dark preview frames render without horizontal clipping at 1440px viewport`);
    await page.selectOption('#layout','vertical'); frames=await framesReady(n*2);
    for(const f of frames) {
      const boxes=await f.locator('.fcitx-candidate').evaluateAll(es=>es.map(e=>{let b=e.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height}}));
      assert.ok(boxes[1].y>boxes[0].y); assert.equal(boxes[0].x,boxes[1].x);
      assert.equal(await f.locator('.fcitx-comment').count(),4);
    }
    await page.selectOption('#mode','dark'); await framesReady(n);
    await page.screenshot({path:path.join(pack,'screenshots','vertical-gallery.png'),fullPage:true});
    checks.push(`${n*2} vertical palettes with comments render correctly`);
    await page.selectOption('#mode','both'); frames=await framesReady(n*2);
    await page.emulateMedia({reducedMotion:'reduce'});
    for(const f of frames) {
      const style=await paint(f);assert.equal(style[0].animation,'none');assert.notEqual(style[0].shadow,'none');
    }
    checks.push('System prefers-reduced-motion disables all animations while preserving selected glow');
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.locator('#motion').uncheck();frames=await framesReady(n*2);
    for(const f of frames) assert.equal((await paint(f))[0].animation,'none');
    checks.push('Manual motion toggle produces static glow');
    assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
    checks.push('No browser script errors; no network asset requests');
    const result={engine:'Playwright WebKit',version:browser.version(),checks,passed:checks.length,errors,externalRequests:external};
    fs.writeFileSync(path.join(pack,'browser-results.json'),JSON.stringify(result,null,2)+'\n');
    console.log(JSON.stringify(result,null,2));
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1});
