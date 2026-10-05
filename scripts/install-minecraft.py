"""Add Minecraft typography, image library and templates without replacing wiki content."""
from pathlib import Path
import http.cookiejar,json,re,urllib.request,urllib.parse

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8087/api.php'
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def api(post=False,**q):
    q.update(format='json',formatversion=2)
    encoded=urllib.parse.urlencode(q).encode()
    response=opener.open(BASE if post else BASE+'?'+encoded.decode(),encoded if post else None,timeout=60)
    data=json.load(response)
    if 'error' in data: raise RuntimeError(data['error'])
    return data
token=api(action='query',meta='tokens',type='login')['query']['tokens']['logintoken']
assert api(True,action='login',lgname='Admin',lgpassword=(ROOT/'runtime/admin-password.txt').read_text(),lgtoken=token)['login']['result']=='Success'
csrf=api(action='query',meta='tokens')['query']['tokens']['csrftoken']
def read(title):
    p=api(action='query',prop='revisions',titles=title,rvprop='ids|content',rvslots='main')['query']['pages'][0]
    if p.get('missing'): return None,0
    r=p['revisions'][0];return r['slots']['main']['content'],r['revid']
def save(title,text,model=None,create_only=False):
    old,rev=read(title)
    if create_only and old is not None:return
    if old==text:return
    q=dict(action='edit',title=title,text=text,summary='Add Minecraft font and local image library',token=csrf,baserevid=rev)
    if model:q['contentmodel']=model
    if old is None:q['createonly']=1
    print(title,api(True,**q)['edit']['result'])
css,rev=read('MediaWiki:Common.css')
marker='/* WIKINATOR MINECRAFT ADDITIONS */'
if marker not in css:
    save('MediaWiki:Common.css',css+'\n'+marker+'\n'+(ROOT/'assets/minecraft.css').read_text(),model='css')
elif '.wk-mc-image img { image-rendering:pixelated; }' not in css:
    save('MediaWiki:Common.css',css+'\n.wk-mc-image img { image-rendering:pixelated; }\n',model='css')
sidebar,_=read('MediaWiki:Sidebar')
if 'Wikinator:Minecraft assets|' not in sidebar:
    sidebar=sidebar.replace('* Editing','* Minecraft\n** Wikinator:Minecraft assets|Minecraft images\n** Help:Minecraft|Minecraft font and images\n* Editing')
    save('MediaWiki:Sidebar',sidebar)

