# -*- coding: utf-8 -*-
"""Anillo permanente en la cabecera y arreglo del texto de apertura."""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ── 1. fuera el reframe de la apertura ──────────────────────────────
p = os.path.join(HERE, "plan_data.py")
t = io.open(p, encoding="utf-8").read()
VIEJO = ('    "Lo que cuenta hoy no es el peso que muevas, son los cuatro números que dejes escritos "\n'
         '    "antes de empezar. Llevas ocho semanas sin ellos.",')
NUEVO = ('    "Apunta los cuatro números de la línea base antes de tocar una máquina. Llevas ocho "\n'
         '    "semanas sin ellos y el plan no puede decidir nada a ciegas.",')
if VIEJO in t:
    t = t.replace(VIEJO, NUEVO)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("apertura: reframe fuera")
else:
    print("apertura: NO ENCONTRADO")

# ── 2. CSS del anillo pequeño ───────────────────────────────────────
p = os.path.join(HERE, "css_nuevo.py")
t = io.open(p, encoding="utf-8").read()
CSS = '''
/* ── anillo pequeño, siempre en la cabecera ───────────────── */
.mini-anillo{width:2.5rem;height:2.5rem;flex:0 0 auto;cursor:pointer;position:relative;
  display:flex;align-items:center;justify-content:center}
.mini-anillo svg{width:100%;height:100%;transform:rotate(-90deg)}
.mini-anillo .b{stroke:var(--line);fill:none}
.mini-anillo .y{stroke:var(--ink-4);fill:none;stroke-linecap:round}
.mini-anillo .v{stroke:var(--ink);fill:none;stroke-linecap:round}
.mini-anillo span{position:absolute;font-size:.72rem;font-weight:700;color:var(--ink);
  letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.mini-anillo:active{transform:scale(.92)}
'''
if ".mini-anillo{" not in t:
    t = t.replace('\n/* ── superficies ─', CSS + '\n/* ── superficies ─')
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css: anillo pequeño")

# ── 3. JS ───────────────────────────────────────────────────────────
p = os.path.join(HERE, "mk_app.py")
t = io.open(p, encoding="utf-8").read()

JS = r'''/* anillo pequeno de cabecera: el mismo dibujo del arranque, a 40 px */
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

/* ── pantalla de arranque'''
if "function anilloMini(" not in t:
    assert "/* ── pantalla de arranque" in t
    t = t.replace("/* ── pantalla de arranque", JS, 1)

    # va en la cabecera de las cuatro vistas
    t = t.replace("""h += '<div class="top"><span class="pill">' + i.b.id + ' · ' + esc(i.b.nombre) +
       '</span><span class="pill solid">Día ' + i.n + ' de ' + i.b.dias + '</span></div>';""",
                  """h += '<div class="top">' + anilloMini(FECHA) +
       '<span class="pill">' + i.b.id + ' · ' + esc(i.b.nombre) + '</span>' +
       '<span class="pill solid">Día ' + i.n + ' de ' + i.b.dur + '</span></div>';""")
    t = t.replace("""let h = '<div class="top"><span class="pill">' + i0.b.id + ' · ' +
          esc(i0.b.nombre) + '</span><span class="pill solid">Semana</span></div>';""",
                  """let h = '<div class="top">' + anilloMini(FECHA) + '<span class="pill">' + i0.b.id +
          ' · ' + esc(i0.b.nombre) + '</span><span class="pill solid">Semana</span></div>';""")
    t = t.replace("""'<div class="top"><span class="pill">Manual de ejercicios</span>' +""",
                  """'<div class="top">' + anilloMini(FECHA) + '<span class="pill">Manual</span>' +""")
    t = t.replace("""'<div class="top"><span class="pill">Historial</span><span class="pill solid">' +""",
                  """'<div class="top">' + anilloMini(FECHA) +
          '<span class="pill">Historial</span><span class="pill solid">' +""")

    # el splash se cierra en cuanto se toca, sin esperar
    t = t.replace("setTimeout(cierraSplash, 2600);", "setTimeout(cierraSplash, 2600);")
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("app: anillo en cabecera")
