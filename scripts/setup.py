"""One-time setup and subsequent start; preserves pages and uploaded files."""
import pathlib, secrets, subprocess, sys, time, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
def run(args):
    subprocess.run(args,cwd=ROOT,check=True)
for folder in ['runtime','config','import','assets']:
    (ROOT/folder).mkdir(exist_ok=True)
if not (ROOT/'.env').exists():
    (ROOT/'.env').write_text('DB_PASSWORD='+secrets.token_hex(24)+'\nDB_ROOT_PASSWORD='+secrets.token_hex(24)+'\n')
if not (ROOT/'runtime/admin-password.txt').exists():
    password=secrets.token_urlsafe(20)
    (ROOT/'runtime/admin-password.txt').write_text(password)
    (ROOT/'runtime/ADMIN.txt').write_text('Wikinator local administrator\nURL: http://localhost:8087\nUsername: Admin\nPassword: '+password+'\n')
if not (ROOT/'assets/reference/site.css').exists() or not (ROOT/'vendor/skins/Vector/skin.json').exists():
    run([sys.executable,'scripts/fetch-dependencies.py'])
run(['docker','compose','up','-d','--build'])
if not (ROOT/'config/InstalledSettings.php').exists():
    args=['docker','run','--rm','--network','wikinator_default','--env-file',str(ROOT/'.env')]
    for name in ['config','runtime','scripts']:
        args += ['--mount','type=bind,source='+str(ROOT/name)+',target=/wikinator/'+name]
    args += ['mediawiki:1.45@sha256:fb18fb59b20d6fe7bc29dd35c762e9f1133635d38db83e1ba6cd3b25a27d0d45','sh','/wikinator/scripts/install.sh','--install-only']
    run(args)
run([sys.executable,'scripts/seed.py'])
run(['docker','compose','exec','-T','wiki','sh','/wikinator/scripts/install.sh'])
for attempt in range(30):
    try:
        with urllib.request.urlopen('http://localhost:8087/w/Main_Page',timeout=5) as r:
            if r.status==200: break
    except Exception:
        if attempt==29: raise
        time.sleep(1)
print('Wikinator is running: http://localhost:8087/w/Main_Page')
