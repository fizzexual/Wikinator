"""Create original editable starter pages; no Hypixel articles are copied."""
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
pages = {}
def add(title, text, ns=0, model='wikitext'):
    pages[title] = (text.strip()+'\n', ns, model)

add('Main Page', '''__NOTOC__
<div class="wk-welcome">''' + "'''Welcome to Wikinator'''" + '''<br>Your own game encyclopedia.</div>
<div class="wk-home-grid">
<div class="wk-box"><div class="wk-box-title">Game content</div><div class="wk-box-body">
* [[Category:Items|Items]]
* [[Category:Weapons|Weapons]]
* [[Category:Armor|Armor]]
* [[Category:Skills|Skills]]
* [[Category:Locations|Locations]]
* [[Category:NPCs|NPCs]]
</div></div>
<div class="wk-box"><div class="wk-box-title">Editing the wiki</div><div class="wk-box-body">
* [[Wikinator:Create a page|Create a page]]
* [[Example Sword|Explore an item page]]
* [[Sandbox|Try the editors in the sandbox]]
* [[Help:Editing|Learn wikitext and templates]]
* [[Special:RecentChanges|Recent changes]]
* [[Special:AllPages|Browse all pages]]
</div></div>
<div class="wk-box"><div class="wk-box-title">Templates</div><div class="wk-box-body">
* [[Template:Item|Item infobox]] — properties and stats
* [[Template:Crafting|Crafting grid]] — ingredients and results
* [[Template:Rarity|Rarity]] — consistent item colours
* [[Template:New article|New article]] — a starting structure
</div></div>
<div class="wk-box"><div class="wk-box-title">Community</div><div class="wk-box-body">
* [[Wikinator:Community portal|Community portal]]
* [[Wikinator:Style manual|Style manual]]
* [[Special:Upload|Upload an image]]
* [[Special:ListFiles|Browse uploaded files]]
* [[Wikinator:About|About Wikinator]]
</div></div></div>
''')
add('MediaWiki:Sidebar', '''* navigation
** mainpage|mainpage-description
** Help:Editing|How to edit
** Wikinator:Create a page|Create a page
** recentchanges-url|recentchanges
** randompage-url|randompage
* Game content
** Category:Items|Items
** Category:Weapons|Weapons
** Category:Armor|Armor
** Category:Skills|Skills
** Category:Locations|Locations
** Category:NPCs|NPCs
* Editing
** Sandbox|Sandbox
** Example Sword|Example item
** Special:AllPages/Template:|Templates
** Special:AllPages/Module:|Lua modules
** upload-url|upload
* Community
** Wikinator:Community portal|Community portal
** Wikinator:Style manual|Style manual
** Wikinator:About|About Wikinator
* SEARCH
* TOOLBOX
* LANGUAGES''',8)
add('MediaWiki:Mainpage','Main Page',8)
add('MediaWiki:Pagetitle','$1 - Wikinator',8)
add('MediaWiki:Sitesubtitle','Your local wiki',8)
add('MediaWiki:Common.css', (ROOT/'assets/reference/site.css').read_text(encoding='utf-8')+'\n'+(ROOT/'assets/local.css').read_text(encoding='utf-8'), 8, 'css')
add('Wikinator:Create a page', '''Start with a title. The new page opens in the source editor with an article outline.
<inputbox>
type=create
buttonlabel=Create page
placeholder=Page title
preload=Template:New article
break=no
</inputbox>
For an item, copy the source from [[Example Sword]] or insert [[Template:Item]] using the visual editor's ''' + "'''Insert → Template'''" + ''' menu.''',4)
add('Template:New article', '''<includeonly>Write a short introduction explaining what this page is about.

== Obtaining ==
Explain how to obtain or unlock it.

== Usage ==
Explain what it does and how to use it.

== History ==
{| class="wikitable"
! Version !! Change
|-
| Initial release || Added.
|}
</includeonly><noinclude>This is the outline used by [[Wikinator:Create a page]]. Edit its source to change the outline for future pages.</noinclude>''',10)
add('Template:Item', '''<includeonly><table class="wk-infobox">
<tr><th colspan="2" class="wk-infobox-title">{{{name|{{PAGENAME}}}}}</th></tr>
<tr><td colspan="2" class="wk-item-image">{{#if:{{{image|}}}|[[File:{{{image}}}|160px|frameless|{{{name|{{PAGENAME}}}}}]]|<span class="wk-image-empty">[[Special:Upload|Upload an item image]]</span>}}</td></tr>
<tr><th>Type</th><td>{{{type|Item}}}</td></tr>
<tr><th>Rarity</th><td>{{Rarity|{{{rarity|common}}}}}</td></tr>
<tr><th>Requirement</th><td>{{{requirement|None}}}</td></tr>
<tr><th colspan="2" class="wk-section">Stats</th></tr>
<tr><th>Damage</th><td>{{{damage|—}}}</td></tr>
<tr><th>Strength</th><td>{{{strength|—}}}</td></tr>
<tr><th>Intelligence</th><td>{{{intelligence|—}}}</td></tr>
<tr><th colspan="2" class="wk-section">Item Properties</th></tr>
<tr><th>Tradeable</th><td>{{{tradeable|Yes}}}</td></tr>
<tr><th>Upgradeable</th><td>{{{upgradeable|Yes}}}</td></tr>
<tr><th colspan="2" class="wk-section">Item Metadata</th></tr>
<tr><th>Item ID</th><td><code>{{{id|}}}</code></td></tr>
</table></includeonly><noinclude>
This template creates the information panel on an item page. Use it through ''' + "'''Insert → Template → Item'''" + ''' in the visual editor, or copy this source:
<pre>{{Item
|name=Your item
|image=
|type=Weapon
|rarity=legendary
|requirement=None
|damage=100
|strength=50
|intelligence=0
|tradeable=Yes
|upgradeable=Yes
|id=YOUR_ITEM
}}</pre>
<templatedata>
{"description":"Item information panel with properties and stats.","params":{"name":{"label":"Name","type":"string","required":true},"image":{"label":"Uploaded image filename","type":"wiki-file-name"},"type":{"label":"Item type","type":"string","suggested":true},"rarity":{"label":"Rarity","type":"string","suggestedvalues":["common","uncommon","rare","epic","legendary","mythic"],"suggested":true},"requirement":{"label":"Requirement","type":"string"},"damage":{"label":"Damage","type":"number","suggested":true},"strength":{"label":"Strength","type":"number","suggested":true},"intelligence":{"label":"Intelligence","type":"number"},"tradeable":{"label":"Tradeable","type":"string"},"upgradeable":{"label":"Upgradeable","type":"string"},"id":{"label":"Item ID","type":"string"}},"format":"block"}
</templatedata></noinclude>''',10)
add('Module:Rarity', '''local p = {}
function p.main(frame)
    local value = mw.ustring.lower(mw.text.trim(frame.args[1] or 'common'))
    local allowed = { common=true, uncommon=true, rare=true, epic=true, legendary=true, mythic=true }
    if not allowed[value] then value = 'common' end
    return tostring(mw.html.create('span'):addClass('wk-rarity-' .. value):wikitext(mw.ustring.upper(value)))
end
return p''',828,'Scribunto')
add('Template:Rarity','''<includeonly>{{#invoke:Rarity|main|{{{1|common}}}}}</includeonly><noinclude>Use <code><nowiki>{{Rarity|legendary}}</nowiki></code> to show {{Rarity|legendary}}. Supports common, uncommon, rare, epic, legendary and mythic. The logic is in [[Module:Rarity]].
<templatedata>{"description":"Display a coloured rarity label.","params":{"1":{"label":"Rarity","type":"string","required":true,"suggestedvalues":["common","uncommon","rare","epic","legendary","mythic"]}}}</templatedata></noinclude>''',10)
add('Template:Crafting','''<includeonly><div class="wk-recipe"><div class="wk-slot">{{{1|}}}</div><div class="wk-slot">{{{2|}}}</div><div class="wk-slot">{{{3|}}}</div><div class="wk-slot">{{{4|}}}</div><div class="wk-slot">{{{5|}}}</div><div class="wk-slot">{{{6|}}}</div><div class="wk-slot">{{{7|}}}</div><div class="wk-slot">{{{8|}}}</div><div class="wk-slot">{{{9|}}}</div></div><span class="wk-recipe-result">→ {{{result|}}}</span></includeonly><noinclude>
Slots are numbered left to right, top to bottom. Each slot can contain an item link or uploaded icon.
<pre>{{Crafting|2=Crystal|5=Crystal|8=Handle|result=Your item}}</pre>
<templatedata>{"description":"A three-by-three crafting grid.","params":{"1":{"label":"Top left"},"2":{"label":"Top centre"},"3":{"label":"Top right"},"4":{"label":"Middle left"},"5":{"label":"Centre"},"6":{"label":"Middle right"},"7":{"label":"Bottom left"},"8":{"label":"Bottom centre"},"9":{"label":"Bottom right"},"result":{"label":"Result","required":true}},"format":"block"}</templatedata></noinclude>''',10)
add('Example Sword', '''{{Item
|name=Example Sword
|type=Weapon
|rarity=legendary
|requirement=Level 10
|damage=100
|strength=50
|intelligence=25
|tradeable=Yes
|upgradeable=Yes
|id=EXAMPLE_SWORD
}}
The ''' + "'''Example Sword'''" + ''' is a {{Rarity|legendary}} weapon. This is a fictional starter article for your wiki; replace its name, stats, and recipe with your own content.

== Obtaining ==
=== Crafting ===
{| class="wikitable"
! Requirement !! Ingredients !! Crafting recipe
|-
| Level 10 || 2 × Crystal<br>1 × Handle || {{Crafting|2=Crystal|5=Crystal|8=Handle|result=Example Sword}}
|}

== Usage ==
Use this section to describe the item's abilities and effects.
{| class="wikitable"
! Ability !! Effect
|-
| Example ability || Describe your game's ability here.
|}

== Upgrading ==
Explain how the item can be improved and which materials are required.

== Tips ==
* Add advice based on your own game mechanics.

== Trivia ==
* This article demonstrates an editable item infobox, Lua rarity labels, and a crafting template.

== History ==
{| class="wikitable"
! Version !! Change
|-
| Initial release || Starter example created.
|}

== Navigation ==
[[Category:Weapons|Weapons]] · [[Category:Items|All items]] · [[Help:Editing|Editing help]]
<div class="wk-footer-clear"></div>
[[Category:Items]]
[[Category:Weapons]]''')
add('Sandbox', '''Welcome to your sandbox. Experiment here with ''' + "'''Edit'''" + ''' or ''' + "'''Edit source'''" + '''. Each saved change appears in ''' + "'''View history'''" + '''.

== Text and links ==
Try ''' + "'''bold text'''" + ''', ''italic text'', and an [[Example Sword|internal link]].

== Templates ==
{{Rarity|legendary}}

{{Crafting|2=Crystal|5=Crystal|8=Handle|result=Example Sword}}

== Tabs ==
<tabber>
Overview=Write an overview here.
|-|
Details=Write details here.
</tabber>

== References ==
An example statement.<ref>A source or note for this statement.</ref>
<references />''')
add('Help:Editing', '''== Choose an editor ==
* ''' + "'''Edit'''" + ''' opens the visual editor. Type directly into the article and use the toolbar for headings, links, tables, images and templates.
* ''' + "'''Edit source'''" + ''' opens real MediaWiki wikitext with syntax highlighting. Edit template calls, categories, tables and article text here.
* Use the section-level ''' + "'''edit'''" + ''' and ''' + "'''edit source'''" + ''' links for an individual section.

== Preview and save ==
In the source editor, choose ''' + "'''Show preview'''" + ''' to render your changes without saving, or ''' + "'''Show changes'''" + ''' to compare your draft. Add an edit summary and choose ''' + "'''Save changes'''" + '''. In the visual editor, use ''' + "'''Save changes'''" + ''' and review the save dialog.

== Wikitext quick reference ==
<pre>== Heading ==
''' + "'''Bold''' and ''italic''" + '''
[[Page title|Link label]]
[https://example.com External link]
* A bullet point
# A numbered item
[[Category:Items]]
[[File:Uploaded image.png|thumb|Image caption]]
{{Rarity|legendary}}
</pre>

== Templates and Lua ==
Visit [[Template:Item]], [[Template:Crafting]], and [[Template:Rarity]] and edit their source to change all pages that use them. In the visual editor choose ''' + "'''Insert → Template'''" + ''' to fill in labelled fields. [[Module:Rarity]] is an editable Lua example.

== History and undo ==
Open ''' + "'''View history'''" + ''' to compare revisions, inspect older source, or undo a change. Your edits are stored in the local database and survive restarting Wikinator.

== Images ==
Log in and use [[Special:Upload]]. Then insert the uploaded file using the visual editor or the File syntax above. The local administrator's sign-in details are in <code>runtime/ADMIN.txt</code> in the Wikinator folder.

== Start a page ==
Use [[Wikinator:Create a page]], or search for a new title and follow its creation link. Practise in [[Sandbox]].''',12)
add('Wikinator:Community portal','''== Working on the wiki ==
Use this page for your project notes and contributor guidance.
* [[Special:RecentChanges|Review recent changes]]
* [[Special:WantedPages|Find pages that need writing]]
* [[Special:WantedFiles|Find missing images]]
* [[Special:UnusedTemplates|Review unused templates]]
Discuss this page using the ''' + "'''Discussion'''" + ''' tab.''',4)
add('Wikinator:Style manual','''== Articles ==
Start with a short definition, then describe obtaining, usage, upgrades and history where relevant. Keep game values in reusable templates.

== Items ==
Use [[Template:Item]] for properties and stats. Use [[Template:Crafting]] for recipes and [[Template:Rarity]] for rarity colours.

== Sources ==
Add references where a claim needs evidence. Use edit summaries so changes are easy to review.''',4)
add('Wikinator:About','''Wikinator is your local MediaWiki for your own content. It uses the Vector skin and a locally stored adaptation of the Hypixel SkyBlock Wiki's public theme.

The starter articles and templates were created for this installation. No Hypixel game articles have been imported. Wikinator is not affiliated with Hypixel or Weird Gloop.

== Theme attribution ==
Theme source: [https://hypixelskyblock.minecraft.wiki/w/MediaWiki:Common.css Hypixel SkyBlock Wiki contributors], including their skin styles and assets. The upstream wiki identifies its site content as [https://creativecommons.org/licenses/by-nc-sa/3.0/ CC BY-NC-SA 3.0]; individual assets and fonts may have their own terms. See <code>THIRD-PARTY.md</code> for source details.

== Software ==
[[Special:Version|Installed software and extensions]] · [[Help:Editing|Editing help]]''',4)
for category in ['Items','Weapons','Armor','Skills','Locations','NPCs']:
    add('Category:'+category, 'Pages about '+category.lower()+'. To include a page here, add <code><nowiki>[[Category:'+category+']]</nowiki></code> to its source.',14)

