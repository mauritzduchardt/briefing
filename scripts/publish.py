#!/usr/bin/env python3
"""Prüft ein Tages-Briefing und veröffentlicht es in data/.

Aufruf:
  python3 scripts/publish.py <entwurf.json>          prüfen + veröffentlichen
  python3 scripts/publish.py <entwurf.json> --check  nur prüfen
  python3 scripts/publish.py --rebuild               nur index.json/search.json neu bauen

Das Skript ergänzt feste Werte selbst (Ressorts, ETFs, Zeitstempel), prüft alle
Felder gegen das Format, schreibt data/JJJJ-MM-TT.json und baut data/index.json
und data/search.json neu. Bei Fehlern wird nichts geschrieben (Exit-Code 1).
"""
import json, re, sys, pathlib, datetime
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TZ = ZoneInfo("Europe/Berlin")

SECTIONS = [
    {"id": "welt", "label": "Welt"},
    {"id": "deutschland", "label": "Deutschland"},
    {"id": "hessen", "label": "Frankfurt & Hessen"},
    {"id": "wirtschaft", "label": "Wirtschaft"},
    {"id": "tech", "label": "Tech & KI"},
]
SECTION_IDS = [s["id"] for s in SECTIONS]
COUNTS = {"welt": (3, 5), "deutschland": (2, 4), "hessen": (1, 4), "wirtschaft": (2, 4), "tech": (1, 3)}
ETFS = [
    {"name": "Vanguard FTSE All-World", "isin": "IE00BK5BQT80"},
    {"name": "Amundi MSCI World", "isin": "IE000BI8OT95"},
]
PORTFOLIO = "Vanguard FTSE All-World + Amundi MSCI World"
TONES = {"pos", "neg", "neu"}
FORECAST_H = ["Heute", "Nächste 5 Tage"]
OUTLOOK_H = ["Nächste Wochen", "Nächste Monate"]

errors, warnings = [], []
err = errors.append
warn = warnings.append


def text(v, path, maxlen, minlen=2):
    if not isinstance(v, str) or len(v.strip()) < minlen:
        err(f"{path}: Text fehlt oder ist leer")
        return
    if len(v) > maxlen:
        err(f"{path}: zu lang ({len(v)} > {maxlen} Zeichen) – kürzen")
    if re.search(r"<[a-zA-Z/][^>]*>", v):
        err(f"{path}: enthält HTML – nur reiner Text erlaubt")
    if "**" in v or re.search(r"\[[^\]]+\]\(", v):
        err(f"{path}: enthält Markdown – nur reiner Text erlaubt")


def tone(v, path):
    if v not in TONES:
        err(f"{path}: tone muss pos, neg oder neu sein (ist {v!r})")


def sources(v, path, required=True):
    if v is None:
        v = []
    if not isinstance(v, list):
        err(f"{path}: sources muss eine Liste sein")
        return
    if required and not v:
        err(f"{path}: mindestens eine Quelle nötig")
    for i, s in enumerate(v):
        p = f"{path}[{i}]"
        if not isinstance(s, dict):
            err(f"{p}: Quelle muss {{name, url}} sein")
            continue
        text(s.get("name"), p + ".name", 30)
        u = s.get("url", "")
        pu = urlparse(u) if isinstance(u, str) else None
        if not pu or pu.scheme != "https" or not pu.netloc:
            err(f"{p}.url: keine gültige https-Adresse ({u!r})")
        elif pu.path.strip("/") == "" or len(pu.path.strip("/")) < 8:
            err(f"{p}.url: führt nicht zu einem konkreten Artikel ({u!r})")


