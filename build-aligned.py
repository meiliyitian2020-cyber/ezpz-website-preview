from pathlib import Path
import base64,copy,hashlib,html,json,re,shutil,runpy
from PIL import Image
root=Path(__file__).resolve().parent
source=(root/'template/ola19.html').read_text('utf-8')
config=json.loads((root/'product-config.json').read_text('utf-8'))
copies=json.loads((root/'product-copy.json').read_text('utf-8'))
out=root/'dist';assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
def obj(s,name):
 start=s.index('const '+name+'=')+len('const '+name+'=');value,length=json.JSONDecoder().raw_decode(s[start:]);return value,start,start+length
def replace_obj(s,name,value):
 _,a,b=obj(s,name);return s[:a]+json.dumps(value,ensure_ascii=False,indent=2)+s[b:]
reference,_,_=obj(source,'CONTENT')
# User-confirmed revision: all display copy is the template verbatim, with product identity substituted.
content=copy.deepcopy(copies)
for lang,t in content.items():
 for i,s in enumerate(t['home']['scenes']):s['source']='placeholder-scene-'+str(i+1)+'.svg'
page=replace_obj(source,'CONTENT',content)
page=replace_obj(page,'LINKS',config['links'])
policies={}
for key in ['terms','privacy','children']:
 data=json.loads((root/'sources'/(key+'-policy.json')).read_text('utf-8'))
 body=data.get('data',{}).get('acticle_content','')
 assert len(body)>1000,'Official policy missing: '+key
 body=re.sub(r'<script\b[^>]*>.*?</script>','',body,flags=re.S|re.I)
 body=re.sub(r'\son\w+="[^"]*"','',body,flags=re.I)
 policies[key]=body
page=replace_obj(page,'POLICIES',policies)
asset_map={}
for f in (root/'template/assets').iterdir():
 shutil.copy2(f,assets/f.name);asset_map[f.name]='assets/'+f.name
