# Sitio personal — andres.ciencre.xyz

HTML, CSS y JS a mano, sin frameworks ni dependencias. GitHub Pages sirve
`master` tal cual: **lo commiteado es lo publicado**, no hay CI ni build en
el servidor.

## Builds

| Si tocas | Lanza | Tarda |
|---|---|---|
| `index.html` | `bash build.sh` | 32 ms |
| `cv/index.html` o `cv/cv.css` | `bash cv/build.sh` | 2,7 s |

`cv/index.html` sirve las cuatro variantes desde un solo fuente, elegidas por
query string: `?lang=es|en&len=short|long`. Para verlas en el navegador sin
generar PDF, levanta el server y abre
`localhost:8000/cv/?lang=en&len=long`.

`build.sh` **no** regenera el CV: chromium le estampa la hora al PDF, asi que
hacerlo en cada cambio del sitio ensuciaba `assets/` con bytes distintos y el
mismo contenido. Si tocas el CV y no lanzas `cv/build.sh`, el PDF que se
descarga de la web se queda atras.

## Invariantes

- `index.html` es la unica fuente. `en/index.html` se genera y **no se edita a
  mano**: cualquier cambio ahi se pisa en el siguiente build.
- El texto bilingue vive en `data-es` / `data-en` sobre nodos de **solo
  texto**. Si metes una etiqueta hija (`<strong>`, `<a>`) dentro de un nodo
  traducible, `build-en.py` lo salta **en silencio** y ese parrafo se queda en
  espanol en `/en/`. Parte el nodo en dos en lugar de anidar.
- La cabecera inglesa (`description`, `og:*`, canonical) esta duplicada en el
  dict `CABECERA` de `build-en.py`. Si tocas esos meta en `index.html`, el
  build aborta hasta que actualices el dict. Falla ruidoso, a proposito.
- El ingles usa apostrofo tipografico `’` (U+2019). `build-en.py` aborta si se
  cuela uno recto dentro de un `data-*`.
- `assets/*.pdf` son los dos PDF que publica la web (las versiones largas).
  `cv/dist/` es el taller: cuatro variantes, en `.gitignore`, no se publica.

## El CV: que entra y que no

Lo miran personas y ATS, y va centrado en **experiencia, estudios y
certificaciones**. Homelab y proyectos dan color al perfil, pero no son el
argumento de contratacion: van al final y solo en la version larga.

- **Del puesto en BBVA**, por defecto solo funcion y vocabulario de sector
  (clasificacion de la informacion, DLP, gobierno del dato). Un proyecto
  interno se puede describir en generico si aporta de verdad, pero **nunca**
  nombres propios de proyecto o de herramienta interna, ni cifras del banco.
- **Cifras solo las que se sostienen en una entrevista.** Si no hay un numero
  real, se describe el alcance ("para toda la plantilla", "en tres
  geografias"). Un agente no estima, no redondea y no se saca un porcentaje
  porque quede mejor.
- **Fuera siempre**: telefono, foto, fecha de nacimiento o edad, y direccion.
  La ubicacion es "Madrid"; el contacto, email y LinkedIn.
- ACCIONA es una linea, y se queda en una linea.
- En Formacion academica, solo titulacion reglada.
- Descripciones de puesto cortas. Cinco bullets por trabajo cansan, y el CV no
  mejora por ser mas largo.

## Tono

Ni en la web ni en el CV entra el registro marca personal: la frase ingeniosa
que busca aplauso, el adjetivo de venta ("apasionado", "proactivo"), ni
definir lo propio por comparacion con lo que hacen otros. Se dice lo que hay,
en llano.

Dentro de eso, la web admite algo mas de voz. El **CV es mas informativo**:
cabe un punto de informalidad, pero bastante menos que la web.

Los terminos tecnicos en ingles del sector (DLP, compliance, threat modeling)
son vocabulario, no relleno. El relleno es "sinergias", "transversal", "360".

## Las fuentes del CV

`cv/mkfonts.py` **no** subsetea: instancia estaticas desde las variables de
`cv/fonts/` y las renombra a `Karla CV`, `Fraunces CV`, `JetBrains Mono CV`.
Existe por un motivo concreto: **Skia rasteriza a Type 3 cualquier fuente
variable**, y de un PDF con Type 3 varios ATS no extraen texto. Con estaticas
salen CID TrueType y el texto se lee. El subset ya lo hace chromium al
imprimir.

Por eso el CSS del CV pide las familias `* CV` y no las del sitio. Si alguna
vez cambias las fuentes, la comprobacion es:

```
pdffonts assets/CV_Andres_AlvarezDeCienfuegos.pdf   # ni un Type 3
pdftotext assets/CV_Andres_AlvarezDeCienfuegos.pdf - | head
```

## Git

Este repo **no** sigue el flujo `feat/ -> develop -> main` de las reglas
globales: aqui solo existe `master`, y es lo que Pages publica. Rama
`tipo/nombre` desde `master`, PR y squash merge.

Cuando cambia el CV, los PDF de `assets/` entran en el mismo commit que el
fuente: son artefactos, pero versionados es la unica forma de publicarlos.

## Herramientas

`cv/build.sh` necesita `chromium`, `qpdf` y `uv` (que se trae `fonttools` para
generar las estaticas la primera vez, ver arriba). El sitio no tiene tests, linter ni
gestor de paquetes: para verlo, `python3 -m http.server` y abrir el navegador.

## Ojo

`.menu-btn`, `.menu` y `.to-top` nacen en `display:none` y solo los enciende
el **ultimo** `@media (max-width:640px)` de `style.css`. Misma especificidad,
asi que gana el que va despues: cualquier regla movil nueva va en ese bloque
final o debajo, nunca antes.

`CNAME` es el que apunta el dominio a Pages. Borrarlo tira
`andres.ciencre.xyz`.

Todo lo que se commitea en la raiz queda accesible en el dominio, incluidos
`build.sh` y `build-en.py`. Los dotfiles no (Jekyll los ignora).
