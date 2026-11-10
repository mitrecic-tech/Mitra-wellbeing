# MITRA Wellbeing – logo

Tri prijedloga loga izrađena na temelju sadržaja stranice [mitrawellbeing.com](https://www.mitrawellbeing.com/).
Boje i pismo preuzeti su sa stranice.

| Boja | HEX |
|---|---|
| Navy | `#0B1F33` |
| Zlatna (naglasak) | `#BFA46A` |
| Krem | `#F7F3EA` |

Pismo: **Manrope** (ExtraBold za MITRA, SemiBold za WELLBEING). U SVG datotekama tekst je pretvoren u krivulje.

## Koncepti

- **B · Progresija (preporuka):** slovo M kao krivulja opterećenja koja raste, strelica prema gore i zlatna točka (čovjek). Najbolje se čita u malim veličinama.
- **A · Iskorak:** dorađena postojeća oznaka sa stranice (struktura, tlo, pokret, glava).
- **C · Ciklus:** prsten od 4 segmenta (4-tjedni ciklus) i 3 rastuća stupca (3 treninga tjedno).

## Datoteke

Za svaki koncept (`iskorak`, `progresija`, `ciklus`):

| Datoteka | Namjena |
|---|---|
| `mitra-<koncept>-horizontalni.svg` | zaglavlje stranice, e-mail potpis, dokumenti |
| `mitra-<koncept>-vertikalni.svg` | naslovnice, plakati, odjeća |
| `mitra-<koncept>-znak.svg` | samo znak |
| `*-inverse.svg` | verzija za tamnu (navy) pozadinu |
| `mitra-<koncept>-ikona.svg` | ikona aplikacije, favicon, profilna slika na društvenim mrežama |

`png/` sadrži iste datoteke kao PNG s prozirnom pozadinom (ikone 1024 × 1024 px, ostalo u 4× rezoluciji).

## Ponovno generiranje

```bash
pip install fonttools
cd brand/logo/src
MANROPE_TTF=/put/do/Manrope[wght].ttf python3 build.py ../svg
```
Naredbu pokreni iz mape `brand/logo/src` (skripta učitava `marks.py` i `typo.py`).
