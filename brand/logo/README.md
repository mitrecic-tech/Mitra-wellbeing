# MITRA Wellbeing – logo (2. krug)

Novi smjerovi nakon prvog kruga (Progresija, Iskorak, Ciklus su u git povijesti).
Polazište: *mitra* znači **prijatelj**. Ovo je program u kojem kineziolog vodi i prati čovjeka kroz održiv trening, a ne izazov u kojem je čovjek sam.

| Boja | HEX |
|---|---|
| Navy | `#0B1F33` |
| Zlatna (naglasak) | `#BFA46A` |
| Krem | `#F7F3EA` |

Pismo: **Manrope** (kao na stranici). U SVG datotekama tekst je pretvoren u krivulje.

## Smjerovi

- **Prijatelji (preporuka):** slovo M čine dvije figure jedna uz drugu, trener (navy) i vježbač (zlatna). Ime, odnos i čovjek u jednom znaku.
- **Ritam:** malo slovo m kao miran ritam opterećenja i oporavka. Drugi luk je viši, kao napredak iz mjeseca u mjesec. Uz znak ide logotip malim slovima, topliji i pristupačniji.
- **Riječ:** samo logotip. Iznad slova I u MITRA stoji zlatna točka, čovjek unutar imena. Najmirnije i najprofinjenije rješenje.

## Datoteke

| Datoteka | Namjena |
|---|---|
| `*-horizontalni.svg` / `*-logotip.svg` | zaglavlje stranice, e-mail potpis, dokumenti |
| `*-vertikalni.svg` | naslovnice, plakati, odjeća |
| `*-znak.svg` | samo znak |
| `*-inverse.svg` | za tamnu (navy) pozadinu |
| `*-ikona.svg` | ikona aplikacije, favicon, profilna slika |

`png/` sadrži iste datoteke kao PNG s prozirnom pozadinom (ikone 1024 × 1024 px, ostalo u 4× rezoluciji).

## Ponovno generiranje

```bash
pip install fonttools
cd brand/logo/src
MANROPE_TTF=/put/do/Manrope[wght].ttf python3 build.py ../svg
```
