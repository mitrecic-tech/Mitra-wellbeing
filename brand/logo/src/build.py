import os, sys
from marks import *
from typo import text_path
OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
NAMES={'a':'iskorak','b':'progresija','c':'ciklus'}

def wordblock(fg, sub):
    # MITRA (ExtraBold) over WELLBEING (SemiBold), both justified to the same width
    d1,w1,c1=text_path('MITRA',800,100,0.06)
    # find tracking so WELLBEING matches MITRA width
    lo,hi=0,2
    for _ in range(40):
        t=(lo+hi)/2; _,w2,_=text_path('WELLBEING',600,30,t)
        lo,hi=(t,hi) if w2<w1 else (lo,t)
    d2,w2,c2=text_path('WELLBEING',600,30,t)
    gap=24; h=c1+gap+c2
    svg=(f'<path transform="translate(0,{c1:.2f})" d="{d1}" fill="{fg}"/>'
         f'<path transform="translate(0,{c1+gap+c2:.2f})" d="{d2}" fill="{sub}"/>')
    return svg, w1, h

def svgdoc(w,h,body,bg=None,title='MITRA Wellbeing'):
    r=f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{r}{body}</svg>\n')

def build(k, theme):
    fg,acc,sub,bg = (NAVY,GOLD,NAVY,None) if theme=='light' else (CREAM,GOLD,GOLD,None)
    m=MARKS[k](fg,acc); suffix='' if theme=='light' else '-inverse'
    base=f'{OUT}/mitra-{NAMES[k]}'
    # mark only (120 grid, 8 padding)
    open(f'{base}-znak{suffix}.svg','w').write(svgdoc(136,136,f'<g transform="translate(8,8)">{m}</g>'))
    tb,tw,th=wordblock(fg,sub)
    # horizontal: mark height = text block height
    pad=12; s=th/120*1.18; mh=120*s; H=mh+2*pad; gap=mh*0.32
    ty=pad+(mh-th)/2
    body=f'<g transform="translate({pad},{pad}) scale({s:.4f})">{m}</g><g transform="translate({pad+mh+gap:.2f},{ty:.2f})">{tb}</g>'
    open(f'{base}-horizontalni{suffix}.svg','w').write(svgdoc(pad*2+mh+gap+tw,H,body))
    # stacked
    ms=200; W=max(tw,ms)+2*pad; mx=(W-ms)/2
    body=f'<g transform="translate({mx:.2f},{pad}) scale({ms/120:.4f})">{m}</g><g transform="translate({(W-tw)/2:.2f},{pad+ms+40})">{tb}</g>'
    open(f'{base}-vertikalni{suffix}.svg','w').write(svgdoc(W,pad*2+ms+40+th,body))
    # app icon / favicon: rounded navy square with inverse mark
    if theme=='light':
        mi=MARKS[k](CREAM,GOLD)
        open(f'{base}-ikona.svg','w').write(svgdoc(512,512,f'<rect width="512" height="512" rx="112" fill="{NAVY}"/><g transform="translate(96,96) scale({320/120:.4f})">{mi}</g>'))

for k in MARKS:
    for t in ('light','inverse'): build(k,t)
print(sorted(os.listdir(OUT)))
