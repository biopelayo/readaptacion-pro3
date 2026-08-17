# readaptacion-pro3

Plan de readaptación tras dolor inguino-púbico (pubalgia atlética sin hernia) y la app móvil que lo ejecuta. Repositorio privado, de uso personal.

## Qué hay aquí

```
app/                 la aplicación
  index.html         un solo archivo, 1,5 MB, sin dependencias ni red
  test.html          banco de 50 pruebas de la lógica
  manifest.json      para instalarla en el móvil
  sw.js              funcionamiento sin conexión
  icon-192/512.png   icono
  COMO_USARLA.md     cómo pasarla al teléfono
src/                 generadores en Python
  mk_app.py          ensambla la app entera
  plan_data.py       los cinco bloques, microciclos y nutrición
  fichas.py          texto de las 35 fichas de ejercicio
  mk_manual.py       genera el manual imprimible
  mk_icon.py         genera el icono
imagenes/web/        las 35 ilustraciones, 1000 px, 2 MB
dias/                hojas diarias imprimibles en A4
docs/                protocolo, plan de bloques, calendario y demás
```

## La app

Abre por el día de hoy, calcula en qué bloque estás y compone la sesión. Lo primero que pide es el dolor de la mañana, y de ahí sale el resto de la pantalla.

| Dolor | Qué muestra |
|-------|-------------|
| 0-1 | Sesión completa |
| 2 | Sesión completa con el isométrico en su escalón |
| 3 | Sin gimnasio ni campo: movilidad, isométrico bajado 20 puntos, agua y aparatos |
| 4 o más | Sesión suspendida, movilidad muy suave y aviso de llamar al fisio |

Marcas lo que vas haciendo, anotas las cargas del gimnasio (recuerda la de la semana pasada), llevas cronómetro para los isométricos y todo se guarda en el propio teléfono. La pestaña Datos exporta a CSV con el esquema de `seguimiento/dolor_24h.csv`.

Si una puerta no se abre, prolongas ese bloque una semana y los cuatro siguientes se recolocan solos, sin dejar huecos en el calendario.

## Reconstruir la app

```bash
python src/mk_app.py
```

Lee `plan_data.py`, `fichas.py` y `imagenes/web/`, y escribe `app/index.html` con todo embebido.

## Pruebas

Abre `app/test.html` en un navegador. Ejecuta 50 comprobaciones sobre la lógica real de la app: fechas, límites de bloque, adaptación por dolor, progresión del isométrico, prolongación de bloques, tracker, integridad del catálogo y que no haya claves ni llamadas a servidores.

## Aviso

Documento operativo de uso personal. No sustituye valoración médica ni de fisioterapia. Manda `docs/PROTOCOLO.md`, y por encima de él, el criterio del fisioterapeuta y del médico.
