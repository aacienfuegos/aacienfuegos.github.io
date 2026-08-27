# Sitio personal — andres.ciencre.xyz

HTML, CSS y JS a mano, sin frameworks ni dependencias. GitHub Pages sirve
`master` tal cual: **lo commiteado es lo publicado**, no hay CI ni build en
el servidor.

## Builds

| Si tocas | Lanza | Tarda |
|---|---|---|
| `index.html` | `bash build.sh` | 32 ms |
| `cv/index.html` o `cv/cv.css` | `bash cv/build.sh` | 2,7 s |

`build.sh` **no** regenera el CV: chromium le estampa la hora al PDF, asi que
hacerlo en cada cambio del sitio ensuciaba `assets/` con bytes distintos y el
mismo contenido. Si tocas el CV y no lanzas `cv/build.sh`, el PDF que se
descarga de la web se queda atras.

## Invariantes

- `index.html` es la unica fuente. `en/index.html` se genera y **no se edita a
  mano**: cualquier cambio ahi se pisa en el siguiente build.
- El texto bilingue vive en `data-es` / `data-en` sobre nodos de solo texto.
- El ingles usa apostrofo tipografico `’` (U+2019). `build-en.py` aborta si se
  cuela uno recto dentro de un `data-*`.
- `assets/*.pdf` son los dos PDF que publica la web (las versiones largas).
  `cv/dist/` es el taller: cuatro variantes, en `.gitignore`, no se publica.

## Git

Este repo **no** sigue el flujo `feat/ -> develop -> main` de las reglas
globales: aqui solo existe `master`, y es lo que Pages publica. Rama
`tipo/nombre` desde `master`, PR y squash merge.

Cuando cambia el CV, los PDF de `assets/` entran en el mismo commit que el
fuente: son artefactos, pero versionados es la unica forma de publicarlos.

## Herramientas

`cv/build.sh` necesita `chromium`, `qpdf` y `uv` (que se trae `fonttools` para
subsetear las fuentes la primera vez). El sitio no tiene tests, linter ni
gestor de paquetes: para verlo, `python3 -m http.server` y abrir el navegador.

## Ojo

Todo lo que se commitea en la raiz queda accesible en el dominio, incluidos
`build.sh` y `build-en.py`. Los dotfiles no (Jekyll los ignora).
