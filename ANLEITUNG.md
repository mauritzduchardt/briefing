# Morgen-Briefing – Arbeitsanweisung

Diese Datei ist die verbindliche Anweisung für den täglichen automatischen Lauf. Niemand schaut zu: keine Rückfragen stellen, nach diesen Regeln entscheiden.

## Ziel

Mauritz liest das Briefing morgens auf dem iPhone (manchmal auf dem MacBook). In unter 5 Minuten soll er über alles Wichtige Bescheid wissen – Welt, Deutschland, Frankfurt/Hessen, Wirtschaft, Tech und seine Geldanlage. Tippt er eine Meldung an, versteht er sie in wenigen Sätzen vollständig. Ton: nüchtern, neutral, sachlich, verständlich. Keine Meinung, keine Wertung.

Du lieferst **nur Daten** (eine JSON-Datei). Design und Darstellung macht die App – nichts an `index.html`, `sw.js`, `manifest.webmanifest`, `icons/` oder `scripts/` ändern.

## Ablauf

1. **Repository holen:** Das Repository ist bereits geklont (siehe Aufgabe). Arbeitsverzeichnis = Repository-Wurzel.
2. **Datum:** heutiges Datum in Europe/Berlin (`TZ=Europe/Berlin date +%F`).
3. **Vorige Ausgaben lesen:** `data/index.json` und die letzten 3 Tagesdateien `data/JJJJ-MM-TT.json`. Zweck: Dopplungen vermeiden und laufende Lagen weiterverfolgen (siehe unten).
4. **Recherche** nach den Regeln unten (Zeitraum: die letzten 24 Stunden, bei Märkten der letzte Handelstag und die Nacht).
5. **Entwurf schreiben:** `/tmp/briefing.json` im Format unten.
6. **Prüfen und veröffentlichen:** `python3 scripts/publish.py /tmp/briefing.json`
   - Meldet das Skript FEHLER: Entwurf korrigieren und erneut ausführen, bis es durchläuft.
   - „Hinweis“-Zeilen sind Warnungen: prüfen, ob sie berechtigt sind; meist kurz nachbessern.
7. **Hochladen:**
   ```
   git add data/
   git commit -m "Briefing JJJJ-MM-TT"
   git push
   ```
   Schlägt `git push` fehl: `git pull --rebase` und erneut pushen. Gibt es schon eine Datei für heute, wird sie überschrieben (das ist gewollt).
8. **Abschluss:** eine kurze Antwort auf Deutsch (Anzahl Meldungen, Besonderheiten). Konnte nicht veröffentlicht werden: `PushNotification` mit dem Grund in einem Satz.

Lieber eine etwas kleinere, aber geprüfte Ausgabe veröffentlichen als gar keine. Was sich nicht verlässlich belegen lässt, weglassen.

## Quellen

Nur Primär- und Qualitätsmedien:

- **Politik & Welt:** NZZ (bevorzugt), Reuters, Bloomberg, FAZ, Süddeutsche Zeitung, Tagesschau, Politico Europe
- **Frankfurt / Hessen:** FAZ (Rhein-Main), Hessenschau, Frankfurter Rundschau
- **Wirtschaft & Finanzen:** Handelsblatt, Financial Times, Bloomberg, The Economist, Wirtschaftswoche
- **Tech & KI:** heise online, Ars Technica, MIT Technology Review, TechCrunch, The Verge

Regeln:
- Keine Boulevard-Medien, keine Pressemitteilungen, kein Clickbait, keine unbestätigten Social-Media-Meldungen.
- Bei politisch umstrittenen Themen mindestens zwei Medien mit unterschiedlicher Ausrichtung lesen (z. B. NZZ und Süddeutsche/Tagesschau) und die Fakten neutral wiedergeben.
- Relevante Themen, über die deutsche Leitmedien wenig berichten (häufig bei der NZZ zu finden), aktiv aufnehmen.
- Zahlen möglichst in zwei Quellen gegenprüfen.

