# MITRA Wellbeing – logo, novi početak (3. krug)

Deset skica u potpuno različitim stilovima. Služe za odabir smjera, a izabrani smjer zatim se razrađuje do kraja.
Raniji prijedlozi (1. i 2. krug) ostaju u git povijesti.

| # | Skica | Dojam |
|---|---|---|
| 1 | Serif | mirno, premium, wellness |
| 2 | Atletski | snažno, sportski, dinamično |
| 3 | Pečat | klasično, ozbiljno, stručno |
| 4 | Kettlebell | trening, snaga, oprema |
| 5 | Pokret | kineziologija, figura u iskoraku s kettlebellom |
| 6 | Kamenje | ravnoteža, oporavak, priroda |
| 7 | Staza | dugoročni put, priroda (kao naslovna slika stranice) |
| 8 | Aplikacija | moderno, digitalno, pristupačno |
| 9 | Krugovi | povezanost trenera i vježbača |
| 10 | Potpis | osobni brend, autor programa |

Datoteke su u `skice/` (SVG, tekst pretvoren u krivulje).

## Ponovno generiranje

Fontovi (Google Fonts, OFL): Manrope, Fraunces, Barlow Condensed (Bold, ExtraBold Italic), Mr Dafoe, Outfit.

```bash
pip install fonttools
cd brand/logo/src
FONT_DIR=/put/do/fontova python3 sk.py ../skice
```
