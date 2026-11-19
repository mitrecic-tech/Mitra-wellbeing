#!/usr/bin/env python3
"""Generira cjenik usluga (CSV) i prikaz cijene s baznom cijenom iz programi.json.

Pravila: Pravilnik o načinu objave cjenika proizvoda i Pravilnik o isticanju
bazne cijene proizvoda (NN 132/2026).

    python3 cjenik/generiraj.py

Izlaz u cjenik/izlaz/:
  public/cjenik/<ID>_ZA_SVA_PRODAJNA_MJESTA_USLUGE_<broj>_<GGGGMMDD_SSMM>.csv
  public/cjenik/index.html  – stranica "Cjenik" na stalnoj adresi /cjenik/
  PriceBlock.jsx            – React komponenta s cijenom i baznom cijenom (hr/en)
  cijena-blok.html, cijena-blok.en.html – isto kao obični HTML
Mapu public/cjenik/ kopiraj u public/ projekta stranice. Nova CSV datoteka
nastaje samo kad se sadržaj cjenika promijeni.
"""
import csv
import html
import io
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

DIR = Path(__file__).resolve().parent
IZLAZ = DIR / "izlaz"
JAVNO = IZLAZ / "public" / "cjenik"
ARHIVA_DANA = 15  # čl. 3. st. 6.
TZ = ZoneInfo("Europe/Zagreb")
UZORAK = re.compile(r"^(\d+)_ZA_SVA_PRODAJNA_MJESTA_USLUGE_(\d+)_(\d{8}_\d{4})\.csv$")

TEKST = {
    "hr": {"cijena": "Cijena", "bazna": "Bazna cijena", "cjenik": "Cjenik",
           "napomena": "Bazna cijena je cijena usluge na dan 10. 9. 2026., odnosno na dan uvođenja usluge u ponudu ako je uvedena kasnije."},
    "en": {"cijena": "Price", "bazna": "Base price", "cjenik": "Price list",
           "napomena": "The base price is the price of the service on 10 September 2026, or on the day it was first offered if later."},
}


def eur_csv(x: float) -> str:
    return f"{x:.2f}".replace(".", ",")


def eur(x: float) -> str:
    cijeli, dec = f"{x:,.2f}".split(".")
    return f"{cijeli.replace(',', '.')},{dec} €"


def eur_en(x: float) -> str:
    return f"€{x:,.2f}"


def ucitaj():
    podaci = json.loads((DIR / "programi.json").read_text(encoding="utf-8"))
    tr = podaci["trgovac"]
    oib, mbo = str(tr.get("oib", "")).strip(), str(tr.get("mbo", "")).strip()
    if tr["vrsta"] == "pravna":
        if not re.fullmatch(r"\d{11}", oib):
            sys.exit("Pravna osoba: OIB mora imati 11 znamenki.")
        ident = oib
    else:
        # čl. 6. st. 3.: trgovac – fizička osoba (obrt) navodi matični broj.
        if re.fullmatch(r"\d{6,9}", mbo):
            ident = mbo
        elif re.fullmatch(r"\d{11}", oib):
            print("UPOZORENJE: za obrt pravilnik traži matični broj (MBO); upiši 'mbo'. Privremeno se koristi OIB.")
            ident = oib
        else:
            sys.exit("Upiši 'mbo' (matični broj obrta) ili barem 'oib'.")
    for u in podaci["usluge"]:
        for k in ("naziv", "cijena", "bazna_cijena"):
            if k not in u:
                sys.exit(f"Usluzi {u.get('naziv', '?')!r} nedostaje polje {k!r}.")
    return ident, podaci["usluge"]


def csv_sadrzaj(usluge) -> str:
    # Redoslijed prema čl. 3. st. 3. i 4.: naziv usluge; maloprodajna cijena +
    # je li primijenjena tijekom posebnog oblika prodaje; bazna cijena.
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", lineterminator="\n")
    w.writerow(["naziv_usluge", "maloprodajna_cijena_eur", "posebni_oblik_prodaje",
                "naziv_posebnog_oblika_prodaje", "bazna_cijena_eur"])
    for u in usluge:
        ak = u.get("akcija")
        w.writerow([u["naziv"], eur_csv(ak["cijena"] if ak else u["cijena"]),
                    "DA" if ak else "NE", ak["naziv"] if ak else "", eur_csv(u["bazna_cijena"])])
    return buf.getvalue()