def uri(file):return 'data:image/png;base64,'+base64.b64encode(file.read_bytes()).decode()
def image_canvas(name,w,h,file):
 (assets/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><image width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="{uri(file)}"/></svg>','utf-8')
 return 'assets/'+name
# Source logo canvas has the template aspect so its rendered DOM rectangle is unchanged.
from PIL import ImageFile
original_assets,_,_=obj(source,'ASSETS')
# These are the intrinsic source dimensions recorded from the pinned baseline.
dimensions=json.loads((root/'template/asset-dimensions.json').read_text('utf-8'))
for key,name in [('ola-share-icon.png','ezpz-logo.svg'),('hero-brand-logo.png','ezpz-hero-logo.svg')]:
 asset_map[key]=image_canvas(name,*dimensions[key],root/'sources/official-logo.png')
def placeholder(name,w,h,label):
 text=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#f4e8de"/><text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" font-family="Arial,sans-serif" font-size="{max(42,round(w*.025))}" fill="#8e7a6a">{label}</text></svg>'
 (assets/name).write_text(text,'utf-8');return 'assets/'+name
for i,s in enumerate(reference['en']['home']['scenes'],1):asset_map[s['image']]=placeholder('placeholder-scene-'+str(i)+'.svg',720,1280,'功能素材待替换 / Feature '+str(i))
asset_map['p1_youngs-38ed979a0c.png']=placeholder('placeholder-about.svg',*dimensions['p1_youngs-38ed979a0c.png'],'素材待替换 / About')
placeholder('placeholder-hero-desktop.svg',1600,900,'首屏素材待替换 / Hero')
placeholder('placeholder-hero-mobile.svg',900,1600,'首屏素材待替换 / Hero')
Image.open(root/'brand/ios-original.png').resize((64,64)).save(assets/'ezpz-favicon.png')
Image.open(root/'brand/ios-original.png').resize((256,256)).save(assets/'ezpz-app-icon.png')
asset_map['favicon-32x32-new.png']='assets/ezpz-favicon.png';asset_map['company-app-logo.png']='assets/ezpz-app-icon.png'
paint=runpy.run_path(str(root/'brand-paint.py'))
(assets/'ezpz-background.svg').write_text(paint['background'](*dimensions['p1_bg-105ed6b6c9.png']),'utf-8')
asset_map['p1_bg-105ed6b6c9.png']='assets/ezpz-background.svg'
page=replace_obj(page,'ASSETS',asset_map)
page=page.replace('href="assets/favicon-32x32-new.png"','href="assets/ezpz-favicon.png"')
poster='''function heroVideoPlaceholder(){return `<div class="hero-media-video"><div class="hero-video-stage"><picture><source media="(max-width:680px)" srcset="assets/placeholder-hero-mobile.svg"><img class="hero-loop-freeze" src="assets/placeholder-hero-desktop.svg" alt="首屏素材待替换 / Hero placeholder" loading="eager" decoding="async"></picture></div><button type="button" class="hero-play-fallback" data-action="start-hero-video" hidden aria-label="${lang==='zh'?'播放视频':lang==='hi'?'वीडियो चलाएँ':'Play video'}">${icon('video')}<span>${lang==='zh'?'播放视频':lang==='hi'?'वीडियो चलाएँ':'Play video'}</span></button></div>`;}
'''
page=re.sub(r'function heroVideoPlaceholder\(\)\{.*?\n(?=function homePage)',lambda _:poster,page,flags=re.S)
page=re.sub(r'const HERO_MEDIA=\{[^\n]*\};','const HERO_MEDIA={};',page)
page=page.replace('Ola Party','Ezpz').replace('OlaParty','Ezpz').replace('ola-preview-','ezpz-preview-')
page=page.replace('HAGO SINGAPORE PTE. LTD.',config['entity']).replace('30 PASIR PANJANG ROAD #15-31A MAPLETREE BUSINESS CITY SINGAPORE 117440',config['address'])
page=page.replace("if(action==='preview-download'){toast(downloadCopy().note);return;}","if(action==='preview-download'){const key=event.target.closest('[data-channel]').dataset.channel;const destination=LINKS[key];if(destination){window.open(destination,'_blank','noopener,noreferrer');}else{toast(PRODUCT_COPY[lang].pending);}return;}")
pending="""
document.addEventListener('click',event=>{const a=event.target.closest('a');if(a&&a.getAttribute('href')===''){event.preventDefault();toast(PRODUCT_COPY[lang].recharge);}});
"""
slot_script=(root/'alignment-slots.js').read_text('utf-8')
encoded_reference=base64.b64encode(json.dumps(reference,ensure_ascii=False).encode()).decode()
reference_js="JSON.parse(new TextDecoder().decode(Uint8Array.from(atob('"+encoded_reference+"'),c=>c.charCodeAt(0))))"
reference_policies,_,_=obj(source,'POLICIES')
policies_encoded=base64.b64encode(json.dumps(reference_policies,ensure_ascii=False).encode()).decode()
policies_js="JSON.parse(new TextDecoder().decode(Uint8Array.from(atob('"+policies_encoded+"'),c=>c.charCodeAt(0))))"
page=page.replace('\nrender();\n})();','\nconst PRODUCT_COPY='+json.dumps(config['feedback'],ensure_ascii=False)+';\nconst ALIGN_REFERENCE='+reference_js+';\nconst ALIGN_POLICIES='+policies_js+';\n'+slot_script+'\n'+pending+'\nrender();\n})();')
page=paint['paint_styles'](page)
page=re.sub(r'function sceneBackground\(\)\{[^\n]*',lambda _:paint['SCENE'],page)
page=page.replace('content="#e7fff5"','content="#fcf7f0"')
# Neutral asset keys retain the fixed slots while removing prior brand names from runtime.
page=page.replace('ola-share-icon.png','brand-logo.svg')
# Baseline copy is only a geometry measurement reference, never visible product content.
page=page.replace('Ola Party','Reference').replace('olapartyservice@gmail.com','reference-support@example.invalid')
page=page.replace('INFRIENDS_ALIGNMENT','EZPZ_ALIGNMENT')
assert [paint['TOKEN'].sub('<color>',x) for x in re.findall(r'<style[^>]*>(.*?)</style>',source,re.S)]==[paint['TOKEN'].sub('<color>',x) for x in re.findall(r'<style[^>]*>(.*?)</style>',page,re.S)]
assert len(content['en']['home']['scenes'])==5
assert [s['id'] for s in content['en']['home']['scenes']]==[s['id'] for s in reference['en']['home']['scenes']]
(out/'index.html').write_text(page,'utf-8');(out/'404.html').write_text(page,'utf-8')
(out/'.nojekyll').write_text('','utf-8');(out/'robots.txt').write_text('User-agent: *\nDisallow: /\n','utf-8')
(root/'check-script.js').write_text('\n'.join(re.findall(r'<script[^>]*>(.*?)</script>',page,re.S)),'utf-8')
(root/'alignment-reference.json').write_text(json.dumps({'version':19,'commit':'f8026d91802eb907a54d9f84c349aa306ef098cd','sha256':hashlib.sha256((root/'template/ola19.html').read_bytes()).hexdigest(),'css_layout_identical':True,'languages':list(content),'scene_ids':[s['id'] for s in reference['en']['home']['scenes']]},indent=2),'utf-8')
print('Built Ezpz. Fixed Ola v19 CSS geometry and scene IDs verified.')
