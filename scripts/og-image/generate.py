#!/usr/bin/env python3
"""Regenerate assets/og-image-{lang}.png from template.html via headless Chrome.

Usage: python3 scripts/og-image/generate.py [lang ...]
       (no args = regenerate all languages)

Content per language is defined in CONTENT below. Edit it, then rerun.
"""
import io
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
ASSETS_DIR = REPO_ROOT / "assets"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CONTENT = {
    "de": dict(
        HEADLINE="Die ersten drei Tage schafft jeder.",
        SUBTEXT="Monats-Challenge-Tracker für iPhone. Kein Account, kein Tracking, keine Werbung.",
        SCREENSHOT="screenshot-heute-de.webp",
    ),
    "en": dict(
        HEADLINE="Everyone makes it three days.",
        SUBTEXT="Monthly challenge tracker for iPhone. No account, no tracking, no ads.",
        SCREENSHOT="screenshot-heute-en.webp",
    ),
    "es": dict(
        HEADLINE="Los primeros tres días los aguanta cualquiera.",
        SUBTEXT="Seguimiento de challenges mensuales para iPhone. Sin cuenta, sin tracking, sin anuncios.",
        SCREENSHOT="screenshot-heute-es.webp",
    ),
    "fr": dict(
        HEADLINE="Les trois premiers jours, tout le monde y arrive.",
        SUBTEXT="Suivi de challenges mensuels pour iPhone. Sans compte, sans tracking, sans pub.",
        SCREENSHOT="screenshot-heute-fr.webp",
    ),
}


def render(lang: str, data: dict) -> None:
    template = (SCRIPT_DIR / "template.html").read_text(encoding="utf-8")
    for key, value in data.items():
        template = template.replace("{{" + key + "}}", value)

    html_path = SCRIPT_DIR / f"_render-{lang}.html"
    html_path.write_text(template, encoding="utf-8")

    out_path = ASSETS_DIR / f"og-image-{lang}.png"
    subprocess.run(
        [
            CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
            "--window-size=1200,630",
            f"--screenshot={out_path}",
            f"file://{html_path}",
        ],
        check=True,
        capture_output=True,
    )
    html_path.unlink()
    print(f"{lang}: wrote {out_path}")


def main() -> None:
    langs = sys.argv[1:] or list(CONTENT)
    for lang in langs:
        if lang not in CONTENT:
            print(f"no content defined for '{lang}', skipping", file=sys.stderr)
            continue
        render(lang, CONTENT[lang])


if __name__ == "__main__":
    main()
