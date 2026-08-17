# PLAN · app de readaptación en el móvil

Objetivo: llevar el plan completo en el bolsillo, ver el día que toca, rellenar los datos sobre la marcha y que el propio registro decida la sesión siguiente.

## El problema que resuelve

Hoy el proyecto tiene dos agujeros. El primero es que las hojas diarias son archivos estáticos: hay que pedir cada día y no se pueden rellenar salvo imprimiéndolos. El segundo es que los CSV de seguimiento llevan diez semanas vacíos, y sin registro el semáforo del `PROTOCOLO.md` no manda nada, porque no hay datos que leer.

Una app que se rellena en el momento, en el móvil, cierra los dos.

## Por qué no son 68 archivos

Del 19 de agosto al 25 de octubre hay 68 días. Escribirlos ahora significaría fijar por calendario lo que el protocolo manda decidir por función. La app guarda **la estructura** de los cinco bloques y **compone el día** con tres entradas: la fecha, el bloque en el que estás de verdad y el dolor de esa mañana. Un día generado hoy para el 12 de octubre sería ficción; un día compuesto el 12 de octubre será correcto.

## Qué hace la app

**Vista del día.** Abre siempre por el día de hoy. Muestra el bloque, el día del microciclo, la regla del día y los bloques 01 a 09 con el mismo contenido que las hojas impresas.

**Se adapta al dolor.** Lo primero que pide al abrir es el número de la mañana. Con 0-1 muestra la sesión completa, con 2 la sesión completa con el isométrico un escalón por debajo, con 3 recorta el gimnasio y deja movilidad, agua y aparatos, y con 4 o más deja solo movilidad suave y un aviso de llamar al fisio. No es un texto informativo: la sesión que ves cambia.

**Se rellena.** Cada ejercicio tiene su casilla de hecho y su campo de dolor. Al final del día están los campos de registro nocturno. Todo se guarda solo, sin botón de guardar.

**Guarda sin conexión.** Los datos viven en el almacenamiento del propio navegador del móvil. No hay servidor, no hay cuenta, no hay nadie más que los vea.

**Exporta.** Un botón vuelca todo el histórico a CSV con el formato exacto de `seguimiento/dolor_24h.csv` y a JSON para copia de seguridad. Así el registro acaba en el proyecto y se puede enseñar al fisio.

**Puertas entre bloques.** Al llegar al final de un bloque aparece su checklist de criterios. Solo si se marcan todos se abre el bloque siguiente. Si falta uno, el bloque se prolonga una semana y la app lo recalcula.

**Manual de ejercicios.** Las 35 fichas ilustradas, buscables, con para qué sirve, cómo se hace y el error frecuente. Se abre desde el nombre del ejercicio en la sesión del día.

**Historial.** Gráfico simple de dolor de los últimos treinta días y el cumplimiento de cada semana, para ver la tendencia de un vistazo.

## Cómo se lleva al móvil

**Fase 1, hoy: archivo único.** Un solo `.html` que contiene el plan, el código y las imágenes. Se pasa al teléfono por Drive, WhatsApp o correo, se abre con Chrome y se añade a la pantalla de inicio. Funciona sin conexión y sin instalar nada.

**Fase 2, opcional: aplicación instalable.** Publicando ese archivo con un `manifest.json` y un service worker en GitHub Pages queda como app instalable, con icono propio, pantalla completa y actualizaciones automáticas al abrirla. Requiere decidir antes si el contenido puede estar en una URL pública, porque incluye tu diagnóstico y tu registro de dolor. Alternativa privada: repositorio privado más un despliegue con acceso restringido.

## Arquitectura

Un solo archivo, sin dependencias externas, sin CDN.

```
index.html
├── <style>        el sistema visual del manual, adaptado a pantalla de móvil
├── <script> PLAN  bloques, microciclos, progresiones, puertas y criterios
├── <script> EJER  catálogo de ejercicios con series, notas y ficha
├── <script> IMG   miniaturas en base64
└── <script> APP   composición del día, estado, almacenamiento y exportación
```

**Modelo de datos del registro**, una entrada por día:

```
{ fecha, bloque, dia_bloque, dolor_manana, dolor_durante, dolor_post,
  dolor_acostar, tos, squeeze_50, squeeze_max, zona, isometrico_pct,
  hechos: [ids de ejercicio], notas, fisio, sesion_recortada }
```

## Diseño para el móvil

Una columna, tipografía grande, objetivos táctiles de 44 píxeles como mínimo. Los campos de dolor son botonera de 0 a 10, no teclado. Barra inferior fija con las cuatro secciones: Hoy, Semana, Manual e Historial. Modo oscuro por defecto, que es el del manual y el que menos molesta a las siete de la mañana. Se mantiene la paleta azul marino y oro.

## Fases de trabajo

| Fase | Contenido | Estado |
|------|-----------|--------|
| 1 | Modelo de datos con los cinco bloques y sus microciclos completos | Hecha |
| 2 | Vista del día con adaptación por dolor y registro rellenable | Hecha |
| 3 | Almacenamiento local, exportación a CSV y JSON | Hecha |
| 4 | Manual de ejercicios integrado con las 35 fichas | Hecha |
| 5 | Semana, historial y puertas entre bloques | Hecha |
| 6 | Empaquetado y prueba a 390 y 360 px | Hecha |
| 7 | Prueba en tu móvil real y paso a la pantalla de inicio | Te toca |
| 8 | Opcional: PWA instalable y decisión sobre alojamiento | Pendiente de tu decisión |

Instrucciones de instalación en `app/COMO_USARLA.md`.

## Fallos encontrados al construirla

**Desfase de fechas por zona horaria.** `toISOString()` convierte a UTC, y en horario de verano de España eso resta un día. Como el cálculo del calendario encadena operaciones, el error se acumulaba: la app situaba el miércoles 19 de agosto en viernes y la semana empezaba el 15. Corregido construyendo la fecha ISO en hora local.

**La fecha ya no se fija al generar.** La app toma la del propio teléfono, que es lo único correcto para algo que se abre cada mañana.

**La escala de dolor desbordaba la pantalla.** Once botones con ancho mínimo de 38 píxeles suman más que un móvil, y el desbordamiento arrastraba todo el layout. Resuelto con rejilla de once columnas fluidas.

## Lo que la app no hace

No sustituye al fisioterapeuta ni al médico, no diagnostica y no decide por encima del `PROTOCOLO.md`. Cuando aparezca cualquiera de las señales de alarma del artículo 2, la app deja de proponer sesión y pasa a un aviso único: parar y consultar.
