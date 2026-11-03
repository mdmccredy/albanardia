/* Albanardia web app shell: home button on every page, service worker, install meta. */
(function(){
  var me=document.currentScript;
  var root=me.src.replace(/app\/app\.js.*$/,'');
  var here=location.href.split('#')[0].split('?')[0];
  var isHome=(here===root||here===root+'index.html');
  var head=document.head||document.getElementsByTagName('head')[0];
  function meta(sel,tag,attrs){if(document.querySelector(sel))return;var e=document.createElement(tag);for(var k in attrs)e.setAttribute(k,attrs[k]);head.appendChild(e)}
  meta('link[rel=manifest]','link',{rel:'manifest',href:root+'manifest.json'});
  meta('link[rel~=icon]','link',{rel:'icon',type:'image/png',href:root+'icons/favicon.png'});
  meta('link[rel=apple-touch-icon]','link',{rel:'apple-touch-icon',href:root+'icons/icon-180.png'});
  meta('meta[name=apple-mobile-web-app-capable]','meta',{name:'apple-mobile-web-app-capable',content:'yes'});
  meta('meta[name=mobile-web-app-capable]','meta',{name:'mobile-web-app-capable',content:'yes'});
  meta('meta[name=apple-mobile-web-app-title]','meta',{name:'apple-mobile-web-app-title',content:'Albanardia'});
  meta('meta[name=apple-mobile-web-app-status-bar-style]','meta',{name:'apple-mobile-web-app-status-bar-style',content:'default'});
  if('serviceWorker' in navigator){addEventListener('load',function(){navigator.serviceWorker.register(root+'sw.js',{scope:root}).catch(function(){})})}
  var standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
  document.documentElement.classList.toggle('app-standalone',standalone);
  if(isHome)return;
  var css=document.createElement('style');
  css.textContent=
   '.ahome{display:inline-flex;align-items:center;gap:6px;height:40px;padding:0 12px 0 8px;border-radius:20px;background:#fff;color:#16202a;border:1px solid rgba(0,0,0,.12);box-shadow:0 2px 10px rgba(0,0,0,.16);font:600 14px/1 system-ui,-apple-system,"Segoe UI",sans-serif;text-decoration:none;-webkit-tap-highlight-color:transparent;z-index:2147483000}'+
   '.ahome img{width:26px;height:26px;border-radius:7px;display:block}'+
   '.ahome svg{width:14px;height:14px;flex:none}'+
   '.ahome:active{transform:scale(.96)}'+
   '.ahome:focus-visible{outline:3px solid #1d5fa8;outline-offset:2px}'+
   '.ahome.float{position:fixed;left:max(12px,env(safe-area-inset-left));bottom:max(14px,calc(env(safe-area-inset-bottom) + 6px))}'+
   '.ahome.top{position:fixed;left:max(10px,env(safe-area-inset-left));top:max(10px,calc(env(safe-area-inset-top) + 6px))}'+
   '.ahome.inbar{box-shadow:none;height:36px;padding:0 10px 0 6px;margin-right:4px;flex:none}'+
   '.ahome.inbar span{display:none}'+
   '@media (prefers-color-scheme:dark){.ahome:not(.inbar){background:#1a2129;color:#eef1f4;border-color:rgba(255,255,255,.14)}}';
  head.appendChild(css);
  var a=document.createElement('a');
  a.href=root;a.className='ahome';a.setAttribute('aria-label','Back to Albanardia home');
  a.innerHTML='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10.5 2.5 5 8l5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg><img src="'+root+'icons/icon-192.png" alt=""><span>Home</span>';
  var mode=me.getAttribute('data-home')||'float';
  function place(){
    var slot=mode.indexOf('slot:')===0&&document.querySelector(mode.slice(5));
    if(slot){a.classList.add('inbar');slot.insertBefore(a,slot.firstChild)}
    else{a.classList.add(mode==='top'?'top':'float');document.body.appendChild(a)}
  }
  if(document.body)place();else addEventListener('DOMContentLoaded',place);
})();
