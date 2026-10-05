"""Verify imported Minecraft assets, image insertion and scoped typography."""
from pathlib import Path
import hashlib,json,re,urllib.request,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8087'
def api(**q):
    q.update(format='json',formatversion=2)
    with urllib.request.urlopen(BASE+'/api.php?'+urllib.parse.urlencode(q),timeout=60) as r:data=json.load(r)
    if 'error' in data:raise RuntimeError(data['error'])
    return data
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name);print('PASS:',name,flush=True)
manifest=json.loads((ROOT/'assets/minecraft/manifest.json').read_text())
check('Manifest includes the full client and asset-index image counts',len(manifest['assets'])==manifest['count']==manifest['jarImageCount']+manifest['assetIndexImageCount'])
check('Every local image matches its recorded source checksum',all(hashlib.sha1((ROOT/'assets/minecraft'/manifest['version']/a['path']).read_bytes()).hexdigest()==a['sha1'] for a in manifest['assets']))
files=set();continuation={}
while True:
    result=api(action='query',list='allimages',aiprefix='Minecraft '+manifest['version']+' - ',ailimit=500,**continuation)
    files.update(a['name'].replace('_',' ') for a in result['query']['allimages'])
    if 'continue' not in result:break
    continuation=result['continue']
missing=[a['filename'] for a in manifest['assets'] if a['filename'] not in files]
if missing:print('Missing uploads:',missing[:20],flush=True)
check('Every catalogued image is an imported MediaWiki file',not missing)
parsed=api(action='parse',title='Minecraft verification',text='{{MC|item/diamond_sword|48}} {{MC|block/stone|32}} {{Minecraft|Minecraft text}} {{Item tooltip|Sword|Damage: +100}}',prop='text')['parse']['text']
check('MC template renders real item and block images','diamond_sword.png' in parsed and 'stone.png' in parsed and 'class="new"' not in parsed and 'scribunto-error' not in parsed)
check('Minecraft text and keyboard-focusable tooltip render','wk-minecraft' in parsed and 'wk-tooltip-content' in parsed and 'tabindex="0"' in parsed)
data=api(action='query',list='search',srnamespace=6,srsearch='Minecraft 26.2 diamond sword')['query']['search']
check('Minecraft items are searchable in the file namespace',any('diamond sword' in p['title'].lower() for p in data))
form=api(action='templatedata',titles='Template:MC')['pages']
check('Visual editor exposes image path and size template fields',set(next(iter(form.values()))['params'])=={'1','2'})
css=api(action='query',prop='revisions',titles='MediaWiki:Common.css',rvprop='content',rvslots='main')['query']['pages'][0]['revisions'][0]['slots']['main']['content']
check('Minecraft font rules are installed for headings and item text',"font-family:'Minecraft'" in css and '.wk-item-name' in css and '#firstHeading' in css)
font=urllib.request.urlopen(BASE+'/wikinator-assets/reference/686550e239b18e7a.woff2').read()
check('Local Minecraft web font is served as a real WOFF2 font',font.startswith(b'wOF2'))
page=urllib.request.urlopen(BASE+'/w/Wikinator:Minecraft_assets').read().decode()
check('Asset browser route and controls script are available','wk-minecraft-library' in page and '/wikinator-assets/minecraft.js' in page)
for path in ['/wikinator-assets/minecraft/manifest.json','/wikinator-assets/minecraft/26.2/minecraft/textures/item/diamond_sword.png']:
    check('Asset endpoint responds: '+path,urllib.request.urlopen(BASE+path).status==200)
(ROOT/'runtime/minecraft-verification.json').write_text(json.dumps({'count':len(files),'passed':checks},indent=2))
print(len(checks),'Minecraft checks passed.',flush=True)
