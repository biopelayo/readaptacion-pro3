# -*- coding: utf-8 -*-
"""Hoja de estilo de la app.

Escala tipografica segun Apple HIG: cuerpo de 17 pt y jerarquia de estilos de
texto. Todo en rem sobre --fs, de modo que el tamano del sistema y el ajuste
de la propia app escalan la interfaz entera sin romper el diseno, que es la
version web de Dynamic Type. Objetivos tactiles por encima de los 44 pt.
"""

CSS = """
/* ── tokens ───────────────────────────────────────────────── */
:root{
  color-scheme:light dark;
  --fs:17px;                      /* cuerpo HIG; Ajustes lo sube a 19 o 21 */
  --bg:#FBFBFA; --surface:#FFFFFF; --surface-2:#F5F5F4; --surface-3:#EDEDEB;
  --line:#E6E6E3; --line-2:#D6D6D1;
  --ink:#0B0B0A; --ink-2:#565652; --ink-3:#87877F; --ink-4:#ADADA6;
  --accent:#0B0B0A; --on-accent:#FFFFFF;
  --ok:#15803D; --ok-bg:#E7F3EB; --warn:#A85B08; --warn-bg:#FBF0E2;
  --bad:#B3261E; --bad-bg:#FBEAE9;
  --shadow-s:0 1px 2px rgba(11,11,10,.05);
  --shadow-m:0 2px 6px rgba(11,11,10,.06),0 12px 32px -14px rgba(11,11,10,.16);
  --shadow-l:0 32px 70px -22px rgba(11,11,10,.32);
  --r-s:12px; --r-m:18px; --r-l:26px; --r-xl:34px;
  --sans:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI Variable Text","Segoe UI",
    Inter,Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono","Cascadia Mono","IBM Plex Mono",Menlo,Consolas,monospace;
  --pad:1.25rem;
  --tap:3rem;                     /* 51 px al tamano por defecto */
}
/* un selector con coma delante de una @media invalida la regla: van separados */
@media (prefers-color-scheme:dark){:root:not([data-t="light"]){
  --bg:#0A0A09; --surface:#141412; --surface-2:#1D1D1A; --surface-3:#262622;
  --line:#2A2A24; --line-2:#3A3A33;
  --ink:#F8F8F6; --ink-2:#AFAFA8; --ink-3:#84847C; --ink-4:#61615B;
  --accent:#F8F8F6; --on-accent:#0A0A09;
  --ok:#5BD98A; --ok-bg:#12251A; --warn:#F5B54A; --warn-bg:#251C0D;
  --bad:#FF8A80; --bad-bg:#2A1513;
  --shadow-s:0 1px 2px rgba(0,0,0,.55);
  --shadow-m:0 2px 6px rgba(0,0,0,.5),0 12px 32px -14px rgba(0,0,0,.85);
  --shadow-l:0 32px 70px -22px rgba(0,0,0,.92);
}}
:root[data-t="dark"]{
  --bg:#0A0A09; --surface:#141412; --surface-2:#1D1D1A; --surface-3:#262622;
  --line:#2A2A24; --line-2:#3A3A33;
  --ink:#F8F8F6; --ink-2:#AFAFA8; --ink-3:#84847C; --ink-4:#61615B;
  --accent:#F8F8F6; --on-accent:#0A0A09;
  --ok:#5BD98A; --ok-bg:#12251A; --warn:#F5B54A; --warn-bg:#251C0D;
  --bad:#FF8A80; --bad-bg:#2A1513;
  --shadow-s:0 1px 2px rgba(0,0,0,.55);
  --shadow-m:0 2px 6px rgba(0,0,0,.5),0 12px 32px -14px rgba(0,0,0,.85);
  --shadow-l:0 32px 70px -22px rgba(0,0,0,.92);
}
:root[data-fs="g"]{--fs:19px} :root[data-fs="xg"]{--fs:21px}

*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{font-size:var(--fs)}
body{
  margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-size:1rem;line-height:1.47;letter-spacing:-.011em;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
  padding-bottom:calc(5.4rem + env(safe-area-inset-bottom));
  overflow-x:hidden;font-variant-numeric:tabular-nums;
}
::selection{background:var(--ink);color:var(--bg)}
.wrap{max-width:46rem;margin:0 auto;padding:0 var(--pad)}

/* ── cabecera ─────────────────────────────────────────────── */
.top{
  position:sticky;top:0;z-index:40;margin:0 calc(var(--pad) * -1);
  padding:calc(env(safe-area-inset-top) + .8rem) var(--pad) .8rem;
  display:flex;justify-content:space-between;align-items:center;gap:.7rem;
  background:color-mix(in srgb,var(--bg) 80%,transparent);
  backdrop-filter:saturate(180%) blur(22px);-webkit-backdrop-filter:saturate(180%) blur(22px);
  border-bottom:1px solid transparent;transition:border-color .2s;
}
.top.stuck{border-bottom-color:var(--line)}
.pill{
  display:inline-flex;align-items:center;gap:.35rem;font-size:.82rem;font-weight:500;
  color:var(--ink-2);background:var(--surface-2);border:1px solid var(--line);
  border-radius:999px;padding:.45rem .8rem;white-space:nowrap;letter-spacing:0;
}
.pill.solid{background:var(--accent);border-color:var(--accent);color:var(--on-accent);font-weight:600}
h1{  /* Large Title */
  font-size:clamp(2rem,8.5vw,2.9rem);line-height:1.06;letter-spacing:-.032em;
  font-weight:660;margin:1.1rem 0 .4rem;color:var(--ink);text-wrap:balance;
}
h1 .g{color:var(--ink-3);font-weight:400}
.sub{color:var(--ink-2);font-size:1rem;margin:0 0 1rem;line-height:1.45;text-wrap:pretty}
.tags{display:flex;flex-wrap:wrap;gap:.45rem;margin-bottom:1.2rem}
.tag{
  font-size:.85rem;font-weight:500;color:var(--ink-2);background:var(--surface-2);
  border:1px solid var(--line);border-radius:999px;padding:.4rem .75rem;
}
.tag.on{background:var(--accent);border-color:var(--accent);color:var(--on-accent);font-weight:600}

/* ── superficies ──────────────────────────────────────────── */
.card{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-l);
  padding:1.25rem;margin-bottom:.9rem;box-shadow:var(--shadow-s);
}
.ch{display:flex;align-items:center;gap:.6rem;margin-bottom:.9rem}
.cn{
  font-family:var(--mono);font-size:.72rem;font-weight:500;color:var(--ink-3);
  background:var(--surface-2);border:1px solid var(--line);border-radius:8px;
  padding:.2rem .45rem;
}
.ct{font-size:1.24rem;font-weight:640;letter-spacing:-.022em;color:var(--ink);margin:0;
  flex:1;line-height:1.18}   /* Title 3 */
.cm{font-size:.82rem;color:var(--ink-3);white-space:nowrap;font-weight:450}
.rule{
  background:var(--surface-2);border:1px solid var(--line);border-radius:var(--r-m);
  padding:1rem 1.1rem;margin-bottom:1.1rem;font-size:1.02rem;line-height:1.45;
  color:var(--ink-2);text-wrap:pretty;
}
.note{
  background:var(--surface-2);border-radius:var(--r-m);padding:.85rem 1rem;
  font-size:.9rem;line-height:1.45;margin:.9rem 0;color:var(--ink-2);
  border-left:3px solid var(--line-2);
}
.note strong{color:var(--ink);font-weight:600}
.note.warn{background:var(--bad-bg);border-left-color:var(--bad)}
.note.warn strong{color:var(--bad)}

/* ── progreso ─────────────────────────────────────────────── */
.prog{margin:0 0 1.3rem}
.prog .pt{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.6rem}
.prog .pn{font-size:2.1rem;font-weight:660;letter-spacing:-.035em;color:var(--ink)}
.prog .pl{font-size:.9rem;color:var(--ink-3);font-weight:450}
.pbar{height:.45rem;border-radius:999px;background:var(--surface-3);overflow:hidden}
.pbar i{display:block;height:100%;background:var(--ink);border-radius:999px;
  transition:width .45s cubic-bezier(.4,0,.2,1)}
.pbar.full i{background:var(--ok)}

/* ── filas ────────────────────────────────────────────────── */
.ex{
  display:grid;grid-template-columns:auto 1fr auto;gap:.85rem;align-items:center;
  padding:.8rem 0;border-bottom:1px solid var(--line);min-height:var(--tap);
}
.ex:last-child{border-bottom:none;padding-bottom:0}
.ex:first-of-type{padding-top:0}
.ex img{width:5.2rem;height:3.9rem;object-fit:cover;border-radius:var(--r-s);
  border:1px solid var(--line);display:block}
.ex .ph{width:5.2rem;height:3.9rem;border-radius:var(--r-s);background:var(--surface-2);
  border:1px solid var(--line)}
.exn{font-size:1.02rem;font-weight:530;color:var(--ink);line-height:1.28;letter-spacing:-.012em}
.exv{font-family:var(--mono);font-size:.82rem;color:var(--ink-3);margin-top:.2rem;
  letter-spacing:-.02em}
.exk{font-size:.7rem;font-weight:700;color:var(--ink);margin-top:.28rem;letter-spacing:.07em;
  text-transform:uppercase}
.chk{
  width:2.2rem;height:2.2rem;border-radius:999px;border:2px solid var(--line-2);
  background:transparent;color:transparent;font-size:.95rem;cursor:pointer;flex:0 0 auto;
  display:flex;align-items:center;justify-content:center;transition:all .18s;padding:0;
}
.chk:active{transform:scale(.88)}
.chk.on{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}

/* ── tira de fotos de una sección de texto ────────────────── */
.tira{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:.4rem;margin:0 0 .9rem}
.tira figure{margin:0;min-width:0}
.tira img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:var(--r-s);
  border:1px solid var(--line);display:block;cursor:pointer;transition:transform .16s}
.tira img:active{transform:scale(.97)}
.tira figcaption{font-size:.68rem;color:var(--ink-3);margin-top:.25rem;line-height:1.2;
  text-align:center;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;
  -webkit-box-orient:vertical}
@media (max-width:24rem){.tira{grid-auto-flow:row;grid-template-columns:1fr 1fr;
  grid-auto-columns:auto}}

/* ── listas ───────────────────────────────────────────────── */
ul.bul{list-style:none;margin:0;padding:0}
ul.bul li{position:relative;padding:.55rem 0 .55rem 1.15rem;font-size:.98rem;line-height:1.45;
  color:var(--ink-2)}
ul.bul li::before{content:"";position:absolute;left:.1rem;top:1.05rem;width:.35rem;height:.35rem;
  background:var(--ink-4);border-radius:50%}
ul.bul li strong{color:var(--ink);font-weight:600}
ol.steps{list-style:none;counter-reset:s;margin:0;padding:0}
ol.steps li{counter-increment:s;position:relative;padding:.75rem 0 .75rem 2.2rem;
  font-size:.98rem;line-height:1.45;color:var(--ink-2);border-bottom:1px solid var(--line)}
ol.steps li:last-child{border-bottom:none;padding-bottom:0}
ol.steps li::before{
  content:counter(s);position:absolute;left:0;top:.7rem;width:1.55rem;height:1.55rem;
  border-radius:999px;background:var(--surface-2);border:1px solid var(--line);
  color:var(--ink-2);font-family:var(--mono);font-size:.78rem;
  display:flex;align-items:center;justify-content:center;
}
ol.steps li strong{color:var(--ink);font-weight:600}
.lab{font-size:.85rem;font-weight:640;color:var(--ink-3);margin:1.3rem 0 .6rem}

/* ── escala de dolor ──────────────────────────────────────── */
.scale{display:grid;grid-template-columns:repeat(11,1fr);gap:.3rem}
.sc{
  min-width:0;padding:0;aspect-ratio:1;border-radius:999px;border:1px solid var(--line);
  background:var(--surface-2);color:var(--ink-2);font-family:var(--sans);
  font-size:1rem;font-weight:520;display:flex;align-items:center;justify-content:center;
  cursor:pointer;transition:all .16s;
}
.sc:active{transform:scale(.86)}
.sc.on{transform:scale(1.1);font-weight:700;box-shadow:var(--shadow-m)}
.sc.g.on{background:var(--ok);border-color:var(--ok);color:#fff}
.sc.a.on{background:var(--warn);border-color:var(--warn);color:#fff}
.sc.r.on{background:var(--bad);border-color:var(--bad);color:#fff}

/* ── campos ───────────────────────────────────────────────── */
input[type=text],textarea,select{
  width:100%;background:var(--surface-2);color:var(--ink);border:1px solid var(--line);
  border-radius:var(--r-m);padding:.85rem 1rem;font-family:var(--sans);font-size:1.02rem;
  min-height:var(--tap);transition:border-color .16s,box-shadow .16s;
}
input[type=text]:focus,textarea:focus{outline:none;border-color:var(--ink-4);
  box-shadow:0 0 0 4px color-mix(in srgb,var(--ink) 8%,transparent)}
input::placeholder,textarea::placeholder{color:var(--ink-4)}
textarea{min-height:5.5rem;resize:vertical;line-height:1.5}
.kg{display:flex;align-items:center;gap:.6rem;margin-top:.6rem;flex-wrap:wrap}
.kg input{width:5rem;padding:.5rem .6rem;font-size:.92rem;border-radius:var(--r-s);
  font-family:var(--mono);text-align:center;min-height:2.4rem}
.kg span{font-size:.82rem;color:var(--ink-3)}
.kg b{color:var(--ink);font-family:var(--mono);font-weight:500}

/* ── botones ──────────────────────────────────────────────── */
.btn{
  display:inline-flex;align-items:center;justify-content:center;gap:.5rem;
  background:var(--accent);color:var(--on-accent);border:1px solid var(--accent);
  border-radius:999px;padding:.85rem 1.4rem;font-weight:580;font-size:.98rem;
  min-height:var(--tap);cursor:pointer;font-family:var(--sans);letter-spacing:-.01em;
  transition:all .16s;
}
.btn:active{transform:scale(.97)}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line-2)}
.btn.wide{width:100%;margin-top:.7rem}
.row{display:flex;gap:.5rem;flex-wrap:wrap}

/* ── navegación inferior ──────────────────────────────────── */
.nav{
  position:fixed;bottom:0;left:0;right:0;z-index:50;display:flex;
  background:color-mix(in srgb,var(--bg) 74%,transparent);
  backdrop-filter:saturate(180%) blur(26px);-webkit-backdrop-filter:saturate(180%) blur(26px);
  border-top:1px solid var(--line);padding-bottom:env(safe-area-inset-bottom);
}
.nav button{
  flex:1;background:none;border:none;color:var(--ink-4);padding:.6rem .25rem .7rem;
  font-size:.7rem;font-weight:550;cursor:pointer;font-family:var(--sans);
  display:flex;flex-direction:column;align-items:center;gap:.25rem;transition:color .16s;
  min-height:var(--tap);
}
.nav button svg{width:1.65rem;height:1.65rem;stroke-width:1.6}
.nav button.on{color:var(--ink)}
.nav button:active{transform:scale(.94)}

/* ── navegación de día ────────────────────────────────────── */
.daynav{display:flex;align-items:center;gap:.6rem;margin:1rem 0 .3rem}
.daynav button{
  width:2.6rem;height:2.6rem;border-radius:999px;border:1px solid var(--line);
  background:var(--surface);color:var(--ink-2);cursor:pointer;flex:0 0 auto;
  display:flex;align-items:center;justify-content:center;transition:all .16s;
}
.daynav button:active{transform:scale(.9)}
.daynav button svg{width:1.15rem;height:1.15rem;stroke-width:1.9}
.daynav .d{flex:1;text-align:center;font-size:.95rem;color:var(--ink-2);font-weight:500}
.daynav .d b{color:var(--ink);font-weight:660}

/* ── semáforo ─────────────────────────────────────────────── */
.sem{display:grid;grid-template-columns:repeat(3,1fr);gap:.55rem}
.semc{border:1px solid var(--line);border-radius:var(--r-m);padding:.9rem .7rem;
  background:var(--surface-2);text-align:center}
.semn{font-size:1.7rem;font-weight:660;letter-spacing:-.03em;line-height:1}
.semt{font-size:.78rem;font-weight:700;margin-top:.35rem}
.g .semn,.g .semt{color:var(--ok)} .a .semn,.a .semt{color:var(--warn)}
.r .semn,.r .semt{color:var(--bad)}
.semd{font-size:.82rem;color:var(--ink-3);margin-top:.35rem;line-height:1.35}

/* ── semana ───────────────────────────────────────────────── */
.week{display:grid;gap:.55rem}
.wd{
  display:grid;grid-template-columns:4rem 1fr auto;gap:.8rem;align-items:center;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-m);
  padding:1rem 1.1rem;cursor:pointer;transition:all .16s;box-shadow:var(--shadow-s);
  min-height:var(--tap);
}
.wd:active{transform:scale(.99)}
.wd.on{border-color:var(--ink);border-width:2px;box-shadow:var(--shadow-m)}
.wd .dd{font-family:var(--mono);font-size:.8rem;color:var(--ink-3);letter-spacing:-.02em}
.wd .tt{font-size:1.02rem;color:var(--ink);line-height:1.25;font-weight:530;
  letter-spacing:-.012em}
.dot{width:.7rem;height:.7rem;border-radius:50%;background:var(--surface-3);
  border:1px solid var(--line-2)}
.dot.g{background:var(--ok);border-color:var(--ok)}
.dot.a{background:var(--warn);border-color:var(--warn)}
.dot.r{background:var(--bad);border-color:var(--bad)}

/* ── fichas del manual ────────────────────────────────────── */
.ficha{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-l);
  overflow:hidden;margin-bottom:.9rem;box-shadow:var(--shadow-s);
}
.ficha img{width:100%;display:block;aspect-ratio:4/3;object-fit:cover}
.ficha .fb{padding:1.3rem}
.ficha h3{font-size:1.3rem;font-weight:640;letter-spacing:-.022em;color:var(--ink);
  margin:0 0 .8rem;line-height:1.15}

/* ── datos ────────────────────────────────────────────────── */
.bar{display:flex;align-items:flex-end;gap:2px;height:7rem;margin:1rem 0}
.bar div{flex:1;background:var(--surface-3);border-radius:2px;min-height:2px;transition:height .3s}
.mono{font-family:var(--mono);font-size:.85rem;color:var(--ink-2);letter-spacing:-.02em}
.streak{display:flex;gap:.85rem;align-items:center;font-size:.98rem;color:var(--ink-2)}
.streak b{font-size:3rem;font-weight:660;letter-spacing:-.045em;color:var(--ink);line-height:1}
.wk{display:grid;grid-template-columns:repeat(7,1fr);gap:.3rem;margin-top:.7rem}
.wk div{height:2.6rem;border-radius:var(--r-s);background:var(--surface-2);
  border:1px solid var(--line);display:flex;align-items:center;justify-content:center;
  font-size:.82rem;color:var(--ink-4);font-weight:550}
.wk div.ok{background:var(--ok-bg);border-color:transparent;color:var(--ok)}
.wk div.mid{background:var(--warn-bg);border-color:transparent;color:var(--warn)}
.wk div.no{background:var(--bad-bg);border-color:transparent;color:var(--bad)}

/* ── cronómetro ───────────────────────────────────────────── */
.tm{
  position:fixed;inset:0;background:color-mix(in srgb,var(--bg) 93%,transparent);
  backdrop-filter:blur(30px);-webkit-backdrop-filter:blur(30px);
  z-index:99;display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:1.6rem;text-align:center;
}
.ring{
  width:min(70vw,17rem);aspect-ratio:1;border-radius:50%;border:1px solid var(--line-2);
  display:flex;align-items:center;justify-content:center;margin-bottom:1.6rem;
  background:var(--surface);box-shadow:var(--shadow-l);
}
.ring.run{border-color:var(--ink);border-width:3px}
.ring.rest{border-style:dashed;border-width:2px}
.tm .n{font-size:clamp(3.4rem,19vw,5.4rem);font-weight:620;letter-spacing:-.05em;
  color:var(--ink);line-height:1;font-variant-numeric:tabular-nums}
.tm .n.rest{color:var(--ink-3)}
.tm .s{font-size:.95rem;font-weight:640;color:var(--ink-2);margin-bottom:1.2rem}
.tm .q{font-size:1rem;color:var(--ink-2);margin:0 0 1.6rem;max-width:22rem;line-height:1.5;
  text-wrap:pretty}
.tm .row{justify-content:center}

/* ── graphical abstract ───────────────────────────────────── */
.ga{position:fixed;inset:0;z-index:120;background:var(--bg);overflow-y:auto;
  animation:gaIn .5s cubic-bezier(.2,.8,.2,1)}
@keyframes gaIn{from{opacity:0}to{opacity:1}}
.ga-in{max-width:46rem;margin:0 auto;padding:calc(env(safe-area-inset-top) + 2rem) var(--pad) 3rem;
  min-height:100%;display:flex;flex-direction:column;justify-content:center}
.ga-k{font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);margin-bottom:.7rem}
.ga h2{font-size:clamp(1.9rem,7.5vw,2.7rem);line-height:1.05;letter-spacing:-.034em;
  font-weight:660;margin:0 0 .8rem;color:var(--ink);text-wrap:balance}
.ga h2 em{font-style:normal;color:var(--ink-3);font-weight:400}
.ga .lede{font-size:1.05rem;color:var(--ink-2);line-height:1.5;margin:0 0 1.6rem;
  text-wrap:pretty}
.ga svg{width:100%;height:auto;display:block;margin:.4rem 0 1.4rem}
.ga-cifras{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin-bottom:1.5rem}
.ga-c{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-m);
  padding:.85rem .6rem;text-align:center}
.ga-c b{display:block;font-size:1.45rem;font-weight:660;letter-spacing:-.03em;color:var(--ink);
  line-height:1}
.ga-c span{display:block;font-size:.7rem;color:var(--ink-3);margin-top:.3rem;line-height:1.25}
.ga-pasos{display:grid;gap:.55rem;margin-bottom:1.6rem}
.ga-p{display:grid;grid-template-columns:2rem 1fr;gap:.85rem;align-items:start;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-m);padding:.9rem 1rem}
.ga-p i{font-style:normal;width:2rem;height:2rem;border-radius:999px;background:var(--accent);
  color:var(--on-accent);font-size:.85rem;font-weight:700;display:flex;align-items:center;
  justify-content:center}
.ga-p b{display:block;font-size:1rem;font-weight:600;color:var(--ink);margin-bottom:.15rem}
.ga-p span{font-size:.9rem;color:var(--ink-2);line-height:1.4}
.ga-cierre{background:var(--surface-2);border-left:3px solid var(--ink);border-radius:0 var(--r-m) var(--r-m) 0;
  padding:1rem 1.1rem;font-size:.98rem;color:var(--ink-2);line-height:1.5;margin-bottom:1.5rem}
.ga-cierre b{color:var(--ink)}
.ga-btn{display:flex;gap:.6rem;align-items:center}
.ga-mini{font-size:.82rem;color:var(--ink-3);display:flex;align-items:center;gap:.4rem;
  cursor:pointer;padding:.5rem}

/* ── resumen del día ──────────────────────────────────────── */
.sum{background:var(--surface);border:1px solid var(--line-2);border-radius:var(--r-l);
  padding:1.1rem 1.2rem;margin-bottom:1rem;box-shadow:var(--shadow-m)}
.sum-t{display:flex;justify-content:space-between;align-items:baseline;gap:.7rem;
  margin-bottom:.8rem;flex-wrap:wrap}
.sum-t b{font-size:1.05rem;font-weight:640;letter-spacing:-.02em;color:var(--ink)}
.sum-t span{font-family:var(--mono);font-size:.8rem;color:var(--ink-3)}
.sum-g{display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;margin-bottom:.8rem}
.sum-c{background:var(--surface-2);border-radius:var(--r-s);padding:.6rem .5rem;text-align:center}
.sum-c b{display:block;font-size:1.1rem;font-weight:640;color:var(--ink);line-height:1.1}
.sum-c span{display:block;font-size:.68rem;color:var(--ink-3);margin-top:.2rem}
.sum-l{display:grid;gap:.4rem}
.sum-i{display:grid;grid-template-columns:auto 1fr;gap:.6rem;align-items:baseline;font-size:.92rem;
  color:var(--ink-2);line-height:1.4}
.sum-i em{font-style:normal;font-size:.66rem;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-4);white-space:nowrap;padding-top:.15rem}
.sum-i b{color:var(--ink);font-weight:600}
@media (max-width:24rem){.ga-cifras{grid-template-columns:repeat(2,1fr)}}

/* ── tablet y escritorio ──────────────────────────────────── */
@media (min-width:44rem){
  :root{--pad:2rem}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:.9rem;align-items:start}
  .cols > .card{margin-bottom:0}
  .fichas-g{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}
  .fichas-g .ficha{margin-bottom:0}
  .nav{max-width:46rem;left:50%;transform:translateX(-50%);
    border-radius:var(--r-xl) var(--r-xl) 0 0;border:1px solid var(--line);border-bottom:none}
}
@media (min-width:64rem){
  .wrap{max-width:58rem}
  .nav{max-width:32rem;bottom:1.4rem;border-radius:999px;border:1px solid var(--line);
    box-shadow:var(--shadow-m)}
  body{padding-bottom:8rem}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""
