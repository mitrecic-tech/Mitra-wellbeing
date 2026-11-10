# MITRA – znak (4. krug: jednostavno)

Cilj: jedan jednostavan znak koji se pamti na prvi pogled i radi u jednoj boji, na majici, kapi, opremi i kao ikona aplikacije, uz čvrst logotip MITRA.

| Znak | Ideja |
|---|---|
| **Zamah** | nagnuto slovo *i* iz imena MITRA, ujedno čovjek nagnut naprijed u pokretu; izvedeno iz dijagonale i točke postojeće oznake |
| **Vrh** | jedan šiljak i točka: čovjek koji čvrsto stoji, vrh, slovo A |
| **Blok** | puni blok s V-urezom odozgo, slovo M koje se može izvesti na bilo čemu |
| **Dva luka** | dva luka s glavama: slovo m i dvoje ljudi jedno uz drugo (*mitra* = prijatelj) |

Datoteke u `svg/` (tekst pretvoren u krivulje):
`mitra-<znak>-znak-*`, `-logo-*` (vodoravno), `-vertikalni-*`, u varijantama `crni`, `bijeli`, `navy`, te `-ikona.svg` (512 px).

Ponovno generiranje (Manrope, Google Fonts):

```bash
pip install fonttools
cd brand/logo/src
FONT_DIR=/put/do/fontova python3 build.py ../svg
```
