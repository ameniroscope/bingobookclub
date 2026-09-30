"""Use the cover images saved with your StoryGraph pages instead of StoryGraph links.

When you saved the StoryGraph pages with Ctrl+S ("Webpage, complete"), your browser also created a folder
next to each .html file, e.g. "amenir - Owned Books _ The StoryGraph_3_files". It contains the cover images.

Usage (from the bibliotheque folder):
    python tools/storygraph_files_to_covers.py "path/to/amenir - Owned Books _ The StoryGraph_3_files"

You can pass several folders. Every book whose cover is a StoryGraph link gets a local copy of the image in
covers/, and books.json is updated to use the file. Covers then also work offline.
"""
import datetime
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "data", "books.json")
COVERS = os.path.join(ROOT, "covers")
PREFIX = "https://cdn.thestorygraph.com/"


def image_ext(path):
    with open(path, "rb") as f:
        head = f.read(12)
    if head.startswith(b"\xff\xd8"):
        return ".jpg"
    if head.startswith(b"\x89PNG"):
        return ".png"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return ".webp"
    if head[:3] == b"GIF":
        return ".gif"
    return None


def main():
    folders = sys.argv[1:]
    if not folders:
        print(__doc__)
        sys.exit(1)
    files = {}
    for folder in folders:
        if not os.path.isdir(folder):
            print(f"Not a folder: {folder}")
            continue
        for name in os.listdir(folder):
            files.setdefault(os.path.splitext(name)[0], os.path.join(folder, name))

    books = json.load(open(BOOKS, encoding="utf-8"))
    os.makedirs(COVERS, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(BOOKS, BOOKS.replace(".json", f".before-sg-files-{stamp}.json"))

    copied = missing = 0
    for b in books:
        cover = b.get("cover") or ""
        if not cover.startswith(PREFIX):
            continue
        key = cover[len(PREFIX):].split("?")[0].strip("/")
        src = files.get(key)
        ext = image_ext(src) if src else None
        if not ext:
            missing += 1
            continue
        name = key + ext
        shutil.copy2(src, os.path.join(COVERS, name))
        b["cover"] = name
        copied += 1

    json.dump(books, open(BOOKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{copied} covers copied into covers/. {missing} StoryGraph links had no saved image and were left as links.")
    print("Reload the library page to see them.")


if __name__ == "__main__":
    main()
