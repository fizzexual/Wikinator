"""Download pinned upstream wiki components and local copies of the reference theme."""
import concurrent.futures
import hashlib
import io
import json
import pathlib
import re
import subprocess
import urllib.parse
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
UA = 'Wikinator/0.1 (personal local wiki setup)'
BASE = 'https://hypixelskyblock.minecraft.wiki'
ASSETS = ROOT / 'assets/reference'
ASSETS.mkdir(parents=True, exist_ok=True)
manifest = {}
LOCKPATH = ROOT / 'upstream-lock.json'
LOCK = json.loads(LOCKPATH.read_text()) if LOCKPATH.exists() else {}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()

def vendor(spec):
    name, repo, branch, kind = spec
    dest = ROOT / 'vendor' / kind / name
    sha = LOCK.get(name, {}).get('commit') or subprocess.check_output(['git', 'ls-remote', 'https://github.com/' + repo + '.git', 'refs/heads/' + branch], text=True).split()[0]
    manifest[name] = {'repository': repo, 'commit': sha, 'branch': branch}
    if (dest / ('skin.json' if kind == 'skins' else 'extension.json')).exists():
        return
    data = get('https://codeload.github.com/' + repo + '/zip/' + sha)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for member in z.infolist():
            parts = pathlib.PurePosixPath(member.filename).parts[1:]
            if not parts or member.is_dir() or '..' in parts:
                continue
            target = dest.joinpath(*parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(member))
    manifest[name] = {'repository': repo, 'commit': sha, 'branch': branch}
    print('Downloaded', name, flush=True)

SPECS = [
    ('Vector', 'weirdgloop/mediawiki-skins-Vector', 'weirdgloop/REL1_45', 'skins'),
    ('CodeMirror', 'wikimedia/mediawiki-extensions-CodeMirror', 'REL1_45', 'extensions'),
    ('TemplateStylesExtender', 'weirdgloop/mediawiki-extensions-TemplateStylesExtender', 'weirdgloop/master', 'extensions'),
    ('Tabber', 'weirdgloop/mediawiki-extensions-Tabber', 'weirdgloop/REL1_45', 'extensions'),
    ('Variables', 'wikimedia/mediawiki-extensions-Variables', 'REL1_45', 'extensions'),
    ('Loops', 'wikimedia/mediawiki-extensions-Loops', 'REL1_45', 'extensions'),
    ('LabeledSectionTransclusion', 'wikimedia/mediawiki-extensions-LabeledSectionTransclusion', 'REL1_45', 'extensions'),
    ('Bucket', 'weirdgloop/mediawiki-extensions-Bucket', 'main', 'extensions'),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(vendor, SPECS))
lockpath = ROOT / 'upstream-lock.json'
previous = json.loads(lockpath.read_text()) if lockpath.exists() else {}
previous.update(manifest)
lockpath.write_text(json.dumps(previous, indent=2), encoding='utf-8')

asset_urls = {}
def local_asset(url):
    if url.startswith('data:') or url.startswith('#'):
        return url
    absolute = urllib.parse.urljoin(BASE, url)
    if absolute in asset_urls:
        return asset_urls[absolute]
    suffix = pathlib.PurePosixPath(urllib.parse.urlparse(absolute).path).suffix
    if not suffix or len(suffix) > 8:
        suffix = '.png'
    name = hashlib.sha256(absolute.encode()).hexdigest()[:16] + suffix
    path = ASSETS / name
    if not path.exists():
        path.write_bytes(get(absolute))
    result = '/wikinator-assets/reference/' + name
    asset_urls[absolute] = result
    return result

def css_localize(url):
    css = get(url).decode('utf-8')
    def imported(m):
        return css_localize(urllib.parse.urljoin(url, m.group(1)))
    css = re.sub(r'@import\s+[\'"]([^\'"]+)[\'"]\s*;', imported, css)
    def asset(m):
        raw = m.group(1).strip().strip('\'"')
        if raw.startswith('/wikinator-assets/'):
            return m.group(0)
        if raw.startswith('data:'):
            return m.group(0)
        try:
            return 'url("' + local_asset(urllib.parse.urljoin(url, raw)) + '")'
        except Exception as e:
            print('Asset unavailable:', raw, str(e), flush=True)
            return 'none'
    return re.sub(r'url\(([^)]+)\)', asset, css)

css = css_localize(BASE + '/load.php?lang=en&modules=site.styles&only=styles&skin=vector')
(ASSETS / 'site.css').write_text(css, encoding='utf-8')
for name, url in [('logo.png', BASE+'/images/Wiki.png'), ('favicon.ico', BASE+'/images/Favicon.ico')]:
    (ASSETS / name).write_bytes(get(url))
(ASSETS / 'manifest.json').write_text(json.dumps(asset_urls, indent=2), encoding='utf-8')
print('Theme saved locally with', len(asset_urls), 'assets.', flush=True)