def validate(d):
    if not isinstance(d, dict):
        err("Datei muss ein JSON-Objekt sein")
        return
    date = d.get("date", "")
    try:
        datetime.date.fromisoformat(date)
    except Exception:
        err(f"date: muss JJJJ-MM-TT sein (ist {date!r})")

    meta = d.get("meta") or {}
    if "note" in meta and meta["note"]:
        text(meta["note"], "meta.note", 300)

    # Meldungen
    stories = d.get("stories")
    ids = set()
    if not isinstance(stories, list) or not stories:
        err("stories: Liste fehlt")
        stories = []
    per = {k: 0 for k in SECTION_IDS}
    seen_sections = []
    for i, s in enumerate(stories):
        p = f"stories[{i}]"
        if not isinstance(s, dict):
            err(f"{p}: muss ein Objekt sein")
            continue
        sid = s.get("id")
        if not isinstance(sid, str) or not sid:
            err(f"{p}.id fehlt")
        elif sid in ids:
            err(f"{p}.id doppelt: {sid}")
        ids.add(sid)
        sec = s.get("section")
        if sec not in SECTION_IDS:
            err(f"{p}.section: unbekannt ({sec!r}); erlaubt: {', '.join(SECTION_IDS)}")
        else:
            per[sec] += 1
            if seen_sections and seen_sections[-1] != sec and sec in seen_sections:
                err(f"{p}: Meldungen eines Ressorts müssen zusammenhängend stehen ({sec})")
            if not seen_sections or seen_sections[-1] != sec:
                seen_sections.append(sec)
        text(s.get("kicker"), p + ".kicker", 30)
        text(s.get("title"), p + ".title", 95, 10)
        text(s.get("summary"), p + ".summary", 300, 40)
        det = s.get("details")
        if not isinstance(det, list) or not 1 <= len(det) <= 4:
            err(f"{p}.details: 1 bis 4 Absätze nötig")
        else:
            for j, para in enumerate(det):
                text(para, f"{p}.details[{j}]", 520, 20)
        text(s.get("why"), p + ".why", 300, 20)
        sources(s.get("sources"), p + ".sources")
        if "ongoing" in s and not isinstance(s["ongoing"], bool):
            err(f"{p}.ongoing: true oder false")
    for k, (lo, hi) in COUNTS.items():
        if per[k] == 0 and k != "hessen":
            err(f"Ressort {k}: keine Meldung")
        elif not lo <= per[k] <= hi:
            warn(f"Ressort {k}: {per[k]} Meldungen (vorgesehen {lo}–{hi})")

    # Auf einen Blick
    g = d.get("glance")
    if not isinstance(g, list) or not 4 <= len(g) <= 6:
        err("glance: 4 bis 6 Punkte nötig")
        g = g if isinstance(g, list) else []
    for i, x in enumerate(g):
        p = f"glance[{i}]"
        if not isinstance(x, dict):
            err(f"{p}: muss {{text, story}} sein")
            continue
        text(x.get("text"), p + ".text", 220, 30)
        if x.get("story") not in ids:
            err(f"{p}.story: verweist auf keine vorhandene Meldung ({x.get('story')!r})")

    # Kurz notiert
    b = d.get("brief", [])
    if not isinstance(b, list):
        err("brief: muss eine Liste sein")
        b = []
    if not 3 <= len(b) <= 8:
        warn(f"brief: {len(b)} Einträge (vorgesehen 3–8)")
    for i, x in enumerate(b):
        p = f"brief[{i}]"
        text(x.get("text") if isinstance(x, dict) else None, p + ".text", 260, 20)
        sources(x.get("sources") if isinstance(x, dict) else None, p + ".sources")

    # Märkte
    m = d.get("markets")
    if not isinstance(m, dict):
        err("markets fehlt")
        return
    fc = m.get("forecast")
    if not isinstance(fc, list) or len(fc) != 2:
        err("markets.forecast: genau 2 Einträge (Heute, Nächste 5 Tage)")
        fc = []
    for i, x in enumerate(fc):
        p = f"markets.forecast[{i}]"
        tone(x.get("tone"), p + ".tone")
        text(x.get("label"), p + ".label", 28)
        text(x.get("text"), p + ".text", 200, 20)
    st = m.get("status") or {}
    tone(st.get("tone"), "markets.status.tone")
    text(st.get("label"), "markets.status.label", 32)
    text(st.get("text"), "markets.status.text", 360, 30)
    sources(st.get("sources"), "markets.status.sources", required=False)
    ol = m.get("outlook")
    if not isinstance(ol, list) or len(ol) != 2:
        err("markets.outlook: genau 2 Einträge (Nächste Wochen, Nächste Monate)")
        ol = []
    for i, x in enumerate(ol):
        p = f"markets.outlook[{i}]"
        tone(x.get("tone"), p + ".tone")
        text(x.get("label"), p + ".label", 28)
        text(x.get("text"), p + ".text", 260, 20)
    for key in ("tailwinds", "headwinds"):
        lst = m.get(key)
        if not isinstance(lst, list) or not 1 <= len(lst) <= 4:
            err(f"markets.{key}: 1 bis 4 Einträge")
            lst = []
        for i, x in enumerate(lst):
            text(x.get("text"), f"markets.{key}[{i}].text", 220, 15)
            sources(x.get("sources"), f"markets.{key}[{i}].sources", required=False)
    ind = m.get("indicators")
    if not isinstance(ind, list) or not 3 <= len(ind) <= 6:
        err("markets.indicators: 3 bis 6 Kacheln")
        ind = []
    for i, x in enumerate(ind):
        p = f"markets.indicators[{i}]"
        text(x.get("label"), p + ".label", 24)
        text(x.get("value"), p + ".value", 14, 1)
        if x.get("tone") is not None:
            tone(x.get("tone"), p + ".tone")
        if x.get("note"):
            text(x.get("note"), p + ".note", 26, 1)
        lab = (x.get("label") or "").lower()
        if "eur" in lab and "usd" in lab or "rendite" in lab:
            err(f"{p}: EUR/USD und Anleiherenditen werden nicht als Kachel angezeigt")
    cal = m.get("calendar")
    if not isinstance(cal, list) or not 2 <= len(cal) <= 8:
        err("markets.calendar: 2 bis 8 Termine")
        cal = []
    for i, x in enumerate(cal):
        text(x.get("when"), f"markets.calendar[{i}].when", 14, 1)
        text(x.get("text"), f"markets.calendar[{i}].text", 120, 5)


