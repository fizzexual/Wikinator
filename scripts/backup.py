"""Make a consistent local backup without exporting credentials to a service."""
from pathlib import Path
from datetime import datetime
import subprocess,shutil
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'backups'/datetime.now().strftime('%Y%m%d-%H%M%S')
target.mkdir(parents=True)
def run(args,**kwargs):
    return subprocess.run(['docker','compose',*args],cwd=ROOT,check=True,**kwargs)
# Temporarily stop writers so the database and uploaded files agree.
run(['up','-d','--wait','db'])
run(['stop','wiki'])
try:
    with (target/'database.sql').open('wb') as f:
        run(['exec','-T','db','sh','-c','exec mariadb-dump -uroot -p"$MARIADB_ROOT_PASSWORD" --single-transaction --routines --triggers wikinator'],stdout=f)
    with (target/'uploads.tar.gz').open('wb') as f:
        run(['run','--rm','--no-deps','-T','wiki','tar','czf','-','-C','/var/www/html','images'],stdout=f)
    shutil.copytree(ROOT/'config',target/'config')
    shutil.copy2(ROOT/'.env',target/'.env')
    shutil.copytree(ROOT/'runtime',target/'runtime')
finally:
    run(['start','wiki'])
print('Backup saved to',target)
