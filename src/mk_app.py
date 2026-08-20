# -*- coding: utf-8 -*-
"""Ensambla la app movil en un unico index.html autocontenido."""
import base64, io, json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from plan_data import BLOQUES, MICRO, NUTRICION, MOMENTOS, ISO, EJ, APERTURA
import glob as _glob
EXTRA_FRAMES = [os.path.basename(f)[:-4] for f in
                _glob.glob(os.path.join(os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))), 'imagenes', 'web', '*--b.jpg'))]  # noqa: E402

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
slugs = sorted({s for s in EJ}) + sorted(EXTRA_FRAMES)
IMGS = {}
for s in slugs:
    med = jpg(s, 520, 70)
    if med:
        IMGS[s] = med
print("imagenes embebidas:", len(IMGS))

DATA = dict(bloques=BLOQUES, micro=MICRO, apertura=APERTURA, nutricion=NUTRICION,
            momentos=MOMENTOS, iso=ISO, ej=EJ, img=IMGS)

from css_nuevo import CSS  # noqa: E402
import subprocess
try:
    _sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                   cwd=os.path.dirname(HERE)).decode().strip()
except Exception:
    _sha = "local"
VERSION = __import__("datetime").datetime.now().strftime("%d/%m %H:%M") + " · " + _sha

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
<div id="ent"></div>
<div id="tm"></div>
<div id="ga-slot"></div>
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
  const r = document.documentElement;
  const m = S.cfg.tema || "auto";
  if (m === "auto") r.removeAttribute("data-t"); else r.setAttribute("data-t", m);
  /* tamano de texto: la version web de Dynamic Type. Escala la interfaz entera
     porque todo el diseno esta en rem sobre el tamano raiz. */
  const f = S.cfg.fs || "n";
  if (f === "n") r.removeAttribute("data-fs"); else r.setAttribute("data-fs", f);
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
  /* el dia 1 del proceso es la linea base, caiga en el dia que caiga */
  const base = (info.b.id === D.bloques[0].id && info.n === 1 && D.apertura)
    ? D.apertura : D.micro[info.b.id][wd(fecha)];
  const r = S.reg[fecha] || {};
  const dol = (r.manana === undefined || r.manana === null) ? null : r.manana;
  /* cada bloque lleva su progresion: R1 sube de 50 a 80, el resto mantiene 80 */
  const tabla = info.b.iso || D.iso;
  const iso_pct = tabla[Math.min(Math.max(info.n - 1, 0), tabla.length - 1)];
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
/* El hash conserva la vista al recargar, pero al ABRIR la app en frio se
   empieza siempre en el dia de hoy. Sin esto, un acceso directo guardado
   con una fecha vieja dejaba la app anclada a ese dia para siempre. */
const MISMA_SESION = (() => {
  try {
    const v = sessionStorage.getItem("readapt_viva");
    sessionStorage.setItem("readapt_viva", HOY0);
    return v === HOY0;      /* misma sesion Y mismo dia: una pestana abierta
                               desde hace una semana tambien vuelve a hoy */
  } catch (e) { return false; }
})();
let VISTA = VISTAS.indexOf(hash[0]) >= 0 ? hash[0] : "hoy";
let FECHA = (MISMA_SESION && /^\\d{4}-\\d{2}-\\d{2}$/.test(hash[1] || "")) ? hash[1] : HOY0;

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

/* tira de gestos en movimiento: usa el segundo fotograma cuando existe */
function movimiento(secs) {
  const vistos = [], clave = [];
  (secs || []).forEach(s => {
    if (s.tipo !== "tabla") return;
    s.items.forEach(it => {
      if (!it[0] || vistos.indexOf(it[0]) >= 0) return;
      if (!D.img[it[0] + "--b"]) return;          /* solo los que tienen 2 fotogramas */
      vistos.push(it[0]);
      clave.push([it[0], it[3] ? 0 : 1]);          /* los marcados, primero */
    });
  });
  if (!clave.length) return "";
  clave.sort((a, b) => a[1] - b[1]);
  const tres = clave.slice(0, 3);
  return '<div class="mov">' + tres.map(c => {
    const s = c[0];
    return '<figure data-ficha="' + s + '"><div class="fr">' +
      '<img class="a" src="' + D.img[s] + '" alt="' + esc(D.ej[s].nombre) + '">' +
      '<img class="b" src="' + D.img[s + "--b"] + '" alt="">' +
      '</div><figcaption>' + esc(D.ej[s].nombre) + '</figcaption></figure>';
  }).join("") + '</div>';
}

/* minutos del dia: se leen de los meta de cada seccion ("20 min", "45 min") */
function minutosDe(secs) {
  let m = 0;
  (secs || []).forEach(s => {
    const x = (s.meta || "").match(/(\d+)\s*(?:a|-|\u2013)?\s*(\d+)?\s*min/);
    if (x) m += x[2] ? Math.round((+x[1] + +x[2]) / 2) : +x[1];
  });
  return m;
}

