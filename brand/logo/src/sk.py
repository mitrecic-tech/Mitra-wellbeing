import math
from tx import text, text_on_circle, arc_text
W,H=360,270; CX=W/2
def card(bg, body): return bg, body

def s1():  # Serif – mirno, premium
    bg='#F3EEE4'; g='#1F3A2E'
    t,_=text('fraunces','Mitra',92,-0.01,{'wght':380,'opsz':144,'SOFT':50,'WONK':0},CX,150,'middle',g)
    s,_=text('manrope','WELLBEING',13,0.42,{'wght':600},CX,190,'middle',g)
    return bg, t+s
def s2():  # Atletski
    bg='#FFFFFF'; n='#0B1F33'; a='#D94F2B'
    t,w=text('barlowi','MITRA',110,0.0,(),CX+6,170,'middle',n)
    sl=f'<path d="M{CX-w/2-30} 186 L{CX+w/2-10} 186 L{CX+w/2-16} 196 L{CX-w/2-36} 196 Z" fill="{a}"/>'
    s,_=text('barlow','WELLBEING · SCIENCE-BASED TRAINING',12,0.18,(),CX,222,'middle',n)
    return bg, t+sl+s
def s3():  # Pečat
    bg='#0B1F33'; c='#F3EEE4'; a='#BFA46A'; cy=135
    ring=f'<circle cx="{CX}" cy="{cy}" r="104" fill="none" stroke="{c}" stroke-width="2"/><circle cx="{CX}" cy="{cy}" r="70" fill="none" stroke="{c}" stroke-width="1.2"/>'
    o=arc_text('manrope','MITRA WELLBEING',14,CX,cy,80,0,0.26,{'wght':700},c)
    o+=arc_text('manrope','SCIENCE-BASED TRAINING',11,CX,cy,90,180,0.22,{'wght':700},c,bottom=True)
    o+=f'<circle cx="{CX-87}" cy="{cy}" r="3" fill="{a}"/><circle cx="{CX+87}" cy="{cy}" r="3" fill="{a}"/>'
    m,_=text('fraunces','M',72,0,{'wght':500,'opsz':144,'SOFT':0,'WONK':0},CX,cy+26,'middle',c)
    yr,_=text('manrope','EST. 2026',8,0.3,{'wght':700},CX,cy+46,'middle',a)
    return bg, ring+o+m+yr
def s4():  # Kettlebell
    bg='#E8E2D6'; k='#141414'
    kb=(f'<path d="M150 62 A30 30 0 0 1 210 62 L214 104 L196 104 L193 70 A13 13 0 0 0 167 70 L164 104 L146 104 Z" fill="{k}"/>'
        f'<circle cx="{CX}" cy="146" r="56" fill="{k}"/>')
    m,_=text('barlow','M',78,0,(),CX,174,'middle','#E8E2D6')
    s,_=text('barlow','MITRA WELLBEING',20,0.16,(),CX,236,'middle',k)
    return bg, kb+m+s
def s5():  # Pokret – figura u iskoraku s kettlebellom
    bg='#FFFFFF'; n='#0B1F33'; a='#BFA46A'
    fig=(f'<g fill="none" stroke="{n}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">'
         f'<path d="M98 98 L96 146"/>'
         f'<path d="M96 146 L128 152 L130 194"/>'
         f'<path d="M96 146 L82 184 L52 190"/>'
         f'<path d="M98 106 L110 128 L116 118"/></g>'
         f'<circle cx="99" cy="76" r="12" fill="{n}"/><circle cx="122" cy="114" r="11" fill="{a}"/>')
    t,_=text('manrope','MITRA',48,0.04,{'wght':800},170,140,'start',n)
    s,_=text('manrope','wellbeing',24,0,{'wght':400},171,170,'start',n)
    return bg, fig+t+s
def s6():  # Kamenje
    bg='#EDE6D8'; g='#2F4A3A'; a='#C08A5B'
    st=(f'<ellipse cx="{CX}" cy="150" rx="58" ry="17" fill="{g}"/>'
        f'<ellipse cx="{CX-4}" cy="119" rx="44" ry="14" fill="{g}"/>'
        f'<ellipse cx="{CX+3}" cy="93" rx="31" ry="11.5" fill="{g}"/>'
        f'<ellipse cx="{CX}" cy="72" rx="18" ry="9" fill="{a}"/>')
    t,_=text('fraunces','mitra',46,0,{'wght':420,'opsz':72,'SOFT':100,'WONK':0},CX,222,'middle',g)
    s,_=text('manrope','WELLBEING',10,0.42,{'wght':600},CX,244,'middle',g)
    return bg, st+t+s
