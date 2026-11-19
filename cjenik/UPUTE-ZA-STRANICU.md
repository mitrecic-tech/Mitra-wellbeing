# Upute za izradu stranice: prikaz cijene (mitrawellbeing.com)

Od 17. 11. 2026. vrijede Pravilnik o isticanju bazne cijene proizvoda i Pravilnik o načinu objave cjenika proizvoda (NN 132/2026). Za MITRA Wellbeing to znači sljedeće.

Sve potrebne datoteke su u mapi `cjenik/izlaz/`.

## 1. Cjenik na `/cjenik/`
Mapu `izlaz/public/cjenik/` kopiraj u `public/cjenik/` u Vite projektu. Nakon objave na Vercelu mora vrijediti:
- `https://www.mitrawellbeing.com/cjenik/` otvara stranicu s cjenikom, a ne React aplikaciju
- CSV datoteka iz te mape može se preuzeti izravno, bez prijave, kolačića i zaštite od botova

Ako `vercel.json` ima rewrite svih ruta na `index.html`, provjeri da se statičke datoteke i dalje poslužuju. Vercel ih po zadanim postavkama poslužuje prije rewritea.

Ne mijenjaj nazive CSV datoteka. Naziv propisuje pravilnik.

## 2. Cijena u odjeljku Pricing
- Tekst "Pricing is determined individually…" i gumb "Request Your Custom Quote" zamijeni stvarnom cijenom, jer svi plaćaju istih 129 €.
- `izlaz/PriceBlock.jsx` kopiraj u `src/components/` i postavi ga u Pricing:
  ```jsx
  import PriceBlock from "./components/PriceBlock";
  <PriceBlock lang="en" />   // na hrvatskoj inačici: lang="hr"
  ```
- Ako mijenjaš dizajn, pazi na ovo:
  - **Bazna cijena** mora stajati odmah uz cijenu i biti vidljiva i čitljiva.
  - Mora imati vlastitu oznaku (Bazna cijena / Base price), da se ne može zamijeniti s cijenom.
  - Ne smije biti precrtana, sakrivena u tooltipu ni prikazana samo na hover.
- Na svim drugim mjestima gdje piše cijena (gumb "Subscribe", checkout prije Stripea, FAQ) uz cijenu treba prikazati i baznu cijenu.
- U podnožje dodaj poveznicu "Cjenik / Price list" na `/cjenik/`.

## 3. Promjena cijene ili akcija
Datoteke se ne uređuju ručno. Mijenja se `cjenik/programi.json`, zatim se pokrene `python3 cjenik/generiraj.py`, kopiraju se nove datoteke i stranica se objavi **do 11:00 istog dana**. Stare CSV datoteke ostaju u `public/cjenik/` još 15 dana.

Oglasi na Instagramu, Facebooku, TikToku i YouTubeu ne moraju imati baznu cijenu. Tiskani i TV oglasi s cijenom moraju je imati.
