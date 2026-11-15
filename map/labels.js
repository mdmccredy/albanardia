// Label collision: after every pan/zoom, hide labels (and their icons) that would
// overlap a more important one, the way Apple Maps thins labels out.
(()=>{
const S=document.getElementById('map');if(!S)return;
// lower number = more important, wins the space
const PRI={towns:0,counties:0,labels:1,subway:2,express:3,ferry:3,air:4,campus:5,sports:6,clubs:7,schools:8,pois:9,offices:10,islands:11,terrain:12,buses:13,shops:14,roads:15,streets:16};
const st=document.createElement('style');st.textContent='#map .lc{visibility:hidden!important;pointer-events:none!important}';document.head.appendChild(st);
let t=0;
function run(){t=0;
 const ov=document.getElementById('overlay');if(!ov)return;
 S.querySelectorAll('.lc').forEach(e=>e.classList.remove('lc'));
 const items=[];
 ov.querySelectorAll('.ov').forEach((e,i)=>{if(e.style.display==='none'||e.classList.contains('cx'))return;
  const r=e.getBoundingClientRect();if(!r.width||!r.height)return;
  if(r.right<0||r.bottom<0||r.left>innerWidth||r.top>innerHeight)return;
  items.push({e,r,p:PRI[e.dataset.layer]??12,i});});
 const sl=document.getElementById('slabels');
 if(sl)sl.querySelectorAll('text').forEach((e,i)=>{const r=e.getBoundingClientRect();if(r.width&&r.right>0&&r.bottom>0&&r.left<innerWidth&&r.top<innerHeight)items.push({e,r,p:17,i:1e6+i});});
 items.sort((a,b)=>a.p-b.p||a.i-b.i);
 const kept=[],pad=2,cell=64,grid=new Map();
 const cells=r=>{const o=[];for(let x=Math.floor(r.left/cell);x<=Math.floor(r.right/cell);x++)for(let y=Math.floor(r.top/cell);y<=Math.floor(r.bottom/cell);y++)o.push(x+','+y);return o;};
 for(const it of items){const r=it.r,ks=cells(r);let hit=false;
  for(const k of ks){const L=grid.get(k);if(!L)continue;for(const q of L){if(r.left<q.right+pad&&r.right>q.left-pad&&r.top<q.bottom+pad&&r.bottom>q.top-pad){hit=true;break;}}if(hit)break;}
  if(hit){it.e.classList.add('lc');continue;}
  for(const k of ks){if(!grid.has(k))grid.set(k,[]);grid.get(k).push(r);}
 }
}
const go=()=>{clearTimeout(t);t=setTimeout(run,140);};
new MutationObserver(go).observe(S,{attributes:true,attributeFilter:['viewBox','class']});
addEventListener('resize',go);document.addEventListener('change',go,true);
setTimeout(run,800);
window.__labelsRun=run;
})();
