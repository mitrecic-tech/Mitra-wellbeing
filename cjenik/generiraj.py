#!/usr/bin/env python3
"""Generira cjenik usluga (CSV) i blok s cijenama (HTML) iz programi.json.

Pravila: Pravilnik o načinu objave cjenika proizvoda i Pravilnik o isticanju
bazne cijene proizvoda (NN 132/2026).

    python3 cjenik/generiraj.py

Izlaz u cjenik/izlaz/:
  <ID>_ZA_SVA_PRODAJNA_MJESTA_USLUGE_<broj>_<GGGGMMDD_SSMM>.csv  – strojno čitljiv cjenik
  cjenik.html      – stranica "Cjenik" (stalni URL): tablica + važeća i arhivske datoteke
  cijena-blok.html – kartice s cijenom i baznom cijenom za stranicu s programima
Nova CSV datoteka nastaje samo kad se sadržaj cjenika promijeni.
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
ARHIVA_DANA = 15  # čl. 3. st. 6.
TZ = ZoneInfo("Europe/Zagreb")
UZORAK = re.compile(r"^(\w+)_ZA_SVA_PRODAJNA_MJESTA_USLUGE_(\d+)_(\d{8}_\d{4})\.csv$")


def eur_csv(x: float) -> str:
    return f"{x:.2f}".replace(".", ",")


def eur(x: float) -> str:
    cijeli, dec = f"{x:,.2f}".split(".")
    return f"{cijeli.replace(',', '.')},{dec} €"


def ucitaj():
    podaci = json.loads((DIR / "programi.json").read_text(encoding="utf-8"))
    tr = podaci["trgovac"]
    ident = str(tr["identifikator"]).strip()
    if tr["vrsta"] == "pravna" and not re.fullmatch(r"\d{11}", ident):
        sys.exit("OIB mora imati 11 znamenki.")
    if tr["vrsta"] == "fizicka" and not re.fullmatch(r"\d{6,9}", ident):
        sys.exit("Matični broj obrta (MBO) mora biti niz znamenki.")
    for u in podaci["usluge"]:
        for k in ("naziv", "cijena", "bazna_cijena"):
            if k not in u:
                sys.exit(f"Usluzi {u.get('naziv', '?')!r} nedostaje polje {k!r}.")
    return ident, podaci["usluge"]


def csv_sadrzaj(usluge) -> str:
    # Redoslijed stupaca prema čl. 3. st. 3. i 4.: naziv usluge; maloprodajna
    # cijena + je li primijenjena tijekom posebnog oblika prodaje; bazna cijena.
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", lineterminator="\n")
    w.writerow(["naziv_usluge", "maloprodajna_cijena_eur", "posebni_oblik_prodaje",
                "naziv_posebnog_oblika_prodaje", "bazna_cijena_eur"])
    for u in usluge:
        ak = u.get("akcija")
        cijena = ak["cijena"] if ak else u["cijena"]
        naziv = u["naziv"] + (f" ({u['jedinica'].strip('/. ')})" if u.get("jedinica") else "")
        w.writerow([naziv, eur_csv(cijena), "DA" if ak else "NE",
                    ak["naziv"] if ak else "", eur_csv(u["bazna_cijena"])])
    return buf.getvalue()


def postojece(ident):
    out = []
    for f in IZLAZ.glob("*.csv"):
        m = UZORAK.match(f.name)
        if m and m.group(1) == ident:
            out.append((int(m.group(2)), datetime.strptime(m.group(3), "%Y%m%d_%H%M").replace(tzinfo=TZ), f))
    return sorted(out)


def blok_html(usluge) -> str:
    kartice = []
    for u in usluge:
        ak = u.get("akcija")
        jed = html.escape(u.get("jedinica", ""))
        naziv = html.escape(u["naziv"])
        opis = f'<p class="mc-opis">{html.escape(u["opis"])}</p>' if u.get("opis") else ""
        if ak:
            cijena = (f'<p class="mc-cijena"><span class="mc-oznaka">{html.escape(ak["naziv"])}</span>'
                      f'<strong>{eur(ak["cijena"])}{jed}</strong></p>')
        else:
            cijena = f'<p class="mc-cijena"><span class="mc-oznaka">Cijena</span><strong>{eur(u["cijena"])}{jed}</strong></p>'
        kartice.append(f"""  <article class="mc-kartica">
    <h3>{naziv}</h3>
    {opis}
    {cijena}
    <p class="mc-bazna"><span class="mc-oznaka">Bazna cijena</span><span>{eur(u["bazna_cijena"])}{jed}</span></p>
  </article>""")
    return f"""<!-- MITRA – blok s cijenama (generirano: cjenik/generiraj.py) -->
