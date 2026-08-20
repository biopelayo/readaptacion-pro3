# -*- coding: utf-8 -*-
"""Versiones ligeras de las ilustraciones, para que el repo no pese 200 MB.

Los PNG a resolucion completa viven fuera del control de versiones, asi que en
un worktree la carpeta esta vacia: se busca tambien en el repo principal.
"""
import glob, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
DST = os.path.join(RAIZ, "imagenes", "web")


def origen():
    """Primero la carpeta local; si esta vacia y esto es un worktree, la del repo."""
    local = os.path.join(RAIZ, "imagenes", "ejercicios")
    if glob.glob(os.path.join(local, "*.png")):
        return local
    marca = os.path.join(".claude", "worktrees")
    if marca in RAIZ:
        principal = RAIZ.split(marca)[0].rstrip("\\/")
        alt = os.path.join(principal, "imagenes", "ejercicios")
        if glob.glob(os.path.join(alt, "*.png")):
            return alt
    return local


SRC = origen()
os.makedirs(DST, exist_ok=True)
print("origen:", SRC)

tot = 0
fuentes = sorted(glob.glob(os.path.join(SRC, "*.png")))
for p in fuentes:
    im = Image.open(p).convert("RGB")
    im.thumbnail((1000, 1000), Image.LANCZOS)
    d = os.path.join(DST, os.path.basename(p).replace(".png", ".jpg"))
    im.save(d, "JPEG", quality=82, optimize=True, progressive=True)
    tot += os.path.getsize(d)

hechos = glob.glob(os.path.join(DST, "*.jpg"))
print("%d png leidos, %d jpg en web, %.1f MB" % (len(fuentes), len(hechos), tot / 1024 / 1024))