/* anillo pequeno de cabecera: el mismo dibujo del arranque, a 40 px */
function anilloMini(fecha) {
  const i = bloqueDe(fecha);
  const B = D.bloques;
  const idx = Math.max(0, B.findIndex(b => b.id === i.b.id));
  const R = 15, C = 2 * Math.PI * R, hueco = 2.6;
  const paso = C / B.length, largo = paso - hueco;
  let a = "";
  B.forEach((b, k) => {
    const off = -k * paso;
    a += '<circle class="b" cx="18" cy="18" r="' + R + '" stroke-width="3" ' +
      'stroke-dasharray="' + largo + ' ' + (C - largo) + '" stroke-dashoffset="' + off + '"/>';
    if (k < idx) a += '<circle class="y" cx="18" cy="18" r="' + R + '" stroke-width="3" ' +
      'stroke-dasharray="' + largo + ' ' + (C - largo) + '" stroke-dashoffset="' + off + '"/>';
  });
  const frac = Math.max(0.05, Math.min(1, i.n / i.dur));
  const vivo = largo * frac;
  a += '<circle class="v" cx="18" cy="18" r="' + R + '" stroke-width="3" ' +
    'stroke-dasharray="' + vivo + ' ' + (C - vivo) + '" stroke-dashoffset="' + (-idx * paso) + '"/>';
  return '<div class="mini-anillo" data-abstract="1" title="' + esc(i.b.nombre) + '">' +
    '<svg viewBox="0 0 36 36">' + a + '</svg><span>' + i.n + '</span></div>';
}

/* -- cronometro de posta ------------------------------------
   Lee la dosis escrita en el plan y decide como contar:
   "5 x 30 s" -> series de tiempo | "10 min" -> cuenta atras sola
   "3 x 12"   -> series por repeticiones, el crono cuenta el descanso */
function leeDosis(txt) {
  const s = (txt || "").replace(/\u00d7/g, "x").toLowerCase();
  let m = s.match(/(\d+)\s*x\s*(\d+)\s*(s|seg)(?![a-z])/);
  if (m) return {modo: "tiempo", series: +m[1], trabajo: +m[2], descanso: 20};
  m = s.match(/(\d+)\s*x\s*(\d+)\s*min/);
  if (m) return {modo: "tiempo", series: +m[1], trabajo: +m[2] * 60, descanso: 60};
  m = s.match(/^(\d+)\s*min/);
  if (m) return {modo: "duracion", series: 1, trabajo: +m[1] * 60, descanso: 0};
  m = s.match(/(\d+)\s*x\s*(\d+)/);
  if (m) return {modo: "reps", series: +m[1], reps: +m[2], trabajo: 0, descanso: 75};
  m = s.match(/^(\d+)\s*s(?![a-z])/);
  if (m) return {modo: "duracion", series: 1, trabajo: +m[1], descanso: 0};
  return null;
}

let T = null;
function abreCrono(cfg) {
  const d = leeDosis(cfg.dosis);
  if (!d) return;
  T = Object.assign({}, d, {
    nombre: cfg.nombre || "", dosis: cfg.dosis || "", pct: cfg.pct || null,
    serie: 1, fase: d.modo === "reps" ? "libre" : "trabajo",
    seg: d.modo === "reps" ? 0 : d.trabajo, corriendo: true,
  });
  pintaTimer();
  T.int = setInterval(tick, 1000);
}
/* la llamada vieja del isometrico sigue valiendo */
function abreTimer(pct) {
  abreCrono({nombre: "Isometrico de aductor", dosis: "5 x 30 s", pct: pct});
}

function tick() {
  if (!T || !T.corriendo) return;
  if (T.fase === "libre") { T.seg++; return pintaTimer(); }
  T.seg--;
  if (T.seg <= 0) {
    if (T.fase === "trabajo") {
      if (T.serie >= T.series) return cierraTimer(true);
      T.fase = "descanso"; T.seg = T.descanso;
    } else {
      T.serie++;
      if (T.modo === "reps") { T.fase = "libre"; T.seg = 0; }
      else { T.fase = "trabajo"; T.seg = T.trabajo; }
    }
    if (navigator.vibrate) navigator.vibrate(220);
  }
  pintaTimer();
}

function mmss(n) {
  return n >= 60 ? Math.floor(n / 60) + ":" + String(n % 60).padStart(2, "0") : String(n);
}

function pintaTimer() {
  if (!T) return;
  const tr = T.fase === "trabajo", lib = T.fase === "libre";
  const cab = T.modo === "duracion"
    ? esc(T.nombre) + " \u00b7 " + esc(T.dosis)
    : "Serie " + T.serie + " de " + T.series + " \u00b7 " + esc(T.nombre);
  const pie = lib
    ? "Haz las " + T.reps + " repeticiones a tu ritmo y pulsa Serie hecha."
    : tr
      ? (T.pct
          ? "Aprieta al " + T.pct + " % y mant\u00e9n. Respira: no aguantes el aire. Si el dolor sube dentro de la serie, para."
          : "En marcha. Si el dolor sube durante la serie, para y an\u00f3talo.")
      : T.pct ? "Descanso. Suelta del todo la cara interna del muslo."
              : "Descanso. Respira y suelta antes de la siguiente serie.";
  document.getElementById("tm").innerHTML =
    '<div class="tm"><div class="s">' + cab + '</div>' +
    '<div class="ring ' + (lib ? "libre" : tr ? "run" : "rest") + '">' +
    '<div class="n' + (tr || lib ? "" : " rest") + '">' + mmss(T.seg) + '</div></div>' +
    '<div class="q">' + pie + '</div>' +
    '<div class="row">' +
    (lib ? '<button class="btn" data-tm="hecha">Serie hecha</button>'
         : '<button class="btn" data-tm="pausa">' + (T.corriendo ? "Pausar" : "Seguir") + '</button>') +
    '<button class="btn ghost" data-tm="salta">Saltar</button>' +
    '<button class="btn ghost" data-tm="cierra">Cerrar</button></div></div>';
}

/* -- modo entreno --------------------------------------------
   Un ejercicio por pantalla, foto grande y nada de scroll. Recorre
   las mismas tareas del dia, asi que lo que marcas aqui queda marcado alli. */
