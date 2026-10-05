<?php
if (!defined('MEDIAWIKI')) { exit; }
require '/wikinator/config/InstalledSettings.php';
$wgSitename = 'Wikinator';
$wgMetaNamespace = 'Wikinator';
$wgServer = 'http://localhost:8087';
$wgCanonicalServer = $wgServer;
$wgScriptPath = '';
$wgArticlePath = '/w/$1';
$wgUsePathInfo = true;
$wgDefaultSkin = 'vector';
$wgVectorDefaultSkinVersion = '1';
$wgVectorResponsive = true;
$wgEnableUploads = true;
$wgFileExtensions = [ 'png', 'gif', 'jpg', 'jpeg', 'webp', 'ico' ];
$wgEnableEmail = false;
$wgEnableUserEmail = false;
$wgLogo = '/wikinator-assets/reference/logo.png';
$wgFavicon = '/wikinator-assets/reference/favicon.ico';
$wgMaxArticleSize = 8192;
$wgMaxTemplateDepth = 100;
$wgMaxPPNodeCount = 1000000;
$wgMaxUploadSize = 64 * 1024 * 1024;
$wgGroupPermissions['*']['edit'] = true;
$wgGroupPermissions['*']['createpage'] = true;
$wgGroupPermissions['user']['upload'] = true;
$wgGroupPermissions['sysop']['editinterface'] = true;
$wgGroupPermissions['sysop']['editsitecss'] = true;
$wgGroupPermissions['sysop']['editsitejs'] = true;
$wgNamespaceAliases['Hypixel_SkyBlock_Wiki'] = NS_PROJECT;
$wgNamespaceAliases['Hypixel_SkyBlock_Wiki_talk'] = NS_PROJECT_TALK;
$wgScribuntoDefaultEngine = 'luastandalone';
$wgScribuntoEngineConf['luastandalone']['memoryLimit'] = 256 * 1024 * 1024;
$wgAllowSiteCSSOnRestrictedPages = true;
$wgAllowUserCss = true;
$wgAllowUserJs = true;
$wgDefaultUserOptions['usebetatoolbar'] = 1;
$wgDefaultUserOptions['visualeditor-enable'] = 1;
$wgDefaultUserOptions['visualeditor-editor'] = 'visualeditor';
$wgDefaultUserOptions['visualeditor-tabs'] = 'multi-tab';
$wgVisualEditorUseSingleEditTab = false;
$wgVisualEditorEnableWikitext = true;
$wgVisualEditorEnableBetaFeature = false;
$wgVisualEditorAvailableNamespaces[NS_TEMPLATE] = true;
$wgDefaultUserOptions['usecodemirror'] = 1;
$wgCodeMirrorV6 = true;
$wgCodeMirrorConf['defaultPreferences']['lineNumbering'] = true;
$wgCodeMirrorConf['defaultPreferences']['lineWrapping'] = true;
$wgParserEnableLegacyMediaDOM = false;
$wgPFEnableStringFunctions = true;
$wgRightsText = 'CC BY-NC-SA 3.0';
$wgRightsUrl = 'https://creativecommons.org/licenses/by-nc-sa/3.0/';
foreach ([ 'WikiEditor', 'VisualEditor', 'ParserFunctions', 'Scribunto', 'TemplateData', 'Cite', 'CiteThisPage', 'CategoryTree', 'ImageMap', 'InputBox', 'Poem', 'SyntaxHighlight_GeSHi', 'CodeEditor', 'Gadgets', 'PageImages', 'TextExtracts', 'MultimediaViewer', 'Linter', 'CodeMirror', 'TemplateStyles', 'TemplateStylesExtender', 'Tabber', 'Variables', 'Loops', 'LabeledSectionTransclusion' ] as $extension) {
    if (!ExtensionRegistry::getInstance()->isLoaded($extension)) { wfLoadExtension($extension); }
}
$wgHooks['BeforePageDisplay'][] = static function ($out, $skin) {
    $out->addHtmlClasses('wgl-theme-dark skin-theme-clientpref-night');
    $out->addScriptFile('/wikinator-assets/local.js');
    $out->addScriptFile('/wikinator-assets/minecraft.js');
};
