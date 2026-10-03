#!/usr/bin/env python3
"""Lokalisierte Komplikations-Mockups mit dem vorhandenen echten Watch-Bezel.

Benötigt Pillow, Node.js und Playwright (oder WATCH_PLAYWRIGHT_MODULE).
Aufruf: python3 scripts/geraete-mockups/watch-complications.py <bezel.png> en es fr ...
Nur fertige Mockups werden veröffentlicht; die Bezel-Quelle bleibt außerhalb des Repos.
"""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from PIL import Image
import subprocess
import sys
import tempfile
from rendern import karte, FENSTER, BREITE, QUALITAET

ROOT = Path(__file__).resolve().parents[2]
KINDS = ('single', 'single-done', 'progress', 'done', 'streak')


def composite(args):
    source, bezel, target = args
    with Image.open(source) as image:
        mockup = karte(image, Path(bezel), FENSTER['watch'], BREITE['watch'])
        mockup.save(target, 'WEBP', quality=QUALITAET, method=4)
    return Path(target).name


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    bezel, languages = sys.argv[1], sys.argv[2:]
    with tempfile.TemporaryDirectory(prefix='12c-watch-complications-') as temporary:
        subprocess.run(['node', str(Path(__file__).with_suffix('.cjs')), temporary, *languages], check=True)
        jobs = [(str(Path(temporary) / f'{kind}-{lang}.png'), bezel,
                 str(ROOT / 'assets/mock' / f'watch-complication-{kind}-{lang}.webp'))
                for lang in languages for kind in KINDS]
        with ProcessPoolExecutor(max_workers=4) as pool:
            for name in pool.map(composite, jobs):
                print(name, flush=True)


if __name__ == '__main__':
    main()
