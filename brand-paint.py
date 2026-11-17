"""Color and decorative artwork only. Layout values remain byte-for-byte identical."""
import re,colorsys,json
from pathlib import Path
PALETTE=json.loads((Path(__file__).resolve().parent/'product-config.json').read_text('utf-8'))['colors']
TOKEN=re.compile(r'#[0-9a-fA-F]{3,8}\b|rgba?\([^)]+\)')
EXACT={'#146d58':'#417865','#d1ff69':'#f3d5c1','#ddfaec':'#f5e7db','#fffdf4':'#fcf7f0','#19264b':'#49382f','#cef5dd':'#efdbcc','#67c99d':'#9bbcab','#ffe476':'#ebc3a9','#a4e8bb':'#d4ddcd'}
EXACT.update({'#146d58':PALETTE['primary'],'#d1ff69':PALETTE['accent'],'#fffdf4':PALETTE['background'],'#19264b':PALETTE['text'],'#e2e7de':PALETTE['border']})
def color(token):
 low=token.lower()
 if low in EXACT:return EXACT[low]
 if low.startswith('rgb'):
  nums=re.findall(r'[\d.]+',low)
  if len(nums)<3:return token
  r,g,b=map(int,nums[:3]);new=color('#%02x%02x%02x'%(r,g,b))
  if new.startswith('#') and len(new)==7:
   parts=[str(int(new[i:i+2],16)) for i in (1,3,5)]
   return ('rgba('+','.join(parts+[nums[3]])+')') if len(nums)==4 else 'rgb('+','.join(parts)+')'
  return token
 v=low[1:]
 if len(v)==3:v=''.join(c*2 for c in v)
 if len(v) not in (6,8):return token
 r,g,b=[int(v[i:i+2],16)/255 for i in (0,2,4)]
 h,l,s=colorsys.rgb_to_hls(r,g,b)
 if s<.02:return token
 if 30/360<=h<=85/360:h,s=25/360,min(.65,s)
 elif 85/360<h<=180/360:h,s=153/360,min(.30,s)
 elif 180/360<h<=290/360:h,s=25/360,min(.27,s)
 elif l>.75:h,s=25/360,min(.45,s)
 r,g,b=colorsys.hls_to_rgb(h,l,s)
 return '#'+''.join(f'{round(x*255):02x}' for x in (r,g,b))+v[6:]
def paint_styles(page):
 return re.sub(r'<style>(.*?)</style>',lambda m:'<style>'+TOKEN.sub(lambda c:color(c[0]),m[1])+'</style>',page,flags=re.S)
def background(w,h):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="base" x2="1" y2="1"><stop stop-color="#fcf9f2"/><stop offset="1" stop-color="#f1dfd3"/></linearGradient><radialGradient id="glow"><stop stop-color="#a5c9b4" stop-opacity=".23"/><stop offset="1" stop-color="#a5c9b4" stop-opacity="0"/></radialGradient></defs><path fill="url(#base)" d="M0 0h1600v900H0z"/><ellipse cx="1320" cy="300" rx="460" ry="440" fill="url(#glow)"/><g fill="#9fb7a5" opacity=".27"><path d="m1440 120 10 18-10 18-10-18zM220 720l6 12-6 12-6-12z"/></g><g fill="#d5b09a" opacity=".3"><path d="m1150 760 7 13-7 13-7-13zM300 100l4 8-4 8-4-8z"/></g></svg>'''
SCENE='''function sceneBackground(){return `<div class="scene-backdrop" aria-hidden="true"><i></i><svg viewBox="0 0 720 420" fill="none"><defs><radialGradient id="scene-glow"><stop stop-color="#c3d9c7" stop-opacity=".4"/><stop offset="1" stop-color="#eecbb8" stop-opacity="0"/></radialGradient></defs><ellipse cx="570" cy="270" rx="260" ry="220" fill="url(#scene-glow)"/><g fill="var(--scene-line)" opacity=".25"><path d="m585 75 7 13-7 13-7-13zM320 340l5 10-5 10-5-10zM660 350l4 8-4 8-4-8z"/></g></svg></div>`;}'''
