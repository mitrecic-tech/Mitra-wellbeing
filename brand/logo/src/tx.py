import functools, math, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
FD=os.environ.get('FONT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts'))
F={'manrope':'Manrope.ttf','fraunces':'Fraunces.ttf','barlowi':'BarlowCEBI.ttf','barlow':'BarlowCB.ttf','dafoe':'MrDafoe.ttf','outfit':'Outfit.ttf'}
@functools.lru_cache(None)
def font(name, axes=()):
    f=TTFont(os.path.join(FD,F[name]))
    if 'fvar' in f:
        f=instantiateVariableFont(f, dict(axes) if axes else {a.axisTag:a.defaultValue for a in f['fvar'].axes})
    return f
def text(name, s, size, tracking=0, axes=(), x=0, y=0, anchor='start', fill='#000'):
    f=font(name, tuple(sorted(axes.items())) if isinstance(axes,dict) else axes); gs=f.getGlyphSet(); cmap=f.getBestCmap(); k=size/f['head'].unitsPerEm
    names=[cmap[ord(c)] for c in s]; w=sum(gs[n].width*k for n in names)+tracking*size*(len(names)-1)
    x0 = x - (w/2 if anchor=='middle' else w if anchor=='end' else 0)
    pen=SVGPathPen(gs); cx=x0
    for n in names:
        gs[n].draw(TransformPen(pen,(k,0,0,-k,cx,y))); cx+=gs[n].width*k+tracking*size
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>', w
def text_on_circle(name, s, size, cx, cy, r, start_deg, tracking=0, axes=(), fill='#000'):
    f=font(name, tuple(sorted(axes.items())) if isinstance(axes,dict) else axes); gs=f.getGlyphSet(); cmap=f.getBestCmap(); k=size/f['head'].unitsPerEm
    out=[]; ang=math.radians(start_deg)
    for c in s:
        n=cmap[ord(c)]; adv=gs[n].width*k
        mid=ang+ (adv/2)/r
        px=cx+r*math.sin(mid); py=cy-r*math.cos(mid)
        pen=SVGPathPen(gs); gs[n].draw(TransformPen(pen,(k,0,0,-k,-adv/2,0)))
        out.append(f'<path transform="translate({px:.2f},{py:.2f}) rotate({math.degrees(mid):.2f})" d="{pen.getCommands()}" fill="{fill}"/>')
        ang+=(adv+tracking*size)/r
    return ''.join(out), ang

def arc_text(name, s, size, cx, cy, r, center_deg, tracking=0, axes=(), fill='#000', bottom=False):
    """Text centred on an arc. Top: reads clockwise, glyphs upright outward. Bottom: reads left-to-right along the bottom."""
    f=font(name, tuple(sorted(axes.items())) if isinstance(axes,dict) else axes); gs=f.getGlyphSet(); cmap=f.getBestCmap(); k=size/f['head'].unitsPerEm
    names=[cmap[ord(c)] for c in s]; advs=[gs[n].width*k for n in names]
    total=(sum(advs)+tracking*size*(len(names)-1))/r
    out=[]; c0=math.radians(center_deg)
    ang = c0-total/2 if not bottom else c0+total/2
    for n,adv in zip(names,advs):
        da=(adv/2)/r
        mid = ang+da if not bottom else ang-da
        px=cx+r*math.sin(mid); py=cy-r*math.cos(mid)
        rot=math.degrees(mid)+(180 if bottom else 0)
        pen=SVGPathPen(gs); gs[n].draw(TransformPen(pen,(k,0,0,-k,-adv/2,0)))
        out.append(f'<path transform="translate({px:.2f},{py:.2f}) rotate({rot:.2f})" d="{pen.getCommands()}" fill="{fill}"/>')
        step=(adv+tracking*size)/r
        ang = ang+step if not bottom else ang-step
    return ''.join(out)
