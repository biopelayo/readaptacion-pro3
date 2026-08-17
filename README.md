# readaptacion_oviedo_2026

Sede única del plan de readaptación futbolística de Pelayo hasta **1 de septiembre de 2026**. Basada en dos documentos fuente (ambos en `fuentes/`):

1. **Manual Pro 3.0 · Real Oviedo Edition** — 10 páginas visuales que estructuran el plan en 5 fases, 10 semanas, con gimnasio A/B/C/D, upper body, nutrición mensual y menú semanal.
2. **Informe de readaptación · pubalgia sin hernia** — 19 páginas técnicas con criterios clínicos, biblioteca de ejercicios detallada, tests semanales y checklist antes de competir.

Los dos documentos están alineados: mismo diagnóstico (dolor inguino-púbico / pubalgia atlética sin hernia), misma fecha de inicio (23 jun 2026), mismo objetivo (llegar a septiembre compitiendo sin reacción al día siguiente), mismo semáforo del dolor y mismos criterios de progresión.

## Reinicio del 17 de agosto de 2026

Tras diez días sin entrenar y con el dolor todavía en 2-3/10, el plan se reinició. La meta del 1 de septiembre queda retirada y la nueva referencia son minutos de partido en la segunda mitad de octubre. El bloque vigente es **R1 · Descarga y control** y manda `PLAN_REINICIO.md`. El microciclo sin balón está en `microciclo/microciclo_reinicio.md` y la dosificación del fisio en `bloques/fisio.md`.

## La app del móvil

`app/index.html` lleva el plan completo de R1 a R5, compone el día que toca según la fecha y el dolor de esa mañana, permite marcar y registrar, guarda en el propio teléfono y exporta a `seguimiento/dolor_24h.csv`. Instrucciones en `app/COMO_USARLA.md` y decisiones de diseño en `PLAN_APP.md`.

## Cómo se usa

- `ESTADO_HOY.md` — a qué fase toca ir hoy, qué día del microciclo, qué decisión (subir / mantener / bajar).
- `PROTOCOLO.md` — reglas duras que mandan sobre todo: semáforo del dolor, criterios de avance, señales de alarma.
- `PLAN_REINICIO.md` — **bloque vigente**: los cinco tramos R1 a R5 del 17 de agosto al 25 de octubre, con sus puertas por criterio.
- `PLAN_MAESTRO.md` — plan original de 10 semanas con las 5 fases y el cross-mapping entre ambos documentos. Sus fechas están retiradas; su lógica sigue vigente.
- `CALENDARIO.md` — tabla día a día desde hoy hasta el 1 de septiembre.
- `plan/` — ficha detallada de cada una de las 5 fases.
- `microciclo/` — plantilla de semana tipo (lunes a domingo).
- `gimnasio/` — planes A/B/C/D y biblioteca de ejercicios.
- `nutricion/` — reglas, semana modelo, ciclo mensual, lista de compra.
- `seguimiento/` — hojas de tests semanales, dolor 24 h, checklist pre-competición.
- `dias/` — plantilla del día y las hojas diarias generadas.
- `fuentes/` — los dos PDF originales + páginas rasterizadas del manual (image-only).

## Sistema visual de la hoja diaria

Cada día se entrega en dos formatos:

- **Markdown** (`dias/YYYY-MM-DD_*.md`) — fuente editable, versionable.
- **HTML autocontenido** (`dias/YYYY-MM-DD_*.html`) — imprimible en A4 y legible en móvil.

Desde el 17 de agosto de 2026 el HTML replica el lenguaje visual del **Manual Pro 3.0 · Real Oviedo Edition**, que es la fuente del proyecto. La plantilla con todas las piezas y sus instrucciones está en `dias/PLANTILLA_MANUAL.html`.

- **Paleta:** azul marino en degradado `#0A1733 → #060E24` con focos en `#17356F` · oro `#C9A227`, claro `#E3C468`, pálido `#F0DFA8` · texto `#C9D4EA` y apagado `#8C9BBB` · semáforo `#54B37A / #E8B93B / #E2685A`.
- **Tipografía:** condensada de palo seco en versales para titulares (Anton, Archivo Black, Oswald, Haettenschweiler o Arial Narrow según lo que tenga el equipo) + Segoe UI para el cuerpo + IBM Plex Mono para cifras.
- **Piezas:** pastillas de cabecera, sello propio en SVG, tarjetas con hairline dorada, franja roja de lo prohibido, regla del día, semáforo de tres celdas, tira de comidas, banda de siete días y métricas de recuperación invisible.
- **Print:** `@page A4` sin márgenes, tres secciones `.page` de 288 mm, fondo aplicado a `html` para que cubra la hoja entera, `print-color-adjust: exact`.
- **Casillas para rellenar:** siempre con fondo claro `#F6F3E8` sobre el azul, para poder escribir a boli sobre la hoja impresa.
- **Móvil:** el breakpoint es `@media screen and (max-width:820px)`. Tiene que llevar `screen`, porque el ancho de un A4 son 794 px y sin esa palabra la impresión se cae a una sola columna.
- **Sin logos de clubes reales.** El sello es propio.

**Verificación obligatoria antes de dar una hoja por buena:** imprimir a PDF con Chrome headless y contar las páginas con PyMuPDF. El visor de PDF miente y una página que desborda se convierte en dos.

```bash
chrome --headless=new --no-pdf-header-footer --print-to-pdf=check.pdf --virtual-time-budget=5000 file:///ruta/hoja.html
```

## Regla de oro

> No se avanza por calendario, se avanza por función. Cada fase se supera solo si no hay peaje 24 h después.