let ENT = null;
function tareasDe(s) {
  const out = [];
  s.secs.forEach(sec => {
    if (sec.tipo !== "tabla") return;
    const gym = sec.titulo.toLowerCase().indexOf("gimnasio") >= 0;
    sec.items.forEach((it, k) => out.push({
      id: sec.n + "_" + k, sec: sec.titulo, slug: it[0] || "",
      nombre: it[1], dosis: it[2], nota: it[3] || "", gym: gym,
    }));
  });
  return out;
}
function abreEntreno(i) {
  const s = sesionDe(FECHA);
  const tot = tareasDe(s);
  if (!tot.length) return;
  ENT = {lista: tot, i: Math.max(0, Math.min(i || 0, tot.length - 1)), pct: s.pct};
  document.body.classList.add("sin-scroll");
  pintaEntreno();
}
function cierraEntreno() {
  ENT = null;
  document.body.classList.remove("sin-scroll");
  document.getElementById("ent").innerHTML = "";
  render();
}
function pintaEntreno() {
  if (!ENT) return;
  const t = ENT.lista[ENT.i], r = S.reg[FECHA] || {};
  const on = (r.hechos || []).indexOf(t.id) >= 0;
  const f = D.ej[t.slug];
  const hechas = ENT.lista.filter(x => (r.hechos || []).indexOf(x.id) >= 0).length;
  const im = D.img[t.slug]
    ? '<img src="' + D.img[t.slug] + '" alt="">'
    : '<div class="ph"></div>';
  let kg = "";
  if (t.gym) {
    const clave = t.slug || t.nombre;
    const val = ((r.cargas || {})[clave]) || "";
    const ant = ultimaCarga(clave, FECHA);
    kg = '<div class="ent-kg"><input type="text" inputmode="decimal" data-kg="' + esc(clave) +
         '" value="' + esc(val) + '" placeholder="kg"><span>' +
         (ant ? "\u00faltima vez " + esc(ant.kg) : "anota la carga") + '</span></div>';
  }
  const crono = leeDosis(t.dosis)
    ? '<button class="btn ghost" data-crono="' + ENT.i + '">Cron\u00f3metro</button>' : "";
  document.getElementById("ent").innerHTML =
    '<div class="ent">' +
    '<div class="ent-top">' +
    '<div class="ent-pb"><i style="width:' + Math.round(hechas / ENT.lista.length * 100) + '%"></i></div>' +
    '<div class="ent-c"><span>' + (ENT.i + 1) + ' de ' + ENT.lista.length + ' \u00b7 ' + esc(t.sec) +
    '</span><button class="ent-x" data-ent="cierra" aria-label="Salir">\u2715</button></div></div>' +
    '<div class="ent-mid">' + im +
    '<div class="ent-n">' + esc(t.nombre) + '</div>' +
    '<div class="ent-d">' + esc(t.dosis) + '</div>' +
    (t.nota ? '<div class="ent-no">' + esc(t.nota) + '</div>' : '') +
    (f && f.error ? '<div class="ent-err"><b>Error t\u00edpico.</b> ' + esc(f.error) + '</div>' : '') +
    (f && f.aviso ? '<div class="ent-av">' + esc(f.aviso) + '</div>' : '') +
    kg + '</div>' +
    '<div class="ent-bot">' +
    '<div class="ent-r">' +
    '<button class="btn ghost" data-ent="prev"' + (ENT.i === 0 ? ' disabled' : '') + '>Anterior</button>' +
    crono +
    '<button class="btn ghost" data-ent="next">Saltar</button></div>' +
    '<button class="btn wide ' + (on ? 'ghost' : '') + '" data-ent="hecho">' +
    (on ? 'Hecho \u2713 \u00b7 siguiente' : 'Marcar hecho y seguir') + '</button>' +
    '</div></div>';
}

/* Pie de cada seccion de trabajo. Dos toques que valen mas que el dolor
   global de la noche, porque dicen QUE actividad molesta: el gimnasio, el
   agua o el campo. La escala es corta a proposito, para que se rellene. */
const MOLESTIA = ["nada", "poco", "bastante", "mucho"];
const ESFUERZO = ["suave", "justo", "fuerte"];
function pieSeccion(n, titulo) {
  const r = S.reg[FECHA] || {};
  const s = (r.sec || {})[n] || {};
  const chips = (clave, ops, val) => ops.map((x, k) =>
    '<button class="chip' + (val === k ? ' on' : '') + '" data-sec="' + n + ':' + clave + ':' + k +
    '">' + x + '</button>').join("");
  return '<div class="pie">' +
    '<div class="pie-r"><span>Molestia</span><div class="chips">' +
    chips("dolor", MOLESTIA, s.dolor) + '</div></div>' +
    '<div class="pie-r"><span>Esfuerzo</span><div class="chips">' +
    chips("rpe", ESFUERZO, s.rpe) + '</div></div></div>';
}

/* Cuanto duro de verdad una seccion, segun las horas que se fueron guardando
   solas al marcar sus tareas. */
function duracionReal(n, ids) {
  const r = S.reg[FECHA] || {}, h = r.horas || {};
  const t = ids.map(i => h[i]).filter(Boolean).sort();
  if (t.length < 2) return "";
  const min = x => (+x.slice(0, 2)) * 60 + (+x.slice(3));
  const d = min(t[t.length - 1]) - min(t[0]);
  return d > 0 && d < 300 ? t[0] + " a " + t[t.length - 1] + " · " + d + " min" : "";
}

/* Que actividad molesta, con los datos que se van dejando en cada seccion.
   Es la pregunta que en pubalgia decide si el plan avanza o recorta, y hasta
   ahora la app solo guardaba un dolor global por sesion. */
