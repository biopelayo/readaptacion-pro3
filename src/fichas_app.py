# -*- coding: utf-8 -*-
"""Aplana el catalogo de fichas a un dict slug -> ficha."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fichas import FICHAS  # noqa: E402

EJ = {}
for bloque, (titulo, _sub, fs) in FICHAS.items():
    for slug, nombre, para_que, pasos, error, aviso in fs:
        EJ[slug] = dict(nombre=nombre, bloque=bloque, para_que=para_que,
                        pasos=list(pasos), error=error, aviso=aviso or "")
