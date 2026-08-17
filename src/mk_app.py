# -*- coding: utf-8 -*-
"""Ensambla la app movil en un unico index.html autocontenido."""
import base64, io, json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from plan_data import BLOQUES, MICRO, NUTRICION, MOMENTOS, ISO, EJ  # noqa: E402

IMG = os.path.join(os.path.dirname(HERE), "imagenes", "web")
DST = os.path.join(os.path.dirname(HERE), "app", "index.html")


def jpg(slug, ancho, q):
    p = os.path.join(IMG, slug + ".jpg")
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGB")
    im.thumbnail((ancho, ancho), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


# imagenes: miniatura para la lista, media para la ficha
slugs = sorted({s for s in EJ})
IMGS = {}
for s in slugs:
    med = jpg(s, 620, 74)
    if med:
        IMGS[s] = med
print("imagenes embebidas:", len(IMGS))

DATA = dict(bloques=BLOQUES, micro=MICRO, nutricion=NUTRICION,
            momentos=MOMENTOS, iso=ISO, ej=EJ, img=IMGS)

CSS = """
:root{--navy0:#060E24;--navy1:#0A1733;--card:#0E2049;--gold:#C9A227;--goldl:#E3C468;
--goldp:#F0DFA8;--white:#fff;--body:#C9D4EA;--dim:#8C9BBB;--green:#54B37A;--amber:#E8B93B;
--red:#E2685A;--hair:rgba(201,162,39,.34);--hairs:rgba(201,162,39,.16);
--disp:"Anton","Archivo Black","Oswald","Haettenschweiler","Arial Narrow",Impact,sans-serif;
--sans:"Segoe UI",system-ui,-apple-system,Roboto,"Helvetica Neue",Arial,sans-serif;
--mono:"IBM Plex Mono","Cascadia Mono",ui-monospace,Consolas,monospace}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
body{background:radial-gradient(120% 60% at 80% 0%,#17356F 0%,rgba(23,53,111,0) 55%),
linear-gradient(170deg,#0A1733,#081228 50%,#060E24);background-attachment:fixed;
color:var(--body);font-family:var(--sans);font-size:16px;line-height:1.5;min-height:100vh;
padding-bottom:84px;overflow-x:hidden}
.wrap,.card{max-width:100%}
.tags{overflow-x:auto}
.wrap{max-width:680px;margin:0 auto;padding:14px 14px 0}
.top{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px}
.pill{font-size:10px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;
border:1px solid var(--hair);border-radius:4px;padding:5px 10px;color:var(--goldp)}
.pill.solid{background:var(--gold);border-color:var(--gold);color:#0A1733;font-weight:800}
h1{font-family:var(--disp);font-weight:400;font-size:30px;line-height:1;margin:0 0 6px;
text-transform:uppercase;color:var(--white)}
h1 .g{color:var(--goldl)}
.sub{color:var(--dim);font-size:14px;margin:0 0 12px}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}
.tag{font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;
border:1px solid var(--hairs);border-radius:3px;padding:4px 8px;color:var(--dim)}
.tag.on{border-color:var(--gold);color:var(--goldl)}
.card{background:linear-gradient(160deg,rgba(19,42,92,.8),rgba(10,23,51,.9));
border:1px solid var(--hair);border-radius:12px;padding:14px;margin-bottom:12px}
.ch{display:flex;align-items:center;gap:9px;margin-bottom:10px}
.cn{font-family:var(--mono);font-size:10px;font-weight:700;color:#0A1733;background:var(--gold);
border-radius:3px;padding:3px 6px}
.ct{font-family:var(--disp);font-size:17px;text-transform:uppercase;color:var(--goldl);
margin:0;line-height:1;flex:1}
.cm{font-family:var(--mono);font-size:10px;color:var(--dim);text-transform:uppercase}
.rule{border-left:3px solid var(--gold);background:rgba(201,162,39,.09);padding:11px 14px;
border-radius:0 6px 6px 0;margin-bottom:12px;font-size:14px;color:var(--white)}
.note{border-left:3px solid var(--gold);background:rgba(201,162,39,.08);padding:9px 12px;
border-radius:0 5px 5px 0;font-size:13px;margin:10px 0}
.note.warn{border-left-color:var(--red);background:rgba(226,104,90,.1)}
.ex{display:grid;grid-template-columns:52px 1fr auto;gap:10px;align-items:center;
padding:9px 0;border-bottom:1px solid rgba(255,255,255,.06)}
.ex:last-child{border-bottom:none}
.ex img{width:52px;height:40px;object-fit:cover;border-radius:5px;border:1px solid var(--hairs)}
.ex .ph{width:52px;height:40px;border-radius:5px;border:1px dashed var(--hairs)}
.exn{font-size:14px;color:var(--white);line-height:1.25}
.exv{font-family:var(--mono);font-size:11px;color:var(--goldp);margin-top:2px}
.exk{font-size:9px;letter-spacing:.1em;color:var(--gold);font-weight:800;margin-top:2px}
.chk{width:30px;height:30px;border-radius:8px;border:1.5px solid var(--hair);background:transparent;
color:var(--gold);font-size:15px;display:flex;align-items:center;justify-content:center;cursor:pointer;flex:0 0 auto}
.chk.on{background:var(--gold);border-color:var(--gold);color:#0A1733}
ul.bul{list-style:none;margin:0;padding:0}
ul.bul li{position:relative;padding:5px 0 5px 15px;font-size:14px}
ul.bul li::before{content:"";position:absolute;left:1px;top:13px;width:4px;height:4px;
background:var(--gold);border-radius:50%}
ol.steps{list-style:none;counter-reset:s;margin:0;padding:0}
ol.steps li{counter-increment:s;position:relative;padding:7px 0 7px 30px;font-size:14px;
border-bottom:1px solid rgba(255,255,255,.05)}
ol.steps li:last-child{border-bottom:none}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:8px;width:21px;height:21px;
border-radius:50%;border:1px solid var(--gold);color:var(--gold);font-family:var(--mono);
font-size:11px;display:flex;align-items:center;justify-content:center}
.lab{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);
font-weight:800;margin:14px 0 7px}
.scale{display:grid;grid-template-columns:repeat(11,1fr);gap:4px}
.sc{min-width:0;padding:0;height:46px;border-radius:8px;border:1.5px solid var(--hairs);
background:rgba(255,255,255,.03);color:var(--body);font-family:var(--mono);font-size:14px;
display:flex;align-items:center;justify-content:center;cursor:pointer}
.sc.on{background:var(--gold);border-color:var(--gold);color:#0A1733;font-weight:700}
.sc.g.on{background:var(--green);border-color:var(--green);color:#04140a}
.sc.a.on{background:var(--amber);border-color:var(--amber);color:#1a1200}
.sc.r.on{background:var(--red);border-color:var(--red);color:#fff}
input[type=text],textarea,select{width:100%;background:rgba(255,255,255,.05);color:var(--white);
border:1px solid var(--hairs);border-radius:9px;padding:11px 12px;font-family:var(--sans);
font-size:15px}
textarea{min-height:70px;resize:vertical}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:7px;background:var(--gold);
color:#0A1733;border:none;border-radius:9px;padding:13px 16px;font-weight:800;font-size:13px;
letter-spacing:.08em;text-transform:uppercase;cursor:pointer;font-family:var(--sans)}
.btn.ghost{background:transparent;color:var(--goldl);border:1px solid var(--hair)}
.btn.wide{width:100%;margin-top:8px}
.row{display:flex;gap:8px;flex-wrap:wrap}
.nav{position:fixed;bottom:0;left:0;right:0;background:rgba(6,14,36,.97);
border-top:1px solid var(--hair);display:flex;z-index:50;
padding-bottom:env(safe-area-inset-bottom)}
.nav button{flex:1;background:none;border:none;color:var(--dim);padding:11px 4px 13px;
font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;cursor:pointer;
font-family:var(--sans)}
.nav button.on{color:var(--gold)}
.nav .ic{display:block;font-size:19px;margin-bottom:3px;line-height:1}
.daynav{display:flex;align-items:center;gap:8px;margin-bottom:12px}
.daynav button{width:44px;height:44px;border-radius:10px;border:1px solid var(--hair);
background:transparent;color:var(--goldl);font-size:19px;cursor:pointer}
.daynav .d{flex:1;text-align:center;font-family:var(--mono);font-size:13px;color:var(--goldp)}
.sem{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-bottom:12px}
.semc{border:1px solid var(--hairs);border-radius:9px;padding:10px;text-align:center}
.semc.on{border-width:2px}
.semn{font-family:var(--disp);font-size:20px;line-height:1}
.semt{font-size:9px;letter-spacing:.1em;text-transform:uppercase;font-weight:800;margin-top:3px}
.g .semn,.g .semt{color:var(--green)} .a .semn,.a .semt{color:var(--amber)}
.r .semn,.r .semt{color:var(--red)}
.week{display:grid;gap:7px}
.wd{display:grid;grid-template-columns:64px 1fr auto;gap:10px;align-items:center;
border:1px solid var(--hairs);border-radius:9px;padding:10px 12px;cursor:pointer}
.wd.on{border-color:var(--gold);background:rgba(201,162,39,.1)}
.wd .dd{font-family:var(--mono);font-size:11px;color:var(--gold);text-transform:uppercase}
.wd .tt{font-size:13.5px;color:var(--white);line-height:1.2}
.dot{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.13)}
.dot.g{background:var(--green)} .dot.a{background:var(--amber)} .dot.r{background:var(--red)}
.ficha{border:1px solid var(--hairs);border-radius:11px;overflow:hidden;margin-bottom:10px}
.ficha img{width:100%;display:block}
.ficha .fb{padding:12px}
.ficha h3{font-family:var(--disp);font-size:15px;text-transform:uppercase;color:var(--white);margin:0 0 8px}
.bar{display:flex;align-items:flex-end;gap:3px;height:110px;margin:10px 0}
.bar div{flex:1;background:var(--hairs);border-radius:3px 3px 0 0;min-height:3px}
.mono{font-family:var(--mono);font-size:11px;color:var(--goldp)}
.hide{display:none}
/* progreso del dia */
.prog{margin-bottom:12px}
.prog .pt{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}
.prog .pn{font-family:var(--disp);font-size:22px;color:var(--white)}
.prog .pl{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);font-weight:700}
.pbar{height:8px;border-radius:4px;background:rgba(255,255,255,.08);overflow:hidden}
.pbar i{display:block;height:100%;background:linear-gradient(90deg,var(--gold),var(--goldl));
border-radius:4px;transition:width .3s}
.pbar.full i{background:linear-gradient(90deg,var(--green),#8fd6a8)}
/* carga por ejercicio */
.kg{display:flex;align-items:center;gap:6px;margin-top:5px}
.kg input{width:66px;padding:5px 7px;font-size:13px;border-radius:6px;font-family:var(--mono);
text-align:center}
.kg span{font-size:10.5px;color:var(--dim)}
.kg b{color:var(--goldp);font-family:var(--mono);font-weight:400}
/* cronometro */
.tm{position:fixed;inset:0;background:rgba(4,9,26,.97);z-index:99;display:flex;
flex-direction:column;align-items:center;justify-content:center;padding:24px;text-align:center}
.tm .n{font-family:var(--disp);font-size:88px;line-height:1;color:var(--white)}
.tm .n.rest{color:var(--goldl)}
.tm .s{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);
font-weight:800;margin-bottom:10px}
.tm .q{font-size:14px;color:var(--dim);margin:14px 0 22px;max-width:300px}
.tm .row{justify-content:center}
.ring{width:210px;height:210px;border-radius:50%;border:3px solid var(--hairs);
display:flex;align-items:center;justify-content:center;margin-bottom:18px;
box-shadow:0 0 40px rgba(201,162,39,.15)}
.ring.run{border-color:var(--gold)}
.ring.rest{border-color:var(--goldl);border-style:dashed}
.streak{display:flex;gap:8px;align-items:center;font-size:13px;color:var(--dim)}
.streak b{font-family:var(--disp);font-size:26px;color:var(--goldl);line-height:1}
.wk{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-top:8px}
.wk div{height:26px;border-radius:5px;background:rgba(255,255,255,.06);display:flex;
align-items:center;justify-content:center;font-family:var(--mono);font-size:10px;color:var(--dim)}
.wk div.ok{background:rgba(84,179,122,.28);color:#bfe8cd}
.wk div.mid{background:rgba(232,185,59,.28);color:#f0dca8}
.wk div.no{background:rgba(226,104,90,.25);color:#f0c4bc}
"""

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0A1733">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Readaptación">
<link rel="manifest" href="./manifest.json">
<link rel="apple-touch-icon" href="./icon-192.png">
<link rel="icon" href="./icon-192.png">
<title>Readaptación · PRO 3.0</title>
<style>__CSS__</style>
</head>
<body>
<div class="wrap" id="app"></div>
<div id="tm"></div>
<nav class="nav">
  <button data-v="hoy" class="on"><span class="ic">☑</span>Hoy</button>
  <button data-v="semana"><span class="ic">▦</span>Semana</button>
  <button data-v="manual"><span class="ic">◈</span>Manual</button>
  <button data-v="datos"><span class="ic">▤</span>Datos</button>
</nav>
<script>
const D = __DATA__;

/* ── estado ───────────────────────────────────────────────── */
const K = "readapt_r1_v1";
let S = JSON.parse(localStorage.getItem(K) || '{"reg":{},"cfg":{"extra":{}}}');
if (!S.cfg) S.cfg = {};
if (!S.cfg.extra) S.cfg.extra = {};
if (!S.reg) S.reg = {};
const save = () => localStorage.setItem(K, JSON.stringify(S));

/* ── fechas ───────────────────────────────────────────────── */
/* ISO en hora LOCAL: toISOString() pasa a UTC y en horario de verano
   se come un dia en cada operacion, con error acumulativo */
const iso = d => d.getFullYear() + "-" +
  String(d.getMonth() + 1).padStart(2, "0") + "-" +
  String(d.getDate()).padStart(2, "0");
const parse = s => { const [a,m,d] = s.split("-").map(Number); return new Date(a, m-1, d); };
const dias = (a, b) => Math.round((parse(b) - parse(a)) / 86400000);
const suma = (s, n) => { const d = parse(s); d.setDate(d.getDate() + n); return iso(d); };
const DS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"];
const MS = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto",
            "septiembre","octubre","noviembre","diciembre"];
