#!/usr/bin/env python3
"""Setzt die App-Screenshots in die echten Apple-Gerätrahmen und legt die
fertigen Mock-ups als WebP unter assets/mock/ ab.

Warum fertige Bilder und nicht wie früher per CSS gezeichnete Rahmen: siehe
README.md in diesem Ordner. Kurz: Die Apple-Design-Resources-Lizenz erlaubt
Mock-ups der eigenen App und deren Abbildung, untersagt aber die Weitergabe der
Rahmendateien. Auf einem Webserver wäre ein Bezel-PNG für jeden herunterladbar,
ein fertiges Mock-up ist es nicht. Deshalb gehören die Rahmen NICHT in dieses
Repo, nur ihr Ergebnis.

Aufruf (Rahmen liegen im App-Repo, siehe README):
    python3 scripts/geraete-mockups/rendern.py \
        "<pfad>/iPhone 17 Pro Max - Deep Blue - Portrait.png" \
        "<pfad>/Apple Watch S11 - 46mm - Aluminum Jet Black + Sport Band Black.png"

Optional eine Sprachliste anhängen, sonst laufen alle fünf:
    ... de en
"""
from PIL import Image
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
ASSETS = REPO / 'assets'
AUSGABE = ASSETS / 'mock'

# Displayfenster im jeweiligen Rahmen: links, oben, rechts, unten.
# Ausgemessen über den Alphakanal; die Werte decken sich mit denen in
# 12c/screenshots/store-bilder/erzeugen.py. Achtung beim Nachmessen des
# iPhones: Die Dynamic Island ist im Rahmen NICHT transparent, eine Messspalte
# durch die Bildmitte liefert deshalb einen um rund 150 px zu tiefen oberen
# Rand. Neben der Insel messen.
FENSTER = {
    'phone': (75, 66, 1395, 2934),   # 1320x2868, iPhone 17 Pro Max
    'watch': (72, 192, 488, 688),    # 416x496,   Apple Watch S11 46 mm
}

# Gehäusebreiten laut Apple, in Millimetern. Nur dafür da, iPhone und Uhr im
# Hero maßstabsgetreu zueinander zu setzen: Die Breite eines Bezel-PNG
# entspricht der Gehäusebreite, das Verhältnis 39,7/78 ergibt also direkt den
# Faktor für die Uhr. Nach Augenmaß gewählte Größen sehen sofort falsch aus.
GEHAEUSE_MM = {'phone': 78.0, 'watch': 39.7}

# Ausgabebreite: das Dreifache der größten CSS-Breite (iPhone 312 px im Hero,
# Uhr 254 px in der Galerie). Damit stimmt es auf Displays mit dreifacher
# Pixeldichte pixelgenau, also auf jedem aktuellen iPhone. Mit dem früheren
# Wert von 620 px musste der Browser dort hochrechnen, was an feinen Stellen
# wie der Datumszeile sichtbar weicher aussah.
# Wer die Breiten in styles.css ändert, muss diese Werte mitziehen - und die
# width/height-Attribute im HTML, die unten ausgegeben werden.
BREITE = {'phone': 940, 'watch': 780}

# WebP-Qualität. Im direkten Vergleich bei fünffacher Vergrößerung war zwischen
# 88 und 72 kein Unterschied auszumachen; 82 spart gegenüber 88 rund 15 % und
# liegt weit genug von der Kante entfernt, dass auch Verläufe sauber bleiben.
# Die Schärfe kommt aus der Auflösung oben, nicht aus dieser Stufe.
QUALITAET = 82

MOTIVE = {
    'phone': ['heute', 'streak', 'detail', 'challenges', 'erfolge', 'reminder', 'archiv',
              'statistiken'],
    'watch': ['checkin', 'liste', 'fertig'],
}

SPRACHEN = ('de', 'en', 'fr', 'es', 'pt', 'it', 'tr', 'pl', 'el')


def karte(schuss: Image.Image, rahmen_datei: pathlib.Path, fenster, breite: int) -> Image.Image:
    """Screenshot hinter den Rahmen setzen und auf `breite` bringen.

    Der Screenshot kommt hinter das Bezel, nicht darauf: Das PNG hat an der
    Stelle des Displays ein transparentes Fenster, genau dort wird eingesetzt.
    Erst das fertige Ganze wird skaliert, damit der Rahmen scharf bleibt.
    """
    rahmen = Image.open(rahmen_datei).convert('RGBA')
    x1, y1, x2, y2 = fenster
    bild = schuss.convert('RGB')
    if bild.size != (x2 - x1, y2 - y1):
        bild = bild.resize((x2 - x1, y2 - y1), Image.LANCZOS)
    ganz = Image.new('RGBA', rahmen.size, (0, 0, 0, 0))
    ganz.paste(bild, (x1, y1))
    ganz.alpha_composite(rahmen)
    hoehe = round(rahmen.height * breite / rahmen.width)
    return ganz.resize((breite, hoehe), Image.LANCZOS)


def quelle(geraet: str, motiv: str, lang: str) -> pathlib.Path:
    """Die rahmenlosen Screenshots, die auch ohne Mock-up im Repo liegen."""
    name = f'screenshot-{motiv}-{lang}.webp' if geraet == 'phone' \
        else f'screenshot-watch-{motiv}-{lang}.webp'
    return ASSETS / name


def main(phone_bezel: str, watch_bezel: str, sprachen=SPRACHEN) -> None:
    rahmen = {'phone': pathlib.Path(phone_bezel), 'watch': pathlib.Path(watch_bezel)}
    for geraet, datei in rahmen.items():
        if not datei.exists():
            sys.exit(f'Rahmen fehlt: {datei}\nSiehe README.md in diesem Ordner.')

    AUSGABE.mkdir(exist_ok=True)
    fehlend, geschrieben = [], 0

    for geraet, motive in MOTIVE.items():
        for lang in sprachen:
            for motiv in motive:
                q = quelle(geraet, motiv, lang)
                if not q.exists():
                    fehlend.append(q.name)
                    continue
                k = karte(Image.open(q), rahmen[geraet], FENSTER[geraet], BREITE[geraet])
                ziel = AUSGABE / (f'{motiv}-{lang}.webp' if geraet == 'phone'
                                  else f'watch-{motiv}-{lang}.webp')
                k.save(ziel, 'WEBP', quality=QUALITAET, method=6)
                print(f'  {ziel.name:26} {k.size}  {ziel.stat().st_size // 1024} KB')
                geschrieben += 1

    faktor = GEHAEUSE_MM['watch'] / GEHAEUSE_MM['phone']
    print(f'\n{geschrieben} Mock-ups geschrieben nach {AUSGABE.relative_to(REPO)}/')
    # Aus dem Rahmen gerechnet, nicht aus einer Datei im Zielordner gelesen:
    # dort können noch Bilder eines früheren Laufs mit anderer Breite liegen.
    for geraet, kuerzel in (('phone', 'mock-phone'), ('watch', 'mock-watch')):
        rb, rh = Image.open(rahmen[geraet]).size
        b = BREITE[geraet]
        print(f'HTML-Attribute für .{kuerzel}: width="{b}" height="{round(rh * b / rb)}"')
    print(f'Maßstab Uhr zu iPhone: {faktor:.3f} (steckt als 0.509 in --hero-watch-w, styles.css)')
    if fehlend:
        print('\nOhne Quelle übersprungen:')
        for f in sorted(set(fehlend)):
            print('  ' + f)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], tuple(sys.argv[3:]) or SPRACHEN)
