"""Genera en/index.html a partir de index.html.

index.html es la unica fuente: lleva los pares data-es/data-en y de ahi sale
la version inglesa. Editar en/index.html a mano no sirve de nada, se pisa.
"""
import html
import re
from pathlib import Path

RAIZ = Path(__file__).parent
ORIGEN = RAIZ / "index.html"
DESTINO = RAIZ / "en" / "index.html"

# atributo -> (valor en espanol, valor en ingles)
CABECERA = {
    "description": (
        "Information &amp; Data Security Manager en BBVA. Clasificación de la información, "
        "DLP, infraestructura self-hosted y desarrollo. Madrid.",
        "Information &amp; Data Security Manager at BBVA. Information classification, DLP, "
        "self-hosted infrastructure and development. Madrid.",
    ),
    "og:description": (
        "Information & Data Security Manager en BBVA. Clasificación de la información, "
        "DLP, infraestructura self-hosted y desarrollo. Madrid.",
        "Information & Data Security Manager at BBVA. Information classification, DLP, "
        "self-hosted infrastructure and development. Madrid.",
    ),
    "og:locale": ("es_ES", "en_US"),
    "og:locale:alternate": ("en_US", "es_ES"),
    "og:url": ("https://andres.ciencre.xyz/", "https://andres.ciencre.xyz/en/"),
}

ETIQUETA = re.compile(r'<(?P<tag>[a-zA-Z][\w-]*)(?P<attrs>(?:"[^"]*"|\'[^\']*\'|[^>"\'])*)>')
TRADUCIBLE = re.compile(r'\bdata-(?:es|en)="[^"]*"')
APOSTROFO_RECTO = re.compile(r"(?<=[A-Za-z])'(?=[A-Za-z])")


def revisar_apostrofos(doc: str) -> None:
    """El texto lleva apostrofo tipografico; el recto solo delimita atributos.

    Solo mira dentro de data-es/data-en: es donde vive todo el texto, y asi el
    recto de sitios como el data URI del favicon queda fuera de tiro.
    """
    fallos = []
    for atributo in TRADUCIBLE.finditer(doc):
        for apostrofo in APOSTROFO_RECTO.finditer(atributo.group(0)):
            i = atributo.start() + apostrofo.start()
            linea = doc[:i].count("\n") + 1
            fallos.append(f"  linea {linea}: ...{doc[i - 25:i + 15]}...")
    assert not fallos, "apostrofo recto en texto, usa ’ (U+2019):\n" + "\n".join(fallos)


def volcar_ingles(doc: str) -> str:
    """Sustituye el contenido de cada elemento con data-en por su version inglesa."""
    trozos, cursor = [], 0
    for m in ETIQUETA.finditer(doc):
        if m.start() < cursor:
            continue
        en = re.search(r'\bdata-en="([^"]*)"', m.group("attrs"))
        if not en:
            continue
        cierre = doc.find(f'</{m.group("tag")}>', m.end())
        if cierre == -1 or "<" in doc[m.end():cierre]:
            continue  # invariante: los nodos traducibles son solo texto
        trozos.append(doc[cursor:m.end()])
        trozos.append(html.unescape(en.group(1)).replace("&", "&amp;").replace("<", "&lt;"))
        cursor = cierre
    trozos.append(doc[cursor:])
    return "".join(trozos)


def main() -> None:
    doc = ORIGEN.read_text()

    revisar_apostrofos(doc)

    doc = volcar_ingles(doc)

    doc = doc.replace('<html lang="es">', '<html lang="en">', 1)

    for clave, (es, en) in CABECERA.items():
        atributo = "property" if clave.startswith("og:") else "name"
        antes = f'<meta {atributo}="{clave}" content="{es}">'
        assert doc.count(antes) == 1, f"no encuentro {clave} en la cabecera"
        doc = doc.replace(antes, f'<meta {atributo}="{clave}" content="{en}">')

    doc = doc.replace(
        '<link rel="canonical" href="https://andres.ciencre.xyz/">',
        '<link rel="canonical" href="https://andres.ciencre.xyz/en/">', 1)

    doc = re.sub(
        r'<a class="lang" id="lang-toggle" href="[^"]*" hreflang="en" aria-label="[^"]*">',
        '<a class="lang" id="lang-toggle" href="/" hreflang="es" aria-label="Cambiar a español">',
        doc, count=1)
    doc = doc.replace('<span class="lang-opt on" data-lang="es">ES</span>',
                      '<span class="lang-opt" data-lang="es">ES</span>', 1)
    doc = doc.replace('<span class="lang-opt" data-lang="en">EN</span>',
                      '<span class="lang-opt on" data-lang="en">EN</span>', 1)

    doc = doc.replace('aria-label="Abrir menú"', 'aria-label="Open menu"', 1)
    doc = doc.replace('aria-label="Volver arriba"', 'aria-label="Back to top"', 1)

    DESTINO.parent.mkdir(exist_ok=True)
    DESTINO.write_text(doc)
    print(f"escrito {DESTINO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
