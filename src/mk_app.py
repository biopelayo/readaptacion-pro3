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

from css_nuevo import CSS  # noqa: E402

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#FBFBFA" media="(prefers-color-scheme:light)">
<meta name="theme-color" content="#0A0A09" media="(prefers-color-scheme:dark)">
<meta name="color-scheme" content="light dark">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
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
  <button data-v="hoy" class="on"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Hoy</button>
  <button data-v="semana"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4.5" width="18" height="16" rx="3"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/></svg>Semana</button>
  <button data-v="manual"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H19v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H19v3H6.5A2.5 2.5 0 0 1 4 20.5z"/></svg>Manual</button>
  <button data-v="datos"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V9M10 19V5M16 19v-6M22 19H2"/></svg>Datos</button>
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

/* ── tema ─────────────────────────────────────────────────── */
function aplicaTema() {
  const m = S.cfg.tema || "auto";
  const r = document.documentElement;
  if (m === "auto") r.removeAttribute("data-t"); else r.setAttribute("data-t", m);
}

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

  h += '<div class="top"><span class="pill">' + i.b.id + ' · ' + esc(i.b.nombre) +
       '</span><span class="pill solid">Día ' + i.n + ' de ' + i.b.dias + '</span></div>';

  h += '<div class="daynav">' +
       '<button data-nav="-1" aria-label="Día anterior"><svg viewBox="0 0 24 24" fill="none" ' +
       'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg></button>' +
       '<div class="d">' + (FECHA === HOY0 ? '<b>Hoy</b> · ' : '') + esc(largo(FECHA)) + '</div>' +
       '<button data-nav="1" aria-label="Día siguiente"><svg viewBox="0 0 24 24" fill="none" ' +
       'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg></button></div>';

  h += '<h1>' + esc(s.base.titulo) + '</h1>';
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
       '<p style="margin:0 0 8px;font-size:13.5px;color:var(--ink-3)">Antes de levantarte de la cama. ' +
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
         '<h2 class="ct" style="color:var(--bad)">Fuera del plan en ' + i.b.id + '</h2></div>' +
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
      h += '<p style="font-size:13.5px;color:var(--ink-3);margin:0 0 8px">Test de la semana. ' +
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
       '<h2 class="ct" style="color:var(--bad)">Parar y consultar</h2></div>' +
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
          esc(i0.b.nombre) + '</span><span class="pill solid">Semana</span></div>';
  h += '<h1>La <span class="g">semana</span></h1><p class="sub">' + esc(i0.b.lema) + '</p>';
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
       '<p style="font-size:13.5px;color:var(--ink-3);margin:0 0 8px">Los criterios que abren el bloque ' +
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
  let h = '<div class="top"><span class="pill">Manual de ejercicios</span>' +
          '<span class="pill solid">' + Object.keys(D.ej).length + ' fichas</span></div>';
  h += '<h1>Cómo se hace <span class="g">cada cosa</span></h1>';
  h += '<input type="text" id="q" placeholder="Buscar ejercicio" value="' + esc(FILTRO) + '">';
  h += '<div style="height:14px"></div><div class="fichas-g">';
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
         '<div class="lab" style="color:var(--bad)">Error frecuente</div>' +
         '<p style="margin:0;font-size:13.5px">' + esc(e.error) + '</p>' +
         (e.aviso ? '<div class="note warn">' + esc(e.aviso) + '</div>' : '') +
         '</div></div>';
  });
  return h + '</div>';
}

/* ── vista DATOS ──────────────────────────────────────────── */
function vistaDatos() {
  const fechas = Object.keys(S.reg).sort();
  const con = fechas.filter(f => S.reg[f].manana !== undefined && S.reg[f].manana !== null);
  let h = '<div class="top"><span class="pill">Historial</span><span class="pill solid">' +
          con.length + ' días</span></div><h1>Tus <span class="g">datos</span></h1>';

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
    const col = v === undefined || v === null ? "var(--line)" :
                (v <= 1 ? "var(--ok)" : (v <= 3 ? "var(--warn)" : "var(--bad)"));
    return '<div style="height:' + alt + 'px;background:' + col + '"></div>';
  }).join("") + '</div>';
  const vals = ult.map(f => (S.reg[f] || {}).manana).filter(v => v !== undefined && v !== null);
  const med = vals.length ? (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(1) : "sin datos";
  h += '<div class="note">Media de los días registrados: <span class="mono">' + med +
       '</span> · registrados <span class="mono">' + vals.length + ' de 30</span></div></div>';

  const tm = S.cfg.tema || "auto";
  h += '<div class="card"><div class="ch"><span class="cn">◐</span>' +
       '<h2 class="ct">Apariencia</h2></div>' +
       '<div class="row">' +
       [["auto", "Automático"], ["light", "Claro"], ["dark", "Oscuro"]].map(o =>
         '<button class="btn ' + (tm === o[0] ? '' : 'ghost') + '" data-tema="' + o[0] + '">' +
         o[1] + '</button>').join("") + '</div>' +
       '<div class="note">En automático sigue al sistema: claro de día y oscuro de noche.</div></div>';

  h += '<div class="card"><div class="ch"><span class="cn">↓</span>' +
       '<h2 class="ct">Exportar</h2></div>' +
       '<p style="font-size:13.5px;color:var(--ink-3);margin:0 0 10px">El CSV sale con el formato de ' +
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
  if (t.dataset.tema) { S.cfg.tema = t.dataset.tema; save(); aplicaTema(); return render(); }
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

aplicaTema();
addEventListener("scroll", () => {
  const el = document.querySelector(".top");
  if (el) el.classList.toggle("stuck", scrollY > 6);
}, {passive: true});

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
