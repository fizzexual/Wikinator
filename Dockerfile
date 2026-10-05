FROM mediawiki:1.45@sha256:fb18fb59b20d6fe7bc29dd35c762e9f1133635d38db83e1ba6cd3b25a27d0d45
COPY vendor/extensions/ /var/www/html/extensions/
COPY vendor/skins/Vector/ /var/www/html/skins/Vector/
COPY config/LocalSettings.php /var/www/html/LocalSettings.php
COPY config/apache.conf /etc/apache2/conf-enabled/wikinator.conf
RUN a2enmod rewrite && printf 'memory_limit=512M\nupload_max_filesize=64M\npost_max_size=64M\n' > /usr/local/etc/php/conf.d/wikinator.ini
