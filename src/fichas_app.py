# -*- coding: utf-8 -*-
"""Aplana el catalogo de fichas a un dict slug -> ficha."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fichas import FICHAS  # noqa: E402
from fichas_extra import EXTRA  # noqa: E402
from fichas_v3 import V3  # noqa: E402

TODAS = dict(FICHAS)
TODAS.update(EXTRA)
TODAS.update(V3)

EJ = {}
for bloque, (titulo, _sub, fs) in TODAS.items():
    for slug, nombre, para_que, pasos, error, aviso in fs:
        EJ[slug] = dict(nombre=nombre, bloque=bloque, para_que=para_que,
                        pasos=list(pasos), error=error, aviso=aviso or "")