ns = 'http://www.mediawiki.org/xml/export-0.11/'
ET.register_namespace('',ns)
root = ET.Element('{'+ns+'}mediawiki', {'version':'0.11','{http://www.w3.org/XML/1998/namespace}lang':'en'})
def elem(parent,name,text):
    e=ET.SubElement(parent,'{'+ns+'}'+name);e.text=text;return e
for i,(title,(text,namespace,model)) in enumerate(pages.items(),1):
    page=ET.SubElement(root,'{'+ns+'}page');elem(page,'title',title);elem(page,'ns',str(namespace));elem(page,'id',str(i))
    rev=ET.SubElement(page,'{'+ns+'}revision');elem(rev,'id',str(i));elem(rev,'timestamp',datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    con=ET.SubElement(rev,'{'+ns+'}contributor');elem(con,'username','Wikinator setup')
    elem(rev,'comment','Wikinator theme; adapted from Hypixel SkyBlock Wiki contributors, CC BY-NC-SA 3.0; see Wikinator:About' if model=='css' else 'Original Wikinator starter content');elem(rev,'model',model);elem(rev,'format',{'Scribunto':'text/plain','css':'text/css'}.get(model,'text/x-wiki'))
    e=elem(rev,'text',text);e.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
(ROOT/'import').mkdir(exist_ok=True)
ET.ElementTree(root).write(ROOT/'import/starter.xml',encoding='utf-8',xml_declaration=True)
print('Prepared',len(pages),'original starter pages.')