function porActividad() {
  const acc = {};
  Object.keys(S.reg).forEach(f => {
    const r = S.reg[f];
    if (!r.sec) return;
    let nom;
    try { nom = {}; sesionDe(f).secs.forEach(x => { nom[x.n] = x.titulo; }); }
    catch (e) { return; }
    Object.keys(r.sec).forEach(n => {
      const d = r.sec[n].dolor;
      if (d === undefined || d === null) return;
      const k = nom[n] || n;
      acc[k] = acc[k] || {n: 0, suma: 0, peor: 0};
      acc[k].n++; acc[k].suma += d; acc[k].peor = Math.max(acc[k].peor, d);
    });
  });
  const ks = Object.keys(acc).sort((a, b) => acc[b].suma / acc[b].n - acc[a].suma / acc[a].n);
  if (!ks.length)
    return '<div class="card"><div class="ch"><span class="cn">◇</span>' +
      '<h2 class="ct">Qué actividad molesta</h2></div>' +
      '<div class="note">Al pie de cada bloque de la sesión hay dos toques: molestia y ' +
      'esfuerzo. En cuanto haya unos días marcados, aquí sale el ranking de qué te sienta ' +
      'peor, que es lo que decide qué recortar.</div></div>';
  return '<div class="card"><div class="ch"><span class="cn">◇</span>' +
    '<h2 class="ct">Qué actividad molesta</h2>' +
    '<span class="cm">' + ks.length + ' actividades</span></div>' +
    '<table class="mini"><tr><th>Actividad</th><th>Media</th><th>Peor</th><th>Días</th></tr>' +
    ks.map(k => {
      const a = acc[k], m = a.suma / a.n;
      return '<tr><td>' + esc(k) + '</td><td>' + MOLESTIA[Math.round(m)] +
        '</td><td>' + MOLESTIA[a.peor] + '</td><td>' + a.n + '</td></tr>';
    }).join("") + '</table>' +
    '<div class="note">La media manda sobre un día suelto. Si una actividad sale en ' +
    '<strong>bastante</strong> dos semanas seguidas, se recorta esa y no la sesión entera.</div></div>';
}

/* Cuanto dura de verdad cada sesion, frente a lo que dice el plan. */
function tiemposReales() {
  const fs = Object.keys(S.reg).filter(f => Object.keys(S.reg[f].horas || {}).length > 1).sort();
  if (!fs.length) return "";
  const min = x => (+x.slice(0, 2)) * 60 + (+x.slice(3));
  const filas = fs.slice(-7).reverse().map(f => {
    const hs = Object.keys(S.reg[f].horas).map(k => S.reg[f].horas[k]).sort();
    const d = min(hs[hs.length - 1]) - min(hs[0]);
    return '<tr><td>' + f.slice(8) + "/" + f.slice(5, 7) + '</td><td>' + hs[0] +
      '</td><td>' + hs[hs.length - 1] + '</td><td>' + (d > 0 ? d + " min" : "") + '</td></tr>';
  }).join("");
  return '<div class="card"><div class="ch"><span class="cn">◷</span>' +
    '<h2 class="ct">A qué hora entrenas</h2><span class="cm">últimos 7</span></div>' +
    '<table class="mini"><tr><th>Día</th><th>Empiezas</th><th>Acabas</th><th>Dura</th></tr>' +
    filas + '</table>' +
    '<div class="note">Se apunta solo al marcar cada tarea. Sirve para ver si la sesión ' +
    'se te está alargando y para comparar el dolor de los días que entrenas tarde.</div></div>';
}

/* -- pantalla de arranque: el anillo de los cinco bloques ──── */
function splashHTML() {
  const i = bloqueDe(HOY0);
  const B = D.bloques;
  const idx = Math.max(0, B.findIndex(b => b.id === i.b.id));
  const R = 128, C = 2 * Math.PI * R;          /* circunferencia del anillo */
  const hueco = 10;                             /* separacion entre bloques */
  const paso = C / B.length;
  const largo = paso - hueco;

  let arcos = "";
  B.forEach((b, k) => {
    const off = -k * paso;
    arcos += '<circle class="base" cx="150" cy="150" r="' + R + '" stroke-width="13" ' +
      'stroke-dasharray="' + largo + ' ' + (C - largo) + '" stroke-dashoffset="' + off + '"/>';
    if (k < idx) {
      arcos += '<circle class="hecho" cx="150" cy="150" r="' + R + '" stroke-width="13" ' +
        'stroke-dasharray="' + largo + ' ' + (C - largo) + '" stroke-dashoffset="' + off + '"/>';
    }
  });
  /* el bloque en curso se dibuja hasta el dia de hoy */
  const frac = Math.max(0.04, Math.min(1, i.n / i.dur));
  const vivo = largo * frac;
  arcos += '<circle class="vivo" cx="150" cy="150" r="' + R + '" stroke-width="13" ' +
    'stroke-dasharray="' + vivo + ' ' + (C - vivo) + '" ' +
    'style="--vacio:' + (-idx * paso + vivo) + 'px;--lleno:' + (-idx * paso) + 'px"/>';

  const puntos = B.map((b, k) =>
    '<i class="' + (k === idx ? "on" : (k < idx ? "ya" : "")) + '"></i>').join("");

  return '<div class="sp" id="sp">' +
    '<div class="sp-marca">Readaptación</div>' +
    '<div class="sp-anillo"><svg viewBox="0 0 300 300" aria-hidden="true">' + arcos + '</svg>' +
    '<div class="sp-centro"><div class="sp-dia">' + i.n + '</div>' +
    '<div class="sp-de">de ' + i.dur + ' · ' + i.b.id + '</div></div></div>' +
    '<div class="sp-bloque"><b>' + esc(i.b.nombre) + '</b>' +
    '<span>' + esc(largoFecha(HOY0)) + '</span></div>' +
    '<div class="sp-puntos">' + puntos + '</div>' +
    '<div class="sp-tap">toca para entrar</div></div>';
}
const largoFecha = s => { const d = parse(s);
  return DS[wd(s)] + " " + d.getDate() + " de " + MS[d.getMonth()]; };

