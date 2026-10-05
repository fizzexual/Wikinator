(function () {
    'use strict';
    function el(tag, text, cls) { var n=document.createElement(tag); if(text)n.textContent=text;if(cls)n.className=cls;return n; }
    function start() {
        var root=document.getElementById('wk-minecraft-library');
        if(!root || root.dataset.ready)return;
        root.dataset.ready='true';
        var status=el('p','Loading Minecraft images…','wk-mc-status');status.setAttribute('role','status');root.append(status);
        fetch('/wikinator-assets/minecraft/manifest.json').then(function(r){if(!r.ok)throw new Error();return r.json();}).then(function(data){
            status.textContent=data.count.toLocaleString()+' images · Java Edition '+data.version;
            var toolbar=el('div',null,'wk-mc-toolbar'),searchLabel=el('label','Search images'),search=el('input');
            search.type='search';search.placeholder='Diamond sword, oak, creeper…';searchLabel.append(search);
            var filterLabel=el('label','Category'),filter=el('select');filter.append(new Option('All categories',''));
            var categories=[...new Set(data.assets.map(function(a){return a.category;}))].sort();
            categories.forEach(function(c){filter.append(new Option(c.replaceAll('_',' '),c));});filterLabel.append(filter);toolbar.append(searchLabel,filterLabel);root.append(toolbar);
            var layout=el('div',null,'wk-mc-layout'),left=el('div'),grid=el('div',null,'wk-mc-grid'),details=el('aside',null,'wk-mc-details');
            details.setAttribute('aria-label','Selected image');details.append(el('p','Choose an image to preview it and copy its wiki code.'));
            var pagination=el('div',null,'wk-mc-pagination'),prev=el('button','Previous','wk-mc-button'),next=el('button','Next','wk-mc-button'),pageLabel=el('span');
            prev.type=next.type='button';pagination.append(prev,pageLabel,next);left.append(grid,pagination);layout.append(left,details);root.append(layout);
            var matches=data.assets,page=0,selected='',size=72;
            function preview(asset,large){
                var box=el('div',null,'wk-mc-preview'),img=el('img');img.src=asset.url;img.alt=asset.name;img.loading='lazy';img.decoding='async';
                if(asset.animated && asset.height>asset.width){box.style.alignItems='flex-start';img.style.width='100%';img.style.maxHeight='none';img.style.flexShrink='0';}
                box.append(img);return box;
            }
            function field(label,value){var l=el('label',label),input=el('input');input.value=value;input.readOnly=true;input.setAttribute('aria-label',label);details.append(l,input);return input;}
            function copyButton(text,input){var b=el('button',text,'wk-mc-button');b.type='button';b.addEventListener('click',function(){
                if(navigator.clipboard && navigator.clipboard.writeText){navigator.clipboard.writeText(input.value).then(function(){status.textContent='Copied '+text.toLowerCase()+'.';}).catch(function(){input.focus();input.select();status.textContent='Press Ctrl+C to copy the selected code.';});}
                else{input.focus();input.select();status.textContent='Press Ctrl+C to copy the selected code.';}
            });return b;}
            function select(asset){
                selected=asset.id;details.replaceChildren(el('h3',asset.name),preview(asset,true));
                details.append(el('p',asset.width+' × '+asset.height+' pixels'+(asset.animated?' · animation sheet (first frame preview)':'')));
                var fileLink=el('a','Open wiki file page');fileLink.href='/w/'+encodeURIComponent('File:'+asset.filename);details.append(fileLink);
                var name=field('Filename for the visual editor',asset.filename),row=el('div',null,'wk-mc-copy-row');row.append(copyButton('Copy filename',name));details.append(row);
                var markup=field('Wikitext','[[File:'+asset.filename+'|32px|alt='+asset.name+']]');row=el('div',null,'wk-mc-copy-row');row.append(copyButton('Copy wikitext',markup));details.append(row);
                var template=field('Compact template','{{MC|'+asset.id+'|32}}');row=el('div',null,'wk-mc-copy-row');row.append(copyButton('Copy template',template));details.append(row);
                details.append(el('p','Use Insert → Images and media in the visual editor, then search for the filename.'));
                grid.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.id===selected));});
            }
            function render(){
                grid.replaceChildren();var total=Math.max(1,Math.ceil(matches.length/size));page=Math.min(page,total-1);
                matches.slice(page*size,(page+1)*size).forEach(function(asset){var b=el('button',null,'wk-mc-card');b.type='button';b.dataset.id=asset.id;b.setAttribute('aria-pressed',String(asset.id===selected));b.setAttribute('aria-label',asset.name+' — '+asset.category);b.append(preview(asset),el('span',asset.name));b.addEventListener('click',function(){select(asset);});grid.append(b);});
                if(!matches.length)grid.append(el('p','No images match your search.'));
                pageLabel.textContent='Page '+(page+1)+' of '+total;prev.disabled=page===0;next.disabled=page>=total-1;
                status.textContent=matches.length.toLocaleString()+' of '+data.count.toLocaleString()+' images · Java Edition '+data.version;
            }
            function update(){var terms=search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);matches=data.assets.filter(function(a){var hay=(a.name+' '+a.id).toLowerCase().replaceAll('_',' ');return(!filter.value||a.category===filter.value)&&terms.every(function(t){return hay.includes(t);});});page=0;render();}
            search.addEventListener('input',update);filter.addEventListener('change',update);prev.addEventListener('click',function(){page--;render();});next.addEventListener('click',function(){page++;render();});render();
        }).catch(function(){status.textContent='The image library could not load. Reload this page, or use Browse uploaded files in the wiki.';});
    }
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
}());
