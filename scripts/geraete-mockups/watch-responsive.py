#!/usr/bin/env python3
"""Erzeugt kleinere WebP-Varianten für die deutsche Watch-Themenseite.

Aufruf: python3 scripts/geraete-mockups/watch-responsive.py
Die Original-Mockups bleiben erhalten; andere Seiten verwenden sie unverändert.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets' / 'mock'
OUTPUT = SOURCE / 'watch-page'
WATCH_NAMES = (
    'watch-checkin-de', 'watch-liste-de', 'watch-fertig-de',
    'watch-complication-single-de', 'watch-complication-single-done-de',
    'watch-complication-progress-de', 'watch-complication-done-de',
    'watch-complication-streak-de',
)


def main():
    OUTPUT.mkdir(exist_ok=True)
    for name in (*WATCH_NAMES, 'detail-de'):
        widths = (240, 380, 570) if name == 'detail-de' else (260, 390, 520)
        with Image.open(SOURCE / f'{name}.webp') as original:
            for width in widths:
                height = round(original.height * width / original.width)
                image = original.resize((width, height), Image.Resampling.LANCZOS)
                target = OUTPUT / f'{name}-{width}.webp'
                image.save(target, 'WEBP', quality=82, method=6)
                print(f'{target.name}: {target.stat().st_size:,} Bytes')


if __name__ == '__main__':
    main()