function cierraSplash() {
  const el = document.getElementById("sp");
  if (!el) return;
  el.classList.add("out");
  setTimeout(() => { const s = document.getElementById("ga-slot"); if (s) s.innerHTML = ""; }, 480);
}

/* la explicacion larga vive en Ajustes, no en la pantalla de cada manana */
function comoFunciona() {
  const pasos = [
    ["Anotas el dolor al despertar",
     "Antes de levantarte. Es el único dato que no puede inventar nadie."],
    ["La app compone la sesión",
     "Con 0-2 va entera. Con 3 caen gimnasio y campo. Con 4 se suspende y llamas al fisio."],
    ["Marcas y registras lo que haces",
     "Cargas, tareas y dolor. Sin registro, un bloque no puede darse por superado."],
    ["El día siguiente es el juez",
     "Si una puerta no se abre, el bloque se prolonga y el resto se recoloca solo."],
  ];
  return '<div class="card"><div class="ch"><span class="cn">?</span>' +
    '<h2 class="ct">Cómo funciona</h2></div><div class="cf">' +
    pasos.map((p, k) => '<div class="cf-p"><i>' + (k + 1) + '</i><div><b>' + p[0] + '.</b> ' +
      p[1] + '</div></div>').join("") + '</div>' +
    '<div class="note">Primero apagar la irritación, después fuerza, luego velocidad y al final ' +
    'el balón parado. Las faltas son lo tuyo y también lo que más castiga el pubis, así que llegan ' +
    'las últimas y con los golpeos contados.</div></div>';
}

/* ── resumen del dia en un vistazo ──────────────────────────── */
function resumenHTML(s, pr, mins) {
  const i = s.info;
  const secs = s.secs;
  const clave = [];
  secs.forEach(x => {
    if (x.tipo !== "tabla") return;
    x.items.forEach(it => { if (it[3] && clave.length < 2) clave.push([it[3], it[1], it[2]]); });
  });
  const campo = secs.find(x => /campo|fútbol|partido/i.test(x.titulo));
  const gym = secs.find(x => /gimnasio/i.test(x.titulo));
  const agua = secs.find(x => /piscina/i.test(x.titulo));
  const fisio = secs.find(x => /fisio/i.test(x.titulo));
  let li = "";
  const fila = (et, txt) => '<div class="sum-i"><em>' + et + '</em><div>' + txt + '</div></div>';
  li += fila("Hoy", '<b>' + esc(s.base.titulo) + '</b>');
  clave.forEach(c => li += fila(c[0], '<b>' + esc(c[1]) + '</b> · ' + esc(c[2])));
  if (gym) li += fila("Gimnasio", esc(gym.titulo.replace(/^Gimnasio · /, "")) +
                      (gym.meta ? " · " + esc(gym.meta) : ""));
  if (campo) li += fila("Campo", esc(campo.titulo.replace(/^Campo · /, "")));
  if (agua) li += fila("Agua", esc(agua.meta || "sesión de piscina"));
  if (fisio) li += fila("Fisio", esc(fisio.meta || "sesión"));
  if (i.b.fuera && i.b.fuera.length)
    li += fila("Fuera", i.b.fuera.slice(0, 4).join(" · ").toLowerCase() +
               (i.b.fuera.length > 4 ? " y " + (i.b.fuera.length - 4) + " más" : ""));
  return '<div class="sum"><div class="sum-t"><b>El día en un vistazo</b>' +
    '<span>' + i.b.id + ' · día ' + i.n + '/' + i.dur + '</span></div>' +
    '<div class="sum-g">' +
    '<div class="sum-c"><b>' + pr.total + '</b><span>tareas</span></div>' +
    '<div class="sum-c"><b>' + (mins >= 60 ? (mins / 60).toFixed(1).replace(".0", "") + " h" : mins + " min") +
    '</b><span>estimado</span></div>' +
    '<div class="sum-c"><b>' + s.pct + ' %</b><span>isométrico</span></div></div>' +
    movimiento(secs) +
    '<div class="sum-l">' + li + '</div></div>';
}

/* tira de miniaturas de una seccion de texto: piscina, aparatos, fisio, comida.
   Tocarlas abre su ficha en el manual. */
function tira(slugs) {
  const con = (slugs || []).filter(s => D.img[s]);
  if (!con.length) return "";
  return '<div class="tira">' + con.map(s =>
    '<figure data-ficha="' + s + '"><img src="' + D.img[s] + '" alt="' +
    esc(D.ej[s] ? D.ej[s].nombre : "") + '" loading="lazy">' +
    '<figcaption>' + esc(D.ej[s] ? D.ej[s].nombre : "") + '</figcaption></figure>'
  ).join("") + '</div>';
}

