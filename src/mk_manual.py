# -*- coding: utf-8 -*-
"""Maqueta el manual de ejercicios del bloque R1 en HTML autocontenido."""
import base64, io, os, re, sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratchpad"))
from fichas import FICHAS  # noqa: E402

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "imagenes", "web")
TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dias", "PLANTILLA_MANUAL.html")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "MANUAL_EJERCICIOS_R1.html")

style = re.search(r"<style>.*?</style>", io.open(TPL, encoding="utf-8").read(), re.S).group(0)

EXTRA = """
<style>
.ficha{background:linear-gradient(160deg,rgba(19,42,92,.85),rgba(10,23,51,.92));
  border:1px solid var(--hair);border-radius:9px;overflow:hidden;break-inside:avoid;
  display:flex;flex-direction:column}
.ficha-h{display:grid;grid-template-columns:22px 1fr;gap:8px;align-items:center;padding:7px 10px 6px}
.ficha-n{font-family:var(--display);font-size:18px;color:var(--gold);line-height:1;text-align:center}
.ficha-t{font-family:var(--display);font-size:12px;line-height:1.06;color:var(--white);
  text-transform:uppercase;letter-spacing:.02em}
.ficha-img{display:block;width:100%;height:37mm;object-fit:cover;
  border-top:1px solid var(--hair-soft);border-bottom:1px solid var(--hair-soft)}
.ficha-b{padding:8px 10px 9px;flex:1}
.fl{font-size:7.5px;letter-spacing:.15em;text-transform:uppercase;font-weight:800;color:var(--gold);
  margin:0 0 2px;display:flex;align-items:center;gap:5px}
.fl.err{color:var(--red)}
.fp{font-size:8.8px;line-height:1.3;margin:0 0 6px;color:var(--body)}
.fp:last-child{margin-bottom:0}
ol.fsteps{list-style:none;counter-reset:f;margin:0 0 6px;padding:0}
ol.fsteps li{counter-increment:f;position:relative;padding:1px 0 1px 15px;font-size:8.8px;line-height:1.28}
ol.fsteps li::before{content:counter(f);position:absolute;left:0;top:2px;width:11px;height:11px;
  border-radius:50%;border:1px solid var(--gold);color:var(--gold);font-family:var(--mono);
  font-size:6.5px;display:flex;align-items:center;justify-content:center}
.faviso{border-left:2px solid var(--red);background:rgba(226,104,90,.1);padding:5px 7px;
  border-radius:0 4px 4px 0;font-size:8.3px;line-height:1.28;color:#F0C4BC;margin-top:5px}
.fichas{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.bloque-h{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:baseline;
  border-bottom:1px solid var(--hair);padding-bottom:9px;margin-bottom:12px}
.bloque-n{font-family:var(--display);font-size:34px;color:var(--gold);line-height:.9}
.bloque-t{font-family:var(--display);font-size:22px;color:var(--white);text-transform:uppercase;
  letter-spacing:.02em;line-height:1;margin:0 0 4px}
.bloque-d{font-size:11.5px;color:var(--dim);margin:0;line-height:1.4}
.idx{display:grid;grid-template-columns:repeat(2,1fr);gap:9px}
.idx-c{border:1px solid var(--hair-soft);border-radius:7px;padding:11px 13px;background:rgba(6,14,36,.45)}
.idx-t{font-family:var(--display);font-size:14px;color:var(--gold-lt);text-transform:uppercase;margin-bottom:6px}
.idx-l{font-size:10.5px;color:var(--body);line-height:1.6;margin:0;padding-left:14px}
@media print{.fichas{grid-template-columns:repeat(3,1fr)}}
@media screen and (max-width:820px){.fichas,.idx{grid-template-columns:1fr}}
</style>
"""


