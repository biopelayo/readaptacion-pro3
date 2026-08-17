# -*- coding: utf-8 -*-
"""Inyecta miniaturas de ejercicio en las tablas de las hojas diarias.

Busca las celdas <td class="k">Nombre</td>, resuelve el slug por palabras clave
y antepone una celda con la miniatura embebida en base64. Es idempotente: si la
hoja ya tiene miniaturas, no las duplica.
"""
import base64, io, os, re, sys
from PIL import Image

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "imagenes", "web")

# nombre visible (en minusculas, sin acentos relevantes) -> slug
MAPA = [
    ("90/90", "90-90-cadera"),
    ("rockback", "adductor-rockback"),
    ("cadera activa", "movilidad-cadera-pie"),
    ("brace", "brace-respiracion"),
    ("isom", "isometrico-aductor"),
    ("puente de gl", "puente-gluteo"),
    ("pallof", "pallof-press"),
    ("dead bug", "dead-bug"),
    ("press de pecho", "press-pecho-maquina"),
    ("press inclinado", "press-inclinado-mancuernas"),
    ("press militar", "press-militar-maquina"),
    ("elevaciones laterales", "elevaciones-laterales"),
    ("tr\u00edceps", "triceps-polea"),
    ("curl femoral", "curl-femoral"),
    ("cu\u00e1driceps", "extension-cuadriceps"),
    ("jal\u00f3n", "jalon-al-pecho"),
    ("remo en m\u00e1quina", "remo-maquina-neutro"),
    ("remo con mancuerna", "remo-mancuerna"),
    ("face pull", "face-pull"),
    ("curl de b\u00edceps", "curl-biceps-inclinado"),
    ("curl martillo", "curl-martillo"),
    ("gemelo", "gemelo-de-pie"),
]

CSS = """
table.mini{table-layout:auto}
table.mini td,table.mini th{padding:4px 5px}
table.mini td.n,table.mini th.n{font-size:9.5px}
td.th,th.th{width:42px;padding:3px 4px 3px 6px}
td.th img{display:block;width:34px;height:26px;object-fit:cover;border-radius:3px;
  border:1px solid var(--hair-soft)}
table.mini td.k{font-size:11px;line-height:1.25}
@media screen and (max-width:820px){td.th,th.th{width:38px}td.th img{width:31px;height:23px}}
"""

_cache = {}


def thumb(slug, w=140, h=104):
    if slug in _cache:
        return _cache[slug]
    p = os.path.join(IMG, slug + ".jpg")
    if not os.path.exists(p):
        _cache[slug] = None
        return None
    im = Image.open(p).convert("RGB")
    # recorte central 4:3 y reduccion
    tw, th = w, h
    ratio = max(tw / im.width, th / im.height)
    im = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=72, optimize=True)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    _cache[slug] = uri
    return uri


def slug_de(nombre):
    n = nombre.lower()
    # las tablas de chequeo y de registro tambien usan td.k: no llevan miniatura
    if "dolor" in n or "comparado" in n or "squeeze" in n or "zona" in n or "lado" in n:
        return None
    for clave, slug in MAPA:
        if clave in n:
            return slug
    return None


def procesa(path):
    html = io.open(path, encoding="utf-8").read()
    if 'td class="th"' in html:
        print(f"  {os.path.basename(path)}: ya tenia miniaturas, se rehace")
        html = re.sub(r'<td class="th">.*?</td>', "", html, flags=re.S)
        html = html.replace('<th class="th"></th>', "")

    puestas, sin_img = 0, set()

    def repl(m):
        nonlocal puestas
        fila, antes, nombre = m.group(0), m.group(1), m.group(2)
        limpio = re.sub(r"<[^>]+>", "", nombre)
        slug = slug_de(limpio)
        if not slug:
            return fila
        uri = thumb(slug)
        if not uri:
            sin_img.add(slug)
            return fila
        puestas += 1
        celda = f'<td class="th"><img src="{uri}" alt=""></td>'
        return "<tr>" + celda + antes + f'<td class="k">{nombre}</td>'

    # se procesa tabla a tabla: solo la que recibe miniaturas gana la columna extra
    def por_tabla(mt):
        tabla = mt.group(0)
        # el patron no puede cruzar </tr>: si lo hiciera, se tragaria el thead entero
        nueva = re.sub(r'<tr>((?:(?!</tr>)(?!<td class="k">).)*?)<td class="k">(.*?)</td>',
                       repl, tabla, flags=re.S)
        if 'td class="th"' not in nueva:
            return nueva
        if "<thead>" in nueva:
            nueva = nueva.replace("<thead><tr>", '<thead><tr><th class="th"></th>', 1)
        # la columna extra roba ancho: se encogen los anchos fijos de las demas
        nueva = re.sub(r"width:(\d+)px",
                       lambda w: "width:%dpx" % max(26, int(int(w.group(1)) * 0.78)), nueva)
        nueva = nueva.replace("<table", '<table class="mini"', 1)
        return nueva

    html = re.sub(r"<table.*?</table>", por_tabla, html, flags=re.S)

    if "td.th{" not in html:
        html = html.replace("</style>", CSS + "</style>", 1)

    io.open(path, "w", encoding="utf-8", newline="\n").write(html)
    print(f"  {os.path.basename(path)}: {puestas} miniaturas"
          + (f" · sin imagen: {sorted(sin_img)}" if sin_img else ""))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        procesa(p)