/* ── vista HOY ────────────────────────────────────────────── */
function vistaHoy() {
  const s = sesionDe(FECHA);
  /* indice de tareas: lo comparten el cronometro de cada fila y el modo entreno */
  const idxPosta = {};
  const postas = tareasDe(s);
  postas.forEach((x, n) => { idxPosta[x.id] = n; });

  const r = S.reg[FECHA] || {};
  const i = s.info;
  let h = "";

  h += '<div class="top">' + anilloMini(FECHA) +
       '<span class="pill">' + i.b.id + ' · ' + esc(i.b.nombre) + '</span>' +
       '<span class="pill solid">Día ' + i.n + ' de ' + i.dur + '</span></div>';

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

  /* resumen y tracker del dia */
  const pr = progresoDe(FECHA);
  h += resumenHTML(s, pr, minutosDe(s.secs));
  const mins = minutosDe(s.secs);
  h += '<div class="prog"><div class="pt"><div><span class="pn">' + pr.hechas + '</span>' +
       '<span class="pl"> de ' + pr.total + ' tareas' +
       (mins ? ' · unos ' + (mins >= 90 ? Math.floor(mins / 60) + ' h ' + (mins % 60 ? (mins % 60) + ' min' : '') : mins + ' min') : '') +
       '</span></div>' +
       '<div class="pl">' + pr.pct + ' %</div></div>' +
       '<div class="pbar' + (pr.pct >= 100 ? ' full' : '') + '"><i style="width:' +
       pr.pct + '%"></i></div></div>';

  if (postas.length)
    h += '<button class="btn wide entrar" data-entreno="1">Modo entreno · ' +
         postas.length + ' postas</button>';

  /* semaforo de la mañana */
  h += '<div class="card"><div class="ch"><span class="cn">01</span>' +
       '<h2 class="ct">Dolor de esta mañana</h2></div>' +
       '<p style="margin:0 0 8px;font-size:13.5px;color:var(--ink-3)">Antes de levantarte de la cama. ' +
       'Es lo que decide la sesión de hoy.</p>' + escala(FECHA, "manana", r.manana) +
       '<div class="dosn">' +
       '<label><span>Sueño</span><input type="text" inputmode="decimal" data-txt="sueno" value="' +
       esc(r.sueno || "") + '" placeholder="h"></label>' +
       '<label><span>Peso</span><input type="text" inputmode="decimal" data-txt="peso" value="' +
       esc(r.peso || "") + '" placeholder="kg"></label></div>';
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
        if (leeDosis(it[2])) {                         /* cronometro de la posta */
          extra += '<div class="kg"><button class="btn ghost mini" data-posta="' +
                   (idxPosta[sec.n + "_" + k] || 0) + '">' +
                   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
                   'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="8"/>' +
                   '<path d="M12 9v4l2.5 2M9 1.5h6"/></svg>Cronómetro</button></div>';
        }
        h += '<div class="ex" data-ficha="' + (it[0] || "") + '">' + im +
             '<div><div class="exn">' + esc(it[1]) + '</div>' +
             '<div class="exv">' + esc(it[2]) + '</div>' +
             (it[3] ? '<div class="exk">' + esc(it[3]) + '</div>' : '') + extra + '</div>' +
             '<button class="chk' + (on ? ' on' : '') + '" data-hecho="' + id + '">' +
             (on ? '✓' : '') + '</button></div>';
      });
      const ids = sec.items.map((x, k) => sec.n + "_" + k);
      const dur = duracionReal(sec.n, ids);
      if (dur) h += '<div class="dur">' + esc(dur) + '</div>';
      h += pieSeccion(sec.n, sec.titulo);
    } else if (sec.tipo === "lista") {
      h += tira(sec.fotos) +
           '<ul class="bul">' + sec.items.map(x => '<li>' + esc(x) + '</li>').join("") + '</ul>';
    } else if (sec.tipo === "pasos") {
      h += tira(sec.fotos);
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
  h += tira(["plato-modelo", "post-entreno"]);
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
  let h = '<div class="top">' + anilloMini(FECHA) + '<span class="pill">' + i0.b.id +
          ' · ' + esc(i0.b.nombre) + '</span><span class="pill solid">Semana</span></div>';
  const dom = suma(lunes, 6);
  const rango = parse(lunes).getDate() + " " + MS[parse(lunes).getMonth()].slice(0, 3) +
                " al " + parse(dom).getDate() + " " + MS[parse(dom).getMonth()].slice(0, 3);
  h += '<h1>La <span class="g">semana</span></h1><p class="sub">' + esc(i0.b.lema) + '</p>';

  h += '<div class="daynav">' +
       '<button data-sem="-7" aria-label="Semana anterior"><svg viewBox="0 0 24 24" fill="none" ' +
       'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg></button>' +
       '<div class="d">' + esc(rango) + '</div>' +
       '<button data-sem="7" aria-label="Semana siguiente"><svg viewBox="0 0 24 24" fill="none" ' +
       'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg></button></div>';

  if (dias(lunes, HOY0) < 0 || dias(HOY0, dom) < 0)
    h += '<button class="btn wide entrar" data-ir="' + HOY0 + '">Volver a hoy</button>';

  h += '<div class="week">';
  for (let k = 0; k < 7; k++) {
    const f = suma(lunes, k);
    const inf = bloqueDe(f);
    const antes = dias(f, D.bloques[0].desde) > 0;
    /* el mismo titulo que pinta la vista Hoy: el dia 1 es la sesion de
       apertura, no el microciclo que le tocaria por dia de la semana */
    const ses = antes ? null : sesionDe(f).base;
    const r = S.reg[f] || {};
    const d = r.manana;
    const cls = d === undefined || d === null ? "" : (d <= 1 ? "g" : (d <= 3 ? "a" : "r"));
    h += '<div class="wd' + (f === FECHA ? ' on' : '') + (f === HOY0 ? ' hoy' : '') +
         (antes ? ' fuera' : '') + '" data-ir="' + f + '">' +
         '<div class="dd">' + DS[k].slice(0,3) + ' ' + parse(f).getDate() +
         (f === HOY0 ? ' · hoy' : '') + '</div>' +
         '<div class="tt">' + esc(ses ? ses.titulo : (antes ? "antes de empezar" : "fuera de plan")) +
         '</div><div class="dot ' + cls + '"></div></div>';
  }
  h += '</div>';

  if (i0.antes) {
    h += '<div class="note">El plan arranca el <span class="mono">' + D.bloques[0].desde +
         '</span>. Los días anteriores no tienen sesión.</div>';
    return h;
  }
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
  let h = '<div class="top">' + anilloMini(FECHA) + '<span class="pill">Manual</span>' +
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
  let h = '<div class="top">' + anilloMini(FECHA) +
          '<span class="pill">Historial</span><span class="pill solid">' +
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

  h += porActividad();
  h += tiemposReales();
  h += comoFunciona();
  const tm = S.cfg.tema || "auto";
  h += '<div class="card"><div class="ch"><span class="cn">◐</span>' +
       '<h2 class="ct">Apariencia</h2></div>' +
       '<div class="row">' +
       [["auto", "Automático"], ["light", "Claro"], ["dark", "Oscuro"]].map(o =>
         '<button class="btn ' + (tm === o[0] ? '' : 'ghost') + '" data-tema="' + o[0] + '">' +
         o[1] + '</button>').join("") + '</div>' +
       '<button class="btn ghost wide" data-abstract="1">Ver la pantalla de arranque</button>' +
       '<div class="note">En automático sigue al sistema: claro de día y oscuro de noche.</div>' +
       '<div class="lab">Tamaño del texto</div><div class="row">' +
       [["n", "Normal"], ["g", "Grande"], ["xg", "Enorme"]].map(o =>
         '<button class="btn ' + ((S.cfg.fs || "n") === o[0] ? '' : 'ghost') +
         '" data-fs="' + o[0] + '">' + o[1] + '</button>').join("") + '</div>' +
       '<div class="note">Escala la aplicación entera, no solo las letras: fotos, botones y ' +
       'espacios crecen con el texto.</div></div>';

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
       '<div class="note">Versión instalada: <span class="mono">__VERSION__</span>. ' +
       'Si no coincide con la última, cierra la app y ábrela otra vez con cobertura.</div>' +
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
  if (e.target.closest("#sp")) { cierraSplash(); return; }
  const t = e.target.closest("button, .ex, .wd, figure[data-ficha]");
  if (!t) return;
  if (t.dataset.v) { VISTA = t.dataset.v; return render(); }
  if (t.dataset.nav) { FECHA = suma(FECHA, +t.dataset.nav); return render(); }
  if (t.dataset.sem) { FECHA = suma(FECHA, +t.dataset.sem); return render(); }
  if (t.dataset.ir) {
    FECHA = t.dataset.ir;
    if (!t.classList.contains("entrar")) VISTA = "hoy";
    return render();
  }
  if (t.dataset.k) { setReg(t.dataset.f, t.dataset.k, +t.dataset.v); return render(); }
  if (t.dataset.hecho) {
    const r = S.reg[FECHA] = S.reg[FECHA] || {};
    /* la hora se guarda sola: de ahi salen la duracion real de la sesion y
       la de cada seccion, sin que haya que apuntar nada */
    if (FECHA === HOY0) {
      r.horas = r.horas || {};
      const ahora = new Date();
      r.horas[t.dataset.hecho] = String(ahora.getHours()).padStart(2, "0") + ":" +
                                 String(ahora.getMinutes()).padStart(2, "0");
    }
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
    if (t.dataset.tm === "hecha") {
      if (T.serie >= T.series) return cierraTimer(true);
      T.fase = "descanso"; T.seg = T.descanso; return pintaTimer();
    }
    if (t.dataset.tm === "salta") {
      if (T.fase === "libre") { T.fase = "trabajo"; T.seg = 1; }
      else T.seg = 1;
      return tick();
    }
    return cierraTimer(false);
  }
  if (t.dataset.crono) {
    const x = ENT ? ENT.lista[+t.dataset.crono] : null;
    if (x) abreCrono({nombre: x.nombre, dosis: x.dosis,
                      pct: x.slug === "isometrico-aductor" ? ENT.pct : null});
    return;
  }
  if (t.dataset.posta) {
    const ss = sesionDe(FECHA), l = tareasDe(ss), x = l[+t.dataset.posta];
    if (x) abreCrono({nombre: x.nombre, dosis: x.dosis,
                      pct: x.slug === "isometrico-aductor" ? ss.pct : null});
    return;
  }
  if (t.dataset.entreno) { abreEntreno(+t.dataset.entreno - 1); return; }
  if (t.dataset.ent) {
    if (t.dataset.ent === "cierra") return cierraEntreno();
    if (t.dataset.ent === "prev") { ENT.i = Math.max(0, ENT.i - 1); return pintaEntreno(); }
    if (t.dataset.ent === "next") {
      if (ENT.i >= ENT.lista.length - 1) return cierraEntreno();
      ENT.i++; return pintaEntreno();
    }
    if (t.dataset.ent === "hecho") {
      const r = S.reg[FECHA] = S.reg[FECHA] || {};
      r.hechos = r.hechos || [];
      const x = ENT.lista[ENT.i].id;
      if (r.hechos.indexOf(x) < 0) r.hechos.push(x);
      save();
      if (ENT.i >= ENT.lista.length - 1) return cierraEntreno();
      ENT.i++; return pintaEntreno();
    }
  }
  if (t.closest && t.closest("#sp")) { cierraSplash(); return; }
  if (t.dataset.abstract) {
    document.getElementById("ga-slot").innerHTML = splashHTML();
    setTimeout(cierraSplash, 2600); return;
  }
  if (t.dataset.sec) {
    const [n, clave, v] = t.dataset.sec.split(":");
    const r = S.reg[FECHA] = S.reg[FECHA] || {};
    r.sec = r.sec || {};
    r.sec[n] = r.sec[n] || {};
    r.sec[n][clave] = r.sec[n][clave] === +v ? null : +v;   /* volver a tocar lo quita */
    save(); return render();
  }
  if (t.dataset.tema) { S.cfg.tema = t.dataset.tema; save(); aplicaTema(); return render(); }
  if (t.dataset.fs) { S.cfg.fs = t.dataset.fs; save(); aplicaTema(); return render(); }
  if (t.dataset.exp) { exporta(t.dataset.exp); return; }
  if (t.dataset.borrar) {
    if (confirm("Se borra todo el historial. ¿Seguro?")) { S = {reg:{}, cfg:{extra:{}}}; save(); render(); }
  }
});

