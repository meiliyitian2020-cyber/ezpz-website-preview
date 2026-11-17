from pathlib import Path
import zipfile,hashlib,json
root=Path(__file__).resolve().parent
out=root/'Ezpz-offline-review.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in (root/'dist').rglob('*'):
  if p.is_file():z.write(p,str(p.relative_to(root/'dist')))
 z.writestr('START-HERE.txt','Ezpz offline review\nUnzip the whole folder, then open index.html.\nFonts and placeholder artwork are bundled.\nApp Store / Google Play and mail links require a network connection.\nThe contact form is a local validation preview; payment and analytics are not connected.\n')
 for name in ['SOURCES.md','HANDOFF.md','DEPLOYMENT.md']:
  if (root/name).exists():z.write(root/name,'docs/'+name)
(root/'tests/offline-package.json').write_text(json.dumps({'file':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size},indent=2),'utf-8')
print(out, out.stat().st_size)
