/* ------------------------------------------------------------------
   cosmere-data.js — shared data for the Cosmere pages.

   Loaded (as a plain classic script, no build step) by:
     • cosmere.html         — the hub + star chart (one combined page)
     • cosmere_series.html  — the per-series template  (?s=<series id>)

   Everything here is our own paraphrase of publicly known facts. No
   text is copied from Coppermind or Brandon's site, and none of the
   official artwork is used. Book covers are hot-linked from the free
   Open Library cover service by cover id (see `cover` below); we don't
   host them, and any book without one falls back to a drawn tile.
   For the canonical (spoiler-heavy) detail:
     https://coppermind.net/wiki/Cosmere
     https://www.brandonsanderson.com/pages/what-is-the-cosmere

   WORLDS: pos = [x%, y%] on the chart. Open cosmere.html?edit=1 to
   drag worlds around, then copy the values back into `pos` here.
------------------------------------------------------------------- */

const WORLDS = [
  { id:'roshar', name:'Roshar', system:'The Rosharan System', also:'Ashyn and Braize orbit nearby',
    pos:[60,34], tint:'#3b7a93', glyph:'storm', series:'stormlight',
    books:['The Stormlight Archive'], magic:'Surgebinding',
    blurb:'A world scoured by highstorms, enormous storms that sweep the continent and let spren, spirits of ideas and emotions, cross into the physical world.',
    shards:'Honor, Odium and Cultivation' },
  { id:'scadrial', name:'Scadrial', system:'The Scadrian System', also:'',
    pos:[36,56], tint:'#6a6f86', glyph:'metal', series:'mistborn',
    books:['Mistborn series'], magic:'The Metallic Arts',
    blurb:'The most technologically advanced world in the cluster. Its three magic systems all run on metal.',
    shards:'Preservation and Ruin' },
  { id:'sel', name:'Sel', system:'The Selish System', also:'',
    pos:[20,28], tint:'#7a5f8f', glyph:'shape', series:'elantris',
    books:['Elantris','The Emperor’s Soul'], magic:'Shape-based magics',
    blurb:'A large world with three great domains. Its many magic systems depend on where you are, and are worked by drawing the right shapes, rather like programming.',
    shards:'Devotion and Dominion' },
  { id:'nalthis', name:'Nalthis', system:'The Nalthian System', also:'',
    pos:[62,78], tint:'#b0603f', glyph:'ring', series:'warbreaker',
    books:['Warbreaker'], magic:'Awakening',
    blurb:'A world of colour. Its magic runs on colour and on a resource called Breath.',
    shards:'Endowment' },
  { id:'taldain', name:'Taldain', system:'The Taldain System', also:'',
    pos:[80,20], tint:'#b58a3a', glyph:'halfsun', series:'white-sand',
    books:['White Sand'], magic:'Sand mastery',
    blurb:'A world locked between two stars. One side is a vast, blazing desert; the other lies in permanent twilight.',
    shards:'Autonomy' },
  { id:'threnody', name:'Threnody', system:'The Threnodite System', also:'',
    pos:[12,58], tint:'#4c6a4f', glyph:'branch', series:'shadows-for-silence',
    books:['Shadows for Silence in the Forests of Hell'], magic:null,
    blurb:'A haunted world. Part of it has been abandoned entirely, and the rest is the Forests of Hell, where dangerous shades stalk the trees.',
    shards:'Ambition (no longer whole)' },
  { id:'utol', name:'UTol and Komashi', system:'The UTol System', also:'two habitable sister worlds',
    pos:[44,19], tint:'#3f8a8f', glyph:'wave', series:'yumi',
    books:['Yumi and the Nightmare Painter'], magic:null,
    blurb:'Two neighbouring worlds. UTol is covered in water, and Komashi is home to humans.',
    shards:'Virtuosity (no longer whole)' },
  { id:'first-of-the-sun', name:'First of the Sun', system:'The Drominad System', also:'several water-rich worlds',
    pos:[80,52], tint:'#3a78a8', glyph:'sun', series:'isles',
    books:['Isles of the Emberdark'], magic:null,
    blurb:'The innermost planet of a system of water-dominated worlds, several of them inhabited.',
    shards:'An avatar of Autonomy' },
  { id:'miral', name:'Miral', system:'Home of The Fires of December', also:'',
    pos:[25,83], tint:'#a5482f', glyph:'flame', series:'fires-of-december',
    books:['The Fires of December'], magic:null,
    blurb:'A world where people can form bonds with strange and dangerous entities.',
    shards:'Valor' },
  { id:'canticle', name:'Canticle', system:'A world without a Shard', also:'',
    pos:[84,80], tint:'#a8703a', glyph:'rays', series:'sunlit-man',
    books:['The Sunlit Man'], magic:null,
    blurb:'A tiny world where the sunrise is deadly. People survive by never stopping, always staying ahead of the dawn.',
    shards:'None' },
  { id:'lumar', name:'Lumar', system:'A backwater world', also:'twelve moons hang close overhead',
    pos:[58,57], tint:'#4d8a76', glyph:'crescent', series:'tress',
    books:['Tress of the Emerald Sea'], magic:null,
    blurb:'A backwater world beneath twelve close moons, where fast-growing, dangerous spores shape life at sea.',
    shards:'Not known' },
  { id:'yolen', name:'Yolen', system:'Hidden from most of the cluster', also:'',
    pos:[91,37], tint:'#8a99a3', glyph:'unknown', series:null, hidden:true,
    books:[], magic:null,
    blurb:'The original home of humanity, kept hidden from most of the cluster. It has not yet appeared in a published book.',
    shards:'None' }
];

