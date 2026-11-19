# Briefing

Tägliches Morgen-Briefing als Web-App (für iPhone und Mac).

- **App:** `index.html` (Darstellung), `sw.js` (Offline & Aktualisierung), `manifest.webmanifest`, `icons/`
- **Daten:** `data/JJJJ-MM-TT.json` je Ausgabe, `data/index.json` (Archiv), `data/search.json` (Suche)
- **Automatik:** Eine geplante Claude-Aufgabe recherchiert jeden Morgen nach `ANLEITUNG.md`, schreibt die Tagesdatei, prüft sie mit `scripts/publish.py` und lädt sie hoch. GitHub Pages veröffentlicht automatisch.

Auf dem iPhone: Seite in Safari öffnen → Teilen → „Zum Home-Bildschirm“.