const wd = s => (parse(s).getDay() + 6) % 7;
/* la fecha la pone el propio telefono */
const HOY0 = iso(new Date());
const largo = s => { const d = parse(s); return DS[wd(s)] + " " + d.getDate() + " de " + MS[d.getMonth()]; };

/* Que bloque toca en una fecha.
   Cada bloque puede llevar dias extra si su puerta no se abrio: eso PROLONGA
   ese bloque y empuja a todos los siguientes, sin dejar huecos en el calendario. */
function bloqueDe(fecha) {
  const ex = S.cfg.extra || {};
  let acc = 0;
  for (let i = 0; i < D.bloques.length; i++) {
    const b = D.bloques[i];
    const extra = ex[b.id] || 0;
    const desde = suma(b.desde, acc);
    const dur = b.dias + extra;
    const hasta = suma(desde, dur - 1);
    if (dias(desde, fecha) >= 0 && dias(fecha, hasta) >= 0)
      return {b: b, n: dias(desde, fecha) + 1, desde: desde, hasta: hasta, dur: dur, extra: extra};
    acc += extra;
  }
  if (dias(fecha, D.bloques[0].desde) > 0)
    return {b: D.bloques[0], n: 0, dur: D.bloques[0].dias, antes: true};
  const u = D.bloques[D.bloques.length - 1];
  const dur = u.dias + (ex[u.id] || 0);
  return {b: u, n: dur, dur: dur, fin: true};
}
const extraDe = id => (S.cfg.extra || {})[id] || 0;
function prolonga(id, d) {
  S.cfg.extra = S.cfg.extra || {};
  S.cfg.extra[id] = Math.max(0, (S.cfg.extra[id] || 0) + d);
  save();
}