<style>
  .mc-cijene {{ --mc-navy:#0B1F33; --mc-tekst:#0B1F33; --mc-siva:#5A6672; --mc-rub:#D9DEE3; --mc-poz:#fff;
    display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); font-family:inherit; color:var(--mc-tekst); }}
  .mc-kartica {{ background:var(--mc-poz); border:1px solid var(--mc-rub); border-radius:12px; padding:20px; display:flex; flex-direction:column; gap:8px; }}
  .mc-kartica h3 {{ margin:0; font-size:1.1rem; }}
  .mc-opis {{ margin:0; color:var(--mc-siva); font-size:.95rem; }}
  .mc-cijena, .mc-bazna {{ margin:0; display:flex; justify-content:space-between; align-items:baseline; gap:12px; }}
  .mc-cijena {{ margin-top:auto; padding-top:12px; border-top:1px solid var(--mc-rub); }}
  .mc-cijena strong {{ font-size:1.5rem; color:var(--mc-navy); }}
  .mc-bazna {{ font-size:.95rem; color:var(--mc-siva); }}
  .mc-oznaka {{ font-size:.85rem; text-transform:uppercase; letter-spacing:.04em; }}
  .mc-napomena {{ grid-column:1/-1; margin:0; font-size:.85rem; color:var(--mc-siva); }}
</style>
<section class="mc-cijene" aria-label="Cijene programa">
{chr(10).join(kartice)}
  <p class="mc-napomena">Bazna cijena je cijena usluge na dan 10. 9. 2026., odnosno na dan uvođenja usluge u ponudu ako je uvedena kasnije. <a href="/cjenik">Cjenik</a></p>
</section>
"""


def cjenik_html(usluge, datoteke, sada) -> str:
    redovi = []
    for u in usluge:
        ak = u.get("akcija")
        jed = html.escape(u.get("jedinica", ""))
        c = f'{eur(ak["cijena"])}{jed} <small>({html.escape(ak["naziv"])})</small>' if ak else f"{eur(u['cijena'])}{jed}"
        redovi.append(f"<tr><td>{html.escape(u['naziv'])}</td><td>{c}</td><td>{eur(u['bazna_cijena'])}{jed}</td></tr>")
    veze = []
    for i, (broj, ts, f) in enumerate(reversed(datoteke)):
        if i == 0:
            veze.append(f'<li><a href="{f.name}" download>{f.name}</a> – važeći cjenik od {ts:%d. %m. %Y. %H:%M}</li>')
        else:
            zamijenjen = list(reversed(datoteke))[i - 1][1]
            if sada - zamijenjen <= timedelta(days=ARHIVA_DANA):
                veze.append(f'<li><a href="{f.name}" download>{f.name}</a> – arhiva, vrijedio do {zamijenjen:%d. %m. %Y. %H:%M}</li>')
    return f"""<!doctype html>
<html lang="hr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cjenik usluga – MITRA</title>
<style>
 body{{font-family:system-ui,sans-serif;color:#0B1F33;background:#fff;max-width:760px;margin:0 auto;padding:24px 16px;line-height:1.5}}
 table{{width:100%;border-collapse:collapse}} th,td{{text-align:left;padding:8px;border-bottom:1px solid #D9DEE3}}
 td:nth-child(n+2),th:nth-child(n+2){{text-align:right;white-space:nowrap}} small{{color:#5A6672}}
</style></head><body>
<h1>Cjenik usluga</h1>
<table><thead><tr><th>Usluga</th><th>Cijena</th><th>Bazna cijena</th></tr></thead>
<tbody>{"".join(redovi)}</tbody></table>
<p><small>Bazna cijena je cijena usluge na dan 10. 9. 2026., odnosno na dan uvođenja usluge u ponudu ako je uvedena kasnije.</small></p>
<h2>Cjenik za preuzimanje (CSV)</h2>
<ul>{"".join(veze)}</ul>
</body></html>
"""


def main():
    ident, usluge = ucitaj()
    IZLAZ.mkdir(exist_ok=True)
    sadrzaj = csv_sadrzaj(usluge)
    dat = postojece(ident)
    sada = datetime.now(TZ).replace(second=0, microsecond=0)
    if dat and dat[-1][2].read_text(encoding="utf-8") == sadrzaj:
        print(f"Cjenik nepromijenjen: {dat[-1][2].name}")
    else:
        broj = dat[-1][0] + 1 if dat else 1
        ime = f"{ident}_ZA_SVA_PRODAJNA_MJESTA_USLUGE_{broj}_{sada:%Y%m%d_%H%M}.csv"
        (IZLAZ / ime).write_text(sadrzaj, encoding="utf-8")
        dat.append((broj, sada, IZLAZ / ime))
        print(f"Novi cjenik: {ime}")
    (IZLAZ / "cjenik.html").write_text(cjenik_html(usluge, dat, sada), encoding="utf-8")
    (IZLAZ / "cijena-blok.html").write_text(blok_html(usluge), encoding="utf-8")
    print("Ažurirano: cjenik.html, cijena-blok.html")


if __name__ == "__main__":
    main()
