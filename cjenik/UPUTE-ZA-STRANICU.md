# Upute za izradu stranice: prikaz cijene (mitrawellbeing.com)

Od 17. 11. 2026. vrijede Pravilnik o isticanju bazne cijene proizvoda i Pravilnik o načinu objave cjenika proizvoda (NN 132/2026). Za MITRA Wellbeing to znači sljedeće.

Uz ove upute dolaze tri datoteke:

| Datoteka | Kamo ide u projektu |
|---|---|
| `index.html` (stranica cjenika) | `public/cjenik/index.html` |
| `99165244_ZA_SVA_PRODAJNA_MJESTA_USLUGE_1_20261119_1112.csv` | `public/cjenik/` (uz `index.html`) |
| `PriceBlock.jsx` (blok s cijenom) | `src/components/PriceBlock.jsx` |

## 1. Cjenik na `/cjenik/`
Napravi mapu `public/cjenik/` u Vite projektu i u nju stavi `index.html` i CSV datoteku. Nakon objave na Vercelu mora vrijediti:
- `https://www.mitrawellbeing.com/cjenik/` otvara stranicu s cjenikom, a ne React aplikaciju
- CSV datoteka iz te mape može se preuzeti izravno, bez prijave, kolačića i zaštite od botova

Ako `vercel.json` ima rewrite svih ruta na `index.html`, provjeri da se statičke datoteke i dalje poslužuju. Vercel ih po zadanim postavkama poslužuje prije rewritea.

Ne mijenjaj nazive CSV datoteka. Naziv propisuje pravilnik.

## 2. Cijena u odjeljku Pricing
- Tekst "Pricing is determined individually…" i gumb "Request Your Custom Quote" zamijeni stvarnom cijenom, jer svi plaćaju istih 129 €.
- `PriceBlock.jsx` kopiraj u `src/components/` i postavi ga u Pricing:
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
Datoteke se ne uređuju ručno. Kod svake promjene cijene dobit ćeš nove datoteke (novi CSV, `index.html` i `PriceBlock.jsx`). Zamijeni ih i objavi stranicu **do 11:00 istog dana**. Stari CSV ne briši još 15 dana, jer na njega vodi poveznica s cjenika.

Oglasi na Instagramu, Facebooku, TikToku i YouTubeu ne moraju imati baznu cijenu. Tiskani i TV oglasi s cijenom moraju je imati.
