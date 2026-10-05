# Wikinator â€” local wiki 🍂

Open **http://localhost:8087/w/Main_Page**. Double-click **Start Wikinator.cmd** when you want to start it again. Docker Desktop must be running.

Wikinator uses actual MediaWiki 1.45, the Weird Gloop Vector legacy skin, and a local adaptation of the Hypixel SkyBlock Wiki's public theme. It is a wiki for your own content, with original starter pages instead of imported Hypixel articles.

## About

Wikinator is a ready-to-run local MediaWiki setup for people who want their own Minecraft-style wiki on their PC, without hosting or Hypixel content. Docker Compose runs MediaWiki 1.45 with MariaDB, and Python scripts handle first-time setup, starter pages, Minecraft image import and backups. Status: a personal, local-only setup (bound to 127.0.0.1) built for Windows with Docker Desktop.

## Editing

- **Edit**: the MediaWiki visual editor, including links, tables, uploaded images and template forms.
- **Edit source**: real wikitext with CodeMirror syntax highlighting, line numbers, preview and change comparison.
- **View history**: saved revisions, diffs, old source and undo.
- **Discussion**: native talk pages.
- **Create a page** in the sidebar: new article with an editable outline.
- **Example Sword**: a fictional item page showing properties, a Lua rarity label and a crafting grid.
- **Templates** and **Lua modules**: edit their source inside the wiki. TemplateData supplies the visual editor's labelled fields.
- **MediaWiki:Common.css**: edit the actual site theme through the wiki as an administrator. Theme images and fonts are saved locally.
- **Special:Upload**: upload images after signing in.

You can edit articles without logging in because this instance is bound only to your computer. For uploads, theme changes and administration, use username **Admin** and the generated password in **runtime/ADMIN.txt**. That file and all database secrets are excluded from Git.

## Minecraft fonts and images

Headings, item names, and item tooltips use the locally stored Minecraft font; paragraphs and navigation retain the reading font. Use `{{Minecraft|Your text}}` anywhere, `{{Item name|Diamond Sword}}` for item labels, and `{{Item tooltip|Diamond Sword|Damage: +100}}` for a hover/focus tooltip.

Open **Minecraft images** in the sidebar for a searchable library of **3,881 Java 26.2 images**. It includes every image in the client JAR and its asset index: block and item textures, entity sheets, GUI sprites, particles, paintings, trims, launcher icons and other bundled images. These are native image assets; entity sheets retain their original UV layout. Animated textures retain the full frame strip and `.mcmeta` metadata locally.

Select an image to copy its filename for the visual editor, its `[[File:...]]` markup, or a short template such as `{{MC|item/diamond_sword|32}}`. All images are also imported as MediaWiki files and available through **Insert â†’ Images and media**.

Original image files and the provenance/checksum manifest are in `assets/minecraft/26.2/`. Font and asset usage help is at **Help:Minecraft** in the wiki. The Minecraft font comes from the reference wiki's Minecraft 1.8.9 web-font conversion, already stored locally; it is not an approximate system font. Images are the Java 26.2 set, not a collection spanning every Minecraft edition and historical version.

To reproduce the image extraction, run `python scripts/minecraft-assets.py --version 26.2`. It downloads official Mojang resources, verifies their SHA-1 hashes, and extracts only image assets and animation metadata. `scripts/install-minecraft.py` adds the wiki feature pages and typography. The image import command is `docker compose exec -T wiki php maintenance/run.php importImages --user Admin --comment-ext txt /wikinator/import/minecraft/26.2`; existing files are skipped by default. Minecraft asset binaries are excluded from Git.

## Start, stop and backup

- **Start Wikinator.cmd** starts the wiki and opens it.
- **Stop Wikinator.cmd** stops it without removing pages or uploaded images.
- **Back up Wikinator.cmd** briefly stops the web service and saves the database, uploaded files and configuration under `backups/`, then restarts it. Keep backups private because they include local credentials.

Pages, users and revision history live in the Docker volume `wikinator_database`. Uploaded files live in `wikinator_uploads`. Copying this source folder alone does not copy later wiki edits: use the backup shortcut. Do not remove these Docker volumes if you want to keep your wiki.

## Source and setup

The original `fizzexual/Wikinator` Git remote is preserved. Nothing has been pushed to GitHub.

From this folder, first-time setup is `python scripts/setup.py` (Python 3, Git and Docker Desktop). Later starts use `docker compose up -d`. All services bind through `127.0.0.1:8087`; the database has no host port. Page rendering and editing work without reaching the reference wiki after setup.

`config/LocalSettings.php` contains Wikinator's configuration. `config/InstalledSettings.php` is generated and contains local secrets. `scripts/seed.py` defines the starter articles/templates and imports them only during initial setup. Subsequent edits belong in the wiki; rerunning setup does not overwrite them.

MediaWiki's full application source is in the local Docker image/container at `/var/www/html`. Additional extension and skin source is in `vendor/`. `docker compose exec wiki php maintenance/run.php --help` exposes MediaWiki's maintenance runner.

## Scope

This reproduces the wiki's public theme and core editing workflow. It is not a complete copy of Hypixel's hosted service: no Hypixel articles or accounts, live market feed, hosted search cluster, resource-pack selector, Discord integration or private moderation configuration. The item and crafting templates are editable starter templates for your content; they do not include the thousands of game-specific Hypixel Lua/data templates. Upstream sources and theme attribution are in `THIRD-PARTY.md`.
