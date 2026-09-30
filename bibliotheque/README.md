# Bibliothèque

Your library website as a single page, `index.html`, with your data in plain JSON files next to it. No server and nothing to install.

## Open it

1. Double-click `index.html`. It opens in your browser.
2. Click **Choose the library folder** and pick this `bibliotheque` folder.
3. Your browser asks whether the page may edit files in it. Allow it.

Next time, the page remembers the folder: one click on **Open my library** and you're in. Browsers ask for permission again each time the page is opened; that's a safety rule, not a bug.

**Use Chrome or Edge.** They're the browsers that let a page save to files on your computer. In Firefox or Safari you can still browse your library, read-only.

## What's in the folder

| Path | What it holds |
|---|---|
| `index.html` | The whole site: cover wall, library, challenges, 2026 |
| `data/books.json` | Every book: title, author, series, genre, format, place, year acquired, pages, language, read, currently reading, date finished, how acquired, cover |
| `data/challenges.json` | Vellum House and Orilium (rooms, books, riddle solutions, progress) |
| `data/goal.json` | Your 2026 goal and the 19-book plan |
| `data/year-2026.json` | Monthly stats, unhauled books, borrowed books and wishlist (from your CAWPILE sheet) |
| `data/backups/` | Created automatically: one copy of your data per day |
| `covers/` | Cover images (see `covers/README.txt` for naming) |
| `tools/import_notion.py` | Optional: refreshes `books.json` from a new Notion CSV export |
| `tools/fetch_covers.py` | Optional: finds covers online and saves them as links or files |

## Everyday use

- **Mark a book as read or currently reading:** click its cover, then use the buttons at the bottom of the card. Marking a book as read records today's date.
- **Edit a book:** click the pen at the top right of its card.
- **Add a book:** "+ Add a book". Set "How acquired" so the 2026 goal counts it correctly.
- **Add a cover:** in edit mode, paste an image address under "Cover link" (for example from Babelio: right-click the cover, "Copy image address"), or choose a file under "Cover image file" (it's copied into `covers/`). Link covers need an internet connection to show; file covers work offline.
- **Challenges:** type a room number when a room opens on the Vellum House map, then fill in the book and the riddle solution.

Everything saves automatically; the bottom of the page says "All changes saved". You can also open the JSON files in any text editor.

## Fetching covers automatically (optional, needs Python)

In a terminal in this folder:

```
python tools/fetch_covers.py --unread --limit 20
```

It looks up books without a cover on Open Library, then Google Books, and saves each cover as a link in `books.json`. Start with `--limit 20` to check the results, then run it without `--limit`. Add `--download` to save image files in `covers/` instead of links, or `--dry-run` to only preview. Books it can't find (often French small-press editions) are listed in `data/covers-missing.txt`; add those with the pen. Close the library page while it runs and reload it afterwards.

## Refreshing from Notion (optional)

Export the Notion database as CSV, then in a terminal in this folder:

```
python tools/import_notion.py "path/to/Owned Book export.csv"
```

Notion's fields replace the site's for each book. "Currently reading", dates finished, how acquired and covers are kept. The previous `books.json` is backed up first. Reload the page afterwards.

## Backups with Git (recommended)

```
git init
git add .
git commit -m "My library"
```

Commit from time to time, or push to a private GitHub repo, to keep a full history off your computer.