def data_uri(slug, width=760, quality=80):
    p = os.path.join(IMG, slug + ".jpg")
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert("RGB")
    im.thumbnail((width, width), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def ficha_html(n, f):
    slug, titulo, para_que, pasos, error, aviso = f
    uri = data_uri(slug)
    img = (f'<img class="ficha-img" src="{uri}" alt="{esc(titulo)}">' if uri else
           '<div class="ficha-img" style="height:96px;background:rgba(255,255,255,.04)"></div>')
    pasos_html = "".join(f"<li>{esc(p)}</li>" for p in pasos)
    av = f'<div class="faviso">{esc(aviso)}</div>' if aviso else ""
    return f'''<article class="ficha">
  <div class="ficha-h"><div class="ficha-n">{n}</div><h3 class="ficha-t">{esc(titulo)}</h3></div>
  {img}
  <div class="ficha-b">
    <p class="fl">Para qué sirve</p>
    <p class="fp">{esc(para_que)}</p>
    <p class="fl">Cómo se hace</p>
    <ol class="fsteps">{pasos_html}</ol>
    <p class="fl err">Error frecuente</p>
    <p class="fp">{esc(error)}</p>
    {av}
  </div>
</article>'''


CREST = '''<svg width="86" height="98" viewBox="0 0 86 98" fill="none" aria-hidden="true">
        <path d="M43 4 L79 15 V49c0 21-15 36-36 45C22 85 7 70 7 49V15Z" stroke="#C9A227" stroke-width="2" fill="rgba(201,162,39,.07)"/>
        <path d="M43 11 L72 20v28c0 17-12 30-29 37-17-7-29-20-29-37V20Z" stroke="rgba(201,162,39,.4)" stroke-width="1"/>
        <path d="M43 26v34M31 40h24" stroke="#E3C468" stroke-width="2.4" stroke-linecap="round"/>
        <circle cx="43" cy="70" r="7" stroke="#E3C468" stroke-width="1.6"/>
        <path d="M36.5 70h13M43 63.2v13.6" stroke="rgba(227,196,104,.55)" stroke-width="1"/>
      </svg>'''

paginas = []
total = sum(len(v[2]) for v in FICHAS.values())

# ── portada ──────────────────────────────────────────────────────────
idx_cols = []
for bloque, (titulo, _sub, fs) in FICHAS.items():
    items = "".join(f"<li>{esc(t)}</li>" for _s, t, *_ in fs)
    idx_cols.append(f'<div class="idx-c"><div class="idx-t">{bloque} · {esc(titulo)}</div>'
                    f'<ol class="idx-l">{items}</ol></div>')

paginas.append(f'''<section class="page">
  <div class="top">
    <span class="pill"><b>PARTE 3</b> · MANUAL DE EJERCICIOS</span>
    <span class="pill pill-solid">BLOQUE R1</span>
  </div>
  <header class="masthead">
    <div>
      <div class="mast-kicker">Reinicio · 17 de agosto al 30 de agosto de 2026</div>
      <h1 class="title">CÓMO SE HACE <span class="g">CADA COSA</span></h1>
      <p class="subtitle">Las {total} tareas de los bloques 02 a 07, una por una: para qué sirve, cómo se ejecuta paso a paso y el error que se comete siempre.</p>
      <div class="tags">
        <span class="tag on">{total} fichas ilustradas</span>
        <span class="tag">Movilidad · gimnasio · agua · aparatos · mesa</span>
        <span class="tag">Nivel principiante</span>
      </div>
    </div>
    <div class="crest">{CREST}<div class="crest-cap">PRO 3.0</div><div class="crest-sub">Readaptación</div></div>
  </header>
  <div class="ban">
    <div class="ban-h"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/></svg> Nada de esto aparece en el manual, y es a propósito</div>
    <div class="chips"><span>Balón</span><span>Golpeo</span><span>Sprint</span><span>Cambios de dirección</span><span>Pliometría</span><span>Copenhagen</span><span>Sentadilla</span><span>Zancada</span><span>Aductores en máquina</span><span>Braza</span></div>
  </div>
  <div class="rule">
    <div class="rule-l">Cómo se<br>usa</div>
    <div class="rule-t">Se imprime una vez y se consulta cuando dudes. Las hojas diarias dicen qué toca y cuánto; este manual dice cómo se hace. Si un ejercicio no se puede ejecutar como está descrito aquí, se cambia por otro, no se hace a medias.</div>
  </div>
  <div class="idx">{"".join(idx_cols)}</div>
  <div class="note warn" style="margin-top:11px">Las imágenes son ilustraciones generadas para mostrar la posición. Sirven de referencia visual, no de valoración clínica: ante cualquier duda sobre tu caso manda lo que digan tu fisioterapeuta y tu médico.</div>
  <div class="foot">
    <div>Disciplina · Constancia · Inteligencia · Fuerza</div>
    <div class="r">Manual de ejercicios · bloque R1 · portada</div>
  </div>
</section>''')

# ── páginas de fichas ────────────────────────────────────────────────
n_global = 0
for bloque, (titulo, sub, fs) in FICHAS.items():
    trozos = [fs[i:i + 6] for i in range(0, len(fs), 6)]
    for k, trozo in enumerate(trozos):
        cabecera = ""
        if k == 0:
            cabecera = (f'<div class="bloque-h"><div class="bloque-n">{bloque}</div>'
                        f'<div><h2 class="bloque-t">{esc(titulo)}</h2>'
                        f'<p class="bloque-d">{esc(sub)}</p></div></div>')
        cuerpo = "".join(ficha_html(n_global + j + 1, f) for j, f in enumerate(trozo))
        n_global += len(trozo)
        cont = f" · continuación" if k else ""
        paginas.append(f'''<section class="page">
  <div class="top">
    <span class="pill"><b>{bloque}</b> · {esc(titulo.upper())}{cont.upper()}</span>
    <span class="pill pill-solid">MANUAL R1</span>
  </div>
  {cabecera}
  <div class="fichas">{cuerpo}</div>
  <div class="foot">
    <div>Técnica primero · el rango completo antes que el peso</div>
    <div class="r">Manual de ejercicios · bloque {bloque} · {esc(titulo)}</div>
  </div>
</section>''')

out = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
       '<title>Manual de ejercicios · bloque R1 · Reinicio 2026</title>\n'
       + style + EXTRA + '\n</head>\n<body>\n'
       '<button class="print-btn" onclick="window.print()">Imprimir</button>\n'
       + "\n".join(paginas) + '\n</body>\n</html>\n')

io.open(DST, "w", encoding="utf-8", newline="\n").write(out)
print("escrito:", DST, os.path.getsize(DST) // 1024, "KB ·", len(paginas), "paginas ·", n_global, "fichas")
