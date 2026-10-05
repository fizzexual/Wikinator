/* Local-only preferences. Article editing and persistence belong to MediaWiki. */
(function () {
    'use strict';
    function ready() {
        var target = document.querySelector('#p-personal ul');
        if (!target || document.getElementById('wk-theme-toggle')) return;
        var item = document.createElement('li');
        var button = document.createElement('button');
        button.id = 'wk-theme-toggle';
        button.className = 'wk-theme-toggle';
        function apply(light) {
            document.documentElement.classList.toggle('wk-light', light);
            document.documentElement.classList.toggle('wgl-theme-dark', !light);
            document.documentElement.classList.toggle('skin-theme-clientpref-night', !light);
            button.textContent = light ? 'Dark theme' : 'Light theme';
        }
        var light = false;
        try { light = localStorage.getItem('wikinator-theme') === 'light'; } catch (e) {}
        apply(light);
        button.addEventListener('click', function () {
            light = !light; apply(light);
            try { localStorage.setItem('wikinator-theme', light ? 'light' : 'dark'); } catch (e) {}
        });
        item.appendChild(button); target.appendChild(item);
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
    else ready();
}());