**Links (wichtig):**
- Jede Quelle verlinkt direkt den konkreten Artikel – nie eine Startseite oder Ressortseite.
- Nur Adressen verwenden, die wörtlich in einem Suchergebnis oder einer abgerufenen Seite vorkamen. **Nie eine Adresse selbst zusammenbauen oder raten.**
- Lässt sich eine Seite nicht abrufen (Paywall), ist die Adresse aus dem Suchergebnis in Ordnung, wenn Titel und Inhalt zur Meldung passen.
- `name` = kurzer Medienname: NZZ, FAZ, Reuters, Bloomberg, SZ, Tagesschau, Politico, Hessenschau, FR, Handelsblatt, FT, Economist, WiWo, heise, Ars Technica, MIT Tech Review, TechCrunch, The Verge.

## Inhalt und Ressorts

Reihenfolge ist fest: Welt → Deutschland → Frankfurt & Hessen → Wirtschaft → Tech & KI → Kurz notiert.

| Ressort | `section` | Anzahl | Schwerpunkt |
|---|---|---|---|
| Welt | `welt` | 3–5 | Geopolitik, Kriege, Großmächte, EU, Wahlen – der Schwerpunkt des Briefings |
| Deutschland | `deutschland` | 2–4 | Bundespolitik, Entscheidungen mit Folgen für Bürger, Gesetze, Steuern |
| Frankfurt & Hessen | `hessen` | 1–4 | Nur Relevantes: Sicherheit, Demonstrationen, Verkehr/Streiks/Sperrungen, Stadt- und Landespolitik, Finanzplatz, Flughafen, Großereignisse. Kein Vereinsleben, keine Kleinmeldungen. |
| Wirtschaft | `wirtschaft` | 2–4 | Konjunktur, Arbeitsmarkt, große Unternehmen, Standort, Welthandel – kurz und verständlich |
| Tech & KI | `tech` | 1–3 | Nur, was ein interessierter Nicht-Techniker wissen sollte: große KI-Firmen und -Modelle, Börsengänge, Regulierung, Sicherheitsvorfälle mit Alltagsfolgen. Keine Fachdetails (keine CVE-Nummern, Versionsnummern, Konfigurationen). |
| Kurz notiert | `brief` | 3–8 | Einzeiler aus weiteren Bereichen, damit nichts Wichtiges fehlt: Wissenschaft, Gesundheit, Energie & Klima, Gesellschaft, Recht, Sport (nur Großereignisse), Kultur, sowie kleinere Meldungen der Ressorts oben |

Innerhalb eines Ressorts nach Wichtigkeit sortieren; die erste Meldung ist der Aufmacher (wird groß dargestellt). Kein Thema doppelt (auch nicht zwischen Ressorts).

**Laufende Lagen:** Themen, die sich über Tage entwickeln (z. B. Proteste in Frankfurt, Streiks, Verhandlungen, Konflikte), weiterverfolgen: Ankündigung → Verlauf → Bilanz und Nachberichterstattung. Solange es eine neue Entwicklung gibt, erneut aufnehmen, mit `"ongoing": true`, und im Text sagen, was seit gestern neu ist. Ohne neue Entwicklung nicht wiederholen.

**Wiederholungen:** Was gestern schon im Briefing stand, nur aufnehmen, wenn es eine neue Entwicklung gibt – dann die Neuigkeit in den Vordergrund stellen.

## Aufbau einer Meldung (das Wichtigste)

Jede Meldung muss nach dem Lesen der Zusammenfassung verständlich sein und nach dem Antippen vollständig erklärt.

- **`kicker`** – Unterthema in 1–2 Wörtern (z. B. „Geopolitik“, „Ukraine“, „Banken“, „Frankfurt“).
- **`title`** – sachliche Überschrift, max. ca. 80 Zeichen. Keine Frage, kein Wortspiel.
- **`summary`** – 1–2 Sätze, die **für sich allein** sagen, was passiert ist und worum es geht. Mit den entscheidenden Zahlen und Namen. Keine Atmosphäre oder Nebensächlichkeiten.
- **`details`** – 2–3 kurze Absätze (bei einfachen Themen 1), je 1–3 Sätze. Erklären statt nacherzählen:
  - Was genau ist passiert (Fakten, Zahlen, Beteiligte)?
  - Hintergrund: Wie kam es dazu? Fachbegriffe, Abkommen, Institutionen kurz erklären.
  - Wer will was, was sind die Streitpunkte, was passiert als Nächstes (Termine)?
  - Nicht die `summary` wiederholen.
