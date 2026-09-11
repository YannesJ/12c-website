# Gerätemockups für die Website

Die iPhones und Apple Watches auf der Startseite sind **fertig gerenderte
Bilder**: der App-Screenshot sitzt im echten Apple-Produktrahmen, beides in
einer Datei. Sie liegen unter `assets/mock/` und entstehen mit
`rendern.py` aus diesem Ordner.

Vorher zeichnete das Stylesheet die Geräte selbst nach, als abgerundete
Rechtecke mit CSS (`.phone-frame`, `.watch-frame`). Das sieht man den Uhren an:
ohne Beschriftung daneben war die Silhouette nicht als Apple Watch erkennbar.

## Warum Bilder und nicht die Rahmendateien auf dem Server

Die Rahmen stammen aus den **Apple Design Resources** (Product Bezels). Deren
Lizenz erlaubt ausdrücklich Mock-ups der eigenen App und das Zeigen dieser
Mock-ups in Bildern. Sie untersagt aber die Weitergabe der Rahmendateien
selbst.

Für eine Website heißt das: Ein Bezel-PNG im `assets/`-Ordner wäre für jeden
Besucher herunterladbar, also weitergegeben. Ein fertiges Mock-up ist es nicht,
dort steckt der Rahmen im Bild.

**Die Bezel-PNGs gehören deshalb nicht in dieses Repo.** Sie liegen im App-Repo
unter `12c/screenshots/store-bilder/bezels/` und sind dort per `.gitignore`
ausgenommen, aus demselben Grund. Wer neu aufsetzt, lädt sie einmalig von
<https://developer.apple.com/design/resources/>, Abschnitt Product Bezels: das
Paket `Bezel-iPhone-17.dmg` und `Bezel-Apple-Watch-Series-11-2025.dmg`.

Aus den Paketen werden genau zwei Dateien gebraucht, unter diesen Namen
abgelegt:

| aus dem Paket | Name im bezels-Ordner |
|---|---|
| `iPhone 17 Pro Max - Deep Blue - Portrait.png` | `iphone-17-pro-max-deep-blue.png` |
| `Apple Watch S11 - 46mm - Aluminum Jet Black + Sport Band Black.png` | `watch-s11-46mm-jetblack-sportband.png` |

Die Pakete sind zusammen knapp 600 MB, die beiden Dateien daraus unter 1 MB.
Wer sie nur in einem Temp-Ordner entpackt, lädt beim nächsten Satz erneut alles
herunter, deshalb gehören sie dauerhaft in den `bezels`-Ordner.

## Welche Rahmen im Einsatz sind

| Gerät | Datei aus dem Apple-Paket |
|---|---|
| iPhone | `iPhone 17 Pro Max - Deep Blue - Portrait.png` |
| Apple Watch | `Apple Watch S11 - 46mm - Aluminum Jet Black + Sport Band Black.png` |

Beides bewusst die dunklen Ausführungen. Auf dem fast schwarzen Seitenhintergrund
fällt ein silbernes Gehäuse als heller Block auf, und das Champagner-Milanaise-
Armband, mit dem die Auswahl anfing, zieht die Aufmerksamkeit vom Display weg.
Die Pakete enthalten weitere Farben und Armbänder, ein Wechsel ist ein erneuter
Lauf von `rendern.py` mit anderen Pfaden, sonst nichts.

## Displayfenster

Das Bezel-PNG hat an der Stelle des Displays ein transparentes Fenster, dort
wird der Screenshot eingesetzt. Die Maße:

| Gerät | Fenster (l, o, r, u) | Größe |
|---|---|---|
| iPhone 17 Pro Max | `(75, 66, 1395, 2934)` | 1320 x 2868 |
| Apple Watch 46 mm | `(72, 192, 488, 688)` | 416 x 496 |

Die Werte decken sich mit denen in `12c/screenshots/store-bilder/erzeugen.py`,
das die App-Store-Bilder auf demselben Weg baut.

**Falle beim Nachmessen des iPhones:** Die Dynamic Island ist im Rahmen nicht
transparent. Wer den Alphakanal in der Bildmitte abtastet, findet den oberen
Rand deshalb rund 150 px zu tief. Neben der Insel messen, etwa 150 px rechts der
linken Fensterkante.

Alle Watch-Varianten des Pakets teilen sich dasselbe Fenster, ein Wechsel des
Armbands ändert an der Geometrie also nichts.

## Größenverhältnis von Uhr und iPhone

Im Hero stehen beide Geräte nebeneinander. Damit das Verhältnis stimmt, zählen
die echten Gehäusebreiten: iPhone 78 mm, Apple Watch 46 mm Gehäuse 39,7 mm.
Die Breite eines Bezel-PNG entspricht der Gehäusebreite, der Faktor ist also

    39,7 / 78 = 0,509

