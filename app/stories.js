/* Albanardia shared stories: "All stories" pages, article view and "Latest stories" embeds.
   Data: stories/data.js (window.ALB_STORIES), built by tools/build_stories.py from stories/stories.json. */
(function () {
  const D = window.ALB_STORIES; if (!D) return;
  const SITES = D.sites, ALL = D.stories.slice().sort((a, b) => b.date.localeCompare(a.date) || a.title.localeCompare(b.title));
  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const MONL = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const fd = d => { const [y, m, dd] = d.split('-'); return `${MON[+m - 1]} ${+dd}, ${y}` };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const root = document.currentScript && document.currentScript.dataset.root || (document.body.dataset.root || './');
  const url = u => !u ? '' : /^https?:/.test(u) ? u : root + u;
  const siteOf = s => SITES[s.site] || { name: s.site, c1: '#22498a' };
  function href(s, page) { // where a story card goes
    if (s.link) return url(s.link);
    const si = siteOf(s); return (page && page.site === s.site ? '' : url(si.stories)) + '#' + s.slug;
  }
  function card(s, showSite) {
    const si = siteOf(s), ext = !!s.link;
    return `<a class="as-c" href="${href(s, PAGE)}"${s.img ? '' : ' data-noimg'}>${s.img ? `<span class="as-ph" style="background-image:url('${esc(url(s.img))}')"></span>` : ''}<span class="as-tx"><span class="as-k">${showSite ? `<b style="color:${si.c1}">${esc(si.name)}</b> · ` : ''}${esc(s.cat)} · ${fd(s.date)}${s.added && s.added !== 'original' ? ' <i class="as-new">New</i>' : ''}</span><span class="as-t">${esc(s.title)}</span>${s.dek ? `<span class="as-d">${esc(s.dek)}</span>` : ''}${ext ? `<span class="as-x">Read on ${esc(si.name)} →</span>` : ''}</span></a>`;
  }
  /* ---------- full page ---------- */
  const PAGE = (() => { const el = document.getElementById('alb-stories'); return el ? { el, site: el.dataset.site || '' } : null })();
  if (PAGE) {
    const master = !PAGE.site, si = master ? null : SITES[PAGE.site];
    const mine = master ? ALL : ALL.filter(s => s.site === PAGE.site);
    if (si) { document.documentElement.style.setProperty('--as1', si.c1); document.documentElement.style.setProperty('--as2', si.c2 || '#111') }
    const groups = master ? [...new Set(Object.values(SITES).map(x => x.group))] : [];
    const cats = [...new Set(mine.map(s => s.cat))].sort();
    let st = { q: '', cat: '', grp: '' };
    try { const g = new URLSearchParams(location.search).get('site'); if (g && SITES[g]) location.replace(url(SITES[g].stories)) } catch (e) { }
    PAGE.el.innerHTML = `<header class="as-hd"><div class="as-in"><a class="as-back" href="${master ? root : url(si.home)}">← ${master ? 'Albanardia.gov' : esc(si.name)}</a><div class="as-hk">${master ? 'Every story from every Albanardia website' : esc(si.name)}</div><h1>All stories</h1><p class="as-cnt"></p></div></header>
    <div class="as-in as-tools"><input type="search" class="as-q" placeholder="Search stories" aria-label="Search stories">${master ? `<select class="as-g" aria-label="Website"><option value="">All websites</option>${groups.map(g => `<optgroup label="${esc(g)}">${Object.entries(SITES).filter(([k, v]) => v.group === g).map(([k, v]) => `<option value="${k}">${esc(v.name)}</option>`).join('')}</optgroup>`).join('')}</select>` : ''}
    <div class="as-chips"><button class="on" data-c="">All</button>${cats.map(c => `<button data-c="${esc(c)}">${esc(c)}</button>`).join('')}</div></div>
    <main class="as-in as-list"></main><article class="as-in as-art" hidden></article>`;
    const L = PAGE.el.querySelector('.as-list'), A = PAGE.el.querySelector('.as-art'), C = PAGE.el.querySelector('.as-cnt');
    function list() {
      const q = st.q.toLowerCase();
      const r = mine.filter(s => (!st.cat || s.cat === st.cat) && (!st.grp || s.site === st.grp) && (!q || (s.title + ' ' + s.dek + ' ' + (s.body || []).join(' ') + ' ' + siteOf(s).name).toLowerCase().includes(q)));
      C.textContent = `${r.length} of ${mine.length} stories${master ? ` from ${new Set(mine.map(s => s.site)).size} websites` : ''}`;
      let last = '', h = '';
      r.forEach(s => { const m = s.date.slice(0, 7); if (m !== last) { h += `<h2 class="as-m">${MONL[+m.slice(5) - 1]} ${m.slice(0, 4)}</h2>`; last = m } h += card(s, master) });
      L.innerHTML = h || '<p class="as-none">No stories match.</p>';
    }
    function art(slug) {
      const s = mine.find(x => x.slug === slug && (!x.link)) || (master && ALL.find(x => (x.site + '/' + x.slug) === slug));
      if (!s) { A.hidden = true; L.hidden = false; PAGE.el.querySelector('.as-tools').hidden = false; return false }
      const sx = siteOf(s);
      A.innerHTML = `<a class="as-bk" href="#">← All stories</a><div class="as-ak">${master ? `<b style="color:${sx.c1}">${esc(sx.name)}</b> · ` : ''}${esc(s.cat)} · ${fd(s.date)}</div><h1>${esc(s.title)}</h1>${s.dek ? `<p class="as-dk">${esc(s.dek)}</p>` : ''}${s.img ? `<img class="as-im" src="${esc(url(s.img))}" alt="">` : ''}${(s.body && s.body.length ? s.body : [s.dek]).map(p => `<p>${p}</p>`).join('')}
      <p class="as-from">From <a href="${url(sx.home)}" style="color:${sx.c1}">${esc(sx.name)}</a></p><h2 class="as-m">More stories</h2><div class="as-more">${mine.filter(x => x !== s && x.site === s.site).slice(0, 3).map(x => card(x, false)).join('')}</div>`;
      A.hidden = false; L.hidden = true; PAGE.el.querySelector('.as-tools').hidden = true; scrollTo(0, 0); document.title = s.title + ' | ' + sx.name; return true;
    }
    function route() { const h = decodeURIComponent(location.hash.slice(1)); if (!h || !art(h)) { list(); document.title = 'All stories | ' + (master ? 'Albanardia' : si.name) } }
    PAGE.el.querySelector('.as-q').addEventListener('input', e => { st.q = e.target.value; list() });
    const g = PAGE.el.querySelector('.as-g'); if (g) g.addEventListener('change', e => { st.grp = e.target.value; list() });
    PAGE.el.querySelectorAll('.as-chips button').forEach(b => b.addEventListener('click', () => { st.cat = b.dataset.c; PAGE.el.querySelectorAll('.as-chips button').forEach(x => x.classList.toggle('on', x === b)); list() }));
    addEventListener('hashchange', route); route();
  }
  /* ---------- embeds ---------- */
  document.querySelectorAll('[data-alb-latest]').forEach(el => {
    const site = el.dataset.albLatest, n = +(el.dataset.n || 3), si = SITES[site];
    const r = ALL.filter(s => site === '*' ? true : s.site === site).slice(0, n);
    el.classList.add('as-embed');
    el.innerHTML = `<div class="as-eh"><h2>${esc(el.dataset.title || 'Latest stories')}</h2><a href="${site === '*' ? url('stories/') : url(si.stories)}">All stories →</a></div><div class="as-eg">${r.map(s => card(s, site === '*')).join('')}</div>`;
  });
})();
