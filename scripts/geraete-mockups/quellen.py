#!/usr/bin/env python3
"""Holt die Screenshots aus dem App-Repo nach assets/.

Ersetzt screenshots/website/uebertragen-website.sh aus dem App-Repo, das an
zwei Stellen nicht mehr passt: Es kennt nur fünf Sprachen (inzwischen sind es
neun) und sucht die Uhr-Motive unter screenshots/appstore/watch/, während sie
unter screenshots/aufnahmen/watch/ liegen.

Besonderheit beim Motiv "fertig": Der Screenshot fängt einen Scroll-Zustand
ein, unten ragt der Button „Liste anzeigen" mitten durch seine Beschriftung ins
Bild und liest sich auf der Website wie ein Renderfehler. Der Bereich darunter
ist reines Schwarz wie der App-Hintergrund, deshalb wird er aufgefüllt.

Wichtig: Die Schnittkante darf NICHT fest verdrahtet werden. Der Text darüber
ist je Sprache verschieden lang, im Französischen etwa 45 px länger als im
Deutschen - eine feste Kante schnitt dort mitten in den Satz. Sie wird deshalb
je Bild gesucht.

Sauberer wäre eine Neuaufnahme ohne den angeschnittenen Button.

    python3 scripts/geraete-mockups/watch-quellen.py
"""
from PIL import Image
import pathlib
import sys

WATCH = pathlib.Path.home() / '12c/screenshots/aufnahmen/watch'
PHONE = pathlib.Path.home() / '12c/screenshots/website'
ZIEL = pathlib.Path(__file__).resolve().parents[2] / 'assets'

MOTIVE = {
    'checkin': '01_erledigt',           # eine Challenge, großer Erledigt-Knopf
    'liste':   '02_heute',              # Tagesliste mehrerer Challenges
    'fertig':  '03_alles_geschafft',    # „Für heute geschafft!"
}

# Website-Dateiname zu Motiv im Generator. Die Website bindet die Dark-Mode-
# Aufnahmen ein, der Generator legt sie unter <sprache>_dark ab.
MOTIVE_PHONE = {
    'heute':      '02_heute',
    'streak':     '01_allesgeschafft',
    'detail':     '03_detail',
    'challenges': '04_challenges',
    'archiv':     '05_archiv',
    'reminder':   'extra_erinnerungszeit',
    'erfolge':    'extra_erfolge',
    'statistiken': '06_statistiken',
}

SPRACHEN = ('de', 'en', 'fr', 'es', 'pt', 'it', 'tr', 'pl', 'el')


def button_oberkante(im: Image.Image) -> int | None:
    """Oberkante des grauen Buttons am unteren Bildrand.

    Von unten nach oben gesucht: Der Button ist eine durchgehende graue Fläche,
    Text darüber ist heller und deckt nie die ganze Breite ab.
    """
    b, h = im.size
    treffer = None
    for y in range(h - 1, h // 2, -1):
        grau = sum(1 for x in range(60, b - 60, 2)
                   if 45 <= sum(im.getpixel((x, y))) / 3 <= 80)
        if grau > (b - 120) / 2 * 0.6:
            treffer = y
        elif treffer is not None:
            return treffer
    return treffer


def main() -> None:
    if not WATCH.exists():
        sys.exit(f'Quellordner fehlt: {WATCH}')

    print('iPhone-Motive:')
    for lang in SPRACHEN:
        for name, motiv in MOTIVE_PHONE.items():
            q = PHONE / f'{lang}_dark' / f'{motiv}.png'
            if not q.exists():
                print(f'  fehlt: {q.relative_to(PHONE.parent)}')
                continue
            im = Image.open(q).convert('RGB')
            t = ZIEL / f'screenshot-{name}-{lang}.webp'
            im.save(t, 'WEBP', quality=90, method=6)
    print(f'  {len(SPRACHEN) * len(MOTIVE_PHONE)} Bilder geschrieben')

    print('\nUhr-Motive:')
    for lang in SPRACHEN:
        for name, motiv in MOTIVE.items():
            q = WATCH / lang / f'{motiv}.png'
            if not q.exists():
                print(f'  fehlt: {q.relative_to(WATCH.parent)}')
                continue
            im = Image.open(q).convert('RGB')

            if name == 'fertig':
                kante = button_oberkante(im)
                if kante:
                    im.paste((0, 0, 0), (0, kante - 2, im.width, im.height))
                    hinweis = f'  Button ab y={kante} geschwärzt'
                else:
                    hinweis = '  kein Button gefunden, unverändert'
            else:
                hinweis = ''

            t = ZIEL / f'screenshot-watch-{name}-{lang}.webp'
            im.save(t, 'WEBP', quality=90, method=6)
            print(f'  {t.name:34} {im.size}  {t.stat().st_size // 1024} KB{hinweis}')

    print('\nDanach rendern.py laufen lassen, damit assets/mock/ nachzieht.')


if __name__ == '__main__':
    main()
