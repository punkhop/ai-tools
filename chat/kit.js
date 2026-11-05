/* Chat kit v2 (ai-tools v1.0.0) — glanceable blocks for T3 Code chat pages.
   Served as https://cdn.jsdelivr.net/gh/punkhop/ai-tools@v1.0.0/chat/kit.js. A page is that one
   script tag plus <k-*> tags written as plain lines.
   Colors come from T3's theme variables (shadcn names). Shelf + short forms: ./README.md */
(() => {
const ME = document.currentScript && document.currentScript.src;
const BASE = ME && ME.startsWith('http') ? ME.replace(/\/[^/]*$/, '') : 'https://cdn.jsdelivr.net/gh/punkhop/ai-tools@v1.0.0/chat';
const CSS = `
:root{color-scheme:dark light}
body{margin:0;padding:2px 0 8px;background:transparent;color:var(--foreground);font:15px/1.5 var(--font-sans,-apple-system,system-ui,sans-serif)}
k-page,k-reply{display:grid;gap:18px;grid-template-columns:minmax(0,1fr)}
k-reply{gap:16px;max-width:720px}
k-page{max-width:720px}
k-reply>p,k-opt>p{margin:0;font-size:15px}
k-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,var(--min,300px)),1fr))}
.k-card{background:var(--card);border:1px solid var(--border);border-radius:12px}
.k-mut{color:var(--muted-foreground)}
.k-ok,.k-passed{--c:var(--success)}.k-needs,.k-do{--c:var(--warning)}.k-work{--c:var(--info)}.k-wait{--c:var(--muted-foreground)}.k-bad{--c:var(--destructive)}
.k-g{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;flex:none;font-size:12px;font-weight:800;color:var(--c);background:color-mix(in srgb,var(--c) 16%,transparent)}
.k-lbl{font-size:15px;font-weight:600;color:var(--foreground);margin:2px 0 8px}
/* mission */
.k-mission h2{margin:0;font-size:20px;line-height:1.25;font-weight:650;letter-spacing:-.01em}
.k-mission p{margin:4px 0 0;font-size:14.5px;color:var(--muted-foreground);max-width:62ch}
/* head: one line = the reply's title; several lines = a grouped list */
.k-title h2{margin:0;font-size:24px;line-height:1.3;font-weight:650;letter-spacing:-.01em}
.k-title p{margin:2px 0 0;font-size:14px;color:var(--muted-foreground)}
.k-group{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.k-item{display:flex;gap:12px;align-items:flex-start;padding:10px 14px;text-decoration:none;color:var(--foreground)}
.k-item+.k-item{border-top:1px solid var(--border)}
.k-item .k-g{width:20px;height:20px;font-size:11px;margin-top:1px}
.k-item b{display:block;font-weight:550;font-size:14.5px}
.k-item small{display:block;font-size:13px;color:var(--muted-foreground)}
a.k-item:hover b{color:var(--accent)}
.k-n{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;flex:none;margin-top:1px;font-style:normal;font-size:11.5px;font-weight:700;color:var(--muted-foreground);border:1px solid var(--border)}
.k-item small i{font-style:normal;font-weight:600;color:var(--foreground)}
/* link rows (k-links only): a colored icon tile for the kind, title in the link color, an open arrow */
.k-lk{align-items:center;padding:11px 14px}
.k-lk svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
.k-lk .k-ic{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;flex:none;color:var(--kc);background:color-mix(in srgb,var(--kc) 16%,transparent)}
.k-lk>span:not(.k-ic){flex:1;min-width:0}
.k-lk b{color:var(--accent);font-weight:600;overflow-wrap:anywhere}
.k-lk .k-g{margin-top:0}
.k-lk .k-go{color:var(--muted-foreground);transition:color .15s}
a.k-lk:hover{background:color-mix(in srgb,var(--foreground) 4%,transparent)}a.k-lk:hover .k-go{color:var(--foreground)}
.k-kpage{--kc:color-mix(in srgb,#3b82f6 78%,var(--foreground))}.k-kgallery{--kc:color-mix(in srgb,#ec4899 78%,var(--foreground))}
.k-kthread{--kc:color-mix(in srgb,#8b5cf6 78%,var(--foreground))}.k-kpr{--kc:color-mix(in srgb,#f97316 78%,var(--foreground))}
.k-ktask{--kc:color-mix(in srgb,#f59e0b 78%,var(--foreground))}.k-knote{--kc:color-mix(in srgb,#22c55e 78%,var(--foreground))}
.k-kvideo{--kc:color-mix(in srgb,#ef4444 78%,var(--foreground))}.k-klink{--kc:var(--accent)}
.k-group.k-you{border-color:color-mix(in srgb,var(--warning) 55%,var(--border))}
.k-you .k-item+.k-item{border-top-color:color-mix(in srgb,var(--warning) 22%,var(--border))}
.k-you .k-n{color:#000;background:var(--warning);border-color:var(--warning)}
k-head{display:block}
.k-row{display:flex;align-items:center;gap:10px;padding:9px 14px;border:1px solid var(--border);background:var(--card);border-radius:999px;font-size:14.5px;font-weight:550}
.k-row span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.k-row small{margin-left:auto;flex:none;font-weight:400;font-size:12.5px;color:var(--muted-foreground)}
.k-list{display:grid;gap:6px}.k-list .k-row{border-radius:10px}
/* status bar: green only when it is safe to close; everything else is gray with a colored mark */
.k-status{display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:12px;font-weight:600;font-size:15px;
  background:color-mix(in srgb,var(--muted) 55%,transparent);border:1px solid var(--border);border-left:3px solid var(--c)}
.k-status.k-ok,.k-status.k-passed{background:color-mix(in srgb,var(--c) 10%,transparent);border-color:color-mix(in srgb,var(--c) 35%,transparent)}
.k-status .k-g{width:28px;height:28px;font-size:15px}
.k-status a{color:inherit;text-decoration:underline;text-underline-offset:3px}
.k-status p{margin:0;font-weight:400;font-size:13.5px;color:var(--muted-foreground)}
.k-status.k-work .k-g{animation:k-spin 2.4s linear infinite}
@keyframes k-spin{to{transform:rotate(360deg)}}
/* stages: how far the whole project has come, one line */
.k-stg{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:0}
.k-st{position:relative;padding:0 8px 0 0}
.k-st:before{content:"";position:absolute;left:12px;right:0;top:9px;height:2px;background:var(--border)}
.k-st:last-child:before{display:none}
.k-st.k-ok:before{background:var(--success)}
.k-st i{position:relative;display:grid;place-items:center;width:20px;height:20px;border-radius:50%;font-style:normal;font-size:11px;font-weight:800;
  background:var(--card);border:2px solid var(--border);color:var(--muted-foreground);margin-bottom:6px}
.k-st.k-ok i{background:var(--success);border-color:var(--success);color:#000}
.k-st.k-work i,.k-st.k-wait i{border-color:var(--c);color:var(--c)}
.k-st b{display:block;font-size:13.5px;font-weight:600}
.k-st small{display:block;font-size:12.5px;color:var(--muted-foreground);line-height:1.35}
@media (max-width:520px){.k-stg{grid-template-columns:1fr;gap:10px}.k-st{display:grid;grid-template-columns:28px 1fr}.k-st i{grid-row:span 2}.k-st:before{display:none}}
/* decide: each row a task you can open for its context; the arrow goes to its board page */
.k-dq{display:flex;gap:12px;align-items:flex-start;padding:10px 14px;cursor:pointer;border-left:3px solid transparent}
.k-dq+.k-dq,.k-pane+.k-dq{border-top:1px solid color-mix(in srgb,var(--warning) 22%,var(--border))}
.k-dq>span{flex:1;min-width:0}
.k-dq b{font-weight:550;font-size:14.5px}
.k-dq small{display:block;font-size:13px;color:var(--muted-foreground)}.k-dq small i{font-style:normal;font-weight:600;color:var(--foreground)}
.k-dq:hover{background:color-mix(in srgb,var(--warning) 5%,transparent)}
.k-dq.on{background:color-mix(in srgb,var(--warning) 10%,transparent);border-left-color:var(--warning)}
.k-pane{display:grid;border-top:1px solid color-mix(in srgb,var(--warning) 22%,var(--border));background:color-mix(in srgb,var(--background) 40%,var(--card))}
.k-dd{grid-area:1/1;visibility:hidden;padding:14px 16px 16px;font-size:14px;display:grid;gap:10px;align-content:start}
.k-dd.on{visibility:visible}
.k-dd p{margin:0}
.k-jump{display:inline-grid;place-items:center;width:20px;height:20px;margin-left:6px;vertical-align:1px;border-radius:6px;border:1px solid var(--border);
  font-size:11px;color:var(--muted-foreground);text-decoration:none}
.k-jump:hover{color:var(--accent);border-color:var(--accent)}
/* trail */
.k-trail{display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:13px}
.k-trail b{font-weight:500;padding:4px 10px;border:1px solid var(--border);background:var(--card);border-radius:7px}
.k-trail b.k-end{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 14%,transparent)}
.k-trail i{font-style:normal;color:var(--muted-foreground)}
.k-trail .k-ok,.k-trail .k-bad{color:var(--c);font-weight:800;margin-right:4px}
/* words diff — one column */
.k-w{display:grid;grid-template-columns:130px 1fr;gap:12px;padding:10px 14px;font-size:14px}
.k-w+.k-w{border-top:1px solid var(--border)}
.k-w em{font-style:normal;font-size:13px;color:var(--muted-foreground)}
.k-w s{color:color-mix(in srgb,var(--destructive) 80%,var(--foreground))}
.k-w ins{text-decoration:none;font-weight:600;color:var(--success)}
@media (max-width:520px){.k-w{grid-template-columns:1fr;gap:2px}}
/* images: click opens full screen; arrows flip through every image on the page */
.k-img{position:relative;overflow:hidden;border-radius:12px;border:1px solid var(--border);background:var(--card);cursor:zoom-in}
.k-img img{display:block;width:100%;height:auto}
k-shot .k-img{width:fit-content;max-width:100%}
k-shot .k-img img{width:auto;max-width:100%;max-height:var(--h,440px)}
.k-draw{padding:14px;height:100%;box-sizing:border-box}
k-pair k-grid>div{display:flex;flex-direction:column}
k-pair k-grid>div>:first-child{flex:1 0 auto}
.k-cap{display:flex;gap:8px;align-items:center;font-size:13px;padding:7px 2px 0}
.k-pin{position:absolute;transform:translate(-50%,-50%);display:grid;place-items:center;width:22px;height:22px;border-radius:50%;
  background:var(--accent);color:#fff;font-size:11.5px;font-weight:800;box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 30%,transparent);pointer-events:none}
.k-notes{display:grid;gap:4px;margin-top:8px;font-size:14px}
.k-notes div{display:flex;gap:10px;align-items:baseline}
.k-notes .k-pin{position:static;transform:none;flex:none;width:20px;height:20px;box-shadow:none}
.k-lb{position:fixed;left:0;right:0;top:var(--lb-top,0px);height:var(--lb-h,100vh);z-index:99;background:rgb(0 0 0/.94);display:none;flex-direction:column;align-items:center;justify-content:center;gap:12px;color:#eee}
.k-lb.on{display:flex}
.k-lb .k-img{border:0;background:none;cursor:zoom-out;display:inline-block}
.k-lb:fullscreen{--lb-top:0px!important;--lb-h:100vh!important}
.k-lb .k-img img{width:auto;max-width:94vw;max-height:calc(var(--lb-h,100vh) - 72px)}
.k-lb .k-pin{width:28px;height:28px;font-size:14px}
.k-lb-bar{display:flex;gap:14px;align-items:center;font-size:14px}
.k-lb-bar button{font:inherit;color:#eee;background:rgb(255 255 255/.12);border:0;border-radius:8px;padding:6px 14px;cursor:pointer}
/* buttons */
.k-btn{font:inherit;font-size:13px;padding:5px 12px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--foreground);cursor:pointer}
.k-btn:hover{background:var(--muted)}
.k-btn[aria-pressed=true]{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 16%,transparent)}
/* links */
.k-links{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}
k-links[list] .k-links{grid-template-columns:minmax(0,1fr);gap:6px}
.k-link{display:flex;align-items:center;gap:10px;padding:10px 14px;text-decoration:none;color:var(--foreground);transition:border-color .15s}
.k-link:hover{border-color:var(--accent)}
.k-link span{min-width:0;flex:1}
.k-link b{display:block;font-weight:550;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.k-link small{font-size:12px;color:var(--muted-foreground)}
.k-tag{flex:none;font-style:normal;font-size:11.5px;font-weight:650;padding:2px 9px;border-radius:999px;color:var(--c);background:color-mix(in srgb,var(--c) 15%,transparent)}
/* choose */
.k-tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
/* every option sits in the same cell, so the block is always as tall as the tallest option: switching never moves the page */
.k-body{display:grid}.k-opt{grid-area:1/1;visibility:hidden}.k-opt.on{visibility:visible}
.k-optname{font-size:12.5px;font-weight:650;margin-bottom:6px}
.k-mine{color:var(--success);font-weight:500}
/* questions */
.k-qs{display:grid;gap:8px;counter-reset:q}
.k-q{display:grid;grid-template-columns:26px 1fr;gap:4px 10px;padding:12px 14px}
.k-q:before{counter-increment:q;content:counter(q);grid-row:span 2;display:grid;place-items:center;width:24px;height:24px;border-radius:50%;
  background:color-mix(in srgb,var(--warning) 18%,transparent);color:var(--warning);font-weight:800;font-size:12.5px}
.k-q b{font-weight:600}
.k-q small{font-size:13px;color:var(--muted-foreground)}
.k-q small i{font-style:normal;color:var(--success);font-weight:600}
/* fold */
.k-fold summary{list-style:none;cursor:pointer;display:flex;gap:8px;align-items:center;padding:10px 14px;font-size:14px;font-weight:550}
.k-fold summary::-webkit-details-marker{display:none}
.k-fold summary:before{content:"›";color:var(--muted-foreground);transition:transform .15s}
.k-fold[open] summary:before{transform:rotate(90deg)}
.k-fold>div{padding:10px 14px;border-top:1px solid var(--border);font-size:14px}
/* lab: real prototype-lab parts in an isolated frame, sized to fit */
k-lab{display:block}
.k-labf{display:block;width:100%;border:0;border-radius:12px;background:transparent;color-scheme:dark}
/* device */
.k-dev{display:grid;grid-template-columns:1fr 190px;gap:14px;align-items:start}
.k-dev>div{min-width:0}
.k-frame{position:relative;overflow:hidden;border:1px solid var(--border);border-radius:10px}
.k-frame iframe{position:absolute;top:0;left:0;border:0;display:block;transform-origin:0 0}
.k-phone{border-radius:22px;padding:6px;background:var(--muted)}
.k-phone .k-frame{border-radius:16px}
@media (max-width:520px){.k-dev{grid-template-columns:1fr}.k-dev>div:last-child{width:200px;margin:auto}}
`;
const S = {ok:'✓',passed:'↪',needs:'?',do:'→',work:'◐',wait:'○',bad:'✗'};
const st = w => (w in S ? w : null);
const lines = el => el.textContent.split('\n').map(s => s.trim()).filter(Boolean);
const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const parse = l => { const [w, ...r] = l.split(' '); const s = st(w); let t = s ? r.join(' ') : l; let m = '';
  if (t.includes(' ~ ')) [t, m] = t.split(' ~ '); return {s: s || 'ok', t, m}; };
const item = ({s, t, m}, href) => `<${href ? `a href="${href}" target="_blank"` : 'div'} class="k-item${s ? ' k-' + s : ''}">${s ? `<i class="k-g">${S[s]}</i>` : ''}<span><b>${t}</b>${m ? `<small>${m}</small>` : ''}</span></${href ? 'a' : 'div'}>`;
// k-links rows: the link's kind from its href (data-kind on the <a> wins), drawn as a Lucide icon
const KIND = h => !h ? 'link' : /^t3-thread:/.test(h) ? 'thread' : /github\.com\/.+\/pull\//.test(h) ? 'pr' : /\.(mp4|mov|m4v|webm)([?#]|$)/i.test(h) ? 'video' : /gallery\.html([?#]|$)/.test(h) ? 'gallery'
  : /SESSION-NOTE\.md|\/memory\/sessions\/.*\.md([?#]|$)/.test(h) ? 'note' : /^(https?:|\/|file:)/.test(h) ? 'page' : 'link';
const ICON = {page: '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/>',
  gallery: '<path d="M18 22H4a2 2 0 0 1-2-2V6"/><path d="m22 13-1.3-1.3a2.4 2.4 0 0 0-3.4 0L11 18"/><circle cx="12" cy="8" r="2"/><rect width="16" height="16" x="6" y="2" rx="2"/>',
  thread: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
  pr: '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><path d="M6 9v12"/>',
  task: '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="m9 12 2 2 4-4"/>',
  note: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
  video: '<path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3Z"/><path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 4"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
  link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>'};
const svg = d => `<svg viewBox="0 0 24 24" aria-hidden="true">${d}</svg>`;
const linkRow = a => { const h = a.getAttribute('href'), k = ICON[a.dataset.kind] ? a.dataset.kind : KIND(h), s = st(a.dataset.s), m = a.dataset.k || '';
  return `<${h ? `a href="${h}" target="_blank"` : 'div'} class="k-item k-lk k-k${k}${s ? ' k-' + s : ''}"><span class="k-ic">${svg(ICON[k])}</span><span><b>${a.innerHTML}</b>${m ? `<small>${m}</small>` : ''}</span>`
    + `${s ? `<i class="k-g">${S[s]}</i>` : ''}${h ? svg('<path d="M7 7h10v10"/><path d="M7 17 17 7"/>').replace('<svg', '<svg class="k-go"') : ''}</${h ? 'a' : 'div'}>`; };
const row = ({s, t, m}) => `<div class="k-row k-${s}"><i class="k-g">${S[s]}</i><span>${t}</span>${m ? `<small>${m}</small>` : ''}</div>`;
const lbl = el => el.getAttribute('label') ? `<div class="k-lbl">${esc(el.getAttribute('label'))}</div>` : '';
const img = (src, pins = '', cap = '') => `<div class="k-img" data-cap="${esc(cap)}"><img src="${src}" alt="">${pins}</div>`;

// lightbox — real full screen when the frame allows it. Else it covers what the reader
// can see: the window, or, in a frame sized to the whole page, a box around the clicked image.
let lb, shots = [], at = 0;
const show = i => { at = (i + shots.length) % shots.length; const s = shots[at];
  lb.querySelector('.k-lb-stage').innerHTML = s.outerHTML;
  lb.querySelector('.k-lb-n').textContent = `${at + 1} of ${shots.length}${s.dataset.cap ? ' · ' + s.dataset.cap : ''}`; };
const place = el => { const set = (top, h) => { lb.style.setProperty('--lb-top', top + 'px'); lb.style.setProperty('--lb-h', h + 'px'); };
  if (innerHeight <= screen.availHeight) return set(0, innerHeight);
  // a frame sized to the whole page: a box around the image now, then exactly the slice on screen
  const r = el.getBoundingClientRect(), h = Math.min(innerHeight, 640);
  set(Math.max(0, Math.min(innerHeight - h, r.top + r.height / 2 - h / 2)), h);
  new IntersectionObserver(([e], o) => { o.disconnect(); const v = e.intersectionRect;
    if (v.height >= 240) set(v.top, v.height); }).observe(document.documentElement); };
const open = el => { shots = [...document.querySelectorAll('.k-img')].filter(e => !lb.contains(e));
  place(el); show(shots.indexOf(el)); lb.classList.add('on'); if (lb.requestFullscreen) lb.requestFullscreen().catch(() => {}); };
const close = () => { lb.classList.remove('on'); if (document.fullscreenElement) document.exitFullscreen(); };
const lightbox = () => { lb = document.createElement('div'); lb.className = 'k-lb';
  lb.innerHTML = `<div class="k-lb-stage"></div><div class="k-lb-bar"><button>←</button><span class="k-lb-n"></span><button>→</button><button>Close · Esc</button></div>`;
  const [a, b, c] = lb.querySelectorAll('button'); a.onclick = () => show(at - 1); b.onclick = () => show(at + 1); c.onclick = close;
  lb.querySelector('.k-lb-stage').onclick = close; document.body.appendChild(lb);
  document.addEventListener('fullscreenchange', () => { if (!document.fullscreenElement) lb.classList.remove('on'); });
  addEventListener('keydown', e => { if (!lb.classList.contains('on')) return;
    if (e.key === 'ArrowLeft') show(at - 1); if (e.key === 'ArrowRight') show(at + 1); if (e.key === 'Escape') close(); });
  // preventDefault claims the click, so T3's own image zoom stays shut
  document.addEventListener('click', e => { const k = e.target.closest('.k-img'); if (!k) return; e.preventDefault(); if (!lb.contains(k)) open(k); }); };

// a frame holding real prototype-lab parts (lab kit.css), dark, sized to its content
const labDoc = (html, w, id) => `<!doctype html><html style="color-scheme:dark"><head><meta charset="utf-8"><meta name="color-scheme" content="dark"><meta name="viewport" content="width=${w || 'device-width'}">
<link rel="stylesheet" href="${BASE}/lab/kit.css"><style>html,body{margin:0;background:transparent}.k-labroot{padding:2px 2px 22px;background:transparent}</style></head>
<body><div class="k-labroot" data-theme="dark">${html}</div><script>(()=>{const r=document.querySelector('.k-labroot'),p=()=>parent.postMessage({kLab:${id || 0},h:r.scrollHeight},'*');new ResizeObserver(p).observe(r);addEventListener('load',p);p()})()<\/script></body></html>`;
// the frame reports its own height (T3's chat frame blocks reading it from outside)
let labN = 0; const labs = {};
addEventListener('message', e => { const d = e.data; if (d && d.kLab && labs[d.kLab] && !labs[d.kLab].fixed) labs[d.kLab].style.height = d.h + 'px'; });
const labFrame = (html, h) => { const f = document.createElement('iframe'), id = ++labN; labs[id] = f; f.fixed = !!h;
  f.className = 'k-labf'; f.srcdoc = labDoc(html, 0, id); f.style.height = (h || 120) + 'px'; return f; };

const RANK = {'K-MISSION': 0, 'K-HEAD': 1, 'K-STATUS': 9}; // head first, status bar last; everything between keeps the order it was written in // everything else is Show (2)
const R = {
  // the one reply shape: Head → Show → Links → Status → Questions, whatever order they were written in
  'k-reply'(el) { const kids = [...el.children].map((c, i) => [RANK[c.tagName] ?? 2, i, c]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    kids.forEach(([, , c]) => el.appendChild(c));
    if (!el.querySelector(':scope > k-status')) { const s = st(el.getAttribute('s')) || 'ok', q = el.querySelector(':scope > k-qs'), dq = el.querySelectorAll(':scope > k-decide > k-q').length, n = dq || (q ? lines(q).length : 0);
      const txt = {ok: 'Note written · nothing left\nSafe to close this tab.', needs: n ? `Answer question${n > 1 ? `s 1–${n}` : ' 1'}` : ''}[s];
      if (txt) { const b = document.createElement('k-status'); b.setAttribute('s', s); b.textContent = txt; el.appendChild(b); } } },
  'k-mission'(el) { el.innerHTML = `<div class="k-mission"><h2>${esc(el.getAttribute('title') || '')}</h2><p>${el.innerHTML.trim()}</p></div>`; },
  'k-head'(el) { const ls = lines(el);
    if (ls.length === 1) { const {t, m} = parse(ls[0]); el.innerHTML = `<div class="k-title"><h2>${t}</h2>${m ? `<p>${m}</p>` : ''}</div>`; }
    else el.innerHTML = lbl(el) + `<div class="k-group">${ls.map(l => item(parse(l))).join('')}</div>`; },
  // the green bar is a claim, so it has to carry its proof: note="<url of the session note written this turn>" on the
  // bar or its k-reply. No note, no green — the bar says so instead.
  'k-status'(el) { let s = st(el.getAttribute('s')) || 'ok'; let [head, ...rest] = lines(el);
    if (s === 'ok') { const note = el.getAttribute('note') || el.closest('k-reply')?.getAttribute('note');
      if (!note) { s = 'bad'; head = 'Not finished · no session note linked'; rest = ['The green bar needs note="…": the link to the note /note wrote this turn.']; }
      else { const a = `<a href="${esc(note)}" target="_blank" rel="noopener">Note written</a>`; head = head.includes('Note written') ? head.replace('Note written', a) : `${a} · ${head}`; } }
    el.innerHTML = `<div class="k-status k-${s}"><i class="k-g">${S[s]}</i><div>${head}${rest.length ? `<p>${rest.join('<br>')}</p>` : ''}</div></div>`; },
  'k-trail'(el) { const steps = el.textContent.trim().split('>').map(s => s.trim());
    el.innerHTML = lbl(el) + '<div class="k-trail">' + steps.map((s, i) => { const [w, ...r] = s.split(' ');
      const g = w === 'ok' ? '<span class="k-ok">✓</span>' : w === 'bad' ? '<span class="k-bad">✗</span>' : '';
      const t = g ? r.join(' ') : s; return `<b class="${i === steps.length - 1 ? 'k-end' : ''}">${g}${t}</b>`; }).join('<i>→</i>') + '</div>'; },
  'k-words'(el) { el.innerHTML = lbl(el) + '<div class="k-card">' + lines(el).map(l => { const [where, was, now] = l.split('|').map(s => s.trim());
      return `<div class="k-w"><em>${where}</em><span>${was ? `<s>${was}</s> → ` : '<i class="k-tag k-ok">new</i> '}<ins>${now}</ins></span></div>`; }).join('') + '</div>'; },
  'k-shot'(el) { const src = el.getAttribute('src'); const ps = lines(el).map(l => { const m = l.match(/^(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\s+(.*)$/); return m && {x: m[1], y: m[2], t: m[3]}; }).filter(Boolean);
    el.innerHTML = lbl(el) + img(src, ps.map((p, i) => `<i class="k-pin" style="left:${p.x}%;top:${p.y}%">${i + 1}</i>`).join(''), el.getAttribute('label') || '')
      + (ps.length ? `<div class="k-notes">${ps.map((p, i) => `<div><i class="k-pin">${i + 1}</i>${p.t}</div>`).join('')}</div>` : ''); },
  // children: <img alt="caption">, <k-lab cap="caption">…</k-lab>, or any element with cap="caption"
  'k-pair'(el) { const kids = [...el.children]; const cap = c => c.getAttribute('alt') || c.getAttribute('cap') || ''; const labs = [];
    const cell = c => c.tagName === 'IMG' ? img(c.getAttribute('src'), '', cap(c)) : c.tagName === 'K-LAB' ? (labs.push(c), '<i data-lab></i>') : `<div class="k-card k-draw">${c.innerHTML}</div>`;
    el.innerHTML = lbl(el) + '<k-grid style="--min:240px">' + kids.map(c => `<div>${cell(c)}<div class="k-cap">${cap(c)}</div></div>`).join('') + '</k-grid>';
    el.querySelectorAll('[data-lab]').forEach((p, i) => p.replaceWith(labFrame(labs[i].innerHTML, +labs[i].getAttribute('h') || 0))); },
  // a row of thumbnails; click any → full screen, arrows flip
  'k-flip'(el) { const ims = [...el.querySelectorAll('img')];
    el.innerHTML = lbl(el) + `<div style="display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(150px,1fr))">${ims.map(i => `<div>${img(i.getAttribute('src'), '', i.alt || '')}<div class="k-cap">${i.alt || ''}</div></div>`).join('')}</div>`; },
  'k-links'(el) { el.innerHTML = lbl(el) + `<div class="k-group${el.classList.contains('k-you') ? ' k-you' : ''}">` + [...el.querySelectorAll('a')].map(linkRow).join('') + '</div>'; },
  'k-choose'(el) { const opts = [...el.querySelectorAll(':scope > k-opt')];
    const name = o => `${o.getAttribute('name')}${o.hasAttribute('mine') ? ' <span class="k-mine">· my call</span>' : ''}`;
    el.innerHTML = lbl(el) + `<div class="k-tabs">${opts.map(o => `<button class="k-btn">${o.getAttribute('name')}</button>`).join('')}</div><div class="k-body"></div>`;
    const body = el.querySelector('.k-body');
    opts.forEach(o => { const d = document.createElement('div'); d.className = 'k-opt'; d.innerHTML = `<div class="k-optname">${name(o)}</div>`;
      const lab = o.querySelector('k-lab'); if (lab) { lab.dataset.k = 1; d.appendChild(labFrame(lab.innerHTML, +lab.getAttribute('h') || 0)); } else d.append(...o.childNodes);
      body.appendChild(d); });
    const bs = [...el.querySelectorAll('.k-tabs .k-btn')], os = [...body.children];
    const pick = i => { bs.forEach((b, j) => b.setAttribute('aria-pressed', j === i)); os.forEach((o, j) => o.classList.toggle('on', j === i));
 };
    bs.forEach((b, i) => b.onclick = () => pick(i)); pick(Math.max(0, opts.findIndex(o => o.hasAttribute('mine')))); },
  'k-lab'(el) { if (el.closest('k-pair,k-choose,k-device')) return; const h = +el.getAttribute('h') || 0; const html = el.innerHTML; el.innerHTML = ''; el.appendChild(labFrame(html, h)); },
  // lines: "status Stage ~ note"; a stage with no status word is not started
  'k-stages'(el) { const ls = lines(el); el.innerHTML = lbl(el) + `<div class="k-stg" style="--n:${ls.length}">` + ls.map((l, i) => {
      const [w, ...r] = l.split(' '); const s = st(w); const [t, m] = (s ? r.join(' ') : l).split(' ~ ');
      return `<div class="k-st${s ? ' k-' + s : ''}"><i>${s === 'ok' ? '✓' : i + 1}</i><b>${t}</b>${m ? `<small>${m}</small>` : ''}</div>`; }).join('') + '</div>'; },
  // <k-q title="the task, plain words" call="my call" href="task url">context paragraph, a k-lab drawing…</k-q>
  // Mail-style: the tasks on top, one reading pane under them. The pane is as tall as the longest
  // context (all panes share one cell), so picking a task never moves the page.
  'k-decide'(el) { const qs = [...el.querySelectorAll(':scope > k-q')];
    const box = document.createElement('div'); box.className = 'k-group k-you';
    const list = document.createElement('div'); const pane = document.createElement('div'); pane.className = 'k-pane';
    qs.forEach((q, i) => { const href = q.getAttribute('href'), call = q.getAttribute('call');
      const r = document.createElement('div'); r.className = 'k-dq'; r.tabIndex = 0;
      r.innerHTML = `<i class="k-n">${i + 1}</i><span><b>${q.getAttribute('title') || ''}</b>${href ? `<a class="k-jump" href="${href}" target="_blank" title="Open on the board">↗</a>` : ''}${call ? `<small>My call: <i>${call}</i></small>` : ''}</span>`;
      const d = document.createElement('div'); d.className = 'k-dd'; d.append(...q.childNodes);
      list.appendChild(r); pane.appendChild(d); });
    const rows = [...list.children], ds = [...pane.children];
    const pick = i => { rows.forEach((r, j) => r.classList.toggle('on', j === i)); ds.forEach((d, j) => d.classList.toggle('on', j === i)); rows[i].after(pane); };
    rows.forEach((r, i) => { r.onclick = e => { if (!e.target.closest('.k-jump')) pick(i); }; r.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(i); } }; });
    box.append(list, pane); el.innerHTML = lbl(el); el.appendChild(box); pick(0); },
  'k-qs'(el) { const ls = el.innerHTML.split('\n').map(s => s.trim()).filter(Boolean);
    el.innerHTML = `<div class="k-lbl">${esc(el.getAttribute('label') || 'Questions')}</div><div class="k-group k-you">` + ls.map((l, i) => { let [q, c] = l.split('|').map(s => s.trim()), n0 = +(el.getAttribute('start') || 1), m = q.match(/^(\d+)\.\s+/), n = m ? +m[1] : i + n0; if (m) q = q.slice(m[0].length);
      return `<div class="k-item"><i class="k-n">${n}</i><span><b>${q}</b>${c ? `<small>My call: <i>${c}</i></small>` : ''}</span></div>`; }).join('') + '</div>'; },
  'k-fold'(el) { el.innerHTML = `<details class="k-card k-fold"><summary>${el.getAttribute('title') || 'More'}<span class="k-mut" style="margin-left:auto;font-weight:400;font-size:12.5px">${el.getAttribute('meta') || ''}</span></summary><div>${el.innerHTML}</div></details>`; },
  // one lab surface at desktop (1280) and phone (390) width
  'k-device'(el) { const html = (el.querySelector('template') || el).innerHTML; const h = +(el.getAttribute('h') || 800);
    el.innerHTML = lbl(el) + `<div class="k-dev"><div><div class="k-frame" data-w="1280"><iframe></iframe></div><div class="k-cap k-mut">Desktop</div></div><div><div class="k-phone"><div class="k-frame" data-w="390"><iframe></iframe></div></div><div class="k-cap k-mut">Phone</div></div></div>`;
    el.querySelectorAll('.k-frame').forEach(f => { const w = +f.dataset.w, fr = f.querySelector('iframe'); fr.srcdoc = labDoc(html, w);
      const fit = () => { const s = f.clientWidth / w; const hh = w === 390 ? Math.min(h * 1.6, 844) : h; fr.style.width = w + 'px'; fr.style.height = hh + 'px'; fr.style.transform = `scale(${s})`; f.style.height = hh * s + 'px'; };
      fit(); addEventListener('resize', fit); }); },
};
const st0 = document.createElement('style'); st0.textContent = CSS; document.head.appendChild(st0);
const run = () => { lightbox(); for (const tag in R) document.querySelectorAll(tag).forEach(el => { if (!el.dataset.k) { el.dataset.k = 1; R[tag](el); } }); };
document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', run) : run();
})();
