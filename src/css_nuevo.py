# -*- coding: utf-8 -*-
"""Hoja de estilo de la app. Paleta neutra, hairlines, radios amplios."""

CSS = """
/* ── tokens ───────────────────────────────────────────────── */
:root{
  color-scheme:light dark;
  --bg:#FBFBFA; --surface:#FFFFFF; --surface-2:#F5F5F4; --surface-3:#EFEFEE;
  --line:#E7E7E4; --line-2:#DCDCD8;
  --ink:#0B0B0A; --ink-2:#5B5B57; --ink-3:#8E8E88; --ink-4:#B4B4AE;
  --accent:#0B0B0A; --on-accent:#FFFFFF;
  --ok:#15803D; --ok-bg:#E8F3EC; --warn:#B45309; --warn-bg:#FBF1E4; --bad:#B91C1C; --bad-bg:#FBEBEA;
  --shadow-s:0 1px 2px rgba(11,11,10,.04);
  --shadow-m:0 1px 3px rgba(11,11,10,.05),0 8px 24px -12px rgba(11,11,10,.12);
  --shadow-l:0 24px 60px -20px rgba(11,11,10,.28);
  --r-s:10px; --r-m:14px; --r-l:20px; --r-xl:26px;
  --sans:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI Variable Text","Segoe UI",
    Inter,Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono","Cascadia Mono","IBM Plex Mono",Menlo,Consolas,monospace;
  --pad:20px;
}
/* un selector con coma delante de una @media invalida toda la regla: van separados */
@media (prefers-color-scheme:dark){:root:not([data-t="light"]){
  --bg:#0A0A09; --surface:#131312; --surface-2:#1B1B19; --surface-3:#232320;
  --line:#26261F; --line-2:#33332C;
  --ink:#F7F7F5; --ink-2:#A8A8A2; --ink-3:#7C7C76; --ink-4:#5A5A55;
  --accent:#F7F7F5; --on-accent:#0A0A09;
  --ok:#4ADE80; --ok-bg:#12241A; --warn:#FBBF24; --warn-bg:#241C0E; --bad:#F87171; --bad-bg:#261413;
  --shadow-s:0 1px 2px rgba(0,0,0,.5);
  --shadow-m:0 1px 3px rgba(0,0,0,.5),0 8px 24px -12px rgba(0,0,0,.8);
  --shadow-l:0 24px 60px -20px rgba(0,0,0,.9);
}}
:root[data-t="dark"]{
  --bg:#0A0A09; --surface:#131312; --surface-2:#1B1B19; --surface-3:#232320;
  --line:#26261F; --line-2:#33332C;
  --ink:#F7F7F5; --ink-2:#A8A8A2; --ink-3:#7C7C76; --ink-4:#5A5A55;
  --accent:#F7F7F5; --on-accent:#0A0A09;
  --ok:#4ADE80; --ok-bg:#12241A; --warn:#FBBF24; --warn-bg:#241C0E; --bad:#F87171; --bad-bg:#261413;
  --shadow-s:0 1px 2px rgba(0,0,0,.5);
  --shadow-m:0 1px 3px rgba(0,0,0,.5),0 8px 24px -12px rgba(0,0,0,.8);
  --shadow-l:0 24px 60px -20px rgba(0,0,0,.9);
}

*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
body{
  background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-size:16px;line-height:1.5;letter-spacing:-.011em;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
  padding-bottom:calc(78px + env(safe-area-inset-bottom));
  overflow-x:hidden;font-variant-numeric:tabular-nums;
}
::selection{background:var(--ink);color:var(--bg)}
.wrap{max-width:760px;margin:0 auto;padding:0 var(--pad)}

/* ── cabecera ─────────────────────────────────────────────── */
.top{
  position:sticky;top:0;z-index:40;margin:0 calc(var(--pad) * -1);
  padding:calc(env(safe-area-inset-top) + 12px) var(--pad) 12px;
  display:flex;justify-content:space-between;align-items:center;gap:12px;
  background:color-mix(in srgb,var(--bg) 82%,transparent);
  backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid transparent;transition:border-color .2s;
}
.top.stuck{border-bottom-color:var(--line)}
.pill{
  display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:500;
  letter-spacing:0;color:var(--ink-2);background:var(--surface-2);
  border:1px solid var(--line);border-radius:999px;padding:6px 12px;white-space:nowrap;
}
.pill.solid{background:var(--accent);border-color:var(--accent);color:var(--on-accent);font-weight:600}
.pill.ghost{background:transparent}
h1{
  font-size:clamp(28px,7.5vw,38px);line-height:1.08;letter-spacing:-.035em;
  font-weight:640;margin:18px 0 6px;color:var(--ink);text-wrap:balance;
}
h1 .g{color:var(--ink-3);font-weight:400}
.sub{color:var(--ink-2);font-size:15px;margin:0 0 16px;line-height:1.45;text-wrap:pretty}
.tags{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:20px}
.tag{
  font-size:12.5px;font-weight:500;color:var(--ink-2);background:var(--surface-2);
  border:1px solid var(--line);border-radius:999px;padding:5px 11px;letter-spacing:0;
}
.tag.on{background:var(--accent);border-color:var(--accent);color:var(--on-accent);font-weight:600}

/* ── superficies ──────────────────────────────────────────── */
.card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-l);
  padding:18px;margin-bottom:14px;box-shadow:var(--shadow-s);
}
.ch{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.cn{
  font-family:var(--mono);font-size:11px;font-weight:500;color:var(--ink-3);
  background:var(--surface-2);border:1px solid var(--line);border-radius:7px;
  padding:3px 7px;letter-spacing:.02em;
}
.ct{font-size:17px;font-weight:600;letter-spacing:-.02em;color:var(--ink);margin:0;flex:1;line-height:1.2}
.cm{font-size:12.5px;color:var(--ink-3);white-space:nowrap;font-weight:450}
.rule{
  background:var(--surface-2);border:1px solid var(--line);border-radius:var(--r-m);
  padding:14px 16px;margin-bottom:16px;font-size:15px;line-height:1.45;color:var(--ink-2);
  text-wrap:pretty;
}
.note{
  background:var(--surface-2);border-radius:var(--r-m);padding:12px 14px;
  font-size:13.5px;line-height:1.45;margin:12px 0;color:var(--ink-2);
  border-left:2px solid var(--line-2);
}
.note strong{color:var(--ink);font-weight:600}
.note.warn{background:var(--bad-bg);border-left-color:var(--bad);color:var(--ink-2)}
.note.warn strong{color:var(--bad)}

/* ── progreso ─────────────────────────────────────────────── */
.prog{margin:0 0 20px}
.prog .pt{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:9px}
.prog .pn{font-size:26px;font-weight:640;letter-spacing:-.03em;color:var(--ink)}
.prog .pl{font-size:13px;color:var(--ink-3);font-weight:450}
.pbar{height:5px;border-radius:999px;background:var(--surface-3);overflow:hidden}
.pbar i{display:block;height:100%;background:var(--ink);border-radius:999px;
  transition:width .45s cubic-bezier(.4,0,.2,1)}
.pbar.full i{background:var(--ok)}

/* ── filas ────────────────────────────────────────────────── */
.ex{
  display:grid;grid-template-columns:auto 1fr auto;gap:13px;align-items:center;
  padding:11px 0;border-bottom:1px solid var(--line);
}
.ex:last-child{border-bottom:none;padding-bottom:0}
.ex:first-of-type{padding-top:0}
.ex img{width:54px;height:42px;object-fit:cover;border-radius:var(--r-s);
  border:1px solid var(--line);display:block}
.ex .ph{width:54px;height:42px;border-radius:var(--r-s);background:var(--surface-2);
  border:1px solid var(--line)}
.exn{font-size:15px;font-weight:500;color:var(--ink);line-height:1.3;letter-spacing:-.01em}
.exv{font-family:var(--mono);font-size:12px;color:var(--ink-3);margin-top:3px;letter-spacing:-.02em}
.exk{font-size:10.5px;font-weight:600;color:var(--ink);margin-top:4px;letter-spacing:.06em;
  text-transform:uppercase}
.chk{
  width:28px;height:28px;border-radius:999px;border:1.5px solid var(--line-2);
  background:transparent;color:transparent;font-size:13px;cursor:pointer;flex:0 0 auto;
  display:flex;align-items:center;justify-content:center;transition:all .18s;padding:0;
}
.chk:active{transform:scale(.9)}
.chk.on{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}

/* ── listas ───────────────────────────────────────────────── */
ul.bul{list-style:none;margin:0;padding:0}
ul.bul li{position:relative;padding:7px 0 7px 18px;font-size:14.5px;line-height:1.45;
  color:var(--ink-2)}
ul.bul li::before{content:"";position:absolute;left:2px;top:15px;width:5px;height:5px;
  background:var(--ink-4);border-radius:50%}
ul.bul li strong{color:var(--ink);font-weight:600}
ol.steps{list-style:none;counter-reset:s;margin:0;padding:0}
ol.steps li{counter-increment:s;position:relative;padding:10px 0 10px 34px;font-size:14.5px;
  line-height:1.45;color:var(--ink-2);border-bottom:1px solid var(--line)}
ol.steps li:last-child{border-bottom:none;padding-bottom:0}
ol.steps li::before{
  content:counter(s);position:absolute;left:0;top:10px;width:23px;height:23px;border-radius:999px;
  background:var(--surface-2);border:1px solid var(--line);color:var(--ink-2);
  font-family:var(--mono);font-size:11px;display:flex;align-items:center;justify-content:center;
}
ol.steps li strong{color:var(--ink);font-weight:600}
.lab{font-size:12px;font-weight:600;color:var(--ink-3);margin:18px 0 9px;letter-spacing:.01em}

/* ── escala de dolor ──────────────────────────────────────── */
.scale{display:grid;grid-template-columns:repeat(11,1fr);gap:5px}
.sc{
  min-width:0;padding:0;aspect-ratio:1;border-radius:999px;border:1px solid var(--line);
  background:var(--surface-2);color:var(--ink-2);font-family:var(--sans);
  font-size:14px;font-weight:500;display:flex;align-items:center;justify-content:center;
  cursor:pointer;transition:all .16s;
}
.sc:active{transform:scale(.88)}
.sc.on{transform:scale(1.06);font-weight:600;box-shadow:var(--shadow-m)}
.sc.g.on{background:var(--ok);border-color:var(--ok);color:#fff}
.sc.a.on{background:var(--warn);border-color:var(--warn);color:#fff}
.sc.r.on{background:var(--bad);border-color:var(--bad);color:#fff}

/* ── campos ───────────────────────────────────────────────── */
input[type=text],textarea,select{
  width:100%;background:var(--surface-2);color:var(--ink);border:1px solid var(--line);
  border-radius:var(--r-m);padding:12px 14px;font-family:var(--sans);font-size:15.5px;
  transition:border-color .16s,box-shadow .16s;
}
input[type=text]:focus,textarea:focus{outline:none;border-color:var(--ink-4);
  box-shadow:0 0 0 3px color-mix(in srgb,var(--ink) 8%,transparent)}
input::placeholder,textarea::placeholder{color:var(--ink-4)}
textarea{min-height:80px;resize:vertical;line-height:1.5}
.kg{display:flex;align-items:center;gap:9px;margin-top:8px;flex-wrap:wrap}
.kg input{width:74px;padding:7px 9px;font-size:13.5px;border-radius:var(--r-s);
  font-family:var(--mono);text-align:center}
.kg span{font-size:12px;color:var(--ink-3)}
.kg b{color:var(--ink);font-family:var(--mono);font-weight:500}

/* ── botones ──────────────────────────────────────────────── */
.btn{
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  background:var(--accent);color:var(--on-accent);border:1px solid var(--accent);
  border-radius:999px;padding:12px 20px;font-weight:550;font-size:14.5px;
  cursor:pointer;font-family:var(--sans);letter-spacing:-.01em;transition:all .16s;
}
.btn:active{transform:scale(.97)}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line-2)}
.btn.wide{width:100%;margin-top:10px}
.row{display:flex;gap:9px;flex-wrap:wrap}

/* ── navegación inferior ──────────────────────────────────── */
.nav{
  position:fixed;bottom:0;left:0;right:0;z-index:50;display:flex;
  background:color-mix(in srgb,var(--bg) 76%,transparent);
  backdrop-filter:saturate(180%) blur(24px);-webkit-backdrop-filter:saturate(180%) blur(24px);
  border-top:1px solid var(--line);padding-bottom:env(safe-area-inset-bottom);
}
.nav button{
  flex:1;background:none;border:none;color:var(--ink-4);padding:9px 4px 10px;
  font-size:10.5px;font-weight:500;cursor:pointer;font-family:var(--sans);
  display:flex;flex-direction:column;align-items:center;gap:4px;transition:color .16s;
  letter-spacing:.01em;
}
.nav button svg{width:22px;height:22px;stroke-width:1.6}
.nav button.on{color:var(--ink)}
.nav button:active{transform:scale(.94)}

/* ── navegación de día ────────────────────────────────────── */
.daynav{display:flex;align-items:center;gap:10px;margin:16px 0 4px}
.daynav button{
  width:38px;height:38px;border-radius:999px;border:1px solid var(--line);
  background:var(--surface);color:var(--ink-2);cursor:pointer;flex:0 0 auto;
  display:flex;align-items:center;justify-content:center;transition:all .16s;
}
.daynav button:active{transform:scale(.9)}
.daynav button svg{width:17px;height:17px;stroke-width:1.8}
.daynav .d{flex:1;text-align:center;font-size:13.5px;color:var(--ink-2);font-weight:500}
.daynav .d b{color:var(--ink);font-weight:600}

/* ── semáforo ─────────────────────────────────────────────── */
.sem{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.semc{border:1px solid var(--line);border-radius:var(--r-m);padding:13px 12px;
  background:var(--surface-2);text-align:center}
.semn{font-size:22px;font-weight:640;letter-spacing:-.03em;line-height:1}
.semt{font-size:11px;font-weight:600;margin-top:5px}
.g .semn,.g .semt{color:var(--ok)} .a .semn,.a .semt{color:var(--warn)}
.r .semn,.r .semt{color:var(--bad)}
.semd{font-size:12px;color:var(--ink-3);margin-top:5px;line-height:1.35}

/* ── semana ───────────────────────────────────────────────── */
.week{display:grid;gap:8px}
.wd{
  display:grid;grid-template-columns:58px 1fr auto;gap:12px;align-items:center;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-m);
  padding:13px 15px;cursor:pointer;transition:all .16s;box-shadow:var(--shadow-s);
}
.wd:active{transform:scale(.99)}
.wd.on{border-color:var(--ink);box-shadow:var(--shadow-m)}
.wd .dd{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);letter-spacing:-.02em}
.wd .tt{font-size:14.5px;color:var(--ink);line-height:1.25;font-weight:500;letter-spacing:-.01em}
.dot{width:9px;height:9px;border-radius:50%;background:var(--surface-3);
  border:1px solid var(--line-2)}
.dot.g{background:var(--ok);border-color:var(--ok)}
.dot.a{background:var(--warn);border-color:var(--warn)}
.dot.r{background:var(--bad);border-color:var(--bad)}

/* ── fichas del manual ────────────────────────────────────── */
.ficha{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-l);
  overflow:hidden;margin-bottom:14px;box-shadow:var(--shadow-s);
}
.ficha img{width:100%;display:block;aspect-ratio:4/3;object-fit:cover}
.ficha .fb{padding:18px}
.ficha h3{font-size:17px;font-weight:600;letter-spacing:-.02em;color:var(--ink);margin:0 0 12px}

/* ── datos ────────────────────────────────────────────────── */
.bar{display:flex;align-items:flex-end;gap:2px;height:96px;margin:14px 0}
.bar div{flex:1;background:var(--surface-3);border-radius:2px;min-height:2px;
  transition:height .3s}
.mono{font-family:var(--mono);font-size:12.5px;color:var(--ink-2);letter-spacing:-.02em}
.streak{display:flex;gap:12px;align-items:center;font-size:14px;color:var(--ink-2)}
.streak b{font-size:34px;font-weight:640;letter-spacing:-.04em;color:var(--ink);line-height:1}
.wk{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;margin-top:10px}
.wk div{height:34px;border-radius:var(--r-s);background:var(--surface-2);
  border:1px solid var(--line);display:flex;align-items:center;justify-content:center;
  font-size:11.5px;color:var(--ink-4);font-weight:500}
.wk div.ok{background:var(--ok-bg);border-color:transparent;color:var(--ok)}
.wk div.mid{background:var(--warn-bg);border-color:transparent;color:var(--warn)}
.wk div.no{background:var(--bad-bg);border-color:transparent;color:var(--bad)}

/* ── cronómetro ───────────────────────────────────────────── */
.tm{
  position:fixed;inset:0;background:color-mix(in srgb,var(--bg) 94%,transparent);
  backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px);
  z-index:99;display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:28px;text-align:center;
}
.ring{
  width:min(64vw,240px);aspect-ratio:1;border-radius:50%;border:1px solid var(--line-2);
  display:flex;align-items:center;justify-content:center;margin-bottom:26px;
  background:var(--surface);box-shadow:var(--shadow-l);
}
.ring.run{border-color:var(--ink);border-width:2px}
.ring.rest{border-style:dashed}
.tm .n{font-size:clamp(56px,17vw,80px);font-weight:600;letter-spacing:-.05em;color:var(--ink);
  line-height:1;font-variant-numeric:tabular-nums}
.tm .n.rest{color:var(--ink-3)}
.tm .s{font-size:13px;font-weight:600;color:var(--ink-2);margin-bottom:20px;letter-spacing:-.01em}
.tm .q{font-size:14.5px;color:var(--ink-2);margin:0 0 26px;max-width:330px;line-height:1.5;
  text-wrap:pretty}
.tm .row{justify-content:center}

/* ── tablet y escritorio ──────────────────────────────────── */
@media (min-width:700px){
  :root{--pad:32px}
  body{font-size:16.5px}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
  .cols > .card{margin-bottom:0}
  .fichas-g{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  .fichas-g .ficha{margin-bottom:0}
  .nav{max-width:760px;left:50%;transform:translateX(-50%);border-radius:var(--r-xl) var(--r-xl) 0 0;
    border:1px solid var(--line);border-bottom:none}
}
@media (min-width:1040px){
  .wrap{max-width:960px}
  .nav{max-width:520px;bottom:22px;border-radius:999px;border:1px solid var(--line);
    box-shadow:var(--shadow-m)}
  .nav button{padding:11px 4px}
  body{padding-bottom:120px}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""