def s7():  # Staza
    bg='#F6F3EC'; g='#22402F'; a='#BFA46A'; cy=118
    sym=(f'<defs><clipPath id="c7"><circle cx="{CX}" cy="{cy}" r="62"/></clipPath></defs>'
         f'<g clip-path="url(#c7)"><rect x="{CX-62}" y="{cy-62}" width="124" height="124" fill="{g}"/>'
         f'<circle cx="{CX+22}" cy="{cy-20}" r="13" fill="{a}"/>'
         f'<path d="M{CX-70} {cy+10} Q{CX-20} {cy-6} {CX+70} {cy+6} V{cy+70} H{CX-70} Z" fill="#2E5A41"/>'
         f'<path d="M{CX-40} {cy+64} C{CX-14} {cy+40} {CX+26} {cy+30} {CX-1} {cy+4} L{CX+3} {cy+4} C{CX+40} {cy+30} {CX+12} {cy+46} {CX+30} {cy+64} Z" fill="{bg}"/></g>')
    t,_=text('manrope','MITRA',30,0.22,{'wght':700},CX,222,'middle',g)
    s,_=text('manrope','WELLBEING',10,0.5,{'wght':600},CX,242,'middle',g)
    return bg, sym+t+s
def s8():  # Mono m – aplikacija
    bg='#4A7FC1'; w='#FFFFFF'
    m,_=text('outfit','m',150,0,{'wght':700},CX,150,'middle',w)
    s,_=text('outfit','mitra wellbeing',22,0.02,{'wght':500},CX,214,'middle',w)
    return bg, m+s
def s9():  # Krugovi – povezanost
    bg='#FFFFFF'; n='#0B1F33'; a='#BFA46A'; cy=112
    sym=(f'<defs><clipPath id="c9"><circle cx="{CX-20}" cy="{cy}" r="44"/></clipPath></defs>'
         f'<circle cx="{CX-20}" cy="{cy}" r="44" fill="none" stroke="{n}" stroke-width="8"/>'
         f'<circle cx="{CX+20}" cy="{cy}" r="44" fill="none" stroke="{n}" stroke-width="8"/>'
         f'<circle cx="{CX+20}" cy="{cy}" r="40" fill="{a}" clip-path="url(#c9)"/>')
    t,_=text('manrope','MITRA',30,0.2,{'wght':800},CX,208,'middle',n)
    s,_=text('manrope','WELLBEING',10,0.5,{'wght':600},CX,228,'middle',n)
    return bg, sym+t+s
def s10(): # Potpis
    bg='#111111'; w='#F3EEE4'; a='#BFA46A'
    t,_=text('dafoe','Mitra',110,0,(),CX,158,'middle',w)
    s,_=text('manrope','WELLBEING  ·  KRISTIJAN MITREČIĆ, PhD',10,0.24,{'wght':600},CX,208,'middle',a)
    return bg, t+s
S=[('Serif','Mirno, premium, wellness',s1),('Atletski','Snažno, sportski, dinamično',s2),('Pečat','Klasično, ozbiljno, stručno',s3),
   ('Kettlebell','Trening, snaga, oprema',s4),('Pokret','Kineziologija, figura u iskoraku',s5),('Kamenje','Ravnoteža, oporavak, priroda',s6),
   ('Staza','Dugoročni put, priroda, kao na naslovnoj slici',s7),('Aplikacija','Moderno, digitalno, pristupačno',s8),
   ('Krugovi','Povezanost, trener i vježbač',s9),('Potpis','Osobni brend, ti kao autor',s10)]
def slug(n): return n.lower().replace('č','c').replace('ć','c').replace('š','s').replace('ž','z')
def card_svg(i, fn):
    bg,body=fn()
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>\n'
if __name__=='__main__':
    import os, sys
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    for i,(n,d,fn) in enumerate(S,1):
        open(f'{out}/skica-{i:02d}-{slug(n)}.svg','w').write(card_svg(i,fn))
    cells=''.join(f'<div><img src="{out}/skica-{i:02d}-{slug(n)}.svg" width=360><p>{i}. {n}</p></div>' for i,(n,d,fn) in enumerate(S,1))
    open('sheet.html','w').write(f'<html><head><base href="file://{os.getcwd()}/"><style>body{{margin:0;padding:16px;background:#ccc;display:grid;grid-template-columns:repeat(4,360px);gap:12px;font-family:sans-serif}}p{{margin:4px 0}}</style></head><body>{cells}</body></html>')