document.addEventListener("input", e => {
  const d = e.target.dataset;
  if (!d) return;
  if (d.txt) setReg(FECHA, d.txt, e.target.value);
  if (d.ga === "nomas") { S.cfg.noGa = e.target.checked; save(); return; }
  if (d.kg) {                                   /* carga usada, sin repintar */
    const r = S.reg[FECHA] = S.reg[FECHA] || {};
    r.cargas = r.cargas || {};
    r.cargas[d.kg] = e.target.value;
    save();
  }
});

function cierraTimer(completo) {
  if (T && T.nombre) {                    /* series reales, no las del papel */
    const r = S.reg[FECHA] = S.reg[FECHA] || {};
    r.series = r.series || {};
    const hechas = completo ? T.series : Math.max(0, T.serie - 1);
    if (hechas > 0) { r.series[T.nombre] = hechas + " de " + T.series; save(); }
  }
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

function cabeceraCSV() {
  return "fecha,bloque,dia_bloque,sesion,dolor_reposo_0_10,dolor_durante_0_10," +
    "dolor_post_entreno_0_10,dolor_dia_siguiente_0_10,tos_estornudo_0_10,squeeze_max_0_10," +
    "isometrico_pct,zona_dolor,tareas_hechas,tareas_totales,cumplimiento_pct," +
    "sueno_h,peso_kg,inicio,fin,duracion_min,molestia_por_actividad,esfuerzo_por_actividad," +
    "series_reales,cargas,notas";
}

function exporta(tipo) {
  let txt, nom;
  if (tipo === "json") {
    txt = JSON.stringify(S, null, 1); nom = "readaptacion_copia.json";
  } else {
    const cab = cabeceraCSV();
    const fs = Object.keys(S.reg).sort();
    const filas = fs.map(f => {
      const r = S.reg[f], s = sesionDe(f), p = progresoDe(f);
      const sig = S.reg[suma(f, 1)] ? S.reg[suma(f, 1)].manana : "";
      const v = x => (x === undefined || x === null) ? "" : x;
      const cg = Object.keys(r.cargas || {}).map(k => k + ":" + r.cargas[k]).join(" | ");
      const sr = Object.keys(r.series || {}).map(k => k + ":" + r.series[k]).join(" | ");
      const hs = Object.keys(r.horas || {}).map(k => r.horas[k]).sort();
      const min = x => (+x.slice(0, 2)) * 60 + (+x.slice(3));
      const dur = hs.length > 1 ? (min(hs[hs.length - 1]) - min(hs[0])) : "";
      /* la molestia y el esfuerzo se guardan por numero de seccion: el CSV
         lleva el nombre de la actividad para que se entienda fuera de la app */
      const nom = {};
      s.secs.forEach(x => { nom[x.n] = x.titulo; });
      const sec = clave => Object.keys(r.sec || {})
        .filter(n => (r.sec[n] || {})[clave] !== undefined && r.sec[n][clave] !== null)
        .map(n => (nom[n] || n) + ":" +
             (clave === "dolor" ? MOLESTIA[r.sec[n][clave]] : ESFUERZO[r.sec[n][clave]]))
        .join(" | ");
      return [f, s.info.b.id, s.info.n, '"' + s.base.titulo + '"',
              v(r.manana), v(r.durante), v(r.acostar), v(sig), v(r.tos), v(r.squeeze),
              s.pct, '"' + (r.zona || "") + '"',
              p.hechas, p.total, p.pct,
              v(r.sueno), v(r.peso), hs[0] || "", hs[hs.length - 1] || "", dur,
              '"' + sec("dolor") + '"', '"' + sec("rpe") + '"', '"' + sr + '"',
              '"' + cg + '"',
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
              leeDosis, tareasDe, FECHA_INICIAL: FECHA, FECHA_ACTUAL: () => FECHA,
              cabeceraCSV,
              ultimaCarga, exporta, D, get S(){ return S; }, set S(x){ S = x; },
              setVista: v => { VISTA = v; render(); },
              setFecha: f => { FECHA = f; render(); },
              render: render};

/* app instalable: solo cuando se sirve por http(s); con file:// se ignora */
if ("serviceWorker" in navigator && location.protocol.indexOf("http") === 0) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

aplicaTema();
if (!S.cfg.noGa) {
  document.getElementById('ga-slot').innerHTML = splashHTML();
  setTimeout(cierraSplash, 2600);
}
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
           .replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
           .replace("__VERSION__", VERSION))

os.makedirs(os.path.dirname(DST), exist_ok=True)
io.open(DST, "w", encoding="utf-8", newline="\n").write(out)
print("escrito:", DST, os.path.getsize(DST) // 1024, "KB")
