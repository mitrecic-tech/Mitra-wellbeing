// MITRA – cijena i bazna cijena (generirano: cjenik/generiraj.py, ne uređuj ručno)
// Upotreba: <PriceBlock lang="hr" /> ili <PriceBlock lang="en" />
const USLUGE = [
  {
    "naziv": {
      "hr": "MITRA Wellbeing program – mjesečna pretplata",
      "en": "MITRA Wellbeing program – monthly subscription"
    },
    "opis": {
      "hr": "12 strukturiranih treninga mjesečno (3 tjedno), video upute, praćenje opterećenja i oporavka, podrška u aplikaciji.",
      "en": "12 structured workouts a month (3 per week), video guidance, load and recovery tracking, in-app support."
    },
    "jedinica": {
      "hr": "/mj.",
      "en": "/month"
    },
    "cijena": 129.0,
    "akcija": null,
    "bazna": 129.0
  }
];

const TEKST = {
  "hr": {
    "cijena": "Cijena",
    "bazna": "Bazna cijena",
    "cjenik": "Cjenik",
    "napomena": "Bazna cijena je cijena usluge na dan 10. 9. 2026., odnosno na dan uvođenja usluge u ponudu ako je uvedena kasnije."
  },
  "en": {
    "cijena": "Price",
    "bazna": "Base price",
    "cjenik": "Price list",
    "napomena": "The base price is the price of the service on 10 September 2026, or on the day it was first offered if later."
  }
};

const CSS = `  .mc-cijene { --mc-navy:#0B1F33; --mc-siva:#5A6672; --mc-rub:#D9DEE3; --mc-poz:#fff;
    display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); color:var(--mc-navy); }
  .mc-kartica { background:var(--mc-poz); border:1px solid var(--mc-rub); border-radius:12px; padding:20px; display:flex; flex-direction:column; gap:8px; }
  .mc-kartica h3 { margin:0; font-size:1.1rem; }
  .mc-opis { margin:0; color:var(--mc-siva); font-size:.95rem; }
  .mc-cijena, .mc-bazna { margin:0; display:flex; justify-content:space-between; align-items:baseline; gap:12px; }
  .mc-cijena { margin-top:auto; padding-top:12px; border-top:1px solid var(--mc-rub); }
  .mc-cijena strong { font-size:1.5rem; }
  .mc-bazna { font-size:.95rem; color:var(--mc-siva); }
  .mc-oznaka { font-size:.85rem; text-transform:uppercase; letter-spacing:.04em; }
  .mc-napomena { grid-column:1/-1; margin:0; font-size:.85rem; color:var(--mc-siva); }`;

const iznos = (x, lang) =>
  new Intl.NumberFormat(lang === "en" ? "en-IE" : "hr-HR", { style: "currency", currency: "EUR" }).format(x);

export default function PriceBlock({ lang = "hr" }) {
  const t = TEKST[lang] ?? TEKST.hr;
  return (
    <section className="mc-cijene" aria-label={t.cijena}>
      <style>{CSS}</style>
      {USLUGE.map((u) => (
        <article className="mc-kartica" key={u.naziv.hr}>
          <h3>{u.naziv[lang] || u.naziv.hr}</h3>
          {u.opis[lang] && <p className="mc-opis">{u.opis[lang]}</p>}
          <p className="mc-cijena">
            <span className="mc-oznaka">{u.akcija ?? t.cijena}</span>
            <strong>{iznos(u.cijena, lang)}{u.jedinica[lang]}</strong>
          </p>
          <p className="mc-bazna">
            <span className="mc-oznaka">{t.bazna}</span>
            <span>{iznos(u.bazna, lang)}{u.jedinica[lang]}</span>
          </p>
        </article>
      ))}
      <p className="mc-napomena">{t.napomena} <a href="/cjenik/">{t.cjenik}</a></p>
    </section>
  );
}
