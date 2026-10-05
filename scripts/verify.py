"""Integration smoke test: source edits, preview, history, undo and visual editing.

Uses the local Sandbox, restoring its source in a finally block.
"""
from pathlib import Path
import json,re,urllib.request,urllib.parse,http.cookiejar
ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8087'
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
class Response:
    def __init__(self, response):
        self.status_code=response.status
        self.text=response.read().decode('utf-8')
    def raise_for_status(self): pass
    def json(self): return json.loads(self.text)
class Session:
    def get(self,url,params=None,timeout=30):
        if params: url+='?'+urllib.parse.urlencode(params)
        return Response(opener.open(url,timeout=timeout))
    def post(self,url,data,timeout=30):
        return Response(opener.open(url,urllib.parse.urlencode(data).encode(),timeout=timeout))
session=Session()
checks=[]
def api(post=False,**q):
    q.update(format='json',formatversion=2)
    response=session.post(BASE+'/api.php',data=q,timeout=45) if post else session.get(BASE+'/api.php',params=q,timeout=45)
    response.raise_for_status(); data=response.json()
    if 'error' in data: raise RuntimeError(data['error'])
    return data
def check(name,condition):
    if not condition: raise AssertionError(name)
    checks.append(name);print('PASS:',name)
def revision():
    return api(action='query',prop='revisions',titles='Sandbox',rvprop='ids|content',rvslots='main')['query']['pages'][0]['revisions'][0]

login_token=api(action='query',meta='tokens',type='login')['query']['tokens']['logintoken']
login=api(True,action='login',lgname='Admin',lgpassword=(ROOT/'runtime/admin-password.txt').read_text(),lgtoken=login_token)
check('Administrator login',login['login']['result']=='Success')
token=api(action='query',meta='tokens')['query']['tokens']['csrftoken']
original=revision(); source=original['slots']['main']['content'];changed=False
try:
    preview=api(True,action='parse',text=source+"\n== Preview verification ==\n'''Preview only'''",title='Sandbox',prop='text')['parse']['text']
    check('Source preview renders without saving','Preview only' in preview and revision()['revid']==original['revid'])
    edited=api(True,action='edit',title='Sandbox',text=source+'\n== Local verification ==\nSaved by the Wikinator setup check.',summary='Verify local editing and revision history',baserevid=original['revid'],token=token)
    changed=True
    new_id=edited['edit']['newrevid']
    check('Source edit persists',revision()['revid']==new_id)
    diff=api(action='compare',fromrev=original['revid'],torev=new_id,prop='diff')['compare']['body']
    check('Revision diff shows saved changes','Local verification' in diff)
    visual=api(action='visualeditor',paction='parse',page='Sandbox')['visualeditor']
    check('Visual editor loads Parsoid document',visual.get('result')=='success' and 'Local verification' in visual.get('content',''))
    # Exercise the exact visual-editor save API, including HTML-to-wikitext conversion.
    html=visual['content'].replace('Saved by the Wikinator setup check.','Saved through the visual editor API.')
    saved=api(True,action='visualeditoredit',paction='save',page='Sandbox',html=html,oldid=new_id,basetimestamp=visual['basetimestamp'],starttimestamp=visual['starttimestamp'],summary='Verify visual editor save',token=token)
    check('Visual editor save round trip',saved.get('visualeditoredit',{}).get('result')=='success' and 'Saved through the visual editor API.' in revision()['slots']['main']['content'])
finally:
    if changed:
        latest=revision()['revid']
        api(True,action='edit',title='Sandbox',undo=latest,undoafter=original['revid'],baserevid=latest,summary='Restore sandbox after setup verification',token=token)
check('Undo restores original source',revision()['slots']['main']['content'].rstrip()==source.rstrip())
data=api(action='templatedata',titles='Template:Item')['pages']
check('Visual template form has labelled item fields','damage' in next(iter(data.values()))['params'])
parsed=api(action='parse',page='Example Sword',prop='text')['parse']['text']
check('Item template, crafting and Lua render','wk-infobox' in parsed and 'wk-recipe' in parsed and 'wk-rarity-legendary' in parsed and 'scribunto-error' not in parsed)
main=api(action='parse',page='Main Page',prop='text')['parse']['text']
check('Wikinator home replaces installer page','wk-home-grid' in main and 'MediaWiki has been installed' not in main)
check('Full text search returns the item',any(p['title']=='Example Sword' for p in api(action='query',list='search',srsearch='Example Sword')['query']['search']))
edit=session.get(BASE+'/w/Sandbox?action=edit',timeout=30)
check('Source editor route loads with CodeMirror',edit.status_code==200 and 'ext.CodeMirror' in edit.text)
view=session.get(BASE+'/w/Example_Sword',timeout=30)
check('Article exposes both editors and history',all(x in view.text for x in ['id="ca-edit"','id="ca-ve-edit"','id="ca-history"']))
css_source=api(action='query',prop='revisions',titles='MediaWiki:Common.css',rvprop='content',rvslots='main')['query']['pages'][0]['revisions'][0]['slots']['main']['content']
check('Site theme is editable as wiki source','--body-background-image' in css_source and 'wk-infobox' in css_source)
paths=set(re.findall(r'/wikinator-assets/reference/[^"\s)\']+',css_source))
check('All theme asset files are present locally',all((ROOT/'assets/reference'/p.rsplit('/',1)[-1]).exists() for p in paths))
theme=session.get(BASE+'/load.php?lang=en&modules=site.styles&only=styles&skin=vector',timeout=30)
check('Wiki serves the editable theme stylesheet',theme.status_code==200 and 'wk-infobox' in theme.text)
(ROOT/'runtime/verification.json').write_text(json.dumps({'passed':checks},indent=2))
print(len(checks),'checks passed.')
