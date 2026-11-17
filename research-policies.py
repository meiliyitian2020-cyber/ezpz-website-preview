from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,re,json,concurrent.futures
p=Path(__file__).resolve().parent
files=[p/'sources'/n for n in ['official-logo.png','official-logo-small.png','store-icon.png','apple-icon.png']]+list((p/'brand').glob('*.png'))
out=Image.new('RGB',(900,600),'#f4f1ed');d=ImageDraw.Draw(out)
for i,f in enumerate(files):
 im=ImageOps.contain(Image.open(f).convert('RGBA'),(260,220));out.paste(im,((i%3)*300+20,(i//3)*300+35),im)
 d.text(((i%3)*300+10,(i//3)*300+5),f.name,fill='black')
out.save(p/'sources'/'brand-comparison.png')
def fetch(key):
 s=(p/'sources'/(key+'-original.html')).read_text('utf-8')
 matches=re.findall(r'type:"module",src:"([^"]+)',s)
 for match in matches:
  url='https://static.ezpzapp.net/a/license/'+match.lstrip('./')
  try:
   data=urllib.request.urlopen(url,timeout=35).read().decode('utf-8');(p/'sources'/(key+'-bundle.js')).write_text(data,'utf-8'); print(key,'bundle',len(data))
  except Exception as e:print(key,e)
 post={'terms':'user','privacy':'privacy','children':'children-policy'}[key]
 url='https://feapi.ezpzapp.net/post-platform/getPostDetail?lang=en'
 try:
  req=urllib.request.Request(url,headers={'x-app-name':'ezpz','x-app-os':'web','x-app-post-type':post})
  data=json.loads(urllib.request.urlopen(req,timeout=35).read())
  (p/'sources'/(key+'-policy.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf-8')
  print(key,'API',str(data)[:220])
 except Exception as e:print(key,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(fetch,['terms','privacy','children']))
