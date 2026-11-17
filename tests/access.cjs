const {chromium}=require('@playwright/test');
const {pathToFileURL}=require('url');
const path=require('path'),fs=require('fs'),assert=require('assert/strict');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const results=[];
 for(const [mode,url] of [['offline',pathToFileURL(path.resolve('dist/index.html')).href],['anonymous-online',process.env.PUBLIC_URL||'https://meiliyitian2020-cyber.github.io/ezpz-website-preview/']]){
  const ctx=await browser.newContext({storageState:{cookies:[],origins:[]},serviceWorkers:'block'});
  for(const [width,height] of [[1440,900],[390,844]]){
   const p=await ctx.newPage({viewport:{width,height}});await p.setViewportSize({width,height});const errors=[];const requests=[];
   p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
   p.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url());});
   p.on('request',r=>requests.push(r.url()));
   const response=await p.goto(url+'?lang=zh#/home',{waitUntil:'domcontentloaded'});
   await p.evaluate(async()=>{await document.fonts.ready;for(const img of document.images)img.loading='eager';await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});await p.waitForTimeout(300);
   if(mode==='anonymous-online')assert.equal(response.status(),200);
   assert.match(await p.title(),/Ezpz/);assert.match(await p.locator('html').getAttribute('lang'),/^zh(?:-CN)?$/);
   assert.ok((await p.locator('#site-header .brand img').getAttribute('src')).includes('ezpz-logo.svg'));
   assert.ok((await p.locator('#hello .hero-loop-freeze').first().getAttribute('src')).includes('placeholder'));
   assert.equal(await p.locator('.home-slide:not(.loop-clone)').count(),6);
   await p.screenshot({path:`tests/screenshots/${mode}-${width}-zh.png`,fullPage:true});
   await p.goto(url+'?lang=zh#/contact',{waitUntil:'domcontentloaded'});await p.locator('#contact-form').waitFor();
   assert.equal(await p.locator('#contact-form').evaluate(f=>f.checkValidity()),false);
   assert.equal(errors.length,0,JSON.stringify(errors));
   results.push({mode,width,height,httpStatus:response?.status()||null,finalUrl:response?.url()||p.url(),title:await p.title(),initialCookies:0,scriptAndConsoleErrors:errors,passed:true,networkRequests:requests.filter(u=>/^https?:/.test(u)).length});await p.close();
  }
  await ctx.close();
 }
 await browser.close();fs.writeFileSync('tests/access.json',JSON.stringify({verifiedAt:new Date().toISOString(),results},null,2));console.log(JSON.stringify(results));
})().catch(e=>{console.error(e);process.exit(1);});
