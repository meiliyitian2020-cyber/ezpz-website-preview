from pathlib import Path
import urllib.request,re,json,concurrent.futures,shutil
root=Path(__file__).resolve().parent
sources=root/'sources';sources.mkdir(exist_ok=True)
for name in ['official-home.html','official-bundle.js']:
 if (root/name).exists():shutil.move(root/name,sources/name)
items={
 'official-logo.png':'https://static.ezpzapp.net/a/ezpz-site-pc/assets/logo-DQER-zi7.png',
 'official-logo-small.png':'https://static.ezpzapp.net/a/ezpz-site-pc/assets/logo-small-C9u1ufkd.png',
 'google-play.html':'https://play.google.com/store/apps/details?id=com.party.ezpz&hl=en',
 'apple.html':'https://apps.apple.com/bh/app/dera-3d-avatar-meet-chat/id1625619255',
 'apple-lookup.json':'https://itunes.apple.com/lookup?id=1625619255&country=bh',
 'terms-original.html':'https://www.ezpzapp.net/a/license/ezpz-user.html?lang=en',
 'privacy-original.html':'https://www.ezpzapp.net/a/license/ezpz-privacy.html?lang=en',
 'children-original.html':'https://www.ezpzapp.net/a/license/ezpz-children-policy.html?lang=en',
 'feishu.html':'https://lp3jrqympq.feishu.cn/wiki/X4Czwro8ci1QBikh3uRccNDMnsb?sheet=ymlzGV',
}
def fetch(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=40) as r:
   data=r.read();(sources/name).write_bytes(data)
   return {'file':name,'url':url,'final_url':r.url,'status':r.status,'bytes':len(data)}
 except Exception as e:return {'file':name,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex: results=list(ex.map(fetch,items.items()))
(sources/'fetch-log.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),'utf-8')
for r in results:print(r)
for key in ['terms','privacy','children']:
 p=sources/(key+'-original.html')
 if p.exists():
  s=p.read_text('utf-8');print(key, s[-1600:])
play=(sources/'google-play.html').read_text('utf-8')
urls=re.findall(r'https://play-lh.googleusercontent.com/[^"<>\s]+',play)
if urls:print(fetch(('store-icon.png',urls[0].split('=')[0]+'=w512')))
if (sources/'apple-lookup.json').exists():
 d=json.loads((sources/'apple-lookup.json').read_text('utf-8'))
 for a in d.get('results',[]):print({k:a.get(k) for k in ['trackName','sellerName','bundleId','artworkUrl512','trackViewUrl','description']});print(fetch(('apple-icon.png',a['artworkUrl512'])))
brand=root/'brand';brand.mkdir(exist_ok=True)
for n,k in [('安卓.png','android-original.png'),('ios.png','ios-original.png')]:shutil.copy2(Path(r'\\TrueNAS-01.skyit.local\OASIS-share\f\项目素材\ezpz\01-logo\新')/n,brand/k)
