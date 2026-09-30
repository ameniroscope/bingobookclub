"""Fill missing covers from StoryGraph pages you saved with Ctrl+S.

Usage (from the bibliotheque folder):
    python tools/storygraph_covers.py "amenir - Owned Books _ The StoryGraph_3.html" [more saved pages...]

Only books WITHOUT a cover are touched, so covers you already have (or added by hand) are kept.
Matching tolerates small spelling differences in titles and authors (typos, accents, "Tome 3" vs "Vol. 03"),
but refuses a match when the authors are clearly different, and never mixes up volume numbers.
"""
import datetime
import difflib
import html
import json
import os
import re
import shutil
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "data", "books.json")
PREFIX = "https://cdn.thestorygraph.com/"
UNKNOWN_AUTHORS = {"collectif", "multiple", "", "divers", "anonyme"}


def fold(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def flat(s):
    return re.sub(r"[^a-z0-9]", "", fold(s))


def names(s):
    return [w for w in re.findall(r"[a-z]{3,}", fold(s)) if w not in {"and", "et", "the"}]


VOL = re.compile(r"(?:vol(?:ume)?|tome|t|#)\.?\s*0*(\d+)\s*$", re.I)


def split_volume(title):
    m = VOL.search(title.strip())
    if not m:
        return None, None
    base = re.split(r"\s+-\s+|,\s*|\s+(?=(?:vol|tome|volume|#))|\s+T\d", title.strip(), flags=re.I)[0]
    return flat(base), m.group(1)


ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8, "ix": 9, "x": 10}


def trailing_number(title):
    """'Le Secret de Ji 2' -> 2, 'Le Secret de Ji : I' -> 1, 'Vingt ans après II' -> 2, otherwise None."""
    m = re.search(r"[\s:#.-]([0-9]+|[ivx]+)\s*$", fold(title).strip())
    if not m:
        return None
    tok = m.group(1)
    return int(tok) if tok.isdigit() else ROMAN.get(tok)


def authors_compatible(ours, theirs):
    if fold(ours).strip(" -") in UNKNOWN_AUTHORS or not theirs:
        return True
    a, b = names(ours), names(theirs)
    if not a or not b:
        return True
    return any(difflib.SequenceMatcher(None, x, y).ratio() >= 0.8 for x in a for y in b)


def read_pages(paths):
    entries = []
    for p in paths:
        text = open(p, encoding="utf-8", errors="ignore").read()
        for alt, src in re.findall(r'<img alt="([^"]+?)" class="rounded-sm shadow-lg[^"]*" src="([^"]+)"', text):
            key = src.rsplit("/", 1)[-1]
            if "placeholder" in key or not re.fullmatch(r"[a-z0-9]{20,40}", key):
                continue
            alt = html.unescape(alt)
            title, author = (alt.rsplit(" by ", 1) + [""])[:2] if " by " in alt else (alt, "")
            title = title.strip()
            base, vol = split_volume(title)
            entries.append({"title": title, "author": author, "key": key, "flat": flat(title), "base": base, "vol": vol})
    return entries


def find(book, entries, by_flat):
    t, a = book["title"], book.get("author", "")
    base, vol = split_volume(t)
    ok = [e for e in by_flat.get(flat(t), []) if authors_compatible(a, e["author"])]
    if ok:
        return ok[0]
    if vol:  # a volume: same series and same number only
        ok = [e for e in entries if e["vol"] and e["base"] == base and int(e["vol"]) == int(vol) and authors_compatible(a, e["author"])]
        return ok[0] if ok else None
    ft = flat(t)
    if len(ft) < 5:
        return None
    candidates = [e for e in entries if not e["vol"]]
    scored = []
    for e in candidates:
        r = difflib.SequenceMatcher(None, ft, e["flat"]).ratio()
        starts = e["flat"].startswith(ft) and len(ft) >= 6  # StoryGraph title adds a subtitle
        if trailing_number(t) != trailing_number(e["title"]):
            continue
        if (r >= 0.85 or starts) and authors_compatible(a, e["author"]):
            scored.append((r + (0.1 if starts else 0), e))
    return max(scored, key=lambda x: x[0])[1] if scored else None


def main():
    pages = sys.argv[1:]
    if not pages:
        print(__doc__)
        sys.exit(1)
    entries = read_pages(pages)
    by_flat = {}
    for e in entries:
        by_flat.setdefault(e["flat"], []).append(e)
    print(f"{len(entries)} covers found in the saved pages.")

    books = json.load(open(BOOKS, encoding="utf-8"))
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(BOOKS, BOOKS.replace(".json", f".before-storygraph-{stamp}.json"))
    added = []
    for b in books:
        if b.get("cover"):
            continue
        e = find(b, entries, by_flat)
        if e:
            b["cover"] = PREFIX + e["key"]
            added.append(f"  {b['title']}  <-  {e['title']} ({e['author']})")
    json.dump(books, open(BOOKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(added)} covers added:")
    print("\n".join(added))
    print("\nCheck the list above for any wrong match, and fix it with the pen. Reload the library page.")


if __name__ == "__main__":
    main()