def postojece(ident):
    out = []
    for f in JAVNO.glob("*.csv"):
        m = UZORAK.match(f.name)
        if m and m.group(1) == ident:
            out.append((int(m.group(2)), datetime.strptime(m.group(3), "%Y%m%d_%H%M").replace(tzinfo=TZ), f))
    return sorted(out)


def polje(u, k, jezik):
    return u.get(f"{k}_en", u.get(k, "")) if jezik == "en" else u.get(k, "")


CSS = """  .mc-cijene { --mc-navy:#0B1F33; --mc-siva:#5A6672; --mc-rub:#D9DEE3; --mc-poz:#fff;
    display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); color:var(--mc-navy); }
  .mc-kartica { background:var(--mc-poz); border:1px solid var(--mc-rub); border-radius:12px; padding:20px; display:flex; flex-direction:column; gap:8px; }
  .mc-kartica h3 { margin:0; font-size:1.1rem; }
  .mc-opis { margin:0; color:var(--mc-siva); font-size:.95rem; }
  .mc-cijena, .mc-bazna { margin:0; display:flex; justify-content:space-between; align-items:baseline; gap:12px; }
  .mc-cijena { margin-top:auto; padding-top:12px; border-top:1px solid var(--mc-rub); }
  .mc-cijena strong { font-size:1.5rem; }
  .mc-bazna { font-size:.95rem; color:var(--mc-siva); }
  .mc-oznaka { font-size:.85rem; text-transform:uppercase; letter-spacing:.04em; }
  .mc-napomena { grid-column:1/-1; margin:0; font-size:.85rem; color:var(--mc-siva); }"""


def blok_html(usluge, jezik) -> str:
    t, f = TEKST[jezik], (eur_en if jezik == "en" else eur)
    kartice = []
    for u in usluge:
        ak = u.get("akcija")
        jed = html.escape(polje(u, "jedinica", jezik))
        opis = polje(u, "opis", jezik)
        opis = f'\n    <p class="mc-opis">{html.escape(opis)}</p>' if opis else ""
        oznaka = html.escape(ak["naziv"]) if ak else t["cijena"]
        kartice.append(f"""  <article class="mc-kartica">
    <h3>{html.escape(polje(u, "naziv", jezik))}</h3>{opis}
    <p class="mc-cijena"><span class="mc-oznaka">{oznaka}</span><strong>{f(ak["cijena"] if ak else u["cijena"])}{jed}</strong></p>
    <p class="mc-bazna"><span class="mc-oznaka">{t["bazna"]}</span><span>{f(u["bazna_cijena"])}{jed}</span></p>
  </article>""")
    return f"""<!-- MITRA – cijena i bazna cijena (generirano: cjenik/generiraj.py) -->
<style>
{CSS}
</style>
<section class="mc-cijene" aria-label="{t['cijena']}">
{chr(10).join(kartice)}
  <p class="mc-napomena">{t["napomena"]} <a href="/cjenik/">{t["cjenik"]}</a></p>
</section>
"""


def jsx(usluge) -> str:
    podaci = [{"naziv": {"hr": u["naziv"], "en": polje(u, "naziv", "en")},
               "opis": {"hr": u.get("opis", ""), "en": polje(u, "opis", "en")},
               "jedinica": {"hr": u.get("jedinica", ""), "en": polje(u, "jedinica", "en")},
               "cijena": (u["akcija"]["cijena"] if u.get("akcija") else u["cijena"]),
               "akcija": u["akcija"]["naziv"] if u.get("akcija") else None,
               "bazna": u["bazna_cijena"]} for u in usluge]
    return f"""// MITRA – cijena i bazna cijena (generirano: cjenik/generiraj.py, ne uređuj ručno)
// Upotreba: <PriceBlock lang="hr" /> ili <PriceBlock lang="en" />
const USLUGE = {json.dumps(podaci, ensure_ascii=False, indent=2)};

const TEKST = {json.dumps(TEKST, ensure_ascii=False, indent=2)};

const CSS = `{CSS}`;

const iznos = (x, lang) =>
  new Intl.NumberFormat(lang === "en" ? "en-IE" : "hr-HR", {{ style: "currency", currency: "EUR" }}).format(x);

export default function PriceBlock({{ lang = "hr" }}) {{
  const t = TEKST[lang] ?? TEKST.hr;
  return (
    <section className="mc-cijene" aria-label={{t.cijena}}>
      <style>{{CSS}}</style>
      {{USLUGE.map((u) => (
        <article className="mc-kartica" key={{u.naziv.hr}}>
          <h3>{{u.naziv[lang] || u.naziv.hr}}</h3>
          {{u.opis[lang] && <p className="mc-opis">{{u.opis[lang]}}</p>}}
          <p className="mc-cijena">
            <span className="mc-oznaka">{{u.akcija ?? t.cijena}}</span>
            <strong>{{iznos(u.cijena, lang)}}{{u.jedinica[lang]}}</strong>
          </p>
          <p className="mc-bazna">
            <span className="mc-oznaka">{{t.bazna}}</span>
            <span>{{iznos(u.bazna, lang)}}{{u.jedinica[lang]}}</span>
          </p>
        </article>
      ))}}
      <p className="mc-napomena">{{t.napomena}} <a href="/cjenik/">{{t.cjenik}}</a></p>
    </section>
  );
}}
"""


