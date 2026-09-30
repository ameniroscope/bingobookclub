"""Adds StoryGraph cover links for books that still have no cover.
Run from the bibliotheque folder:   python tools/apply_storygraph_patch.py
Books that already have a cover are left untouched. A backup of books.json is made first.
"""
import datetime, json, os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "data", "books.json")
PATCH = {
 "D'une Allemagne à l'autre: Journal de l'année 1990": "https://cdn.thestorygraph.com/njuk7rw1g19smwq8uedcx31mncpf",
 "Man's Search for Meaning": "https://cdn.thestorygraph.com/7p5j2m5nqcpaykqvs3tici7aa4y2",
 "Dans la bouche d’une fille": "https://cdn.thestorygraph.com/fb2ilqn6ygean5tnp3pvb9z6vfd8",
 "Pédés": "https://cdn.thestorygraph.com/q5mk0odlbqgz00gmpxw9pf7fiwco",
 "Ni vue Ni connues": "https://cdn.thestorygraph.com/9wvjyy42ykjwxouhy0enebceffgo",
 "Sauvez la différence des sexes": "https://cdn.thestorygraph.com/gqv7eyynuh49b0luzbh5q5sc2h8a",
 "La dimension fantastique (Tome 1-13 nouvelles de Hoffmann à Seignolle)": "https://cdn.thestorygraph.com/hfi1k6om6zw3s6twuubcwnikz1qz",
 "Blanche Neige et les lances-missiles": "https://cdn.thestorygraph.com/phrdkqqg60xpgusilczqzi875imi",
 "La faculté des idées noires": "https://cdn.thestorygraph.com/xajhli7qhmanh8yjelkphhlb4zuk",
 "La cendrillon du canal/Poisson à face humaine": "https://cdn.thestorygraph.com/0rv3kjsvunwwjkpdj4r4u26lcba9",
 "Once on earth we’re briefly gorgeous": "https://cdn.thestorygraph.com/16dha249tl2aee11bivs7l6fr3yg",
 "Piranesi": "https://cdn.thestorygraph.com/atpwdpe6v0zlpqoyk8pissd43u34",
 "Un Roi sans divertissement": "https://cdn.thestorygraph.com/kvr64iyq4gq4rag017dso9ou6td7",
 "Sorcières, sages-femmes & infirmières : une histoire des femmes soignantes": "https://cdn.thestorygraph.com/ny2wxsxtzyjmxu3ri543mtyzliat",
 "Noire n’est pas mon métier": "https://cdn.thestorygraph.com/aespy9j1x99quv1tio4jjzo6hto5",
 "Sororité": "https://cdn.thestorygraph.com/70mpbv1w5qoilv0g78gb2ecn5ktq",
 "Droits Humains pour Tout.e.s": "https://cdn.thestorygraph.com/2vod87y2vw3mb5nzbwrdo9h71sob",
 "Elle sont 300 000 chaque année": "https://cdn.thestorygraph.com/u1yzgm0jmu613xasto1kvgi3n63b",
 "Le fruit de leurs entrailles et L’Oeuf": "https://cdn.thestorygraph.com/6sf1wn4disoq6hlvvjsc22cn7epy",
 "Conte de la mère l'Oye": "https://cdn.thestorygraph.com/rfwjmu93rkgeoq0zbm9os1du0vhw",
 "Affaire Circé": "https://cdn.thestorygraph.com/g87prjy5l2hdy1mn087ss3t555fk",
 "Match d’écriture": "https://cdn.thestorygraph.com/ioxdj3qqkgx6ewzxhjcgur6tn59s",
 "Arsène Lupin contre Sherlock Holmes": "https://cdn.thestorygraph.com/xwbv7z6u1f0h1kh4a9tcf2akc2vx",
 "Maintenant qu'il fait toujours nuit sur toi": "https://cdn.thestorygraph.com/1j1f17yinxqp18rehe67wcph60rz",
 "La Mécanique du coeur": "https://cdn.thestorygraph.com/0221qgq9udv8ymo0efriu1h1wqao",
 "Beautiful World, Were Are You": "https://cdn.thestorygraph.com/56sybuzt6jl6h8uzp935ugfzpkws",
 "Nos temps contraires - Je ne te laisserai pas mourir - Vol.1": "https://cdn.thestorygraph.com/6iaozz2apim3uss10tet3r3rz6dc",
 "L’Enfant du Dragon fantôme - Vol.01": "https://cdn.thestorygraph.com/te721aoejfmx1adz9e0czjyn55ib"
}
books = json.load(open(BOOKS, encoding="utf-8"))
shutil.copy2(BOOKS, BOOKS.replace(".json", "-before-patch-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"))
n = 0
for b in books:
    if not b.get("cover") and b["title"] in PATCH:
        b["cover"] = PATCH[b["title"]]; n += 1
json.dump(books, open(BOOKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{n} covers added. Reload the library page.")