/* ── composicion del dia ──────────────────────────────────── */
function sesionDe(fecha) {
  const info = bloqueDe(fecha);
  const base = D.micro[info.b.id][wd(fecha)];
  const r = S.reg[fecha] || {};
  const dol = (r.manana === undefined || r.manana === null) ? null : r.manana;
  const iso_pct = D.iso[Math.min(Math.max(info.n - 1, 0), D.iso.length - 1)];
  let secs = JSON.parse(JSON.stringify(base.secciones));
  let recorte = null;

  if (dol !== null) {
    if (dol >= 4) {
      recorte = "rojo";
      secs = secs.filter(s => s.n === "02").map(s => {
        s.items = s.items.slice(0, 4); s.meta = "solo movilidad muy suave"; return s;
      });
    } else if (dol === 3) {
      recorte = "ambar";
      secs = secs.filter(s => s.n !== "03" && s.n !== "07");
    }
  }
  /* el isometrico lleva el porcentaje del dia, y baja si hay 3 */
  const pct = dol === 3 ? Math.max(40, iso_pct - 20) : iso_pct;
  secs.forEach(s => {
    if (s.tipo !== "tabla") return;
    s.items.forEach(it => { if (it[0] === "isometrico-aductor") it[2] = "5 × 30 s al " + pct + " %"; });
  });
  return {info: info, base: base, secs: secs, recorte: recorte, pct: pct, dol: dol};
}

