# -*- coding: utf-8 -*-
"""Genera los dias del bloque de reinicio a partir del MISMO modelo que la app.

Escribe una hoja en Markdown por dia y un cuaderno HTML imprimible con todos.
Al leer plan_data.py, la unica fuente, ninguna hoja puede divergir de lo que
la aplicacion compone en el movil.

Aviso que va impreso en cada hoja: de R2 en adelante las fechas son PREVISION.
Si una puerta no se abre, el bloque se prolonga y todo lo posterior se corre.
"""
import datetime as dt
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from plan_data import BLOQUES, MICRO, NUTRICION, MOMENTOS, ISO, EJ  # noqa: E402

DESDE = dt.date(2026, 8, 19)
HASTA = dt.date(2026, 10, 25)
DS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
      "septiembre", "octubre", "noviembre", "diciembre"]


def bloque_de(f):
    """Mismo calculo que bloqueDe() en la app, sin dias extra."""
    for b in BLOQUES:
        desde = dt.date.fromisoformat(b["desde"])
        hasta = desde + dt.timedelta(days=b["dias"] - 1)
        if desde <= f <= hasta:
            return b, (f - desde).days + 1, desde, hasta
    return None, 0, None, None


def largo(f):
    return "%s %d de %s de %d" % (DS[f.weekday()], f.day, MS[f.month - 1], f.year)


def md_dia(f):
    b, n, desde, hasta = bloque_de(f)
    ses = MICRO[b["id"]][f.weekday()]
    tabla = b.get("iso", ISO)
    pct = tabla[min(max(n - 1, 0), len(tabla) - 1)]
    L = []
    A = L.append

    A("# %s · %s · día %d de %d" % (largo(f).capitalize(), b["id"], n, b["dias"]))
    A("")
    A("**%s**" % ses["titulo"])
    A("")
    A("- **Bloque:** %s · %s (%s a %s)." % (b["id"], b["nombre"], desde, hasta))
    A("- **Objetivo del bloque:** %s" % b["lema"])
    A("- **Isométrico de aductor:** %d %%." % pct)
    if b["fuera"]:
        A("- **Fuera del plan:** %s." % ", ".join(b["fuera"]).lower())
    A("")
    A("## Regla del día")
    A("")
    A("> %s" % ses["regla"])
    A("")
    A("## Antes de nada")
    A("")
    A("| Medida | Valor |")
    A("|--------|-------|")
    A("| Dolor al despertar 0-10 | ___ |")
    A("| Comparado con ayer | mejor / igual / peor |")
    A("")
    A("| Dolor de hoy | Qué se hace |")
    A("|--------------|-------------|")
    A("| **0-1** | Sesión completa tal como está escrita. |")
    A("| **2** | Sesión completa, con el isométrico en su escalón. |")
    A("| **3** | Fuera el gimnasio y el campo. Movilidad, isométrico al %d %%, agua y aparatos. |"
      % max(40, pct - 20))
    A("| **4 o más** | Se suspende la sesión. Solo movilidad muy suave y llamar al fisio. |")
    A("")

    for sec in ses["secciones"]:
        A("## %s · %s%s" % (sec["n"], sec["titulo"],
                            (" · %s" % sec["meta"]) if sec["meta"] else ""))
        A("")
        if sec["tipo"] == "tabla":
            A("| Ejercicio | Volumen | Hecho | Dolor |")
            A("|-----------|---------|-------|-------|")
            for it in sec["items"]:
                vol = it[2]
                if it[0] == "isometrico-aductor":
                    vol = "5 × 30 s al %d %%" % pct
                marca = " **%s**" % it[3] if it[3] else ""
                A("| %s%s | %s | ☐ | ___ |" % (it[1], marca, vol))
        elif sec["tipo"] == "lista":
            for x in sec["items"]:
                A("- %s" % x)
        elif sec["tipo"] == "pasos":
            for i, x in enumerate(sec["items"], 1):
                A("%d. **%s.** %s" % (i, x[0], x[1]))
        elif sec["tipo"] == "test":
            A("Test semanal. Se anota en `seguimiento/tests_semanales.csv`.")
            A("")
            A("- Dolor en reposo: ___  ·  Dolor con tos: ___")
            A("- Squeeze al 50 %: ___  ·  Squeeze máximo: ___")
            A("- Decisión para la semana que viene: subir / mantener / bajar")
        A("")

    A("## 08 · Comidas del día")
    A("")
    A("| Momento | Comida |")
    A("|---------|--------|")
    for m, c in zip(MOMENTOS, NUTRICION[f.weekday()]):
        A("| %s | %s |" % (m, c))
    A("")
    A("Agua 2,5 L · creatina 3-5 g · alcohol no · sueño 8 h · proteína 137 g.")
    A("")
    A("## 09 · Registro de la noche")
    A("")
    A("- Dolor durante la sesión: ___")
    A("- Dolor al acostarte: ___")
    A("- Zona: ___")
    A("- Notas: ___")
    A("")

    if n == b["dias"]:
        A("## Puerta de %s" % b["id"])
        A("")
        A("Último día del bloque. Los criterios que abren el siguiente:")
        A("")
        for c in b["puerta"]:
            A("- [ ] %s" % c)
        A("")
        A("Si falta uno, el bloque se prolonga una semana y todo lo posterior se corre.")
        A("")

    A("---")
    A("")
    if b["id"] != "R1":
        A("*Fecha de previsión: si algún bloque anterior se prolongó, este día se desplaza. "
          "Manda la app, que lo recalcula sola.*")
    A("")
    A("*Bloque %s · día %d de %d. Uso personal, no sustituye valoración médica ni de "
      "fisioterapia. Manda `PROTOCOLO.md`.*" % (b["id"], n, b["dias"]))
    return "\n".join(L) + "\n"


def main():
    dias_dir = os.path.join(RAIZ, "dias")
    os.makedirs(dias_dir, exist_ok=True)
    f = DESDE
    hechos, por_bloque = [], {}
    while f <= HASTA:
        b, n, _, _ = bloque_de(f)
        if b is None:
            raise SystemExit("dia sin bloque: %s" % f)
        nombre = "%s_%sd%02d_%s.md" % (f, b["id"], n, DS[f.weekday()].replace("é", "e"))
        io.open(os.path.join(dias_dir, nombre), "w", encoding="utf-8",
                newline="\n").write(md_dia(f))
        hechos.append(nombre)
        por_bloque[b["id"]] = por_bloque.get(b["id"], 0) + 1
        f += dt.timedelta(days=1)

    print("%d hojas escritas en dias/" % len(hechos))
    for k in sorted(por_bloque):
        print("  %s: %d días" % (k, por_bloque[k]))
    return hechos


if __name__ == "__main__":
    main()
