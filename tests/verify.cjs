const {chromium}=require('@playwright/test');
const fs=require('fs');
const assert=require('assert/strict');
const report={started:new Date().toISOString(),comparisons:[],interaction:[],errors:[],alignmentIssues:[]};
const target=process.env.QA_URL||'http://127.0.0.1:8766/';
const baseline='http://127.0.0.1:8767/';
const routes=['home','about','help','contact','safety','policy/terms','policy/privacy','policy/children','policy/community','policy/bullying','policy/cookies','law-enforcement'];
const selectors=['#site-header','.brand','.brand img','.desktop-nav','.header-tools','.language','.header-download','.menu-button','.screen-nav','.screen-nav button','.hero-copy h1','.hero-description','.hero-media-video','.scene-visual','.scene-artwork','.scene-copy h2','.scene-copy>p','.desktop-downloads .download-badge','.more-downloads','.page-intro','.page-intro>.wrap>p','.about-grid','.about-copy','.about-art','.about-values','.about-values article','.support-layout','.support-tabs','#faq-search','.contact-layout','.form-panel','#contact-form input','#contact-form textarea','#contact-form select','#contact-form button','.policy-list','.policy-nav','.app-identity','#site-footer','.entity-name','.entity-address','.footer-bottom','#mobile-home-downloads'];
async function ready(page,url){await page.goto(url,{waitUntil:'domcontentloaded'});await page.evaluate(async()=>{await document.fonts.ready;for(const img of document.images)img.loading='eager';await Promise.all([...document.images].map(img=>img.decode().catch(()=>{})));});await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));}
async function rects(page){return page.evaluate(selectors=>Object.fromEntries(selectors.map(s=>[s,[...document.querySelectorAll(s)].filter(e=>!e.closest('.loop-clone')&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().width>0).map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(n=>Math.round(n*100)/100);})])),selectors);}
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.QA_CHANNEL||'chrome'});
 fs.mkdirSync('tests/screenshots',{recursive:true});
 for(const [w,h] of [[1440,900],[390,844]]){
  const ctx=await browser.newContext({viewport:{width:w,height:h},reducedMotion:'reduce'});
  await ctx.route('**/*',route=>route.request().resourceType()==='media'?route.abort():route.continue());
  const product=await ctx.newPage(),source=await ctx.newPage();
  product.on('pageerror',e=>report.errors.push({w,error:e.message}));
  product.on('response',r=>{if(r.status()>=400)report.errors.push({w,status:r.status(),url:r.url()});});
  for(const lang of ['en','zh','hi','id']){
   for(const route of routes){
    await Promise.all([ready(product,`${target}?lang=${lang}#/${route}`),ready(source,`${baseline}?lang=${lang}#/${route}`)]);
    const [a,b]=await Promise.all([rects(product),rects(source)]);
    const differences=[];
    for(const s of selectors){
     if(a[s].length!==b[s].length){differences.push({s,count:[a[s].length,b[s].length]});continue;}
     a[s].forEach((r,i)=>{const delta=r.map((n,j)=>Math.round((n-b[s][i][j])*100)/100);if(delta.some(n=>Math.abs(n)>.6))differences.push({s,i,actual:r,reference:b[s][i],delta});});
    }
    const issues=await product.evaluate(()=>window.EZPZ_ALIGNMENT?.issues||[]);
    if(issues.length)report.alignmentIssues.push({w,lang,route,issues});
    const horizontal=await product.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
    if(horizontal)differences.push({horizontalOverflow:true});
    report.comparisons.push({w,h,lang,route,differences});
    fs.writeFileSync('tests/report.json',JSON.stringify(report,null,2));
    if(lang==='zh'&&['home','about','contact','safety'].includes(route))await product.screenshot({path:`tests/screenshots/${w}-${route}-zh.png`,fullPage:true});
   }
   console.log('Compared',w,lang,'all routes');
  }
  // Real user paths, with network-free checks for the external destination dispatch.
  await ready(product,`${target}?lang=zh#/home`);
  for(let i=0;i<6;i++){
   await product.locator(`.screen-nav [data-slide="${i}"]`).click();await product.waitForTimeout(200);
   assert.equal(await product.locator(`.screen-nav [data-slide="${i}"]`).getAttribute('aria-current'),'true');
   if(i===1||i===5)await product.screenshot({path:`tests/screenshots/${w}-scene-${i}-zh.png`,fullPage:true});
  }
  await product.locator('.screen-nav [data-slide="0"]').click();
  const downloads= w<680?product.locator('#mobile-home-downloads'):product.locator('#hello .desktop-downloads').first();
  await downloads.locator('[data-action="more-downloads"]').click();
  assert.deepEqual(await product.locator('#dialog-root [data-channel]').evaluateAll(es=>es.map(e=>e.dataset.channel)),['xiaomi','oppo','vivo','huawei']);
  await product.locator('#dialog-root [data-channel="huawei"]').click();assert.match(await product.locator('#toast').innerText(),/待官方确认/);
  await product.keyboard.press('Escape');
  await product.evaluate(()=>{window.open=(url)=>{window.__destination=url;return null;};});
  await downloads.locator('[data-channel="google"]').click();assert.equal(await product.evaluate(()=>window.__destination),'https://play.google.com/store/apps/details?id=com.party.ezpz');
  await downloads.locator('[data-channel="apple"]').click();assert.equal(await product.evaluate(()=>window.__destination),'https://apps.apple.com/bh/app/ezpz-dera/id1625619255');
  await downloads.locator('[data-channel="apk"]').click();assert.match(await product.locator('#toast').innerText(),/待官方确认/);
  if(w>680){await product.locator('.recharge').click();assert.match(await product.locator('#toast').innerText(),/未发起任何支付/);}
  await product.locator('#language').selectOption('id');assert.equal(await product.locator('html').getAttribute('lang'),'id');await product.reload();assert.equal(await product.locator('#language').inputValue(),'zh');
  await ready(product,`${target}#/home`);assert.equal(await product.locator('#language').inputValue(),'id');
  await ready(product,`${target}?lang=zh#/help`);
  await product.locator('#faq-search').fill('zzzznomatch');assert.equal(await product.locator('.faq-item').count(),0);
  await product.locator('#faq-search').fill('');assert.ok(await product.locator('.faq-item').count()>0);
  await product.locator('[data-category="payment"]').click();assert.ok(await product.locator('.faq-item').count()>0);
  await ready(product,`${target}?lang=zh#/contact`);
  assert.equal(await product.locator('#contact-form').evaluate(e=>e.checkValidity()),false);
  await product.locator('[name="name"]').fill('Preview review');await product.locator('[name="email"]').fill('review@example.com');await product.locator('[name="message"]').fill('This is a local preview validation test.');await product.locator('[name="consent"]').check();
  await product.locator('#contact-form button').click();assert.ok(await product.locator('#contact-form').isHidden());assert.match(await product.locator('#form-result').innerText(),/预览|未|不会/);
  await product.locator('[data-action="cookies"]:visible').first().click();await product.locator('#analytics-choice').check();await product.locator('[data-action="cookie-save"]').click();
  assert.equal(await product.evaluate(()=>JSON.parse(localStorage.getItem('ezpz-preview-cookies')).analytics),true);
  await product.locator('[data-action="cookies"]:visible').first().click();assert.equal(await product.locator('#analytics-choice').isChecked(),true);await product.locator('[data-action="cookie-reject"]').click();assert.equal(await product.evaluate(()=>JSON.parse(localStorage.getItem('ezpz-preview-cookies')).analytics),false);
  if(w<680){await product.locator('#menu-toggle').click();assert.equal(await product.locator('#menu-toggle').getAttribute('aria-expanded'),'true');await product.keyboard.press('Escape');assert.equal(await product.locator('#menu-toggle').getAttribute('aria-expanded'),'false');}
  report.interaction.push({w,checks:'six slides; seven download channels; unknown destinations; language + persistence; FAQ search + category; required form fields + valid preview; cookies save/reject + persistence; mobile menu',passed:true});
  await ctx.close();
 }
 await browser.close();
 report.summary={comparisons:report.comparisons.length,geometryFailures:report.comparisons.filter(x=>x.differences.length).length,textOverflowGroups:report.alignmentIssues.length,errors:report.errors.length};
 fs.writeFileSync('tests/report.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report.summary));
 if(report.summary.geometryFailures||report.summary.textOverflowGroups||report.summary.errors)process.exitCode=1;
})().catch(e=>{report.fatal=String(e.stack);fs.writeFileSync('tests/report.json',JSON.stringify(report,null,2));console.error(e);process.exit(1);});
