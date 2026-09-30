"""Find covers for your books and save them in data/books.json.

Looks up each book without a cover on Open Library, then Google Books, both free and official APIs.
By default it saves the cover as a LINK (nothing to store). With --download it saves image files in covers/.

Usage (from the bibliotheque folder):
    python tools/fetch_covers.py                 # books without a cover, saved as links
    python tools/fetch_covers.py --unread        # only books you haven't read yet
    python tools/fetch_covers.py --limit 20      # try it on 20 books first
    python tools/fetch_covers.py --download      # save image files in covers/ instead of links
    python tools/fetch_covers.py --dry-run       # show what it would find, change nothing

Close the library page (or reload it afterwards) while this runs, so the page doesn't overwrite the result.
Books it can't find are listed in data/covers-missing.txt so you can add those by hand.
Only uses the Python standard library.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "data", "books.json")
COVERS = os.path.join(ROOT, "covers")
MISSING = os.path.join(ROOT, "data", "covers-missing.txt")
UA = {"User-Agent": "Bibliotheque-personal-library/1.0 (personal use)"}
PAUSE = 1.0  # seconds between requests, to be polite to the APIs


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


def slug(s):
    return "-".join(fold(s))[:90] or "book"


def clean_title(title):
    """'My Hero Academia - Vol.07' -> ('My Hero Academia', '7'); strips edition noise."""
    vol = None
    m = re.search(r"(?:vol\.?|tome|t\.|#)\s*0*(\d+)", title, re.I)
    if m:
        vol = m.group(1)
    t = re.split(r"\s+-\s+|\s*:\s+", title)[0]
    t = re.sub(r"\((.*?)\)", "", t).strip()
    return t, vol


def get_json(url, tries=4):
    for attempt in range(tries):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < tries - 1:
                wait = 5 * (attempt + 1) ** 2  # 5, 20, 45 seconds
                print(f"   (service busy, waiting {wait}s)")
                time.sleep(wait)
                continue
            raise


def similar(a, b):
    """Share of the words of a (our title) found in b (the returned title), tolerating small typos."""
    import difflib
    wa, wb = fold(a), fold(b)
    if not wa:
        return 0
    hit = sum(1 for w in wa if w in wb or difflib.get_close_matches(w, wb, n=1, cutoff=0.8))
    return hit / len(wa)


def author_ok(ours, theirs):
    """Tolerant author check: small typos are fine ('Shakespear' ~ 'Shakespeare'), 'Collectif' matches anything."""
    import difflib
    o = " ".join(fold(ours))
    if not ours or o.strip(" -") in ("collectif", "multiple", "divers", "anonyme", ""):
        return True
    ow = [w for w in fold(ours) if len(w) > 2]
    tw = [w for a in (theirs or []) for w in fold(a) if len(w) > 2]
    if not ow or not tw:
        return True
    return any(difflib.SequenceMatcher(None, x, y).ratio() >= 0.8 for x in ow for y in tw)


def open_library(title, author, lang):
    base, vol = clean_title(title)
    q = {"title": base, "fields": "title,author_name,cover_i,language", "limit": "10"}
    data = get_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(q))
    want = {"French": "fre", "English": "eng"}.get(lang)
    best = None
    for d in data.get("docs", []):
        if not d.get("cover_i") or similar(base, d.get("title", "")) < 0.6:
            continue
        if not author_ok(author, d.get("author_name")):
            continue
        score = 1 + (1 if want and want in (d.get("language") or []) else 0)
        if best is None or score > best[0]:
            best = (score, d["cover_i"])
    if best and not vol:  # volumes of a series usually share a work cover on Open Library: skip, use Google
        return f"https://covers.openlibrary.org/b/id/{best[1]}-M.jpg"
    return None


def google_books(title, author, lang):
    base, vol = clean_title(title)
    parts = [f'intitle:"{base}"']
    q = " ".join(parts) + (f" {vol}" if vol else "")
    params = {"q": q, "maxResults": "10", "printType": "books"}
    lr = {"French": "fr", "English": "en"}.get(lang)
    if lr:
        params["langRestrict"] = lr
    data = get_json("https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode(params))
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        links = info.get("imageLinks") or {}
        img = links.get("thumbnail") or links.get("smallThumbnail")
        if not img or similar(base, info.get("title", "")) < 0.6 or not author_ok(author, info.get("authors")):
            continue
        nums = {str(int(n)) for n in re.findall(r"\d+", info.get("title", "") + " " + info.get("subtitle", ""))}
        if vol and str(int(vol)) not in nums:
            continue
        img = img.replace("http://", "https://").replace("&edge=curl", "")
        return img
    return None


def download(url, name):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    if len(data) < 1500:  # placeholder or blank image
        return None
    ext = ".png" if "png" in ctype else ".webp" if "webp" in ctype else ".jpg"
    os.makedirs(COVERS, exist_ok=True)
    with open(os.path.join(COVERS, name + ext), "wb") as f:
        f.write(data)
    return name + ext


def has_cover(b):
    c = b.get("cover")
    if c and (c.startswith("http") or os.path.exists(os.path.join(COVERS, c))):
        return True
    s = slug(b["title"])
    return any(os.path.exists(os.path.join(COVERS, s + e)) for e in (".jpg", ".jpeg", ".png", ".webp"))


def main():
    ap = argparse.ArgumentParser(description="Fetch book covers from Open Library and Google Books.")
    ap.add_argument("--unread", action="store_true", help="only books not read yet")
    ap.add_argument("--limit", type=int, default=0, help="stop after this many books")
    ap.add_argument("--download", action="store_true", help="save image files in covers/ instead of links")
    ap.add_argument("--dry-run", action="store_true", help="show results without changing anything")
    args = ap.parse_args()

    books = json.load(open(BOOKS, encoding="utf-8"))
    todo = [b for b in books if not has_cover(b) and (not args.unread or not b.get("read"))]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(todo)} books to look up. This takes about {len(todo) * 2 // 60 + 1} minute(s).")

    if not args.dry_run:
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(BOOKS, BOOKS.replace(".json", f".before-covers-{stamp}.json"))

    found, missing = 0, []
    try:
        for i, b in enumerate(todo, 1):
            url = None
            for source in (open_library, google_books):
                try:
                    url = source(b["title"], b.get("author", ""), b.get("lang", ""))
                except (urllib.error.URLError, TimeoutError, ValueError) as e:
                    print(f"   ({source.__name__} error: {e})")
                time.sleep(PAUSE)
                if url:
                    break
            label = f"[{i}/{len(todo)}] {b['title']}"
            if not url:
                print(f"{label}: not found")
                missing.append(f"{b['title']} | {b.get('author', '')}")
                continue
            if args.dry_run:
                print(f"{label}: {url}")
                found += 1
                continue
            if args.download:
                try:
                    name = download(url, slug(b["title"]))
                except (urllib.error.URLError, TimeoutError) as e:
                    name = None
                    print(f"   (download error: {e})")
                if not name:
                    print(f"{label}: found but the image was empty")
                    missing.append(f"{b['title']} | {b.get('author', '')}")
                    continue
                b["cover"] = name
            else:
                b["cover"] = url
            found += 1
            print(f"{label}: ok")
            if not args.dry_run and found % 20 == 0:  # save progress regularly
                json.dump(books, open(BOOKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except KeyboardInterrupt:
        print("\nStopped early; saving what was found so far.")

    if not args.dry_run:
        json.dump(books, open(BOOKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        with open(MISSING, "w", encoding="utf-8") as f:
            f.write("Covers not found automatically (title | author). Add them from the site with the pen.\n\n")
            f.write("\n".join(missing) + "\n")
    print(f"\nDone: {found} covers found, {len(missing)} not found"
          + ("" if args.dry_run else f" (listed in data/covers-missing.txt)") + ".")
    print("Reload the library page to see them.")


if __name__ == "__main__":
    main()
