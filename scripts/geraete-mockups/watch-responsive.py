#!/usr/bin/env python3
"""Kleinere WebP-Varianten für die Watch-Themenseiten.

Aufruf: python3 scripts/geraete-mockups/watch-responsive.py [de en es fr ...]
Ohne Sprachargument wird nur Deutsch erzeugt. Benötigt Pillow.
Die Original-Mockups bleiben erhalten; andere Seiten verwenden sie unverändert.
"""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from PIL import Image
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets/mock'
OUTPUT = SOURCE / 'watch-page'
NAMES = ('watch-checkin', 'watch-liste', 'watch-fertig',
         'watch-complication-single', 'watch-complication-single-done',
         'watch-complication-progress', 'watch-complication-done',
         'watch-complication-streak', 'detail')


def resize(args):
    name, width = args
    with Image.open(SOURCE / f'{name}.webp') as original:
        height = round(original.height * width / original.width)
        image = original.resize((width, height), Image.Resampling.LANCZOS)
        target = OUTPUT / f'{name}-{width}.webp'
        image.save(target, 'WEBP', quality=82, method=4)
    return f'{target.name}: {target.stat().st_size:,} Bytes'


def main():
    OUTPUT.mkdir(exist_ok=True)
    jobs = [(f'{name}-{lang}', width) for lang in (sys.argv[1:] or ['de']) for name in NAMES
            for width in ((240, 380, 570) if name == 'detail' else (260, 390, 520))]
    with ProcessPoolExecutor(max_workers=4) as pool:
        for result in pool.map(resize, jobs):
            print(result, flush=True)


if __name__ == '__main__':
    main()