const GLYPHS = {
  storm:'M4 9c3-4 6 4 9 0s5 2 7-1M4 15c3-4 6 4 9 0s5 2 7-1',
  metal:'M12 3l6 9-6 9-6-9z M12 3v18',
  shape:'M5 5h14v14H5z M5 5l14 14',
  ring:'M4 12a8 8 0 1 0 16 0a8 8 0 1 0-16 0 M9 12a3 3 0 1 0 6 0a3 3 0 1 0-6 0',
  halfsun:'M4 12a8 8 0 1 0 16 0a8 8 0 1 0-16 0 M12 4v16 M12 4a8 8 0 0 1 0 16',
  branch:'M12 3v18 M12 8l-5 4 M12 8l5 4 M12 13l-6 5 M12 13l6 5',
  wave:'M3 10c3-3 6 3 9 0s6 3 9 0 M3 16c3-3 6 3 9 0s6 3 9 0',
  sun:'M8 12a4 4 0 1 0 8 0a4 4 0 1 0-8 0 M12 3v3 M12 18v3 M3 12h3 M18 12h3',
  flame:'M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-3 2-4 3-6 1 2 2 2 2-4z',
  rays:'M9 12a3 3 0 1 0 6 0a3 3 0 1 0-6 0 M12 3v4 M12 17v4 M3 12h4 M17 12h4 M6 6l2 2 M16 16l2 2',
  crescent:'M15 4a8 8 0 1 0 0 16a6.5 6.5 0 0 1 0-16z',
  unknown:'M9 9a3 3 0 1 1 4 3c-1 1-1 2-1 3 M12 18.5v.5'
};

/* ------------------------------------------------------------------
   SERIES — keyed by the ids the map uses in each world's `series`
   field. cosmere_series.html?s=<id> renders one of these.

   Fields:
     title   — series / book name
     world   — matching WORLDS id (for the "back to the chart" link and glyph)
     planet  — where it takes place
     magic   — the magic system, in one short phrase
     blurb   — spoiler-free pitch, a couple of sentences
     start   — if set, why this is a good first Cosmere read (drives the
               "Where to start" section and the "Good first read" badge)
     books   — reading order: { title, year, note?, cover? }
               cover = Open Library cover id, shown via covers.openlibrary.org
     spoiler — the deeper stuff, hidden behind a click-to-reveal toggle
------------------------------------------------------------------- */

