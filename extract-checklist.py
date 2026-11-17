"""Read-only extraction of the available local checklist snapshot; no workbook edits."""
from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json
p=Path('G:/26.11.05-官网优化/官网缺失项.xlsx')
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z:
 shared=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  shared=[''.join(e.itertext()) for e in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
 result=[]
 for name in z.namelist():
  if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
   for row in E.fromstring(z.read(name)).findall('.//s:row',ns):
    cells=[]
    for c in row.findall('s:c',ns):
     v=c.find('s:v',ns);txt=v.text if v is not None else ''.join(c.find('s:is',ns).itertext()) if c.find('s:is',ns) is not None else ''
     if c.attrib.get('t')=='s':txt=shared[int(txt)]
     if txt:cells.append({'cell':c.attrib['r'],'text':txt})
    if cells:result.append({'sheet_file':name,'row':row.attrib['r'],'cells':cells})
out=Path(__file__).resolve().parent/'sources/local-checklist.json'
out.write_text(json.dumps({'source':str(p),'modified':p.stat().st_mtime,'rows':result},ensure_ascii=False,indent=2),'utf-8')
for r in result:print(' | '.join(x['text'] for x in r['cells']))
