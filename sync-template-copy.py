"""User-confirmed copy source: pinned template, identity substitutions only."""
from pathlib import Path
import json
root=Path(__file__).resolve().parent
source=(root/'template/ola19.html').read_text('utf-8')
config=json.loads((root/'product-config.json').read_text('utf-8'))
original_copy=json.loads((root/'product-copy.json').read_text('utf-8'))
if 'feedback' not in config:
 config['feedback']={lang:{k:c[k] for k in ['pending','recharge']} for lang,c in original_copy.items()}
 (root/'product-config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),'utf-8')
content=json.JSONDecoder().raw_decode(source.split('const CONTENT=',1)[1])[0]
text=json.dumps(content,ensure_ascii=False).replace('Ola Party',config['brand']).replace('OlaParty',config['brand']).replace('olapartyservice@gmail.com',config['links']['email'])
(root/'product-copy.json').write_text(json.dumps(json.loads(text),ensure_ascii=False,indent=2),'utf-8')
print('Display copy synchronized from the pinned template; product identity substituted only.')
