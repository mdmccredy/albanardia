// Place cards: tap any business or landmark on the map to open a card with
// photos, description, address, phone, hours and website (Apple Maps style).
(()=>{
const el=document.getElementById('place');if(!el||!window.__openPlace)return;
const SITES=[["^Silverbrooks Yacht Club$", "../sbyc/", "sbyc.org", "At the outer end of Hanson Bay Marina on Silverbrooks' north shore.", ""], ["^Northeastern Yacht Club$", "../neyc/", "neyc.org", "Rutherford's big-boat and junior racing club.", ""], ["^Corinthian Yacht Club", "../cyc/", "cycsb.org", "A racing club on the north shore of the bay, home of a strong junior team.", ""], ["^Waterloo Yacht Club$", "../wyc/", "waterlooyc.org", "River and bay sailing in Rochester County.", ""], ["^Foxford Yacht Club$", "../fyc/", "foxfordyc.org", "Sound sailing a short walk from the Larssen boat works.", ""], ["^Albanardia City Yacht Club$", "../acyc/", "acyc.org", "The state's second city's home club.", ""], ["^New Brolin Yacht Club$", "../nbyc/", "nbyc.org", "Ocean-side sailing near the Olympic Sailing Pavilion.", ""], ["^Cape Sturgeon Yacht Club$", "../csyc/", "csyc.org", "Open-water sailing at the tip of Cape Sturgeon.", ""], ["^Belwether Yacht Club$", "../bwyc/", "belwetheryc.org", "The college town's club, beside the Alex Bennett Marina.", ""], ["^Everett Yacht Club$", "../eyc/", "everettyc.org", "A neighborhood club in Silverbrooks.", ""], ["^Elliott Bay Yacht Club$", "../ebyc/", "ebyc.org", "Marisfield's club on Elliott Bay.", ""], ["^Notrhabite Sailing Club", "../nsc/", "notrhabite.org", "A river sailing club on the Wellington.", ""], ["^Sjagette Yacht Club$", "../syc/", "sjagetteyc.org", "On Farsgod Point at the harbor mouth.", ""], ["^Northmark Yacht Club$", "../nmyc/", "northmarkyc.org", "Farm-country river sailing in Northmark County.", ""], ["^Stepford Yacht Club$", "../styc/", "stepfordyc.org", "Archila County's yacht club.", ""], ["^Marianoe Yacht Club$", "../myc/", "marianoeyc.org", "A small island-town club on the Sound.", ""], ["^Silverbrooks Community Sailing", "../sbcs/", "sbcommunitysailing.org", "Public sailing for the whole city, from first sails to racing teams.", ""], ["^Pearl's End Sailing Center$", "../pesc/", "pesc.org", "On the oyster-boat waterfront at Pearl's End.", ""], ["^Hamilton Island Sailing Club$", "../his/", "hisc.org", "A community sailing club on the island, reached by ferry.", ""], ["^Willamette Boating Center$", "../wbc/", "wboating.org", "Boating and sailing lessons for Coven County.", ""], ["^Coven Community Sailing", "../ccs/", "covencommsail.org", "Community sailing on Coven Bay, next to the Maritime Academy.", ""], ["^Archila Community Sailing", "../acsc/", "acsc.org", "Public sailing for Archila County.", ""], ["^Northeastern Sailing Foundation", "../nesf/", "nesf.org", "Albanardia's sailing foundation: the AYRC, youth grants, race officer and coach training.", ""], ["^Silverbrooks Sailing Foundation", "../sbsf/", "sbsf.org", "The nonprofit behind Silverbrooks Yacht Club and the Silverbrooks Community Sailing Center.", ""], ["^Larssen", "../larssensailing/", "larssensailing.com", "Larssen Sailing builds the Larssen ILCA, Club 420, Club FJ, Bauer and SK range in Foxford, Albanardia. Approved ILCA builder.", "(302) 555-0144"], ["^Silverbrooks Public Library", "../sbpl/", "sbpl.org", "", ""], ["Silverbrooks Thompson International|^SBX\\b", "../flysbx/", "flysbx.com", "Flights, parking, transit, dining and travel information for Silverbrooks Thompson International Airport (SBX).", ""], ["^(Silverbrooks )?City Hall$", "../gov/", "silverbrooks.gov", "", ""], ["^(Alexandria Hall|The Mainsail|Foundry Hall|New Sweden Heritage Hall|Tidewater Lab|Silverbrooks Museum of Art|Albanardia Maritime Museum|Lantern Night Market|Lantern Garden)", "../visit/", "visitsilverbrooks.com", "", ""], ["^McKay University", "../colleges/mckay/", "mckay.edu", "", ""], ["^Aldense( University)?$|^Aldense (Specter|Mirano)", "../colleges/aldense/", "aldense.edu", "", ""], ["^(AlbTech|Albanardia Institute of Technology)$", "../colleges/albtech/", "albtech.edu", "", ""], ["^Silverbrooks University$", "../colleges/sbu/", "sbu.edu", "", ""], ["^Smithsonian College", "../colleges/smithsonian/", "smithsoniancollege.edu", "", ""], ["Saint-Mars", "../colleges/saint-marse/", "usm.edu", "", ""], ["^University of Albanardia: Silverbrooks", "../colleges/ua-silverbrooks/", "silverbrooks.ua.edu", "", ""], ["^University of Albanardia: Foxford", "../colleges/ua-foxford/", "foxford.ua.edu", "", ""], ["^University of Albanardia: Waterloo", "../colleges/ua-waterloo/", "waterloo.ua.edu", "", ""], ["^University of Albanardia: Albanardia City", "../colleges/ua-albanardia-city/", "acity.ua.edu", "", ""], ["^University of Albanardia: Mo", "../colleges/ua-moiyane/", "moiyane.ua.edu", "", ""]].map(s=>[new RegExp(s[0]),s[1],s[2],s[3],s[4]]);
const BRANDS={"Starbucks": "starbucks.com", "McDonald's": "mcdonalds.com", "Dunkin'": "dunkindonuts.com", "Wawa": "wawa.com", "Chick-fil-A": "chick-fil-a.com", "Subway": "subway.com", "Chipotle": "chipotle.com", "Taco Bell": "tacobell.com", "Wendy's": "wendys.com", "Burger King": "bk.com", "Panera Bread": "panerabread.com", "Domino's": "dominos.com", "CVS Pharmacy": "cvs.com", "Walgreens": "walgreens.com", "7-Eleven": "7-eleven.com", "Acme Markets": "acmemarkets.com", "Giant": "giantfood.com", "Trader Joe's": "traderjoes.com", "Whole Foods Market": "wholefoodsmarket.com", "Shell": "shell.us", "Exxon": "exxon.com", "Sunoco": "sunoco.com", "Target": "target.com", "Walmart": "walmart.com", "The Home Depot": "homedepot.com", "Costco": "costco.com", "Best Buy": "bestbuy.com", "Apple Store": "apple.com/retail", "Dollar General": "dollargeneral.com", "Tractor Supply": "tractorsupply.com", "Royal Farms": "royalfarms.com", "Apple": "apple.com", "Microsoft": "microsoft.com", "Amazon": "amazon.com", "Google": "google.com", "Delta": "delta.com"};
const PH={"yacht": ["1512602110-67198e50f815", "1587365001066-8263b7061a38", "1548689572-a7eacaf43534", "1559818003-d08b891edeb3"], "sailing": ["1506527240747-720a3e17b910", "1601860750456-2a7fd1384772", "1506527115643-b3b387978fad", "1599134432254-e8cbfb74f1ab"], "marina": ["1590473713374-dc331cb3f60e", "1595973641416-35ae8a6eb1d3", "1548689572-a7eacaf43534"], "college": ["1562774053-701939374585", "1583373834259-46cc92173cb7", "1576495199011-eb94736d05d6"], "school": ["1509062522246-3755977927d7", "1580582932707-520aed937b7b", "1577896851231-70ef18881754", "1588072432836-e10032774350"], "library": ["1576164285450-6d26c5b1a2a6", "1521587760476-6c12a4b040da", "1507842217343-583bb7270b66"], "stadium": ["1489944440615-453fc2b6a9a9", "1599158150601-1417ebbaafdd", "1522778119026-d647f0596c20"], "arena": ["1577125527890-475beedd75d3", "1546519638-68e109498ffc", "1504450758481-7338eba7524a"], "hall": ["1519683109079-d5f539e1542f", "1458639817867-2c9d4c5dcad4", "1519682718457-c82ce8296645"], "museum": ["1491156855053-9cdff72c7f85", "1575223970966-76ae61ee7838", "1534445291134-f70b7a81f691"], "gov": ["1611010638643-051de75362ff", "1581097543550-b3cbe2e6ea6e", "1520525003249-2b9cdda513bc"], "church": ["1511527661048-7fe73d85e9a4", "1642695113989-105367adabe6", "1594990375715-2d008aaaa31b"], "hospital": ["1586773860418-d37222d8fce3", "1519494026892-80bbd2d6fd0d", "1479839672679-a46483c0e7c8"], "airport": ["1561101904-da649fcbf03f", "1549897411-b06572cdf806", "1530521954074-e64f6810b32d"], "park": ["1605540827677-693bad36b91f", "1621661514271-48da9d48580f", "1623593419606-7f9c8c22d736"], "cafe": ["1567880905822-56f8e06fe630", "1521017432531-fbd92d768814", "1511081692775-05d0f180a065"], "restaurant": ["1517248135467-4c7edcad34c4", "1551632436-cbf8dd35adfa", "1508424757105-b6d5ad9329d0"], "fastfood": ["1545575950-59f935d6521c", "1566380055434-1dfac9eb516d", "1593462386344-bc7ffba51a1e"], "grocery": ["1604719312566-8912e9227c6a", "1542838132-92c53300491e", "1583258292688-d0213dc5a3a8"], "gas": ["1567777176186-dfa735f1fe20", "1585740452884-2a29a1d21514"], "store": ["1441986300917-64674bd600d8", "1472851294608-062f824d29cc", "1567958451986-2de427a4a0be"], "office": ["1486406146926-c627a92ad1ab", "1534237710431-e2fc698436d0"], "ferry": ["1633775362313-fed93ef8e824"], "landmark": ["1534237710431-e2fc698436d0", "1486406146926-c627a92ad1ab"], "hotel": ["1551632436-cbf8dd35adfa"], "station": ["1597629623484-27ba27a4e47f", "1533404378786-7ef0715ec859", "1572414323397-e7918784a4b7"], "subway": ["1597629623484-27ba27a4e47f", "1533404378786-7ef0715ec859"], "rail": ["1533404378786-7ef0715ec859", "1597629623484-27ba27a4e47f"], "stop": ["1561101904-da649fcbf03f", "1549897411-b06572cdf806"], "bus": ["1570933657058-401caa810e60", "1557418223-39e7931d52af"], "peak": ["1632853359743-edcc974313f2", "1588765838710-db90bd1a4013", "1551120738-c3fcea8d0cf8"], "hood": ["1557418223-39e7931d52af", "1570933657058-401caa810e60", "1516458819443-0f257d640de9"], "road": ["1496055401924-5e7fdc885742", "1508916319692-80a99da75692", "1501276276428-88ec0b385919"], "island": ["1636334657600-527eb23abe8b", "1642266116733-832d23c249f0"], "city": ["1630408653504-20c9d4849b72", "1642266116733-832d23c249f0", "1611839234650-997b22bd1ea6"], "town": ["1683547664033-2c2f4d6d1b5d", "1557418223-39e7931d52af", "1570933657058-401caa810e60"], "county": ["1629016943072-0bf0ce4e2608", "1451440063999-77a8b2960d2b", "1683547664033-2c2f4d6d1b5d"]};
const esc=s=>String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const img=(i,w=800)=>`https://images.unsplash.com/photo-${i}?auto=format&fit=crop&w=${w}&q=70`;
const LBL={yacht:'Yacht club',sailing:'Sailing center',marina:'Marina',college:'College',school:'School',library:'Library',stadium:'Stadium',arena:'Arena',hall:'Performing arts',museum:'Museum',gov:'Government',church:'Place of worship',hospital:'Hospital',airport:'Airport',park:'Park',cafe:'Coffee shop',restaurant:'Restaurant',fastfood:'Fast food',grocery:'Grocery store',gas:'Gas station',store:'Store',office:'Office',ferry:'Ferry',fire:'Fire station',hotel:'Hotel',landmark:'Landmark',place:'Place'};
const HRS={yacht:'Clubhouse 11 AM–10 PM · Office Tue–Sat 9–5',sailing:'Daily 9 AM–6 PM (season) · Office Mon–Fri 9–5',marina:'Harbormaster 7 AM–7 PM daily',college:'Campus open daily · Visitor center Mon–Fri 9–5',school:'Mon–Fri 7:30 AM–3:30 PM',library:'Mon–Thu 9–8 · Fri–Sat 9–6 · Sun 12–5',stadium:'Box office Mon–Fri 10–6 and game days',arena:'Box office Mon–Fri 10–6 and event days',hall:'Box office Tue–Sat 11–6 and 2 hrs before shows',museum:'Tue–Sun 10 AM–5 PM · Closed Mon',gov:'Mon–Fri 8:30 AM–4:30 PM',church:'Daily 8 AM–6 PM · Mass/services Sun',hospital:'Open 24 hours · Emergency 24/7',airport:'Open 24 hours',park:'Daily 6 AM–10 PM',cafe:'Daily 6 AM–7 PM',restaurant:'Daily 11:30 AM–10 PM',fastfood:'Daily 6 AM–11 PM',grocery:'Daily 7 AM–10 PM',gas:'Open 24 hours',store:'Mon–Sat 9–9 · Sun 10–7',office:'Mon–Fri 8 AM–6 PM',ferry:'First sailing 5:30 AM · Last 12:30 AM',fire:'Open 24 hours · Call 911 for emergencies',hotel:'Check-in 3 PM · Check-out 11 AM · Front desk 24 hours',landmark:'Daily 9 AM–10 PM'};
function cat(n,d){return cat1(n.toLowerCase())||cat1((n+' | '+d).toLowerCase())||'place';}
function cat1(s){
 const T=[[/yacht club|keelboat club|sailing club/,'yacht'],[/sailing (center|pavilion)|community sailing|boating center|boathouse|sailing foundation|sailcraft|sailing team/,'sailing'],[/marina/,'marina'],
 [/amex garden|mckay garden|coliseum|rink$|\bgym$/,'arena'],[/jetblue park|ballpark|stadium$|\bfield$/,'stadium'],[/mainsail|monument|observation/,'landmark'],[/food hall|market hall|crab house|oyster house|brewing|donut|fries/,'restaurant'],
 [/library/,'library'],[/museum|gallery|heritage|aquarium|\blab\b/,'museum'],[/hospital|medical center|clinic/,'hospital'],[/ferry/,'ferry'],[/international$|airport|concourse|terminal\b/,'airport'],[/hotel|\binn$/,'hotel'],[/fire co|fire station|fire dept/,'fire'],
 [/elementary|middle school|high school|private school|academy|école|prep\b|\bschool$/,'school'],[/headquarters|\bhq\b|fulfillment|engineering campus|regional office|\bbank\b|the silverbrooks times/,'office'],[/university|college|institute|school of (law|engineering)|campus/,'college'],
 [/stadium|ballpark|field\b.*home|football|baseball|soccer/,'stadium'],[/arena|fieldhouse|garden\b.*home|basketball|hockey|gym and/,'arena'],
 [/opera|ballet|symphony|concert|konserthus|entrium|theat|movie palace|performing|music hall|\bhall\b.*(arts|lobby)/,'hall'],
 [/capitol|city hall|town hall|courthouse|department of|state house/,'gov'],[/cathédrale|cathedral|church|église|temple|chapel|basilica|mosque|synagogue/,'church'],
 [/fast food|mcdonald|burger|wendy|taco bell|chick-fil-a|subway|chipotle|domino|panera/,'fastfood'],[/coffee|café|cafe|bakery|kaffe|starbucks|dunkin/,'cafe'],
 [/restaurant|oyster bar|wine bar|bistro|brewery|market of food|covered market|fish pier|grill|diner|pizz/,'restaurant'],
 [/grocery|markets?$|acme|giant|trader joe|whole foods|wawa|royal farms|7-eleven/,'grocery'],[/gas station|shell|exxon|sunoco/,'gas'],
 [/store|pharmacy|cvs|walgreens|target|walmart|home depot|costco|best buy|dollar general|tractor supply|hardware|arcade|shop/,'store'],
 [/office|tower/,'office'],[/park|commons|square|garden|green\b|trail|beach|lighthouse|\blight$|reservoir|plaza|promenade|fairgrounds|orchard|vineyard|farm\b/,'park']];
 for(const [r,c] of T)if(r.test(s))return c;return '';}
const hash=s=>{let h=7;for(const c of s)h=(h*31+c.charCodeAt(0))>>>0;return h;};
const phoneFor=n=>`(302) 555-01${String(hash(n)%100).padStart(2,'0')}`;
function siteFor(n){for(const s of SITES)if(s[0].test(n))return {url:s[1],dom:s[2],about:s[3],phone:s[4]};
 const b=Object.keys(BRANDS).sort((a,c)=>c.length-a.length).find(k=>n===k||n.startsWith(k+' ')||n.startsWith(k+' ·'));if(b)return {url:'https://www.'+BRANDS[b].replace(/^www\./,''),dom:BRANDS[b],ext:true};return null;}
const TIPS={};
function parseTip(t){const m=String(t||'').match(/^<b>(.*?)<\/b>([\s\S]*)$/);if(!m)return null;const tmp=document.createElement('div');tmp.innerHTML=m[1];const name=tmp.textContent.trim();
 tmp.innerHTML=m[2].replace(/<br\s*\/?>/g,'\n');const lines=tmp.textContent.split('\n').map(s=>s.trim()).filter(Boolean);return {name,lines};}
function qualifies(h){const t=h.getAttribute('data-tip');const p=parseTip(t);if(!p||!p.name)return null;
 p.name=p.name.replace(/^✈\s*/,'');return p;}
function kindOf(h,p){const t=h.getAttribute('data-tip')||'',j=p.lines.join(' · ');
 if(h.dataset.line||h.closest('[data-line]')){if(/SBMetro/.test(t))return 'bus';if(/ALBExpress/.test(t))return 'rail';if(/SBFerry|Ferry/.test(t))return 'ferry';return 'subway';}
 if(/SBTrain station/.test(t))return 'station';if(/ALBExpress station/.test(t))return 'rail';if(/Shuttle stop/.test(t))return 'stop';
 if(/^(Interstate|I-\d|US Route|US \d|State Route|Route \d|AB-\d|Exit \d)/.test(p.name)||/ (St|Ave|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Pkwy|Parkway|Way|Hwy|Highway)$/.test(p.name)||/tunnel|bridge$/i.test(p.name))return 'road';
 if(/^\d[\d,]* ft\b/.test(p.lines[0]||''))return 'peak';if(/Neighborhood in/.test(j))return 'hood';if(/island/i.test(p.name+j)&&!/, AB \d{5}/.test(j))return 'island';
 return '';}
// tag markers just before the map's own click handler runs, so it opens our card
document.addEventListener('pointerdown',e=>{const h=e.target.closest&&e.target.closest('.hit');if(!h||h.dataset.place)return;const p=qualifies(h);if(!p)return;p.k=kindOf(h,p);TIPS[p.name]=p;h.dataset.place='biz|'+p.name;},true);
const TRANSIT_SITE={bus:['../transit/sbmetro.html','SBMetro map'],subway:['../transit/sbtrain.html','SBTrain map'],station:['../transit/sbtrain.html','SBTrain map'],rail:['../transit/sbexpress.html','ALBExpress map'],ferry:['../transit/sbferry.html','SBFerry map'],stop:['../flysbx/','flysbx.com']};
const XLBL={bus:'Bus route',subway:'Train line',rail:'ALBExpress',ferry:'Ferry route',station:'SBTrain station',stop:'Airport shuttle stop',road:'Road',peak:'Mountain',hood:'Neighborhood',island:'Island',town:'City',county:'County',state:'State',club:''};
// one card layout for everything (the Foster High School look)
function card(o){
 if(matchMedia('(max-width:640px), (max-height:500px)').matches){const pn=document.getElementById('panel');if(pn)pn.open=false;const d=document.getElementById('dir');if(d&&d.classList)d.classList.remove('on');}
 document.body.classList.add('placeon');const pics=o.pics||[],s=o.site,ph=o.phone;
 const sub=[o.badge?`<img class="pc-badge" src="${o.badge}" alt="">`:'',esc(o.label||'Place'),o.town?' · '+esc(o.town):''].join('');
 el.innerHTML=`<button class="x" aria-label="Close">✕</button>
 ${pics.length?`<div class="pc-ph">${pics.map((i,k)=>`<img src="${img(i,k?500:900)}" alt="" loading="lazy" onerror="const q=this.parentNode;this.remove();if(q&&!q.children.length)q.remove()">`).join('')}</div>`:''}
 <h2>${esc(o.name)}</h2><div class="sub">${sub}</div>
 <div class="pc-act">
  ${o.go?`<button data-go="${o.go[0]},${o.go[1]}"><span>⌖</span>Show on map</button>`:`<button data-pc="dir"><span>➜</span>Directions</button>`}
  ${ph?`<a href="tel:${ph.replace(/\D/g,'')}"><span>✆</span>Call</a>`:''}
  ${s?`<a href="${esc(s.url)}" ${s.ext?'target="_blank" rel="noopener"':''}><span>⌂</span>Website</a>`:''}
 </div>
 ${o.about&&o.about.length?`<div class="pc-about">${o.about.map(a=>`<p>${esc(a)}</p>`).join('')}</div>`:''}
 <div class="pc-rows">
  ${o.addr?`<div><b>Address</b>${esc(o.addr)}</div>`:''}
  ${(o.rows||[]).map(r=>`<div><b>${esc(r[0])}</b>${r[2]?r[1]:esc(r[1])}</div>`).join('')}
  ${o.hours?`<div><b>Hours</b>${esc(o.hours)}</div>`:''}
  ${ph?`<div><b>Phone</b><a href="tel:${ph.replace(/\D/g,'')}">${esc(ph)}</a></div>`:''}
  ${s?`<div><b>Website</b><a href="${esc(s.url)}" ${s.ext?'target="_blank" rel="noopener"':''}>${esc(s.dom)}</a></div>`:''}
 </div>
 ${o.extra?`<div class="pc-extra">${o.extra}</div>`:''}
 ${pics.length?`<div class="note">Photos are representative, via Unsplash.</div>`:''}`;
 el.classList.add('on');el.scrollTop=0;el.dataset.pc=o.dirTo||o.name;}
function openBiz(n){const p=TIPS[n]||{name:n,lines:[]};const all=p.lines.join(' · ');
 let addr='',town='';const parts=all.split(' · ');const ai=parts.findIndex(x=>/, AB( \d{5})?/.test(x));if(ai>=0){addr=parts.splice(ai,1)[0];const m=addr.match(/,\s*([^,]+),\s*AB/);if(m)town=m[1];}
 const desc=parts.filter(x=>x&&!/^(click for|AYRC member club)/i.test(x)&&x!==town&&!/^[A-Z][A-Z-]{1,6}$/.test(x)).join(' · ');
 const k=p.k||'';
 if(k){const ts=TRANSIT_SITE[k];
  return card({name:n,label:XLBL[k],town,pics:(PH[k]||[]).slice(0,3),about:desc?[desc]:[],addr,site:ts?{url:ts[0],dom:ts[1]}:(k==='hood'&&/Silverbrooks/.test(desc)?{url:'../gov/#neighborhoods',dom:'silverbrooks.gov'}:null),
   hours:k==='station'||k==='rail'?'5 AM–1 AM daily':k==='stop'?'24 hours':'',phone:k==='station'||k==='rail'||k==='bus'||k==='subway'?'(302) 555-0110':''});}
 const c=cat(n,desc);let s=siteFor(n);if(!s&&c==='school'&&/Silverbrooks/.test(addr)&&!/private/i.test(desc))s={url:'../sbps/#schools',dom:'sbps.org'};if(!s&&c==='library'&&/Silverbrooks, AB/.test(addr))s={url:'../sbpl/#locations',dom:'sbpl.org'};const ph=(s&&s.phone)||(['place'].includes(c)?'':phoneFor(n));
 const about=[s&&s.about,desc].filter(Boolean).filter((x,i,a)=>a.indexOf(x)===i);
 card({name:n,label:LBL[c]||'Place',town,pics:(PH[c]||[]).slice(0,3),about,addr,hours:HRS[c]||'',phone:ph,site:s});}
function openClub(id){const C=(window.__CLUB||{})[id]||[id,''];const I=window.__CLUBINFO;const n=C[0];
 const addr=typeof caddrTxt==='function'?caddrTxt(id):'';const m=addr.match(/,\s*([^,]+),\s*AB/);const kind=I?I.kind(id):'Yacht club';
 const c=/community|center|foundation|boating/i.test(kind+' '+n)?'sailing':'yacht';const s0=siteFor(n);
 const site=I?{url:(window.SITE_BASE||'../')+I.dir(id)+'/',dom:(I.info.WEB||{})[id]||(s0&&s0.dom)||'Website'}:s0;
 const kd=kind.toLowerCase().replace(/\bayrc\b/g,'AYRC').replace(/^./,c=>c.toUpperCase());
 card({name:n,label:kd,town:m?m[1]:'',badge:window.__BURGEE?window.__BURGEE(id):'',pics:PH[c].slice(0,3),about:[s0&&s0.about].filter(Boolean),addr,hours:HRS[c],phone:(s0&&s0.phone)||phoneFor(n),site});}
function openStats(t,n){orig(t,n);const tmp=document.createElement('div');tmp.innerHTML=el.innerHTML;
 tmp.querySelector('.x')?.remove();const h=tmp.querySelector('h2');const name=h?h.textContent:n;h?.remove();const sb=tmp.querySelector('.sub');const sub=sb?sb.textContent:'';sb?.remove();
 const go=tmp.querySelector('[data-go]');const gc=go?go.dataset.go.split(',').map(Number):null;
 const sb2=t==='town'&&/^Silverbrooks$/.test(n)?{url:'../gov/',dom:'silverbrooks.gov'}:t==='town'?siteFor(n):null;
 const big=t==='state'||(t==='town'&&/^(Silverbrooks|Albanardia City)$/.test(n));
 card({name,label:t==='town'?'City':t==='county'?'County':'State',town:'',pics:(PH[big?'city':t==='town'?'town':'county']||[]).slice(0,3),about:sub?[sub]:[],extra:tmp.innerHTML,site:sb2,go:t!=='town'?gc:null,dirTo:n});}
el.addEventListener('click',e=>{const b=e.target.closest('[data-pc="dir"]');if(!b)return;const n=el.dataset.pc;const dir=document.getElementById('dir'),btn=document.getElementById('dirbtn'),to=document.getElementById('dto');
 if(dir&&dir.hidden&&btn)btn.click();if(!to)return;to.value=n;to.dispatchEvent(new Event('input'));setTimeout(()=>{to.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter'}));},30);
 if(matchMedia('(max-width:640px)').matches){el.classList.remove('on');document.body.classList.remove('placeon');}});
window.__pc={cat,qualifies,parseTip};
const orig=window.__openPlace;window.__openPlace=(t,n)=>t==='biz'?openBiz(n):t==='club'?openClub(n):openStats(t,n);
const st=document.createElement('style');st.textContent=`
#place .pc-ph{display:flex;gap:4px;margin:-14px -16px 12px;height:150px;overflow-x:auto;scroll-snap-type:x mandatory;border-radius:14px 14px 0 0;scrollbar-width:none}
#place .pc-ph img{height:100%;flex:0 0 auto;width:78%;object-fit:cover;scroll-snap-align:start;background:#ddd}
#place .pc-ph img:only-child{width:100%}
#place:has(.pc-ph) .x{background:rgba(0,0,0,.55);color:#fff;border-radius:50%;width:28px;height:28px;font-size:14px;z-index:1}
#place .pc-act{display:flex;gap:8px;margin:10px 0 12px}
#place .pc-act>*{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 4px;border-radius:10px;border:0;background:rgba(47,111,214,.12);color:#2f6fd6;font:600 12px var(--font,system-ui);text-decoration:none;cursor:pointer}
#place .pc-act span{font-size:17px;line-height:1}
#place .pc-about p{margin:0 0 8px;line-height:1.45}
#place .pc-rows>div{padding:8px 0;border-top:1px solid rgba(128,128,128,.22)}
#place .pc-badge{height:14px;vertical-align:-2px;margin-right:6px}
#place .pc-extra{margin-top:6px}
#place .pc-extra h3{font-size:11px;color:#8e8e93;font-weight:600;text-transform:uppercase;letter-spacing:.4px;margin:12px 0 4px}
#place .pc-rows b{display:block;font-size:11px;color:#8e8e93;font-weight:600;text-transform:uppercase;letter-spacing:.4px}`;
document.head.appendChild(st);
})();

// Deep links: map/#place=<name> (or ?place=) centers the map on that place and opens its card.
(()=>{
const norm=s=>String(s||'').toLowerCase().replace(/[’']/g,"'").replace(/\s+/g,' ').trim();
function want(){const a=new URLSearchParams(location.hash.slice(1)).get('place');const b=new URLSearchParams(location.search).get('place');return a||b||'';}
function club(n){const C=window.__CLUB||{};return Object.keys(C).find(id=>norm(C[id][0])===norm(n)||norm(id)===norm(n));}
function hitFor(n){for(const h of document.querySelectorAll('svg .hit')){if(h.dataset.place&&h.dataset.place.split('|')[1]&&norm(h.dataset.place.split('|')[1])===norm(n))return h;const p=window.__pc&&window.__pc.qualifies(h);if(p&&norm(p.name)===norm(n))return {p,h};}return null;}
const ALIAS={'silverbrooks thompson international airport':'SBX Concourse C','sbx':'SBX Concourse C','silverbrooks sailing foundation':'Silverbrooks Yacht Club','port of silverbrooks':'Port of Silverbrooks','university of albanardia: moïyane':'Moïyane'};
function open(q){q=ALIAS[norm(q)]||q;
 const go=window.__go;if(typeof placeSearch!=='function'||typeof go!=='function')return false;
 const hs=placeSearch(q)||[];const h=hs.find(x=>norm(x.n)===norm(q))||hs.find(x=>norm(x.n).startsWith(norm(q)))||hs[0];
 if(!h)return true;
 go(h);
 const id=club(h.n)||club(q);
 setTimeout(()=>{const tip=document.getElementById('tip');
  if(id){if(tip)tip.style.opacity=0;window.__openPlace('club',id);setTimeout(()=>fit(h),60);return;}
  if(document.body.classList.contains('placeon')){setTimeout(()=>fit(h),60);return;}
  const f=hitFor(h.n);
  if(f&&f.p){f.h.dataset.place='biz|'+f.p.name;f.h.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));if(tip)tip.style.opacity=0;window.__openPlace('biz',f.p.name);}
  else if(f&&f.dataset){if(tip)tip.style.opacity=0;const [t,n]=f.dataset.place.split('|');window.__openPlace(t,n);}
 setTimeout(()=>fit(h),60);},900);
 return true;}
// keep the landmark in view above the bottom card on phones (or right of the side card on desktop)
function fit(h){const card=document.getElementById('place'),svg=document.querySelector('svg');if(!svg||!window.mapGoto)return;
 const r=svg.getBoundingClientRect(),vbA=(svg.getAttribute('viewBox')||'').split(/[ ,]+/).map(Number);if(vbA.length<4||!vbA[2])return;
 const u=vbA[2]/r.width;let cx=r.left+r.width/2,cy=r.top+r.height/2,tx=cx,ty=cy;
 if(card&&document.body.classList.contains('placeon')){const c=card.getBoundingClientRect();
  if(c.top>r.top+r.height*0.3&&c.width>r.width*0.8)ty=r.top+(c.top-r.top)/2;   // bottom sheet
  else if(c.right<r.left+r.width*0.6){const pn=document.getElementById('panel');const pr=pn&&pn.getBoundingClientRect();const R=pr&&pr.width&&pr.left>c.right&&pr.left>r.left+r.width*0.5?pr.left:r.right;tx=c.right+(R-c.right)/2;}}          // side card
 if(tx===cx&&ty===cy)return;
 window.mapGoto(h.x+(cx-tx)*u,h.y+(cy-ty)*u,h.k);if(window.__pinHook)window.__pinHook();}
function run(){const q=want();if(!q)return;let tries=0;(function t(){if(open(q)||++tries>40)return;setTimeout(t,150);})();}
addEventListener('hashchange',run);
if(document.readyState==='complete')setTimeout(run,200);else addEventListener('load',()=>setTimeout(run,200));
})();