- **`why`** – „Was das bedeutet“: 1–2 Sätze zu Folgen und Einordnung, wo passend für Deutschland, Frankfurt oder Mauritz' Geldanlage. Einschätzungen als solche kennzeichnen („gilt als“, „nach Einschätzung von …“).
- **`sources`** – 1–2 Quellen `{ "name", "url" }`.
- **`ongoing`** – `true` bei laufenden Lagen, sonst weglassen.

Beispiel, was **nicht** gewünscht ist:
> summary: „Am Rande des Apec-Gipfels empfing Xi Trump mit einer Umarmung; heute folgen Einzelgespräche.“ → sagt nicht, worum es geht.

So ist es richtig:
> summary: „Die Staatschefs der USA, Chinas und Russlands verhandeln heute erstmals gemeinsam – über Atomwaffen-Kontrolle, Handel, KI und den Ukraine-Krieg.“
> details: Ort und Anlass; was der ausgelaufene New-Start-Vertrag war und warum das wichtig ist; in welcher Lage die Beteiligten anreisen.
> why: „Eine Einigung zu Handel oder Abrüstung würde Märkte und Sicherheitslage in Europa direkt beeinflussen; bleibt es bei Symbolik, ändert sich wenig.“

## Auf einen Blick

`glance`: die 5 wichtigsten Meldungen des Tages über alle Ressorts (4–6 erlaubt). Je ein Satz (max. ca. 25 Wörter) mit Kernaussage – nicht nur die Schlagzeile. `story` verweist auf die `id` der Meldung. Reihenfolge nach Wichtigkeit.

## Märkte und Portfolio

Mauritz besitzt zwei Welt-ETFs, die als **ein gemeinsames Portfolio** betrachtet werden: Vanguard FTSE All-World (IE00BK5BQT80) und Amundi MSCI World (IE000BI8OT95). Beide bewegen sich fast gleich; Schwerpunkt große US-Unternehmen (rund 70 % USA, hoher Tech-Anteil), Bewertung in Euro – der Euro-Dollar-Kurs wirkt also mit.

Recherchieren: Schluss des Vortags (MSCI World bzw. FTSE All-World, S&P 500, Nasdaq, DAX), US-Futures/Vorbörse am Morgen, Asien über Nacht, Euro-Dollar-Kurs, Anleiherenditen, Ölpreis, Notenbanken, anstehende Termine, aktuelle Markttrends und -stimmung.

- **`forecast`** – genau 2 Einträge, Reihenfolge: **Heute**, dann **Nächste 5 Tage**.
  - `tone`: `pos` / `neu` / `neg`
  - `label`: 2–3 Wörter, z. B. „Deutlich fester“, „Leicht freundlich“, „Seitwärts“, „Seitwärts, schwankend“, „Leicht schwächer“, „Deutlich schwächer“
  - `text`: 1 Satz Begründung (Futures, Asien, Nachrichten bzw. Termine, Zinsen, Trends)
- **`status`** – Lage der letzten Tage (ca. 5 Handelstage): `tone`, `label`, `text` (1–2 Sätze: Was ist passiert und warum, möglichst mit Prozentzahl), `sources` (optional).
- **`outlook`** – genau 2 Einträge: **Nächste Wochen**, **Nächste Monate**; je `tone`, `label`, `text` (1–2 Sätze: Zinspfad, Unternehmensgewinne, Konjunktur, Geopolitik).
- **`tailwinds`** / **`headwinds`** – je 2–3 Sätze `{ "text", "sources" }`: was das Portfolio aktuell stützt bzw. belastet.
- **`indicators`** – 4–6 Kacheln `{ "label", "value", "tone"?, "note"? }`, in dieser Reihenfolge:
  1. MSCI World (Veränderung Vortag, `note` z. B. „Vortag“) – alternativ 5 Tage mit passender `note`
  2. DAX (Vortag)
  3. Nasdaq-Futures oder S&P-500-Futures (vorbörslich)
  4. EZB-Einlagensatz (`note`: nächste Sitzung)
  5. Fed Funds Rate (`note`: nächste Sitzung)
  6. optional: eine besonders relevante Kennzahl des Tages (z. B. Ölpreis Brent, Gold)
  - **Kein** Euro-Dollar-Kurs und **keine** Anleiherendite als Kachel (fließen nur in die Begründungen ein).
  - `tone`: `pos`/`neg` bei Kursveränderungen, sonst weglassen. Werte im deutschen Format („−1,2 %“, „+0,8 %“, „2,50 %“). Ungefähre Werte mit „≈“ und `note` „ungefähr“. Nie erfinden – nicht ermittelbar → Kachel weglassen.
