// Keep source text slots and navigation widths fixed when product copy changes.
function alignProductSlots(){
 const reference=ALIGN_REFERENCE[lang];if(!reference)return;
 const issues=[];
 function reserve(element,referenceHtml){
  if(!element)return;
  element.style.removeProperty('height');element.style.removeProperty('min-height');
  const width=element.getBoundingClientRect().width;if(!width)return;
  const probe=element.cloneNode(false);probe.innerHTML=referenceHtml;
  probe.setAttribute('aria-hidden','true');probe.inert=true;
  Object.assign(probe.style,{position:'fixed',left:'0',top:'-99999px',width:width+'px',height:'auto',minHeight:'0',maxHeight:'none',visibility:'hidden',pointerEvents:'none'});
  element.parentElement.appendChild(probe);
  const height=probe.getBoundingClientRect().height,referenceScrollHeight=probe.scrollHeight;probe.remove();
  element.style.height=height+'px';element.style.minHeight=height+'px';
  if(element.scrollHeight>referenceScrollHeight+2)issues.push({selector:element.tagName+'.'+element.className,text:element.textContent,referenceHeight:height,actualHeight:element.scrollHeight});
 }
 reserve($('.entity-name'),'HAGO SINGAPORE PTE. LTD.');
 reserve($('.entity-address'),'30 PASIR PANJANG ROAD #15-31A MAPLETREE BUSINESS CITY SINGAPORE 117440');
 if(activePage==='home'){
  reserve($('#hello h1'),reference.home.title);reserve($('#hello .hero-description'),reference.home.description);
  reference.home.scenes.forEach(s=>{
   reserve($('#'+s.id+' .scene-copy h2'),s.title);reserve($('#'+s.id+' .scene-copy>p'),s.description);
  });
  const referenceLabels=[reference.nav.home,...reference.home.scenes.map(s=>s.title)];
  $$('.screen-nav button').forEach((button,i)=>{
   button.style.removeProperty('width');button.style.removeProperty('min-width');
   const probe=button.cloneNode(true);$('span',probe).textContent=referenceLabels[i];
   probe.setAttribute('aria-hidden','true');probe.inert=true;
   Object.assign(probe.style,{position:'fixed',left:'0',top:'-99999px',width:'auto',visibility:'hidden',pointerEvents:'none'});
   button.parentElement.appendChild(probe);const width=probe.getBoundingClientRect().width;probe.remove();
   button.style.width=width+'px';button.style.minWidth=width+'px';
  });
  fitMobileHome(true);
 }else{
  let introText=reference[activePage]?.intro;
  if(activePage.startsWith('policy/'))introText=reference.policyDescriptions[activePage.split('/')[1]];
  if(activePage==='law-enforcement')introText=reference.policyDescriptions.law;
  if(introText)reserve($('.page-intro>.wrap>p'),introText);
  const band=$('.download-band>.wrap');
  if(band){
   const probe=band.cloneNode(true);
   $('h2',probe).innerHTML=reference.home.downloadTitle;
   $('p',probe).innerHTML=reference.home.downloadText;
   for(const e of [probe.firstElementChild,$('h2',probe),$('p',probe)])e.removeAttribute('style');
   probe.setAttribute('aria-hidden','true');probe.inert=true;
   Object.assign(probe.style,{position:'fixed',left:'0',top:'-99999px',width:band.getBoundingClientRect().width+'px',visibility:'hidden',pointerEvents:'none'});
   band.parentElement.appendChild(probe);
   const width=probe.firstElementChild.getBoundingClientRect().width;probe.remove();
   band.firstElementChild.style.width=width+'px';
  }
  reserve($('.download-band h2'),reference.home.downloadTitle);
  reserve($('.download-band p'),reference.home.downloadText);
  if(activePage.startsWith('policy/')){
   const key=activePage.split('/')[1];
   const article=$('.legal-article');
   if(ALIGN_POLICIES[key]&&article){
    article.style.removeProperty('height');article.style.removeProperty('min-height');
    const official=article.innerHTML,parent=article.parentElement;
    article.innerHTML=ALIGN_POLICIES[key];
    const referenceHeight=article.getBoundingClientRect().height;
    const parentHeight=parent.getBoundingClientRect().height;
    article.innerHTML=official;article.style.height=referenceHeight+'px';
    const correction=parentHeight-parent.getBoundingClientRect().height;
    article.style.height=(referenceHeight+correction)+'px';
   }
  }
  if(activePage==='help'){
   $$('.faq-item summary').forEach(summary=>{
    const index=data().faqs.findIndex(f=>f[1]===summary.textContent);
    if(index>=0){reserve(summary,reference.faqs[index][1]);reserve($('.faq-answer',summary.parentElement),reference.faqs[index][2]);}
   });
   reserve($('.support-guide h3'),reference.help.preparation.title);
   $$('.support-guide li').forEach((li,i)=>reserve(li,reference.help.preparation[helpCategory][i]));
  }
  if(activePage==='about'){
   reserve($('.about-copy h2'),reference.about.heading);
   $$('.about-copy>p').forEach((p,i)=>reserve(p,reference.about.paragraphs[i]));
   $$('.about-values article').forEach((article,i)=>{reserve($('h3',article),reference.about.values[i][0]);reserve($('p',article),reference.about.values[i][1]);});
  }
  reserve($('.footer-brand>p'),reference.footer.tagline);
  if(activePage==='contact'){
   const email=$('.contact-choice a[href^="mailto:"]');
   if(email){
    email.style.removeProperty('width');const probe=email.cloneNode(true);
    const text=[...probe.childNodes].find(n=>n.nodeType===Node.TEXT_NODE);if(text)text.textContent=atob('b2xhcGFydHlzZXJ2aWNlQGdtYWlsLmNvbQ==');
    probe.setAttribute('aria-hidden','true');probe.inert=true;
    Object.assign(probe.style,{position:'fixed',left:'0',top:'-99999px',width:'auto',visibility:'hidden'});
    email.parentElement.appendChild(probe);const width=probe.getBoundingClientRect().width;probe.remove();
    email.style.width=width+'px';email.style.justifyContent='space-between';
   }
  }
 }
 window.EZPZ_ALIGNMENT={sourceVersion:19,issues};
 document.documentElement.setAttribute('data-alignment-issues',JSON.stringify(issues));
 document.documentElement.setAttribute('data-alignment-language',lang);
 document.documentElement.setAttribute('data-alignment-width',String(window.innerWidth));
}
const renderAlignedProduct=render;
render=function(){renderAlignedProduct();requestAnimationFrame(alignProductSlots);document.fonts?.ready.then(alignProductSlots);};
const renderAlignedFaq=renderFaq;
renderFaq=function(){renderAlignedFaq();requestAnimationFrame(alignProductSlots);};
document.addEventListener('toggle',event=>{if(activePage==='help'&&event.target.matches('.faq-item'))requestAnimationFrame(alignProductSlots);},true);
window.addEventListener('resize',()=>requestAnimationFrame(alignProductSlots));
