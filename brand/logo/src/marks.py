NAVY="#0B1F33"; GOLD="#BFA46A"; BLUE="#4A7FC1"; CREAM="#F7F3EA"

def mark_a(fg=NAVY, acc=GOLD):
    # "Iskorak" – refined evolution of the existing mark
    return f'''<g fill="none" stroke="{fg}" stroke-width="11" stroke-linecap="butt">
<line x1="34" y1="12" x2="34" y2="108"/>
<line x1="10" y1="84" x2="108" y2="84"/>
<line x1="52" y1="110" x2="108" y2="58"/>
</g><circle cx="90" cy="32" r="13" fill="{acc}"/>'''

def mark_b(fg=NAVY, acc=GOLD):
    # "Progresija" – M drawn as a rising training-load curve
    return f'''<path d="M14 102 V46 L42 78 L74 34 V102" fill="none" stroke="{fg}" stroke-width="12" stroke-linejoin="miter" stroke-miterlimit="10"/>
<path d="M74 34 L104 70" fill="none" stroke="{fg}" stroke-width="12" stroke-linecap="butt"/>
<circle cx="103" cy="22" r="10.5" fill="{acc}"/>'''

def mark_c(fg=NAVY, acc=GOLD):
    # "Ciklus" – 4-week ring + 3 progressive sessions
    import math
    cx=cy=60; r=50; gap=14
    arcs=[]
    for i in range(4):
        a0=-90+i*90+gap/2; a1=-90+(i+1)*90-gap/2
        p=lambda a:(cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
        (x0,y0),(x1,y1)=p(a0),p(a1)
        col = acc if i==0 else fg
        arcs.append(f'<path d="M{x0:.2f} {y0:.2f} A{r} {r} 0 0 1 {x1:.2f} {y1:.2f}" fill="none" stroke="{col}" stroke-width="9"/>')
    bars=''.join(f'<rect x="{x}" y="{82-h}" width="12" height="{h}" fill="{fg}"/>' for x,h in [(36,22),(54,34),(72,46)])
    return ''.join(arcs)+bars

MARKS={'a':mark_a,'b':mark_b,'c':mark_c}
