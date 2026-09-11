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
        SCREENSHOT="mock/heute-de.webp",
    ),
    "en": dict(
        HEADLINE="Everyone makes it three days.",
        SUBTEXT="Monthly challenge tracker for iPhone. No account, no tracking, no ads.",
        SCREENSHOT="mock/heute-en.webp",
    ),
    "es": dict(
        HEADLINE="Los primeros tres días los aguanta cualquiera.",
        SUBTEXT="Seguimiento de challenges mensuales para iPhone. Sin cuenta, sin tracking, sin anuncios.",
        SCREENSHOT="mock/heute-es.webp",
    ),
    "fr": dict(
        HEADLINE="Les trois premiers jours, tout le monde y arrive.",
        SUBTEXT="Suivi de challenges mensuels pour iPhone. Sans compte, sans tracking, sans pub.",
        SCREENSHOT="mock/heute-fr.webp",
    ),
    "it": dict(
        HEADLINE="I primi tre giorni li regge chiunque.",
        SUBTEXT="Tracker di challenge mensili per iPhone. Senza account, senza tracciamento, senza pubblicità.",
        SCREENSHOT="mock/heute-it.webp",
    ),
    "tr": dict(
        HEADLINE="İlk üç günü herkes götürür.",
        SUBTEXT="iPhone için aylık challenge takibi. Hesap yok, takip yok, reklam yok.",
        SCREENSHOT="mock/heute-tr.webp",
    ),
    "pl": dict(
        HEADLINE="Pierwsze trzy dni wytrzyma każdy.",
        SUBTEXT="Śledzenie miesięcznych challenge’ów na iPhone’a. Bez konta, bez śledzenia, bez reklam.",
        SCREENSHOT="mock/heute-pl.webp",
    ),
    "el": dict(
        HEADLINE="Τις πρώτες τρεις μέρες τις βγάζει ο καθένας.",
        SUBTEXT="Παρακολούθηση μηνιαίων challenges για iPhone. Χωρίς λογαριασμό, χωρίς παρακολούθηση, χωρίς διαφημίσεις.",
        SCREENSHOT="mock/heute-el.webp",
    ),
    "pt": dict(
        HEADLINE="Os primeiros três dias qualquer um aguenta.",
        SUBTEXT="Acompanhamento de challenges mensais para iPhone. Sem conta, sem tracking, sem anúncios.",
        SCREENSHOT="mock/heute-pt.webp",
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
