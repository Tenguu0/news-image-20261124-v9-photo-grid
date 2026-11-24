# The World in One Page — Photo Grid, 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Tenguu0/news-image-20261124-v9-photo-grid/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Tenguu0/news-image-20261124-v9-photo-grid/reward.svg)](https://make.fun/bounty/news-image-20261124)

A make.fun entry for
[news-image-20261124](https://make.fun/bounty/news-image-20261124):
the whole world of Tuesday 24 November 2026 squeezed onto a single
newspaper front page, as a photo grid. Twelve stories, three columns
by four rows, and every cell is led by a picture that shows what the
story is about: a radar base burning under a fighter jet in Bahrain,
rescuers in a blacked-out Kyiv street, an empty COP31 hall in
Antalya, the ICJ bench in The Hague, three leaders deadlocked in
Shenzhen, Alcaraz lifting the trophy in Turin, a Russian warship
listing off Libya, Korean jets scrambling, a candy factory on fire
in Java, a car bomb in Colombia, a flooded Himalayan village, and a
school vaccination drive in Bangladesh. Bold headline plus one
summary line under each picture; no whitespace wasted.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

It writes `out/entry.png` (1024x1024 PNG). Python 3.12+, PIL only —
no network, no randomness, no clock, so every run writes the same
bytes.

## How it works

`main.py` composites the page from the twelve pictures committed
under `assets/` (AI-generated illustrations, one per story): a
newsprint masthead, then the 3x4 grid — picture on top of each cell
with a place tag, headline, and summary line below. Every story on
the page is a real event from 24 November 2026, cross-checked in
news sources; claims are hedged as claims ("TEHRAN CLAIMS",
"KYIV CLAIMS").
