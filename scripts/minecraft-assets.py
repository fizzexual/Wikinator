"""Extract and catalogue official Minecraft Java images for this local wiki.

Only image assets and their animation metadata are extracted; game code is not run.
"""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,struct,urllib.request,zipfile

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--version',default='26.2')
parser.add_argument('--client',type=Path)
parser.add_argument('--metadata',type=Path)
args=parser.parse_args()
version=args.version
def get(url):
    with urllib.request.urlopen(url,timeout=90) as r: return r.read()
if args.metadata:
    metadata=json.loads(args.metadata.read_text())
else:
    versions=json.loads(get('https://piston-meta.mojang.com/mc/game/version_manifest_v2.json'))
    metadata=json.loads(get(next(v['url'] for v in versions['versions'] if v['id']==version)))
assert metadata['id']==version
client=metadata['downloads']['client']
blob=args.client.read_bytes() if args.client else get(client['url'])
assert hashlib.sha1(blob).hexdigest()==client['sha1'],'Client checksum mismatch'
dest=ROOT/'assets/minecraft'/version
stage=ROOT/'import/minecraft'/version
dest.mkdir(parents=True,exist_ok=True);stage.mkdir(parents=True,exist_ok=True)
entries=[];names=set()

def save(path,data,origin,animation=None):
    safe=Path(path)
    if safe.is_absolute() or '..' in safe.parts: raise ValueError(path)
    out=dest/safe;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
    relative=path.removeprefix('minecraft/textures/')
    filename='Minecraft '+version+' - '+relative.replace('/',' - ').replace('_',' ')
    if filename in names: raise ValueError('Duplicate filename '+filename)
    names.add(filename)
    (stage/filename).write_bytes(data)
    (stage/(Path(filename).stem+'.txt')).write_text(
        'Minecraft Java Edition '+version+' image asset.\n\n'
        'Original asset: <code>'+path+'</code>\n\n'
        'Source: Mojang/Microsoft official distribution, verified by SHA-1.\n\n'
        'Copyright Mojang/Microsoft. Imported for use in this local wiki; this file is not relicensed under the wiki text license.\n\n'
        '[[Category:Minecraft assets]]',encoding='utf8')
    width,height=struct.unpack('>II',data[16:24]) if data[:8]==b'\x89PNG\r\n\x1a\n' else (0,0)
    if animation:
        out.with_suffix(out.suffix+'.mcmeta').write_bytes(animation)
    entries.append({'id':relative.rsplit('.',1)[0], 'name':safe.stem.replace('_',' '),
        'category':relative.split('/')[0] if '/' in relative else 'other',
        'path':path,'filename':filename,'url':'/wikinator-assets/minecraft/'+version+'/'+path,
        'width':width,'height':height,'animated':bool(animation),'sha1':hashlib.sha1(data).hexdigest(),'origin':origin})

import io
with zipfile.ZipFile(io.BytesIO(blob)) as archive:
    files=set(archive.namelist())
    for path in sorted(files):
        if (path.startswith('assets/') or path=='pack.png') and path.lower().endswith(('.png','.jpg','.jpeg','.gif')):
            animation=archive.read(path+'.mcmeta') if path+'.mcmeta' in files else None
            save(path.removeprefix('assets/'),archive.read(path),'client.jar',animation)
jar_count=len(entries)
index_blob=get(metadata['assetIndex']['url'])
assert hashlib.sha1(index_blob).hexdigest()==metadata['assetIndex']['sha1']
index=json.loads(index_blob)
existing={e['path'] for e in entries}
extras=[(path,item) for path,item in index['objects'].items() if path not in existing and path.lower().endswith(('.png','.jpg','.jpeg','.gif'))]
def download(entry):
    path,item=entry
    data=get('https://resources.download.minecraft.net/'+item['hash'][:2]+'/'+item['hash'])
    assert hashlib.sha1(data).hexdigest()==item['hash'],path
    return path,data
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for path,data in pool.map(download,extras): save(path,data,'asset index')
entries.sort(key=lambda e:(e['category'],e['name'],e['id']))
manifest={'version':version,'clientUrl':client['url'],'clientSha1':client['sha1'],
    'assetIndexUrl':metadata['assetIndex']['url'],'jarImageCount':jar_count,'assetIndexImageCount':len(extras),
    'count':len(entries),'assets':entries}
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False),encoding='utf8')
(ROOT/'assets/minecraft/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False),encoding='utf8')
print('Prepared',len(entries),'images:',jar_count,'from the client and',len(extras),'from the asset index.',flush=True)
print('Import directory:',stage,flush=True)
