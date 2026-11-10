import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx import text
INK="#111111"; NAVY="#0B1F33"; CREAM="#F3EEE4"; GOLD="#BFA46A"
def zamah(fg):  # an italic "i" (from MITRA) that is also a person leaning forward into the movement
    return f'<path d="M23 106 L53 106 L84 52.3 L54 52.3 Z" fill="{fg}"/><circle cx="82.5" cy="29" r="15" fill="{fg}"/>'
def vrh(fg):    # one chevron + dot: a person standing firm, a peak, the A of MITRA
    return f'<path d="M14 106 L60 44 L106 106 H80 L60 78 L40 106 Z" fill="{fg}"/><circle cx="60" cy="20" r="13" fill="{fg}"/>'
def blok(fg):   # solid block with a V cut from the top: an M you can stitch on anything
    return f'<path d="M14 28 L60 66 L106 28 V98 H14 Z" fill="{fg}"/>'
def luka(fg):   # two arches with heads: m, two people side by side (mitra = friend)
    return (f'<path d="M10 104 V74 A25 25 0 0 1 60 74 V104 H46 V74 A11 11 0 0 0 24 74 V104 Z" fill="{fg}"/>'
            f'<path d="M60 104 V74 A25 25 0 0 1 110 74 V104 H96 V74 A11 11 0 0 0 74 74 V104 Z" fill="{fg}"/>'
            f'<circle cx="35" cy="32" r="11" fill="{fg}"/><circle cx="85" cy="32" r="11" fill="{fg}"/>')
M={'zamah':zamah,'vrh':vrh,'blok':blok,'dva-luka':luka}
def doc(w,h,body,bg=None):
    r=f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="MITRA"><title>MITRA</title>{r}{body}</svg>\n'
def word(fg, size=100):
    t,w=text('manrope','MITRA',size,0.02,{'wght':800},0,0,'start',fg)
    return t,w,size*0.72
def lockup(k, fg):
    t,w,cap=word(fg); mh=cap*1.5; s=mh/120; gap=cap*0.55; pad=10
    body=f'<g transform="translate({pad},{pad}) scale({s:.4f})">{M[k](fg)}</g><g transform="translate({pad+mh+gap:.2f},{pad+mh/2+cap/2:.2f})">{t}</g>'
    return doc(2*pad+mh+gap+w, 2*pad+mh, body)
def stacked(k, fg):
    t,w,cap=word(fg,60); ms=170; pad=10; W=max(w,ms)+2*pad
    body=f'<g transform="translate({(W-ms)/2:.2f},{pad}) scale({ms/120:.4f})">{M[k](fg)}</g><g transform="translate({(W-w)/2:.2f},{pad+ms+24+cap:.2f})">{t}</g>'
    return doc(W, pad*2+ms+24+cap, body)
if __name__=='__main__':
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    for k in M:
        for nm,fg in (('crni',INK),('bijeli','#FFFFFF'),('navy',NAVY)):
            open(f'{out}/mitra-{k}-znak-{nm}.svg','w').write(doc(136,136,f'<g transform="translate(8,8)">{M[k](fg)}</g>'))
            open(f'{out}/mitra-{k}-logo-{nm}.svg','w').write(lockup(k,fg))
            open(f'{out}/mitra-{k}-vertikalni-{nm}.svg','w').write(stacked(k,fg))
        open(f'{out}/mitra-{k}-ikona.svg','w').write(doc(512,512,f'<rect width="512" height="512" rx="112" fill="{INK}"/><g transform="translate(106,106) scale({300/120:.4f})">{M[k]("#FFFFFF")}</g>'))
    print(len(os.listdir(out)))
