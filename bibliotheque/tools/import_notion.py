"""Update data/books.json from a fresh Notion CSV export.

Usage:  python tools/import_notion.py "path/to/Owned Book ....csv"

Notion stays the source for: title, author, series, genre, format, place, year, pages, language, read.
The site keeps what Notion doesn't have: currently reading, date finished, how acquired, cover.
Books are matched by title + author. A backup of the old books.json is written first.
"""
import csv, json, os, shutil, sys, unicodedata, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "data", "books.json")

def key(title, author):
    s = f"{title}|{author}"
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9|]", "", s)

def num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    old = json.load(open(BOOKS, encoding="utf-8")) if os.path.exists(BOOKS) else []
    by_key = {key(b["title"], b["author"]): b for b in old}
    next_id = max([b["id"] for b in old] or [0]) + 1
    out, seen = [], set()
    with open(sys.argv[1], encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            title = (row.get("Title") or "").strip()
            if not title:
                continue
            author = (row.get("Author") or "").strip()
            k = key(title, author)
            prev = by_key.get(k)
            b = dict(prev) if prev else {"id": next_id, "reading": False, "date_finished": None, "acquired_how": None, "cover": None}
            if not prev:
                next_id += 1
            b.update(title=title, author=author, series=(row.get("Serie Name") or "").strip(),
                     genre=(row.get("Genre") or "").strip(), format=(row.get("Fiction/Non Fiction") or "").strip(),
                     owned=(row.get("Owned") or "").strip(), year=num(row.get("Year acquired")),
                     pages=num(row.get("Page Nb")), lang=(row.get("Language") or "").strip(),
                     read=(row.get("Read") or "").strip().lower() == "yes")
            if b["read"]:
                b["reading"] = False
            out.append(b); seen.add(k)
    only_site = [b for b in old if key(b["title"], b["author"]) not in seen]
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    if os.path.exists(BOOKS):
        shutil.copy2(BOOKS, BOOKS.replace(".json", f".before-import-{stamp}.json"))
    out.extend(only_site)
    json.dump(out, open(BOOKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(out)} books written. {len(only_site)} were only in the site and were kept.")

if __name__ == "__main__":
    main()