def complete(d):
    """Feste Werte ergänzen, damit Format und Design immer gleich bleiben."""
    d["sections"] = SECTIONS
    d.setdefault("meta", {})
    d["meta"]["generated"] = datetime.datetime.now(TZ).isoformat(timespec="minutes")
    m = d.get("markets") or {}
    m["portfolio"] = PORTFOLIO
    m["etfs"] = ETFS
    for x, h in zip(m.get("forecast") or [], FORECAST_H):
        x["horizon"] = h
    for x, h in zip(m.get("outlook") or [], OUTLOOK_H):
        x["horizon"] = h
    for s in d.get("stories") or []:
        s.setdefault("ongoing", False)
    d.setdefault("brief", [])
    return d


def rebuild():
    days = []
    for f in sorted(DATA.glob("????-??-??.json"), reverse=True):
        try:
            days.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"Warnung: {f.name} unlesbar ({e})")
    index = [{"date": d["date"], "top": (d.get("glance") or [{}])[0].get("text", "")} for d in days]
    labels = {s["id"]: s["label"] for s in SECTIONS}
    search = []
    for d in days:
        for s in d.get("stories", []):
            search.append({
                "d": d["date"], "id": s["id"], "s": labels.get(s["section"], ""), "k": s.get("kicker", ""),
                "t": s["title"], "m": s["summary"], "x": " ".join(s.get("details", []) + [s.get("why", "")]),
                "q": " ".join(x["name"] for x in s.get("sources", [])),
            })
        for b in d.get("brief", []):
            search.append({"d": d["date"], "b": 1, "t": b["text"], "src": b.get("sources", [])})
    (DATA / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    (DATA / "search.json").write_text(json.dumps(search, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"index.json: {len(index)} Ausgaben · search.json: {len(search)} Einträge")


def main(argv):
    if "--rebuild" in argv:
        rebuild()
        return 0
    files = [a for a in argv if not a.startswith("--")]
    if len(files) != 1:
        print(__doc__)
        return 2
    try:
        d = json.loads(pathlib.Path(files[0]).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FEHLER: JSON nicht lesbar: {e}")
        return 1
    validate(d)
    for w in warnings:
        print("Hinweis:", w)
    if errors:
        print(f"\n{len(errors)} FEHLER – nichts veröffentlicht:")
        for e in errors:
            print(" -", e)
        return 1
    if "--check" in argv:
        print("Prüfung bestanden.")
        return 0
    d = complete(d)
    DATA.mkdir(exist_ok=True)
    out = DATA / f"{d['date']}.json"
    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Geschrieben: data/{out.name} ({len(d['stories'])} Meldungen, {len(d['brief'])} Kurzmeldungen)")
    rebuild()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
