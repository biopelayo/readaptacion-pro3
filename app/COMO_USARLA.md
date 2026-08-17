# Cómo llevar la app al móvil

El archivo es `app/index.html`. Pesa 1,5 MB y lo lleva todo dentro: el plan de los cinco bloques, las 35 fichas ilustradas y el código. No necesita internet ni instalar nada.

## Pasarla al teléfono

**Por Google Drive, que es lo más cómodo.** Sube `index.html` a tu Drive, ábrelo desde la app de Drive en el móvil y elige «Abrir con Chrome». Una vez abierto, menú de Chrome, «Añadir a pantalla de inicio». A partir de ahí la abres con un icono como cualquier app.

**Por WhatsApp a ti mismo.** Envíatelo al chat contigo, descárgalo en el teléfono y ábrelo con Chrome desde la carpeta de descargas.

**Por cable.** Copia el archivo a la carpeta Descargas del teléfono y ábrelo con Chrome.

**Aviso para iPhone:** Safari no abre archivos HTML locales con la misma facilidad. En iPhone funciona mejor guardándolo en Archivos y abriéndolo desde ahí, o pasando a la fase 2.

## Fase 2, si quieres que sea una app de verdad

Publicando el archivo con un `manifest.json` y un service worker queda instalable, a pantalla completa, con icono propio y actualizándose sola. Eso implica ponerlo en una URL. Como el contenido incluye tu diagnóstico y tu registro de dolor, la decisión es tuya:

- **GitHub Pages público:** gratis y a mano desde cualquier sitio, pero cualquiera con la URL lo ve.
- **Repositorio privado con despliegue restringido:** más pasos, pero solo tú entras.
- **Quedarse en archivo local:** cero exposición, a cambio de pasarlo a mano cuando cambie.

Dime cuál prefieres y lo monto.

## Qué hace

**Abre por el día de hoy.** Coge la fecha del propio teléfono, calcula en qué bloque estás y compone la sesión que toca.

**Lo primero es el dolor de la mañana.** Toca el número antes de levantarte. De ahí sale todo lo demás:

| Dolor | Qué hace la app |
|-------|-----------------|
| 0-1 | Sesión completa tal como está escrita |
| 2 | Sesión completa, con el isométrico en su escalón |
| 3 | Quita el gimnasio y el campo. Deja movilidad, isométricos bajados 20 puntos, agua y aparatos |
| 4 o más | Suspende la sesión, deja solo movilidad muy suave y te dice que llames al fisio |

**Marca lo que vas haciendo.** Cada ejercicio tiene su casilla. Las comidas también.

**El isométrico sube solo.** Del 50 al 80 % según el día del bloque, con la progresión escrita en el plan.

**Toca el nombre de un ejercicio** y saltas a su ficha en el manual, con foto, pasos y error frecuente.

**Se guarda solo.** No hay botón de guardar. Los datos viven en tu teléfono, en el almacenamiento del navegador. Nadie más los ve.

**Exporta en la pestaña Datos.** El CSV sale con el formato exacto de `seguimiento/dolor_24h.csv`, así que se copia directo al proyecto y se le puede enseñar al fisio.

**Si una puerta no se abre**, en la pestaña Semana pulsas «El bloque necesita una semana más» y todas las fechas de los bloques siguientes se recalculan solas. Es lo que hace que el plan avance por función y no por calendario.

## Lo que no hace

No decide por encima del `PROTOCOLO.md`, no diagnostica y no sustituye a tu fisioterapeuta ni a tu médico. La pantalla de cada día termina con las señales de alarma del artículo 2: si aparece cualquiera, se para y se consulta.

## Detalle técnico que conviene saber

Los datos se guardan en el almacenamiento local del navegador con el que la abras. Si borras los datos de navegación de Chrome, **se pierden**. Por eso conviene exportar la copia de seguridad de vez en cuando, sobre todo los domingos al rellenar el test semanal.