const SERIES = {
  stormlight: {
    title:'The Stormlight Archive',
    world:'roshar',
    planet:'Roshar',
    magic:'Surgebinding',
    start:'For readers who want the big, immersive epic and don’t mind settling in for a long, rewarding ride.',
    blurb:'Brandon’s flagship epic: a war-torn world of stone and storm where a handful of broken people begin to bond spirits and relearn powers thought lost for millennia. It is his longest, most ambitious series, and the spine of the whole Cosmere.',
    books:[
      { title:'The Way of Kings', year:2010, cover:14658316 },
      { title:'Words of Radiance', year:2014, cover:14658334 },
      { title:'Edgedancer', year:2016, note:'novella, best read after Words of Radiance', cover:14658530 },
      { title:'Oathbringer', year:2017, cover:14658111 },
      { title:'Dawnshard', year:2020, note:'novella, best read after Oathbringer', cover:11385385 },
      { title:'Rhythm of War', year:2020, cover:14658361 },
      { title:'Wind and Truth', year:2024, cover:14836765 }
    ],
    spoiler:'Roshar carries three of the sixteen Shards. Honor and Cultivation shaped its people and its spren; Odium, the Shard of divine hatred, drives the conflict across the series. The Knights Radiant draw their powers from bonds with spren, and the storms that batter the world are far from a natural accident. Stormlight ties into the wider Cosmere more tightly than any other series, and several familiar faces from other worlds turn up along the way.'
  },

  mistborn: {
    title:'Mistborn',
    world:'scadrial',
    planet:'Scadrial',
    magic:'The Metallic Arts — Allomancy, Feruchemy and Hemalurgy',
    start:'The most popular on-ramp: a tight, self-contained opening trilogy with one of fantasy’s best magic systems.',
    blurb:'It starts with a simple question: what if the prophesied hero failed, and the Dark Lord won? Era One is a heist against a thousand-year empire. Era Two jumps centuries ahead into a frontier-and-railways world where the old magic has become almost mundane. Both are fast, twisty, and very easy to love.',
    books:[
      { title:'The Final Empire', year:2006, note:'Era One', cover:14658160 },
      { title:'The Well of Ascension', year:2007, note:'Era One', cover:14658341 },
      { title:'The Hero of Ages', year:2008, note:'Era One', cover:14658094 },
      { title:'The Alloy of Law', year:2011, note:'Era Two', cover:14658081 },
      { title:'Shadows of Self', year:2015, note:'Era Two', cover:14658321 },
      { title:'The Bands of Mourning', year:2016, note:'Era Two', cover:14658335 },
      { title:'Mistborn: Secret History', year:2016, note:'novella, read after The Bands of Mourning', cover:8737946 },
      { title:'The Lost Metal', year:2022, note:'Era Two', cover:14658507 }
    ],
    spoiler:'Scadrial was made and is held between two opposed Shards: Preservation and Ruin. The three metal-based magics are three faces of the same underlying system, and the mists are anything but weather. Because Scadrial is where the Cosmere’s technology races ahead fastest, it also becomes a crossroads: threads from Era Two reach directly toward the future of the wider universe.'
  },

  elantris: {
    title:'Elantris',
    world:'sel',
    planet:'Sel',
    magic:'AonDor and the other Selish magics',
    start:'His standalone debut: one book, one world, a clean and self-contained place to begin.',
    blurb:'Brandon’s debut, and a great one-volume entry point. A city of shining, god-like beings has fallen; its magic has curdled, and those it once blessed are now trapped between life and death. A prince, a priest and a princess each try to work out why. The Emperor’s Soul, a short and much-loved companion, is set on the same world.',
    books:[
      { title:'Elantris', year:2005, cover:14658083 },
      { title:'The Hope of Elantris', year:2006, note:'short story' },
      { title:'The Emperor’s Soul', year:2012, note:'novella, same world', cover:14658408 }
    ],
    spoiler:'Sel held two Shards, Devotion and Dominion, and what happened to them warped magic across the entire planet. The Selish systems are location-bound and worked by drawing precise symbols — closer to programming than to spellcasting — which is why the fall of Elantris broke the magic so literally. Sel is considered one of the more dangerous and tangled corners of the Cosmere.'
  },

  warbreaker: {
    title:'Warbreaker',
    world:'nalthis',
    planet:'Nalthis',
    magic:'Awakening, powered by colour and Breath',
    start:'A single standalone novel — a low-commitment way to try Brandon’s style, and a good friend to have read before Stormlight.',
    blurb:'A standalone of two sister-princesses, two very different gods, a talking sword with opinions, and a magic that trades away colour to bring objects to life. Warm, funny and clever.',
    books:[
      { title:'Warbreaker', year:2009, cover:14658347 }
    ],
    spoiler:'Nalthis belongs to Endowment. Its magic runs on Breath, a piece of a person’s own soul that can be given away, gathered and used to Awaken. The sentient sword Nightblood is one of the most important objects in the whole Cosmere, and where it travels next matters a great deal beyond this one book.'
  },

  'white-sand': {
    title:'White Sand',
    world:'taldain',
    planet:'Taldain',
    magic:'Sand Mastery',
    blurb:'Told as a graphic-novel trilogy. On the blazing day side of a world caught between two suns, certain people can command ribbons of white sand. When his order is massacred, a weak sand master has to survive long enough to understand what really happened.',
    books:[
      { title:'White Sand, Volume 1', year:2016, note:'graphic novel', cover:14658405 },
      { title:'White Sand, Volume 2', year:2017, note:'graphic novel', cover:9220015 },
      { title:'White Sand, Volume 3', year:2019, note:'graphic novel', cover:9145290 }
    ],
    spoiler:'Taldain is the domain of Autonomy, a Shard with a habit of setting up avatars and pulling strings from a distance. Sand Mastery draws on water to move the sand, and the locked day/night sides of the planet are central to how the magic and the politics both work. Autonomy’s wider schemes reach into several other series.'
  },

  tress: {
    title:'Tress of the Emerald Sea',
    world:'lumar',
    planet:'Lumar',
    magic:'The spores of the twelve seas',
    start:'The gentlest, most charming entry — a self-contained fairy tale that’s lovely even if you’ve never touched the Cosmere.',
    blurb:'A gentle, witty fairy tale: a practical young woman leaves her tiny island to rescue the boy she loves, crossing seas made not of water but of coloured spores that react — explosively — to the slightest damp.',
    books:[
      { title:'Tress of the Emerald Sea', year:2023, cover:13143232 }
    ],
    spoiler:'Lumar sits beneath twelve moons that rain down the aether spores that make up its seas, each colour with its own dangerous behaviour. The story is narrated by a familiar Cosmere traveller whose own arc runs across several books, and that framing is a quiet reward for readers who have met him elsewhere.'
  },

  'sunlit-man': {
    title:'The Sunlit Man',
    world:'canticle',
    planet:'Canticle',
    magic:'Borrowed and improvised powers on a hostile world',
    blurb:'A lone, hunted man crash-lands on Canticle, a planet where the sunrise itself will kill you, and the only way to live is to keep moving ahead of the dawn. Darker and more breathless than most of the Cosmere, and set notably later in its timeline.',
    books:[
      { title:'The Sunlit Man', year:2023, cover:13989844 }
    ],
    spoiler:'Canticle has no Shard of its own, but its deadly sun and buried secrets are bound up with Cosmere-wide forces. This is one of the furthest-future stories yet published, so it rewards readers who already know the wider universe: the protagonist is not a stranger, and the technology on show hints at where everything is heading.'
  },

  yumi: {
    title:'Yumi and the Nightmare Painter',
    world:'utol',
    planet:'Komashi (with its sister world, UTol)',
    magic:'Summoning spirits by stacking stones, and painting away nightmares',
    blurb:'Two people from two very different worlds — a revered spirit-summoner and a lonely painter of nightmares — are forced to share a life, swapping days and bodies. Inspired by anime and told with real tenderness. A lovely standalone.',
    books:[
      { title:'Yumi and the Nightmare Painter', year:2023, cover:13989845 }
    ],
    spoiler:'The bright, ordered world and the dark, haunted one are two halves of a single broken story, tied to a Shard the book slowly reveals. Like Tress, it is narrated by the same wandering Cosmere storyteller, and the connection between the two worlds is the heart of the mystery.'
  },

  'shadows-for-silence': {
    title:'Shadows for Silence in the Forests of Hell',
    world:'threnody',
    planet:'Threnody',
    magic:'The hard rules that keep the shades at bay',
    blurb:'A tense, self-contained novella. Silence Montane runs a lonely waystop on the edge of the Forests of Hell, where breaking three simple rules calls up the shades — and hunting a wanted man is about to break all of them. Short, grim and gripping.',
    books:[
      { title:'Shadows for Silence in the Forests of Hell', year:2013, note:'novella', cover:11439565 }
    ],
    spoiler:'Threnody once held the Shard Ambition, which was attacked and shattered; the shades and the strange rules of survival are the fallout. It is one of the bleakest worlds in the Cosmere, and the wider consequences of what happened here are still being uncovered.'
  },

  isles: {
    title:'Isles of the Emberdark',
    world:'first-of-the-sun',
    planet:'First of the Sun',
    magic:'Bonding with Aviar, birds that grant talents',
    blurb:'Set among the island worlds of the Drominad system, first glimpsed in the short story Sixth of the Dusk. Read that novella first: it introduces a trapper, the deadly islands, and the birds whose bonds grant strange gifts. Isles of the Emberdark carries the story outward.',
    books:[
      { title:'Sixth of the Dusk', year:2014, note:'novella, read first', cover:15249754 },
      { title:'Isles of the Emberdark', year:2025, cover:15228811 }
    ],
    spoiler:'First of the Sun is watched over by an avatar of Autonomy rather than a full Shard. The Aviar and their talents matter well beyond these islands, and Isles of the Emberdark pushes the Cosmere’s story into space and toward its larger, interstellar future.'
  },

  'fires-of-december': {
    title:'The Fires of December',
    world:'miral',
    planet:'Miral',
    magic:'Bonds with strange and dangerous entities',
    blurb:'A newer addition to the Cosmere, set on Miral, a world where people can bind themselves to powerful and perilous beings. Details are still thin on the ground — check Coppermind for the latest before diving in.',
    books:[
      { title:'The Fires of December', year:null, note:'newer / upcoming — see Coppermind for status', cover:15248329 }
    ],
    spoiler:'Miral is tied to the Shard Valor. Beyond that, very little has been confirmed yet, so treat anything you read about it as provisional.'
  }
};

/* Helper: cover image URL for a book, or null if it has no known cover. */
function coverUrl(book, size){
  return book && book.cover ? 'https://covers.openlibrary.org/b/id/' + book.cover + '-' + (size||'M') + '.jpg' : null;
}
