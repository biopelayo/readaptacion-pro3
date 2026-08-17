# -*- coding: utf-8 -*-
"""Versiones ligeras de las ilustraciones, para que el repo no pese 85 MB."""
import glob, os
from PIL import Image

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "imagenes", "ejercicios")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "imagenes", "web")
os.makedirs(DST, exist_ok=True)

tot = 0
for p in sorted(glob.glob(os.path.join(SRC, "*.png"))):
    im = Image.open(p).convert("RGB")
    im.thumbnail((1000, 1000), Image.LANCZOS)
    d = os.path.join(DST, os.path.basename(p).replace(".png", ".jpg"))
    im.save(d, "JPEG", quality=82, optimize=True, progressive=True)
    tot += os.path.getsize(d)
print(len(glob.glob(os.path.join(DST, "*.jpg"))), "jpg ·", tot // 1024 // 1024, "MB")