save('Module:MC', '''local p = {}
function p.main(frame)
    local path = mw.text.trim(frame.args[1] or '')
    if not path:match('^[%w_/%-%.]+$') or path:find('..', 1, true) then
        return '<strong class="error">Use an asset path such as item/diamond_sword.</strong>'
    end
    path = path:gsub('%.png$', '')
    local size = math.floor(math.max(8, math.min(512, tonumber(frame.args[2]) or 32)))
    local filename = 'Minecraft 26.2 - ' .. path:gsub('/', ' - '):gsub('_', ' ') .. '.png'
    local label = path:match('([^/]+)$'):gsub('_', ' ')
    return '[[File:' .. filename .. '|' .. size .. 'px|link=File:' .. filename .. '|alt=' .. label .. ']]'
end
return p
''',model='Scribunto',create_only=True)
save('Template:MC','''<includeonly><span class="wk-mc-image">{{#invoke:MC|main|{{{1|}}}|{{{2|32}}}}}</span></includeonly><noinclude>
Insert a Minecraft Java 26.2 image by its asset path. Browse [[Wikinator:Minecraft assets|Minecraft images]] for paths.
<pre>{{MC|item/diamond_sword|32}}</pre>
{{MC|item/diamond_sword|32}}
<templatedata>{"description":"Insert an image from the local Minecraft asset library.","params":{"1":{"label":"Asset path","description":"For example item/diamond_sword or block/stone.","type":"string","required":true},"2":{"label":"Size in pixels","type":"number","default":"32"}}}</templatedata></noinclude>''',create_only=True)
save('Template:Minecraft','''<includeonly><span class="wk-minecraft">{{{1|}}}</span></includeonly><noinclude>
Use Minecraft lettering anywhere in an article:
<pre>{{Minecraft|Your text here}}</pre>
{{Minecraft|Your text here}}
<templatedata>{"description":"Display a short piece of text using the Minecraft font.","params":{"1":{"label":"Text","type":"content","required":true}}}</templatedata></noinclude>''',create_only=True)
save('Template:Item name','''<includeonly><span class="wk-item-name">{{{1|}}}</span></includeonly><noinclude>Format an item name with the Minecraft font: <code><nowiki>{{Item name|Diamond Sword}}</nowiki></code>.
<templatedata>{"description":"Format an item name in the Minecraft font.","params":{"1":{"label":"Item name","type":"content","required":true}}}</templatedata></noinclude>''',create_only=True)
save('Template:Item tooltip','''<includeonly><span class="wk-mc-tooltip"><span class="wk-item-name" tabindex="0">{{{1|Item}}}</span><span class="wk-tooltip-content" role="tooltip">{{{2|}}}</span></span></includeonly><noinclude>
Create an item tooltip using Minecraft lettering. Hover over or focus the item name with the keyboard.
<pre>{{Item tooltip|Diamond Sword|{{Rarity|rare}}&lt;br&gt;Damage: +100}}</pre>
{{Item tooltip|Diamond Sword|{{Rarity|rare}}<br>Damage: +100}}
<templatedata>{"description":"Item name with a Minecraft-style tooltip.","params":{"1":{"label":"Item name","type":"content","required":true},"2":{"label":"Tooltip content","type":"content","required":true}}}</templatedata></noinclude>''',create_only=True)
manifest=json.loads((ROOT/'assets/minecraft/manifest.json').read_text())
save('Wikinator:Minecraft assets','''__NOTOC__
Browse '''+str(manifest['count'])+''' Minecraft Java '''+manifest['version']+''' image assets. Search by name, filter by category, then choose an image to copy its filename or wiki code.

<div id="wk-minecraft-library"></div>

[[Special:ListFiles|Browse wiki file records]] · [[Help:Minecraft|Using Minecraft fonts and images]]

The library includes item icons, block textures, entity texture sheets, GUI images, particles, paintings, trims and other bundled images. Animated textures retain their sprite sheets and animation metadata. Entity images are the original texture sheets.
''',create_only=True)
save('Help:Minecraft','''== Minecraft font ==
Headings, item names and tooltips use the locally stored Minecraft font from the reference wiki's font library. Article paragraphs and navigation keep the regular reading font.

Use the font anywhere with <code><nowiki>{{Minecraft|Your text}}</nowiki></code>. For item names use <code><nowiki>{{Item name|Diamond Sword}}</nowiki></code>.

== Images ==
Open [[Wikinator:Minecraft assets|Minecraft images]] in the sidebar. Search for an image and select it to copy its filename, full wikitext, or compact template call.

''' + "'''Visual editor:'''" + ''' choose ''' + "'''Insert → Images and media'''" + ''' and search for the copied filename. The files are already imported into this wiki.

''' + "'''Source editor:'''" + ''' paste the copied code, for example:
<pre>{{MC|item/diamond_sword|32}}
{{MC|block/stone|48}}
[[File:Minecraft 26.2 - item - diamond sword.png|64px]]</pre>

{{MC|item/diamond_sword|48}} {{MC|block/stone|48}} {{MC|item/emerald|48}} {{MC|item/golden_apple|48}}

== Item tooltips ==
<pre>{{Item tooltip|Diamond Sword|{{Rarity|rare}}&lt;br&gt;Damage: +100}}</pre>
{{Item tooltip|Diamond Sword|{{Rarity|rare}}<br>Damage: +100}}

== Item infoboxes ==
Set the image field in [[Template:Item]] to a library filename:
<pre>|image=Minecraft 26.2 - item - diamond sword.png</pre>

== Asset scope ==
The library contains all '''+str(manifest['count'])+''' image files found in the Java 26.2 client and its asset index. Assets are stored locally. Textures, including animations and entity sheets, retain their original game format. Minecraft images remain copyright Mojang/Microsoft and are not relicensed under the wiki's text license.
''',create_only=True)
save('Category:Minecraft assets','Images from the official Minecraft Java 26.2 client and asset index. Use [[Wikinator:Minecraft assets|the searchable image library]] to browse them. Copyright Mojang/Microsoft.',create_only=True)
for title in ['Wikinator:Minecraft assets','Help:Minecraft']:
    current,_=read(title)
    updated=re.sub(r'Browse \d+ Minecraft Java', 'Browse '+str(manifest['count'])+' Minecraft Java',current)
    updated=re.sub(r'all \d+ image files found in the Java', 'all '+str(manifest['count'])+' image files found in the Java',updated)
    if updated!=current:save(title,updated)
example,_=read('Example Sword')
if example:
    updated=example.replace("'''Example Sword'''",'{{Item name|Example Sword}}')
    if '|image=' not in updated and '|name=Example Sword' in updated:
        updated=updated.replace('|name=Example Sword','|name=Example Sword\n|image=Minecraft 26.2 - item - diamond sword.png')
    if updated!=example:save('Example Sword',updated)
print('Minecraft features installed. Existing articles were preserved.')
