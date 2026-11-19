# Cjenik usluga i bazna cijena

Usklađeno s Pravilnikom o isticanju bazne cijene proizvoda i Pravilnikom o načinu objave cjenika proizvoda (NN 132/2026, na snazi od 17. 11. 2026.).

## Postupak

1. Podatke uređuješ samo u `programi.json`:
   - `trgovac.mbo`: matični broj obrta. Pravilnik za obrt (trgovac – fizička osoba) u nazivu datoteke traži matični broj. Dok je `mbo` prazan, koristi se OIB i ispisuje se upozorenje.
   - za svaku uslugu: `naziv`, `cijena`, `bazna_cijena`, `jedinica`, `opis`, te engleske inačice (`*_en`). Po potrebi i `akcija`: `{"naziv": "Akcija", "cijena": 99.00}`.
2. Pokreni:
   ```bash
   python3 cjenik/generiraj.py
   ```
3. Prenesi izlaz u projekt stranice (React/Vite na Vercelu):
   - **Mapu `izlaz/public/cjenik/` kopiraj u `public/cjenik/`.** Stranica će biti dostupna na `https://www.mitrawellbeing.com/cjenik/`, uključujući važeću i arhivske CSV datoteke. Ne smije biti iza prijave ni zaštite od botova (čl. 5.).
   - **`izlaz/PriceBlock.jsx` kopiraj u `src/components/`.** U odjeljku Pricing stavi `<PriceBlock lang="en" />`, a na hrvatskoj inačici `<PriceBlock lang="hr" />`. Ako stranica nije u Reactu, koristi `cijena-blok.html` ili `cijena-blok.en.html`.
   - Objavi (deploy).

Kad promijeniš cijenu, ponovi korake 1–3 **do 11:00 istog dana**. Skripta tada napravi novu CSV datoteku (sljedeći broj pohrane i nova vremenska oznaka), a staru 15 dana prikazuje kao arhivsku. Zato pri kopiranju zadrži i stare CSV datoteke u `public/cjenik/`. One starije od 15 dana od zamjene možeš obrisati.

## Bazna cijena

| Situacija | Bazna cijena |
|---|---|
| Usluga se nudila 10. 9. 2026. | Cijena koja je vrijedila 10. 9. 2026. |
| 10. 9. 2026. bila je na akciji | Redovna cijena prije te akcije |
| Usluga je uvedena nakon 10. 9. 2026. | Cijena na dan uvođenja |

Bazna cijena se ne mijenja kad mijenjaš cijenu. U cjenik ne ulaze cijene dogovorene s pojedinim klijentom, popusti za skupine kupaca ili za način plaćanja te dinamičke cijene (čl. 4.).

## Format CSV-a

- Kodiranje UTF-8, stupci odvojeni s `;`, decimalni zarez
- Stupci: naziv usluge; maloprodajna cijena; je li u tijeku posebni oblik prodaje (DA/NE); naziv posebnog oblika prodaje; bazna cijena
- Naziv datoteke: `<MBO|OIB>_ZA_SVA_PRODAJNA_MJESTA_USLUGE_<broj pohrane>_<GGGGMMDD_SSMM>.csv`

Pravilnik ne propisuje točan zapis oznake usluga ni broja pohrane. Ovdje su odabrani `USLUGE` i redni broj.
