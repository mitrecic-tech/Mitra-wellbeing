import os, sys
from typo import text_path, font
NAVY="#0B1F33"; GOLD="#BFA46A"; CREAM="#F7F3EA"
OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)

# ---------- marks (120 x 120 grid) ----------
def m_prijatelji(fg, acc):
    return (f'<path d="M15 106 L38 60 L60 98" fill="none" stroke="{fg}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M60 98 L82 60 L105 106" fill="none" stroke="{acc}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="38" cy="34" r="11" fill="{fg}"/><circle cx="82" cy="34" r="11" fill="{acc}"/>')
def m_ritam(fg, acc):
    return (f'<path d="M16 104 V72 A14 14 0 0 1 44 72 V104 M44 72 V56 A17 17 0 0 1 78 56 V104" fill="none" stroke="{fg}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="98" cy="34" r="10" fill="{acc}"/>')
def m_rijec(fg, acc):
    d,w,c=text_path('M',800,100)
    s=80/w
    return f'<g transform="translate(8,{66+c*s/2:.2f}) scale({s:.4f})"><path d="{d}" fill="{fg}"/></g><circle cx="102" cy="26" r="10" fill="{acc}"/>'

# ---------- wordmarks: return (svg, width, height) with top at y=0 ----------
def wm_caps(fg, sub, acc):
    d1,w1,c1=text_path('MITRA',800,100,0.06)
    lo,hi=0,2
    for _ in range(40):
        t=(lo+hi)/2; _,w2,_=text_path('WELLBEING',600,30,t); lo,hi=(t,hi) if w2<w1 else (lo,t)
    d2,w2,c2=text_path('WELLBEING',600,30,t); gap=24
    return (f'<path transform="translate(0,{c1:.2f})" d="{d1}" fill="{fg}"/><path transform="translate(0,{c1+gap+c2:.2f})" d="{d2}" fill="{sub}"/>', w1, c1+gap+c2)
def wm_lower(fg, sub, acc):
    f=font(700); xh=f['OS/2'].sxHeight*100/f['head'].unitsPerEm
    asc=f['OS/2'].sCapHeight*100/f['head'].unitsPerEm*1.04
    d1,w1,_=text_path('mitra',700,100,-0.01); d2,w2,_=text_path('wellbeing',400,100,-0.01)
    sp=26
    return (f'<path transform="translate(0,{asc:.2f})" d="{d1}" fill="{fg}"/><path transform="translate({w1+sp:.2f},{asc:.2f})" d="{d2}" fill="{sub}"/>', w1+sp+w2, asc)
def wm_dot(fg, sub, acc):
    # MITRA where the I carries a gold dot: a person standing in the name
    dm,wm,c=text_path('M',800,100); di,wi,_=text_path('I',800,100); dr,wr,_=text_path('TRA',800,100,0.06)
    tr=0.06*100; xI=wm+tr; xT=xI+wi+tr
    # find I stem centre from glyph bounds
    from fontTools.pens.boundsPen import BoundsPen
    f=font(800); gs=f.getGlyphSet(); bp=BoundsPen(gs); gs['I'].draw(bp); s=100/f['head'].unitsPerEm
    cxI=xI+(bp.bounds[0]+bp.bounds[2])/2*s; r=(bp.bounds[2]-bp.bounds[0])*s*0.78
    top=2*r+12
    d2,w2,c2=text_path('WELLBEING',600,30,0)
    W=xT+wr
    lo,hi=0,2
    for _ in range(40):
        t=(lo+hi)/2; _,w2,_=text_path('WELLBEING',600,30,t); lo,hi=(t,hi) if w2<W else (lo,t)
    d2,w2,c2=text_path('WELLBEING',600,30,t); gap=24
    y=top+c
    svg=(f'<circle cx="{cxI:.2f}" cy="{r:.2f}" r="{r:.2f}" fill="{acc}"/>'
         f'<g transform="translate(0,{y:.2f})" fill="{fg}"><path d="{dm}"/><path transform="translate({xI:.2f},0)" d="{di}"/><path transform="translate({xT:.2f},0)" d="{dr}"/></g>'
         f'<path transform="translate(0,{y+gap+c2:.2f})" d="{d2}" fill="{sub}"/>')
    return svg, W, y+gap+c2

C={'prijatelji':(m_prijatelji,wm_caps),'ritam':(m_ritam,wm_lower),'rijec':(m_rijec,wm_dot)}

def doc(w,h,body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="MITRA Wellbeing">'
            f'<title>MITRA Wellbeing</title>{body}</svg>\n')

for k,(mk,wmf) in C.items():
    for theme in ('light','inverse'):
        fg,acc,sub = (NAVY,GOLD,NAVY) if theme=='light' else (CREAM,GOLD,GOLD)
        if k=='ritam': sub = '#5B6470' if theme=='light' else '#C9C3B4'
        sx='' if theme=='light' else '-inverse'; base=f'{OUT}/mitra-{k}'
        m=mk(fg,acc); tb,tw,th=wmf(fg,sub,acc); pad=12
        if k=='rijec':
            open(f'{base}-logotip{sx}.svg','w').write(doc(tw+2*pad,th+2*pad,f'<g transform="translate({pad},{pad})">{tb}</g>'))
        else:
            mh = th*1.25 if k=='prijatelji' else th*2.1
            s=mh/120; gap=mh*0.30; H=mh+2*pad; ty=pad+(mh-th)/2 + (th*0.18 if k=='ritam' else 0)
            body=f'<g transform="translate({pad},{pad}) scale({s:.4f})">{m}</g><g transform="translate({pad+mh+gap:.2f},{ty:.2f})">{tb}</g>'
            open(f'{base}-horizontalni{sx}.svg','w').write(doc(pad*2+mh+gap+tw,H,body))
            if k=='prijatelji':
                ms=200; W=max(tw,ms)+2*pad
                body=f'<g transform="translate({(W-ms)/2:.2f},{pad}) scale({ms/120:.4f})">{m}</g><g transform="translate({(W-tw)/2:.2f},{pad+ms+36})">{tb}</g>'
                open(f'{base}-vertikalni{sx}.svg','w').write(doc(W,pad*2+ms+36+th,body))
        open(f'{base}-znak{sx}.svg','w').write(doc(136,136,f'<g transform="translate(8,8)">{m}</g>'))
    open(f'{OUT}/mitra-{k}-ikona.svg','w').write(doc(512,512,f'<rect width="512" height="512" rx="112" fill="{NAVY}"/><g transform="translate(96,96) scale({320/120:.4f})">{mk(CREAM,GOLD)}</g>'))
print(sorted(os.listdir(OUT)))
