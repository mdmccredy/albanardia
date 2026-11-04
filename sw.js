/* Network first, cache fallback, so the app opens offline but always shows the newest pages when online. */
const CACHE='albanardia-v8';
const SHELL=['./','index.html','manifest.json','app/app.js','icons/icon-192.png','icons/icon-512.png','icons/icon-180.png','icons/icon-512-maskable.png','icons/favicon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);
  if(u.origin!==location.origin||/\.(mp4|mov)$/i.test(u.pathname)||r.headers.has('range'))return;
  e.respondWith(fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp))}return res}).catch(()=>caches.match(r).then(m=>m||(r.mode==='navigate'?caches.match('./'):undefined))));
});
