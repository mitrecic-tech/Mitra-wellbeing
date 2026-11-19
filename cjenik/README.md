# Cjenik usluga i bazna cijena

Usklađeno s Pravilnikom o isticanju bazne cijene proizvoda i Pravilnikom o načinu objave cjenika proizvoda (NN 132/2026, na snazi od 17. 11. 2026.).

## Postupak

1. U `programi.json` upiši:
   - `trgovac.vrsta`: `"fizicka"` (obrt, koristi matični broj obrta) ili `"pravna"` (d.o.o., koristi OIB)
   - `trgovac.identifikator`: MBO ili OIB
   - za svaku uslugu: `naziv`, `cijena`, `bazna_cijena`, po želji `jedinica` (npr. `"/mj."`), `opis` i `akcija` (`{"naziv": "Akcija", "cijena": 99.00}`)
2. Pokreni:
   ```bash
   python3 cjenik/generiraj.py
   ```
3. Postavi na stranicu sve iz `cjenik/izlaz/`:
   - `cjenik.html` na stalnu adresu, npr. `/cjenik`. Sadrži tablicu i poveznice na važeću te arhivske CSV datoteke.
   - CSV datoteke u istu mapu kao `cjenik.html`. Ne smiju biti iza prijave ni zaštite od botova (čl. 5.).
   - Kod iz `cijena-blok.html` ubaci na stranicu s programima, gdje kupac vidi cijenu.

Kod svake promjene cijene ponovi korake 2 i 3 **do 11:00 istog dana**. Skripta tada napravi novu CSV datoteku (sljedeći broj pohrane i nova vremenska oznaka), a staru 15 dana prikazuje kao arhivsku. Datoteke starije od toga možeš obrisati sa servera.

## Kako odrediti baznu cijenu

| Situacija | Bazna cijena |
|---|---|
| Usluga se nudila 10. 9. 2026. | Cijena koja je vrijedila 10. 9. 2026. |
| 10. 9. 2026. je bila na akciji | Redovna cijena prije te akcije |
| Usluga je uvedena nakon 10. 9. 2026. | Cijena na dan uvođenja |

Bazna cijena se ne mijenja kad mijenjaš cijenu. U cjenik ne ulaze cijene dogovorene s pojedinim klijentom (individualni coaching po mjeri), popusti za skupine kupaca ili za način plaćanja te dinamičke cijene (čl. 4.).

## Format CSV-a

- Kodiranje UTF-8, stupci odvojeni s `;`, decimalni zarez
- Stupci: naziv usluge; maloprodajna cijena; je li u tijeku posebni oblik prodaje (DA/NE); naziv posebnog oblika prodaje; bazna cijena
- Naziv datoteke: `<MBO|OIB>_ZA_SVA_PRODAJNA_MJESTA_USLUGE_<broj pohrane>_<GGGGMMDD_SSMM>.csv`

Pravilnik ne propisuje točan zapis oznake „usluge" ni broja pohrane. Ovdje su odabrani `USLUGE` i redni broj.
