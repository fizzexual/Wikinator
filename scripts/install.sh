#!/bin/sh
set -eu
if [ ! -f /wikinator/config/InstalledSettings.php ]; then
    mkdir -p /tmp/wikinator-install
    php maintenance/run.php install --confpath /tmp/wikinator-install --dbtype mysql --dbserver db --dbname wikinator --dbuser wikinator --dbpass "$DB_PASSWORD" --server http://localhost:8087 --scriptpath '' --lang en --skins Vector --passfile /wikinator/runtime/admin-password.txt Wikinator Admin
    cp /tmp/wikinator-install/LocalSettings.php /wikinator/config/InstalledSettings.php
fi
if [ "${1:-}" = "--install-only" ]; then exit 0; fi
php maintenance/run.php update --quick
if [ ! -f /wikinator/config/.seeded ]; then
    php maintenance/run.php importDump /wikinator/import/starter.xml
    php maintenance/run.php rebuildrecentchanges
    php maintenance/run.php initSiteStats --update
    php maintenance/run.php runJobs --maxjobs 200
    touch /wikinator/config/.seeded
fi