und steckt in `styles.css` als `--hero-watch-w: calc(var(--phone-w) * 0.509)`.
Der frühere CSS-Nachbau lag mit 0,46 zu klein, was man nicht sah, solange die
Uhr keine erkennbare Uhr war.

## Auflösung und Kompression

Ausgabebreite 940 px für iPhones, 780 px für Uhren, bei WebP-Qualität 82.

Das ist das **Dreifache** der größten Darstellung (Hero-iPhone 312 px, Uhren in
der Galerie 254 px) und damit pixelgenau auf Displays mit dreifacher
Pixeldichte, also auf jedem aktuellen iPhone. Ein früherer Anlauf mit dem
Doppelten sah dort an feinen Stellen sichtbar weicher aus, etwa an der
Datumszeile unter „Heute".

Die Qualitätsstufe stammt aus einem direkten Vergleich: Zwischen 88 und 72 war
bei fünffacher Vergrößerung kein Unterschied auszumachen, 82 spart gegenüber 88
rund 15 %. Die Schärfe kommt aus der Auflösung, nicht aus dieser Stufe.

**Wer die Breiten in `styles.css` ändert, muss drei Stellen mitziehen:** die
Werte in `BREITE` hier, und die `width`/`height`-Attribute an den Bildern im
HTML aller fünf Sprachen. Die passenden Attributwerte gibt das Skript am Ende
seines Laufs aus.

## Darstellungsgröße

Hero 312 px, Bild-Text-Zeilen 280 px, Galerie 257 px, Uhren-Galerie 254 px.

Diese Werte liegen 6 % über denen der früheren CSS-Nachbauten, und das ist
Absicht: Beim Nachbau war der Rahmen eine dünne Linie, beim echten Bezel ist es
ein sichtbares Gehäuse. Bei gleicher Außenbreite bleiben dadurch 1,5 % weniger
Display übrig, und der sichtbare Rand lässt es zusätzlich kleiner wirken. Mit
den 6 % steht der App-Inhalt etwas größer da als in der alten Fassung.

## Quellen und Aufruf

Als Quelle dienen die rahmenlosen Screenshots, die ohnehin unter `assets/`
liegen (`screenshot-*.webp`). **Die bleiben im Repo**, auch wenn die Seite sie
nicht mehr direkt einbindet: Ohne sie lässt sich kein Mock-up neu bauen.

```sh
BEZELS=~/12c/screenshots/store-bilder/bezels
python3 scripts/geraete-mockups/rendern.py \
    "$BEZELS/iphone-17-pro-max-deep-blue.png" \
    "$BEZELS/watch-s11-46mm-jetblack-sportband.png"
```

Ohne weitere Angaben laufen alle fünf Sprachen, sonst die genannten anhängen
(`... de en`).

## Die Watch-Quellen

Die iPhone-Motive kommen wie bisher über `uebertragen-website.sh` aus dem
App-Repo. Für die Uhr geht das dort nicht mehr verlässlich, deshalb liegt
daneben `quellen.py`, das beide Geräte für alle neun Sprachen holt: die
iPhone-Motive aus `12c/screenshots/website/<sprache>_dark/`, die Uhr-Motive aus
`12c/screenshots/aufnahmen/watch/<sprache>/`.

Es erledigt dabei eine Retusche: Das Motiv „fertig" fängt einen Scroll-Zustand
ein, unten ragt der Knopf „Liste anzeigen" mitten durch seine Beschriftung ins
Bild. Der Bereich darunter ist reines Schwarz wie der App-Hintergrund und wird
aufgefüllt.

**Die Schnittkante darf nicht fest verdrahtet werden.** Der Text darüber ist je
Sprache verschieden lang, im Französischen rund 45 px länger als im Deutschen.
Eine feste Kante schnitt dort mitten in den Satz, und zwar unauffällig genug,
dass es erst beim Durchsehen der fertigen Seite auffiel. Das Skript sucht die
Oberkante des Knopfes deshalb in jedem Bild einzeln: Von unten nach oben wird
die erste Zeile gesucht, die über die Breite hinweg durchgehend Knopf-Grau
zeigt; Text ist heller und deckt nie die volle Breite ab.

Sauberer als jede Retusche wäre eine Neuaufnahme ohne den angeschnittenen Knopf.

## Wenn neue Screenshots kommen

1. Im App-Repo aufnehmen.
2. `quellen.py` laufen lassen, es holt iPhone- und Uhr-Motive nach `assets/`.
3. `rendern.py` laufen lassen, damit `assets/mock/` nachzieht.

Zwei Dinge, die beim Übertragungsskript aufgefallen sind und dort noch offen
sind: Es sucht die Watch-Motive unter `screenshots/appstore/watch/`, sie liegen
aber unter `screenshots/aufnahmen/watch/`. Und die Motivnamen in seiner
Zuordnungstabelle passen zu `screenshots/aufnahmen/iphone-6.9/`, nicht zum
Ordner `screenshots/website/`, auf den es zeigt.
