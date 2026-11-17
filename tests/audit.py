from pathlib import Path
import re,json,hashlib,urllib.request,concurrent.futures
root=Path(__file__).resolve().parent.parent
source=(root/'template/ola19.html').read_text('utf-8');page=(root/'dist/index.html').read_text('utf-8')
def obj(text,name):return json.JSONDecoder().raw_decode(text.split('const '+name+'=',1)[1])[0]
for old in ['Ola Party','OlaParty','Infriends','olaparty.com','infriends.net','olapartyservice@gmail.com','csinfriends@gmail.com','Rambojoy']:
 assert old.lower() not in page.lower(),old
assert re.search(r'const DOWNLOAD_CHANNELS=.*?;',source)[0]==re.search(r'const DOWNLOAD_CHANNELS=.*?;',page)[0]
assert set(re.findall(r'data-action=["\x27]([^"\x27]+)',source))==set(re.findall(r'data-action=["\x27]([^"\x27]+)',page))
assert '<video' not in page.split('function heroVideoPlaceholder()',1)[1].split('function homePage',1)[0]
assert len(obj(page,'CONTENT')['en']['home']['scenes'])==5
expected=json.loads(json.dumps(obj(source,'CONTENT'),ensure_ascii=False).replace('Ola Party','Ezpz').replace('OlaParty','Ezpz').replace('olapartyservice@gmail.com','contactezpzapp@gmail.com'))
for lang,t in expected.items():
 for i,scene in enumerate(t['home']['scenes']):scene['source']='placeholder-scene-'+str(i+1)+'.svg'
assert obj(page,'CONTENT')==expected,'Display copy differs from the user-confirmed template'
assets=obj(page,'ASSETS')
for k,path in assets.items():assert (root/'dist'/path).exists(),path
assert all('placeholder-scene-' in assets[s['image']] for s in obj(page,'CONTENT')['en']['home']['scenes'])
assert not re.search(r'https?://[^\s"\x27]+\.(mp4|webm)',page)
links=obj(page,'LINKS')
def verify(item):
 key,url=item
 if not url.startswith('http'):return {'key':key,'status':'not configured' if not url else 'email','value':url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as r:return {'key':key,'status':r.status,'url':url,'final_url':r.url}
 except Exception as e:return {'key':key,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:results=list(ex.map(verify,list(links.items())+[('website','https://ezpzapp.net/')]))
result={'date':'2026-11-17','display_copy':'template verbatim, product identity only','runtime_brand_scan':'passed','all_assets_local_and_present':True,'scene_count':5,'placeholder_scenes':5,'event_attributes':'unchanged','channel_order':'unchanged','baseline_sha256':hashlib.sha256((root/'template/ola19.html').read_bytes()).hexdigest(),'links':results}
(root/'tests/audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
