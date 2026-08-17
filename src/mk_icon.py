# -*- coding: utf-8 -*-
"""Icono de la app: escudo dorado sobre azul marino."""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app")


def icono(px):
    S = px * 4                       # se dibuja grande y se reduce, para bordes limpios
    im = Image.new("RGB", (S, S), (10, 23, 51))
    d = ImageDraw.Draw(im)
    for i in range(S):               # degradado suave
        v = i / S
        d.line([(0, i), (S, i)],
               fill=(int(10 + 12 * (1 - v)), int(23 + 22 * (1 - v)), int(51 + 40 * (1 - v))))
    g = (201, 162, 39)
    gl = (227, 196, 104)
    m, w = S * 0.20, S * 0.60
    top, bot = S * 0.16, S * 0.86
    escudo = [(m + w / 2, top), (m + w, top + w * 0.16), (m + w, top + w * 0.62),
              (m + w / 2, bot), (m, top + w * 0.62), (m, top + w * 0.16)]
    d.polygon(escudo, outline=g, width=int(S * 0.022))
    cx, cy = m + w / 2, top + w * 0.42
    d.line([(cx, cy - w * 0.20), (cx, cy + w * 0.26)], fill=gl, width=int(S * 0.030))
    d.line([(cx - w * 0.17, cy - w * 0.02), (cx + w * 0.17, cy - w * 0.02)],
           fill=gl, width=int(S * 0.030))
    r = w * 0.11
    d.ellipse([cx - r, cy + w * 0.26 - r, cx + r, cy + w * 0.26 + r],
              outline=gl, width=int(S * 0.018))
    return im.resize((px, px), Image.LANCZOS)


for px in (192, 512):
    p = os.path.join(OUT, "icon-%d.png" % px)
    icono(px).save(p, "PNG", optimize=True)
    print(p, os.path.getsize(p) // 1024, "KB")