def cjenik_html(usluge, datoteke, sada) -> str:
    redovi = []
    for u in usluge:
        ak = u.get("akcija")
        jed = html.escape(u.get("jedinica", ""))
        c = f'{eur(ak["cijena"])}{jed} <small>({html.escape(ak["naziv"])})</small>' if ak else f"{eur(u['cijena'])}{jed}"
        redovi.append(f"<tr><td>{html.escape(u['naziv'])}</td><td>{c}</td><td>{eur(u['bazna_cijena'])}{jed}</td></tr>")
    obrnuto = list(reversed(datoteke))
    veze = []
    for i, (_, ts, f) in enumerate(obrnuto):
        if i == 0:
            veze.append(f'<li><a href="{f.name}" download>{f.name}</a> – važeći cjenik od {ts:%d. %m. %Y. %H:%M}</li>')
        elif sada - obrnuto[i - 1][1] <= timedelta(days=ARHIVA_DANA):
            veze.append(f'<li><a href="{f.name}" download>{f.name}</a> – arhiva, vrijedio do {obrnuto[i - 1][1]:%d. %m. %Y. %H:%M}</li>')
    return f"""<!doctype html>
<html lang="hr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cjenik usluga – MITRA Wellbeing</title>
<style>
 body{{font-family:system-ui,sans-serif;color:#0B1F33;background:#fff;max-width:760px;margin:0 auto;padding:24px 16px;line-height:1.5}}
 table{{width:100%;border-collapse:collapse}} th,td{{text-align:left;padding:8px;border-bottom:1px solid #D9DEE3}}
 td:nth-child(n+2),th:nth-child(n+2){{text-align:right;white-space:nowrap}} small{{color:#5A6672}} li a{{overflow-wrap:anywhere}}
</style></head><body>
<p><a href="/">← MITRA Wellbeing</a></p>
<h1>Cjenik usluga <small>/ Price list</small></h1>
<table><thead><tr><th>Usluga</th><th>Cijena</th><th>Bazna cijena</th></tr></thead>
<tbody>{"".join(redovi)}</tbody></table>
<p><small>{TEKST["hr"]["napomena"]} Cijene su u eurima i konačne.</small></p>
<h2>Cjenik za preuzimanje (CSV)</h2>
<ul>{"".join(veze)}</ul>
</body></html>
"""


def main():
    ident, usluge = ucitaj()
    JAVNO.mkdir(parents=True, exist_ok=True)
    sadrzaj = csv_sadrzaj(usluge)
    dat = postojece(ident)
    sada = datetime.now(TZ).replace(second=0, microsecond=0)
    if dat and dat[-1][2].read_text(encoding="utf-8") == sadrzaj:
        print(f"Cjenik nepromijenjen: {dat[-1][2].name}")
    else:
        broj = dat[-1][0] + 1 if dat else 1
        ime = f"{ident}_ZA_SVA_PRODAJNA_MJESTA_USLUGE_{broj}_{sada:%Y%m%d_%H%M}.csv"
        (JAVNO / ime).write_text(sadrzaj, encoding="utf-8")
        dat.append((broj, sada, JAVNO / ime))
        print(f"Novi cjenik: {ime}")
    (JAVNO / "index.html").write_text(cjenik_html(usluge, dat, sada), encoding="utf-8")
    (IZLAZ / "cijena-blok.html").write_text(blok_html(usluge, "hr"), encoding="utf-8")
    (IZLAZ / "cijena-blok.en.html").write_text(blok_html(usluge, "en"), encoding="utf-8")
    (IZLAZ / "PriceBlock.jsx").write_text(jsx(usluge), encoding="utf-8")
    print("Ažurirano: public/cjenik/index.html, cijena-blok(.en).html, PriceBlock.jsx")


if __name__ == "__main__":
    main()