/* ── utilidades de render ─────────────────────────────────── */
const esc = t => (t + "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const VISTAS = ["hoy", "semana", "manual", "datos"];
const hash = location.hash.replace("#", "").split(":");
let VISTA = VISTAS.indexOf(hash[0]) >= 0 ? hash[0] : "hoy";
let FECHA = /^\\d{4}-\\d{2}-\\d{2}$/.test(hash[1] || "") ? hash[1] : HOY0;

function setReg(f, k, v) {
  S.reg[f] = S.reg[f] || {};
  S.reg[f][k] = v;
  save();
}

/* ── tracker: progreso, racha y cargas ────────────────────── */
/* cuenta las tareas marcables del dia y cuantas llevas hechas */
function progresoDe(fecha) {
  const s = sesionDe(fecha);
  const r = S.reg[fecha] || {};
  let total = 0;
  s.secs.forEach(sec => { if (sec.tipo === "tabla") total += sec.items.length; });
  const hechas = (r.hechos || []).length;
  const comidas = (r.comidas || []).length;
  const tot = total + 6;                       /* 6 comidas del dia */
  const hec = Math.min(hechas, total) + comidas;
  return {hechas: hec, total: tot, pct: tot ? Math.round(hec * 100 / tot) : 0,
          ejer: Math.min(hechas, total), ejerTotal: total, comidas: comidas};
}

/* dias seguidos, hacia atras desde hoy, con el dolor de la mañana anotado */
function racha() {
  let n = 0;
  for (let k = 0; k < 400; k++) {
    const f = suma(HOY0, -k);
    const r = S.reg[f];
    if (r && r.manana !== undefined && r.manana !== null) n++;
    else if (k > 0) break;                     /* hoy sin anotar todavia no rompe */
  }
  return n;
}

/* ultima carga anotada para un ejercicio, buscando hacia atras */
function ultimaCarga(clave, desde) {
  for (let k = 1; k <= 60; k++) {
    const f = suma(desde, -k);
    const c = (S.reg[f] || {}).cargas;
    if (c && c[clave]) return {kg: c[clave], f: f};
  }
  return null;
}
function escala(f, campo, val, cls) {
  let h = '<div class="scale">';
  for (let i = 0; i <= 10; i++) {
    const c = i <= 1 ? "g" : (i <= 3 ? "a" : "r");
    h += '<button class="sc ' + c + (val === i ? ' on' : '') +
         '" data-f="' + f + '" data-k="' + campo + '" data-v="' + i + '">' + i + '</button>';
  }
  return h + "</div>";
}

/* ── vista HOY ────────────────────────────────────────────── */
function vistaHoy() {
  const s = sesionDe(FECHA);
  const r = S.reg[FECHA] || {};
  const i = s.info;
  let h = "";

  h += '<div class="top"><span class="pill">' + i.b.id + ' · ' + esc(i.b.nombre.toUpperCase()) +
       '</span><span class="pill solid">DÍA ' + i.n + ' DE ' + i.b.dias + '</span></div>';

  h += '<div class="daynav"><button data-nav="-1">‹</button><div class="d">' +
       esc(largo(FECHA)) + (FECHA === HOY0 ? ' · hoy' : '') +
       '</div><button data-nav="1">›</button></div>';

  h += '<h1>' + esc(s.base.titulo.toUpperCase()) + '</h1>';
  h += '<div class="tags"><span class="tag on">Isométrico ' + s.pct + ' %</span>' +
       '<span class="tag">' + esc(i.b.nombre) + '</span>' +
       '<span class="tag">Proteína 137 g</span></div>';

  h += '<div class="rule">' + esc(s.base.regla) + '</div>';

  /* tracker del dia */
  const pr = progresoDe(FECHA);
  h += '<div class="prog"><div class="pt"><div><span class="pn">' + pr.hechas + '</span>' +
       '<span class="pl"> de ' + pr.total + ' tareas</span></div>' +
       '<div class="pl">' + pr.pct + ' %</div></div>' +
       '<div class="pbar' + (pr.pct >= 100 ? ' full' : '') + '"><i style="width:' +
       pr.pct + '%"></i></div></div>';

  /* semaforo de la mañana */
  h += '<div class="card"><div class="ch"><span class="cn">01</span>' +
       '<h2 class="ct">Dolor de esta mañana</h2></div>' +
       '<p style="margin:0 0 8px;font-size:13.5px;color:var(--dim)">Antes de levantarte de la cama. ' +
       'Es lo que decide la sesión de hoy.</p>' + escala(FECHA, "manana", r.manana);
  if (s.dol !== null) {
    if (s.recorte === "rojo")
      h += '<div class="note warn"><strong>Sesión suspendida.</strong> Hoy solo movilidad muy suave. ' +
           'Llama al fisio y no cargues nada hasta su valoración.</div>';
    else if (s.recorte === "ambar")
      h += '<div class="note warn"><strong>Sesión recortada.</strong> Fuera el gimnasio y el campo. ' +
           'Quedan movilidad, isométricos al ' + s.pct + ' %, agua y aparatos.</div>';
    else
      h += '<div class="note">Sesión completa tal como está escrita. No se añade nada por ir bien.</div>';
  }
  h += '</div>';

  if (i.b.fuera && i.b.fuera.length) {
    h += '<div class="card"><div class="ch"><span class="cn">✕</span>' +
         '<h2 class="ct" style="color:var(--red)">Fuera del plan en ' + i.b.id + '</h2></div>' +
         '<div class="tags">' + i.b.fuera.map(x =>
            '<span class="tag" style="border-color:rgba(226,104,90,.45);color:#F0B6AC">' +
            esc(x) + '</span>').join("") + '</div></div>';
  }

  /* secciones de la sesion */
  s.secs.forEach(sec => {
    h += '<div class="card"><div class="ch"><span class="cn">' + sec.n + '</span>' +
         '<h2 class="ct">' + esc(sec.titulo) + '</h2>' +
         '<span class="cm">' + esc(sec.meta) + '</span></div>';
    if (sec.tipo === "tabla") {
      const esGym = sec.titulo.toLowerCase().indexOf("gimnasio") >= 0;
      sec.items.forEach((it, k) => {
        const id = sec.n + "_" + k;
        const on = (r.hechos || []).indexOf(id) >= 0;
        const im = it[0] && D.img[it[0]] ? '<img src="' + D.img[it[0]] + '" alt="">' : '<div class="ph"></div>';
        let extra = "";
        if (esGym) {                                   /* carga usada, con memoria */
          const clave = it[0] || it[1];
          const val = ((r.cargas || {})[clave]) || "";
          const ant = ultimaCarga(clave, FECHA);
          extra = '<div class="kg"><input type="text" inputmode="decimal" data-kg="' +
                  esc(clave) + '" value="' + esc(val) + '" placeholder="kg">' +
                  (ant ? '<span>última vez <b>' + esc(ant.kg) + '</b></span>'
                       : '<span>anota la carga</span>') + '</div>';
        }
        if (it[0] === "isometrico-aductor") {
          extra += '<div class="kg"><button class="btn ghost" style="padding:7px 12px;font-size:11px" ' +
                   'data-timer="' + s.pct + '">Cronómetro 5 × 30 s</button></div>';
        }
        h += '<div class="ex" data-ficha="' + (it[0] || "") + '">' + im +
             '<div><div class="exn">' + esc(it[1]) + '</div>' +
             '<div class="exv">' + esc(it[2]) + '</div>' +
             (it[3] ? '<div class="exk">' + esc(it[3]) + '</div>' : '') + extra + '</div>' +
             '<button class="chk' + (on ? ' on' : '') + '" data-hecho="' + id + '">' +
             (on ? '✓' : '') + '</button></div>';
      });
    } else if (sec.tipo === "lista") {
      h += '<ul class="bul">' + sec.items.map(x => '<li>' + esc(x) + '</li>').join("") + '</ul>';
    } else if (sec.tipo === "pasos") {
      h += '<ol class="steps">' + sec.items.map(x =>
           '<li><strong>' + esc(x[0]) + '.</strong> ' + esc(x[1]) + '</li>').join("") + '</ol>';
    } else if (sec.tipo === "test") {
      h += '<p style="font-size:13.5px;color:var(--dim);margin:0 0 8px">Test de la semana. ' +
           'Se rellena en la pestaña Datos y decide si la semana que viene sube, mantiene o baja.</p>';
      h += '<div class="lab">Squeeze máximo</div>' + escala(FECHA, "squeeze", r.squeeze);
      h += '<div class="lab">Dolor con tos</div>' + escala(FECHA, "tos", r.tos);
    }
    h += '</div>';
  });

  /* nutricion */
  const nut = D.nutricion[wd(FECHA)];
  h += '<div class="card"><div class="ch"><span class="cn">08</span>' +
       '<h2 class="ct">Comidas del día</h2><span class="cm">137 g proteína</span></div>';
  nut.forEach((c, k) => {
    h += '<div class="ex" style="grid-template-columns:1fr auto"><div>' +
         '<div class="exk">' + esc(D.momentos[k]) + '</div>' +
         '<div class="exn" style="font-size:13.5px">' + esc(c) + '</div></div>' +
         '<button class="chk' + ((r.comidas || []).indexOf(k) >= 0 ? ' on' : '') +
         '" data-comida="' + k + '">' + ((r.comidas || []).indexOf(k) >= 0 ? '✓' : '') +
         '</button></div>';
  });
  h += '<div class="note">Agua 2,5 L · creatina 3-5 g · alcohol no · sueño 8 h.</div></div>';

  /* registro */
  h += '<div class="card"><div class="ch"><span class="cn">09</span>' +
       '<h2 class="ct">Registro de la noche</h2></div>' +
       '<div class="lab">Dolor durante la sesión</div>' + escala(FECHA, "durante", r.durante) +
       '<div class="lab">Dolor al acostarte</div>' + escala(FECHA, "acostar", r.acostar) +
       '<div class="lab">Zona</div><input type="text" data-txt="zona" value="' +
       esc(r.zona || "") + '" placeholder="ingle · pubis · aductor · abdominal bajo">' +
       '<div class="lab">Notas</div><textarea data-txt="notas" placeholder="cómo fue, qué notaste">' +
       esc(r.notas || "") + '</textarea>' +
       '<div class="note">El día siguiente es el juez. Mañana comparas con estos números.</div></div>';

  /* alarma */
  h += '<div class="card"><div class="ch"><span class="cn">!</span>' +
       '<h2 class="ct" style="color:var(--red)">Parar y consultar</h2></div>' +
       '<ul class="bul"><li>Bulto en la ingle o el escroto, sobre todo al toser.</li>' +
       '<li>Dolor que crece con la tos o al hacer fuerza.</li>' +
       '<li>Dolor testicular fuerte, náuseas, fiebre.</li>' +
       '<li>Dolor nocturno que no cede.</li>' +
       '<li>Pérdida de fuerza o incapacidad de apoyar la pierna.</li></ul>' +
       '<div class="note warn">Cualquiera de estas: se para y se contacta con médico o fisioterapeuta. ' +
       'Manda el protocolo, no la app.</div></div>';
  return h;
}

/* ── vista SEMANA ─────────────────────────────────────────── */
function vistaSemana() {
  const lunes = suma(FECHA, -wd(FECHA));
  const i0 = bloqueDe(FECHA);
  let h = '<div class="top"><span class="pill">' + i0.b.id + ' · ' +
          esc(i0.b.nombre.toUpperCase()) + '</span><span class="pill solid">SEMANA</span></div>';
  h += '<h1>LA <span class="g">SEMANA</span></h1><p class="sub">' + esc(i0.b.lema) + '</p>';
  h += '<div class="week">';
  for (let k = 0; k < 7; k++) {
    const f = suma(lunes, k);
    const inf = bloqueDe(f);
    const ses = D.micro[inf.b.id] ? D.micro[inf.b.id][wd(f)] : null;
    const r = S.reg[f] || {};
    const d = r.manana;
    const cls = d === undefined || d === null ? "" : (d <= 1 ? "g" : (d <= 3 ? "a" : "r"));
    h += '<div class="wd' + (f === FECHA ? ' on' : '') + '" data-ir="' + f + '">' +
         '<div class="dd">' + DS[k].slice(0,3) + ' ' + parse(f).getDate() + '</div>' +
         '<div class="tt">' + esc(ses ? ses.titulo : "fuera de plan") + '</div>' +
         '<div class="dot ' + cls + '"></div></div>';
  }
  h += '</div>';

  h += '<div class="card" style="margin-top:14px"><div class="ch"><span class="cn">◆</span>' +
       '<h2 class="ct">Puerta de ' + i0.b.id + '</h2></div>' +
       '<p style="font-size:13.5px;color:var(--dim);margin:0 0 8px">Los criterios que abren el bloque ' +
       'siguiente. Si falta uno, el bloque dura una semana más.</p><ul class="bul">' +
       i0.b.puerta.map(x => '<li>' + esc(x) + '</li>').join("") + '</ul>' +
       '<button class="btn ghost wide" data-puerta="' + i0.b.id +
       '">' + i0.b.id + ' necesita una semana más</button>' +
       '<div class="note">' + i0.b.id + ' dura ahora <span class="mono">' + i0.dur +
       ' días</span>' + (i0.extra ? ' (' + i0.extra + ' añadidos)' : '') +
       ' y termina el <span class="mono">' + i0.hasta + '</span>. ' +
       'Los bloques siguientes se recolocan solos.</div></div>';
  return h;
}

/* ── vista MANUAL ─────────────────────────────────────────── */
let FILTRO = "";
function vistaManual() {
  let h = '<div class="top"><span class="pill">MANUAL DE EJERCICIOS</span>' +
          '<span class="pill solid">' + Object.keys(D.ej).length + ' FICHAS</span></div>';
  h += '<h1>CÓMO SE HACE <span class="g">CADA COSA</span></h1>';
  h += '<input type="text" id="q" placeholder="Buscar ejercicio" value="' + esc(FILTRO) + '">';
  h += '<div style="height:12px"></div>';
  Object.keys(D.ej).forEach(slug => {
    const e = D.ej[slug];
    if (FILTRO && e.nombre.toLowerCase().indexOf(FILTRO.toLowerCase()) < 0) return;
    h += '<div class="ficha" id="f_' + slug + '">' +
         (D.img[slug] ? '<img src="' + D.img[slug] + '" alt="">' : '') +
         '<div class="fb"><h3>' + esc(e.nombre) + '</h3>' +
         '<div class="lab">Para qué sirve</div><p style="margin:0 0 6px;font-size:13.5px">' +
         esc(e.para_que) + '</p>' +
         '<div class="lab">Cómo se hace</div><ol class="steps">' +
         e.pasos.map(p => '<li>' + esc(p) + '</li>').join("") + '</ol>' +
         '<div class="lab" style="color:var(--red)">Error frecuente</div>' +
         '<p style="margin:0;font-size:13.5px">' + esc(e.error) + '</p>' +
         (e.aviso ? '<div class="note warn">' + esc(e.aviso) + '</div>' : '') +
         '</div></div>';
  });
  return h;
}

/* ── vista DATOS ──────────────────────────────────────────── */
function vistaDatos() {
  const fechas = Object.keys(S.reg).sort();
  const con = fechas.filter(f => S.reg[f].manana !== undefined && S.reg[f].manana !== null);
  let h = '<div class="top"><span class="pill">HISTORIAL</span><span class="pill solid">' +
          con.length + ' DÍAS</span></div><h1>TUS <span class="g">DATOS</span></h1>';

  /* racha y cumplimiento de la semana */
  const rc = racha();
  const lunes = suma(HOY0, -wd(HOY0));
  let hechasSem = 0, totalSem = 0;
  let wkh = '<div class="wk">';
  for (let k = 0; k < 7; k++) {
    const f = suma(lunes, k);
    const p = progresoDe(f);
    const pasado = dias(f, HOY0) >= 0;
    let cls = "";
    if (pasado) cls = p.pct >= 80 ? "ok" : (p.pct >= 40 ? "mid" : "no");
    if (pasado) { hechasSem += p.hechas; totalSem += p.total; }
    wkh += '<div class="' + cls + '">' + DS[k].slice(0, 1) + '</div>';
  }
  wkh += '</div>';
  const adh = totalSem ? Math.round(hechasSem * 100 / totalSem) : 0;
  h += '<div class="card"><div class="ch"><span class="cn">▲</span>' +
       '<h2 class="ct">Constancia</h2></div>' +
       '<div class="streak"><b>' + rc + '</b><span>días seguidos anotando el dolor de la mañana</span></div>' +
       '<div class="lab">Esta semana</div>' + wkh +
       '<div class="note">Cumplimiento de las tareas de la semana hasta hoy: <span class="mono">' +
       adh + ' %</span> (' + hechasSem + ' de ' + totalSem + ').</div></div>';

  h += '<div class="card"><div class="ch"><span class="cn">◷</span>' +
       '<h2 class="ct">Dolor de la mañana</h2><span class="cm">últimos 30 días</span></div>';
  const ult = [];
  for (let k = 29; k >= 0; k--) ult.push(suma(HOY0, -k));
  h += '<div class="bar">' + ult.map(f => {
    const v = (S.reg[f] || {}).manana;
    const alt = v === undefined || v === null ? 3 : Math.max(4, v * 11);
    const col = v === undefined || v === null ? "var(--hairs)" :
                (v <= 1 ? "var(--green)" : (v <= 3 ? "var(--amber)" : "var(--red)"));
    return '<div style="height:' + alt + 'px;background:' + col + '"></div>';
  }).join("") + '</div>';
  const vals = ult.map(f => (S.reg[f] || {}).manana).filter(v => v !== undefined && v !== null);
  const med = vals.length ? (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(1) : "sin datos";
  h += '<div class="note">Media de los días registrados: <span class="mono">' + med +
       '</span> · registrados <span class="mono">' + vals.length + ' de 30</span></div></div>';

  h += '<div class="card"><div class="ch"><span class="cn">↓</span>' +
       '<h2 class="ct">Exportar</h2></div>' +
       '<p style="font-size:13.5px;color:var(--dim);margin:0 0 10px">El CSV sale con el formato de ' +
       '<span class="mono">seguimiento/dolor_24h.csv</span> del proyecto.</p>' +
       '<div class="row"><button class="btn" data-exp="csv">Descargar CSV</button>' +
       '<button class="btn ghost" data-exp="json">Copia de seguridad</button></div></div>';

  h += '<div class="card"><div class="ch"><span class="cn">⚙</span>' +
       '<h2 class="ct">Ajustes</h2></div>' +
       '<div class="lab">Duración de los bloques</div>' +
       '<p style="font-size:13.5px;margin:0 0 8px">Días añadidos porque una puerta no se abrió a tiempo:</p>' +
       D.bloques.map(b => '<div class="ex" style="grid-template-columns:1fr auto auto;gap:8px">' +
         '<div class="exn">' + b.id + ' · ' + esc(b.nombre) + '<div class="exv">' +
         (b.dias + extraDe(b.id)) + ' días' + (extraDe(b.id) ? ' (+' + extraDe(b.id) + ')' : '') +
         '</div></div>' +
         '<button class="chk" data-prol="' + b.id + ':-7">−</button>' +
         '<button class="chk" data-prol="' + b.id + ':7">+</button></div>').join("") +
       '<div class="note warn">Borrar los datos no se puede deshacer. ' +
       'Exporta antes.<br><button class="btn ghost wide" data-borrar="1">Borrar todo el historial</button></div></div>';
  return h;
}

/* ── render y eventos ─────────────────────────────────────── */
function render() {
  const app = document.getElementById("app");
  app.innerHTML = VISTA === "hoy" ? vistaHoy() :
                  VISTA === "semana" ? vistaSemana() :
                  VISTA === "manual" ? vistaManual() : vistaDatos();
  document.querySelectorAll(".nav button").forEach(b =>
    b.classList.toggle("on", b.dataset.v === VISTA));
  history.replaceState(null, "", "#" + VISTA + ":" + FECHA);
  window.scrollTo(0, 0);
  const q = document.getElementById("q");
  if (q) q.oninput = e => { FILTRO = e.target.value; render(); q.focus(); };
}

document.addEventListener("click", e => {
  const t = e.target.closest("button, .ex, .wd");
  if (!t) return;
  if (t.dataset.v) { VISTA = t.dataset.v; return render(); }
  if (t.dataset.nav) { FECHA = suma(FECHA, +t.dataset.nav); return render(); }
  if (t.dataset.ir) { FECHA = t.dataset.ir; VISTA = "hoy"; return render(); }
  if (t.dataset.k) { setReg(t.dataset.f, t.dataset.k, +t.dataset.v); return render(); }
  if (t.dataset.hecho) {
    const r = S.reg[FECHA] = S.reg[FECHA] || {};
    r.hechos = r.hechos || [];
    const i = r.hechos.indexOf(t.dataset.hecho);
    if (i >= 0) r.hechos.splice(i, 1); else r.hechos.push(t.dataset.hecho);
    save(); return render();
  }
  if (t.dataset.comida) {
    const r = S.reg[FECHA] = S.reg[FECHA] || {};
    r.comidas = r.comidas || [];
    const k = +t.dataset.comida, i = r.comidas.indexOf(k);
    if (i >= 0) r.comidas.splice(i, 1); else r.comidas.push(k);
    save(); return render();
  }
  if (t.dataset.ficha) {
    VISTA = "manual"; FILTRO = D.ej[t.dataset.ficha] ? D.ej[t.dataset.ficha].nombre : "";
    return render();
  }
  if (t.dataset.puerta) { prolonga(t.dataset.puerta, 7); return render(); }
  if (t.dataset.prol) {
    const [id, d] = t.dataset.prol.split(":");
    prolonga(id, +d); return render();
  }
  if (t.dataset.timer) { abreTimer(+t.dataset.timer); return; }
  if (t.dataset.tm) {
    if (t.dataset.tm === "pausa") { T.corriendo = !T.corriendo; return pintaTimer(); }
    if (t.dataset.tm === "salta") { T.seg = 1; return tick(); }
    return cierraTimer(false);
  }
  if (t.dataset.exp) { exporta(t.dataset.exp); return; }
  if (t.dataset.borrar) {
    if (confirm("Se borra todo el historial. ¿Seguro?")) { S = {reg:{}, cfg:{extra:{}}}; save(); render(); }
  }
});

document.addEventListener("input", e => {
  const d = e.target.dataset;
  if (!d) return;
  if (d.txt) setReg(FECHA, d.txt, e.target.value);
  if (d.kg) {                                   /* carga usada, sin repintar */
    const r = S.reg[FECHA] = S.reg[FECHA] || {};
    r.cargas = r.cargas || {};
    r.cargas[d.kg] = e.target.value;
    save();
  }
});

/* ── cronometro de isometricos ────────────────────────────── */
let T = null;
function abreTimer(pct) {
  T = {serie: 1, series: 5, fase: "trabajo", seg: 30, corriendo: true, pct: pct};
  pintaTimer();
  T.int = setInterval(tick, 1000);
}
function tick() {
  if (!T || !T.corriendo) return;
  T.seg--;
  if (T.seg <= 0) {
    if (T.fase === "trabajo") {
      if (T.serie >= T.series) return cierraTimer(true);
      T.fase = "descanso"; T.seg = 30;
    } else {
      T.fase = "trabajo"; T.seg = 30; T.serie++;
    }
    if (navigator.vibrate) navigator.vibrate(220);
  }
  pintaTimer();
}
function pintaTimer() {
  if (!T) return;
  const tr = T.fase === "trabajo";
  document.getElementById("tm").innerHTML =
    '<div class="tm"><div class="s">Serie ' + T.serie + ' de ' + T.series +
    ' · isométrico al ' + T.pct + ' %</div>' +
    '<div class="ring ' + (tr ? "run" : "rest") + '"><div class="n' + (tr ? "" : " rest") + '">' +
    T.seg + '</div></div>' +
    '<div class="q">' + (tr
      ? "Aprieta al " + T.pct + " % y mantén. Respira: no aguantes el aire. Si el dolor sube dentro de la serie, para."
      : "Descanso. Suelta del todo la cara interna del muslo.") + '</div>' +
    '<div class="row"><button class="btn" data-tm="pausa">' +
    (T.corriendo ? "Pausar" : "Seguir") + '</button>' +
    '<button class="btn ghost" data-tm="salta">Saltar</button>' +
    '<button class="btn ghost" data-tm="cierra">Cerrar</button></div></div>';
}
function cierraTimer(completo) {
  if (T && T.int) clearInterval(T.int);
  T = null;
  document.getElementById("tm").innerHTML = "";
  if (completo) {
    const r = S.reg[FECHA] = S.reg[FECHA] || {};
    r.hechos = r.hechos || [];
    /* marca el isometrico de la seccion 02 */
    const s = sesionDe(FECHA);
    s.secs.forEach(sec => {
      if (sec.tipo !== "tabla") return;
      sec.items.forEach((it, k) => {
        if (it[0] === "isometrico-aductor") {
          const id = sec.n + "_" + k;
          if (r.hechos.indexOf(id) < 0) r.hechos.push(id);
        }
      });
    });
    save();
  }
  render();
}

function exporta(tipo) {
  let txt, nom;
  if (tipo === "json") {
    txt = JSON.stringify(S, null, 1); nom = "readaptacion_copia.json";
  } else {
    const cab = "fecha,bloque,dia_bloque,sesion,dolor_reposo_0_10,dolor_durante_0_10," +
      "dolor_post_entreno_0_10,dolor_dia_siguiente_0_10,tos_estornudo_0_10,squeeze_max_0_10," +
      "isometrico_pct,zona_dolor,tareas_hechas,tareas_totales,cumplimiento_pct,cargas,notas";
    const fs = Object.keys(S.reg).sort();
    const filas = fs.map(f => {
      const r = S.reg[f], s = sesionDe(f), p = progresoDe(f);
      const sig = S.reg[suma(f, 1)] ? S.reg[suma(f, 1)].manana : "";
      const v = x => (x === undefined || x === null) ? "" : x;
      const cg = Object.keys(r.cargas || {}).map(k => k + ":" + r.cargas[k]).join(" | ");
      return [f, s.info.b.id, s.info.n, '"' + s.base.titulo + '"',
              v(r.manana), v(r.durante), v(r.acostar), v(sig), v(r.tos), v(r.squeeze),
              s.pct, '"' + (r.zona || "") + '"',
              p.hechas, p.total, p.pct, '"' + cg + '"',
              '"' + (r.notas || "").replace(/"/g, "'") + '"'].join(",");
    });
    txt = cab + "\\n" + filas.join("\\n"); nom = "dolor_24h.csv";
  }
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([txt], {type: "text/plain;charset=utf-8"}));
  a.download = nom; a.click();
}

/* superficie de pruebas: la usa test/test.html */
window.__t = {iso, parse, suma, dias, wd, bloqueDe, sesionDe, progresoDe, racha,
              ultimaCarga, exporta, D, get S(){ return S; }, set S(x){ S = x; },
              setVista: v => { VISTA = v; render(); },
              setFecha: f => { FECHA = f; render(); },
              render: render};

/* app instalable: solo cuando se sirve por http(s); con file:// se ignora */
if ("serviceWorker" in navigator && location.protocol.indexOf("http") === 0) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

render();
</script>
</body>
</html>
"""

out = (HTML.replace("__CSS__", CSS)
           .replace("__DATA__", json.dumps(DATA, ensure_ascii=False)))

os.makedirs(os.path.dirname(DST), exist_ok=True)
io.open(DST, "w", encoding="utf-8", newline="\n").write(out)
print("escrito:", DST, os.path.getsize(DST) // 1024, "KB")