- **`calendar`** – 3–8 Termine der nächsten Tage/Wochen `{ "when", "text" }`, `when` kurz: „Heute“, „Morgen“, „Fr.“, „9. Dez.“.

Prognosen sind Einschätzungen auf Basis der Nachrichtenlage. Ist die Lage unklar, `neu` wählen und das im Text sagen. Keine Kauf- oder Verkaufsempfehlungen.

## Sprache und Stil

- Deutsch, nüchtern, neutral, klar. Kurze Sätze. Keine wertenden Adjektive.
- Fachbegriffe beim ersten Vorkommen kurz erklären.
- Zahlen im deutschen Format: „1,5 Bio. $“, „45 Mrd. €“, „2,05 → 0,1 Cent/kWh“, „−2,1 %“.
- Nur reiner Text: kein HTML, kein Markdown, keine Emojis.
- In eigenen Worten schreiben; keine Sätze aus Artikeln übernehmen, Zitate höchstens kurz.

## Datenformat

```json
{
  "date": "2026-11-19",
  "meta": { "note": "optional: Hinweis zur Ausgabe, z. B. wenn Quellen nicht abrufbar waren" },
  "glance": [ { "text": "…", "story": "s1" } ],
  "stories": [
    {
      "id": "s1", "section": "welt", "kicker": "Geopolitik",
      "title": "…", "summary": "…",
      "details": ["…", "…"],
      "why": "…",
      "sources": [ { "name": "NZZ", "url": "https://www.nzz.ch/…" } ],
      "ongoing": false
    }
  ],
  "brief": [ { "text": "…", "sources": [ { "name": "heise", "url": "https://…" } ] } ],
  "markets": {
    "forecast": [
      { "tone": "pos", "label": "Leicht freundlich", "text": "…" },
      { "tone": "neu", "label": "Seitwärts", "text": "…" }
    ],
    "status": { "tone": "neg", "label": "Leichter Abgabedruck", "text": "…", "sources": [] },
    "outlook": [
      { "tone": "neg", "label": "Eher Gegenwind", "text": "…" },
      { "tone": "neu", "label": "Offen", "text": "…" }
    ],
    "tailwinds": [ { "text": "…", "sources": [] } ],
    "headwinds": [ { "text": "…", "sources": [] } ],
    "indicators": [ { "label": "MSCI World", "value": "−0,6 %", "tone": "neg", "note": "Vortag" } ],
    "calendar": [ { "when": "Heute", "text": "…" } ]
  }
}
```

- `id`: fortlaufend `s1`, `s2`, … Meldungen eines Ressorts stehen direkt hintereinander, Ressorts in der festen Reihenfolge.
- Ressortnamen, ETF-Liste, Zeitstempel und Zeithorizont-Bezeichnungen ergänzt `scripts/publish.py` selbst.
- Ein vollständiges Beispiel ist `data/2026-11-19.json`.

## Letzte Prüfung vor dem Veröffentlichen

- Stimmen alle Fakten und Zahlen mit den Quellen überein?
- Führt jeder Link zu genau dem Artikel, aus dem die Information stammt?
- Ist jede `summary` ohne weiteren Kontext verständlich?
- Erklären die `details` Hintergründe, statt die Zusammenfassung zu wiederholen?
- Keine Dopplungen innerhalb der Ausgabe und keine Wiederholung von gestern ohne neue Entwicklung?
- Laufende Lagen berücksichtigt?
- Tech & KI einfach gehalten?
- Prognose für heute und 5 Tage vorhanden und begründet?
