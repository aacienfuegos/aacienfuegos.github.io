"""Instancia estaticas desde las variables del sitio: Skia rasteriza a Type 3
cualquier fuente variable, y eso rompe la extraccion de texto en varios ATS."""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

SRC = Path(sys.argv[1])
DST = Path(sys.argv[2])
DST.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("karla-400-lat.ttf", "Karla CV", 400, "Regular"),
    ("karla-400-lat.ttf", "Karla CV", 500, "Medium"),
    ("karla-400-lat.ttf", "Karla CV", 600, "SemiBold"),
    ("fraunces-300-700-lat.ttf", "Fraunces CV", 600, "SemiBold"),
    ("jetbrains-mono-400-lat.ttf", "JetBrains Mono CV", 500, "Medium"),
]

for src, family, weight, style in TARGETS:
    font = TTFont(SRC / src)
    axes = {a.axisTag: a.defaultValue for a in font["fvar"].axes}
    axes["wght"] = weight
    instantiateVariableFont(font, axes, inplace=True, updateFontNames=False)
    ps = f"{family}-{style}".replace(" ", "")
    name = font["name"]
    for nid, value in (
        (1, family if style == "Regular" else f"{family} {style}"),
        (2, "Regular"),
        (3, ps),
        (4, f"{family} {style}"),
        (6, ps),
        (16, family),
        (17, style),
    ):
        name.setName(value, nid, 3, 1, 0x409)
    font["OS/2"].usWeightClass = weight
    font.save(DST / f"{ps}.ttf")
    print(f"{ps}.ttf")
