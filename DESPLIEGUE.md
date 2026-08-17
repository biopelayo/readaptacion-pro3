# Desplegar la app en Cloudflare Pages

Todo está preparado. Falta lo único que no puedo hacer por ti: autenticarte en Cloudflare, que abre el navegador y pide tu contraseña.

## Antes de empezar

**El repositorio se queda privado.** Cloudflare Pages despliega igual de bien desde un repo privado que desde una carpeta suelta, así que hacerlo público no aporta nada y sí expondría tu diagnóstico, tu registro de dolor y las ilustraciones con tu cara.

**La URL de Pages es pública mientras no actives el acceso restringido.** Será algo tipo `readaptacion-pro3.pages.dev`: nadie la adivina, pero cualquiera que la tenga entra. Por eso el paso 3 no es opcional. Mientras tanto, el archivo `deploy/_headers` ya manda `noindex` para que no aparezca en buscadores.

## Paso 1 · Autenticarte

Desde la carpeta del proyecto:

```bash
npx wrangler login
```

Se abre el navegador, entras en tu cuenta de Cloudflare y le das permiso. Si no tienes cuenta, se crea gratis en el momento. Vuelve aquí cuando termine y sigo yo.

## Paso 2 · Desplegar

```bash
npx wrangler pages deploy deploy --project-name=readaptacion-pro3 --commit-dirty=true
```

Sube 1,6 MB y devuelve la URL. La primera vez pregunta si crear el proyecto: sí, y rama de producción `main`.

## Paso 3 · Cerrar el acceso (importante)

En el panel de Cloudflare, **Zero Trust → Access → Applications → Add an application → Self-hosted**:

- Nombre: `Readaptación`
- Dominio: `readaptacion-pro3.pages.dev`
- Política: *Allow*, regla **Emails** con `bio.pelayo@gmail.com`

Con eso, entrar exige un código de un solo uso que llega a tu correo. El plan gratuito de Zero Trust cubre hasta cincuenta usuarios, así que para uno sobra.

Aviso práctico: en el móvil, el código por correo se pide cada cierto tiempo. Si te resulta pesado, sube la duración de la sesión en la política a un mes.

## Paso 4 · Instalarla en el móvil

Abre la URL en Chrome, menú, «Instalar aplicación». Queda con icono propio, a pantalla completa y funcionando sin cobertura gracias al service worker.

## Actualizar la app más adelante

```bash
python src/mk_app.py
cp app/index.html app/manifest.json app/sw.js app/icon-*.png deploy/
npx wrangler pages deploy deploy --project-name=readaptacion-pro3 --commit-dirty=true
```

El service worker va primero a la red, así que la versión nueva entra sola en cuanto abras la app con cobertura.

## Si prefieres no depender de Cloudflare

El archivo `app/index.html` sigue funcionando solo, pasado al teléfono por Drive o WhatsApp. Pierdes la instalación como aplicación y la actualización automática, nada más. Está explicado en `app/COMO_USARLA.md`.
