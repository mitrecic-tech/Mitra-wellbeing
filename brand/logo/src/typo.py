from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import functools
import os
SRC=os.environ.get('MANROPE_TTF','Manrope[wght].ttf')
@functools.lru_cache(None)
def font(w):
    return instantiateVariableFont(TTFont(SRC), {'wght':w})
def text_path(text, weight, size, tracking=0.0):
    """Return (svg path d, width, cap height) for text at given px size; tracking in em."""
    f=font(weight); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    s=size/upm; pen=SVGPathPen(gs); x=0; names=[cmap[ord(c)] for c in text]
    for i,n in enumerate(names):
        tp=TransformPen(pen,(s,0,0,-s,x,0)); gs[n].draw(tp)
        x+=gs[n].width*s + (tracking*size if i<len(names)-1 else 0)
    cap=f['OS/2'].sCapHeight*s
    return pen.getCommands(), x, cap
