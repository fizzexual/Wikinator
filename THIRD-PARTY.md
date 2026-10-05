# Upstream sources

This local installation uses MediaWiki (GPL-2.0-or-later) and its bundled extensions. Their source and license files are included in the Docker image at `/var/www/html`. Additional source checkouts and license files are in `vendor/`; exact revisions are recorded in `upstream-lock.json`.

- MediaWiki: https://www.mediawiki.org/wiki/MediaWiki
- MediaWiki Docker distribution: https://hub.docker.com/_/mediawiki
- Vector: https://github.com/weirdgloop/mediawiki-skins-Vector
- Original theme and assets: Hypixel SkyBlock Wiki contributors, https://hypixelskyblock.minecraft.wiki/w/MediaWiki:Common.css and https://hypixelskyblock.minecraft.wiki/w/MediaWiki:Vector.css, retrieved 2026-09-07. This site's footer identifies site content as CC BY-NC-SA 3.0: https://creativecommons.org/licenses/by-nc-sa/3.0/. Additional asset terms: https://meta.weirdgloop.org/w/Licensing.
- Theme was obtained through the public `site.styles` ResourceLoader endpoint. Changes: asset URLs rewritten to local files; local Wikinator identity and starter-template styles appended; fixed dark-theme class supplied locally. The whole resulting stylesheet is editable at `MediaWiki:Common.css`.
- Individual downloaded asset source URLs are preserved in `assets/reference/manifest.json`. Logo and favicon came from `https://hypixelskyblock.minecraft.wiki/images/Wiki.png` and `https://hypixelskyblock.minecraft.wiki/images/Favicon.ico`.
- The theme references the fonts and glyph assets at https://github.com/skyblock-wiki/wiki-assets and Google Fonts' Merriweather, Noto Sans, and Noto Sans Symbols 2. Local copies preserve those font names. Refer to their upstream license files for the respective font terms.

Wikinator is independent of Hypixel and Weird Gloop. The starter articles, item template, crafting template, rarity module, and local controls are original to this installation. Hypixel game articles, accounts, histories, and server-side private configuration were not copied.

## Minecraft Java 26.2 image library

The local library contains 3,856 images from the official Java 26.2 client JAR and 25 additional images from its asset index, 3,881 in total. Client source: https://piston-data.mojang.com/v1/objects/2dc72797acbc1b63fc16a11c4ac393605f453754/client.jar (SHA-1 `2dc72797acbc1b63fc16a11c4ac393605f453754`). Asset-index source: https://piston-meta.mojang.com/v1/packages/a7b53da5fa967c3e8196712f1b734bbc9df44bb6/32.json. All downloads are checksum-verified. The client code is not executed or included in the website.

The original texture paths, dimensions and individual hashes are recorded in `assets/minecraft/26.2/manifest.json`. The images remain copyright Mojang/Microsoft; they are not relicensed under the wiki's text license. Each imported file page carries this provenance. The `MC`, `Minecraft`, `Item name`, and `Item tooltip` templates and asset browser are local Wikinator additions.
