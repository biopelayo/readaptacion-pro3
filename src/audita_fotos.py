# -*- coding: utf-8 -*-
"""Auditoria dura: que NINGUNA foto se quede sin verse en la app.

Comprueba tres cosas distintas, porque una foto puede fallar en cualquiera:
  1. que exista el jpg de origen,
  2. que su data URI este dentro del index.html,
  3. que algun dia del plan la pinte, sea en tabla o en tira.
"""
import glob, io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from plan_data import MICRO, APERTURA  # noqa: E402
from fichas_app import EJ              # noqa: E402

html = io.open(os.path.join(RAIZ, "app", "index.html"), encoding="utf-8").read()

# 1. origen
# los "--b" son el segundo fotograma de un gesto, no fichas del catalogo
web = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(RAIZ, "imagenes", "web", "*.jpg"))
       if not p.endswith("--b.jpg")}

# 2. embebidas: se saca el diccionario img del JSON del propio html
emb = {k for k in re.findall(r'"([a-z0-9-]+)"\s*:\s*"data:image/jpeg;base64,', html)
       if not k.endswith("--b")}

# 3. pintadas por algun dia
pintadas = set()


def recorre(ses):
    for s in ses["secciones"]:
        pintadas.update(s.get("fotos", []))
        if s["tipo"] == "tabla":
            pintadas.update(i[0] for i in s["items"] if i[0])


for dias in MICRO.values():
    for ses in dias.values():
        recorre(ses)
recorre(APERTURA)
pintadas.update({"plato-modelo", "post-entreno"})   # van en la seccion de nutricion

fichas = set(EJ)
print("fichas en el catálogo ...... %d" % len(fichas))
print("jpg de origen .............. %d" % len(web))
print("embebidas en index.html .... %d" % len(emb))
print("pintadas por algún día ..... %d" % len(pintadas & fichas))
print()

problemas = []
sin_origen = sorted(fichas - web)
sin_embeber = sorted(fichas - emb)
sin_pintar = sorted(fichas - pintadas)
sobran = sorted(emb - fichas)

for etiqueta, lista in (("sin jpg de origen", sin_origen),
                        ("no embebidas en la app", sin_embeber),
                        ("nunca se pintan", sin_pintar),
                        ("embebidas de más", sobran)):
    if lista:
        problemas.append("%s: %s" % (etiqueta, ", ".join(lista)))
        print("FALLA %s (%d): %s" % (etiqueta, len(lista), ", ".join(lista)))

kb = len(html) // 1024
print()
print("peso de la app: %d KB" % kb)
if problemas:
    print("\nRESULTADO: %d problemas" % len(problemas))
    sys.exit(1)
print("\nRESULTADO: las %d fotos existen, están embebidas y se pintan." % len(fichas))
