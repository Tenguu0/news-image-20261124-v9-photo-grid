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

## How to run

Requirements: Python 3.12 or newer, with Pillow (PIL) installed —
nothing else, and no network access is needed. The program reads the
twelve pictures already committed under `assets/` and typesets the
page from them.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

It writes `out/entry.png` (1024x1024 PNG) and exits 0. If
`MAKEFUN_OUTPUT_DIR` is not set, or any of the twelve pictures is
missing from `assets/`, it prints an error to stderr and exits 2
instead of writing a partial page.

Determinism: the build uses no network, no randomness, and no clock,
so every run produces byte-identical output. Verify it yourself:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/v9-run1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/v9-run2 python3 main.py
sha256sum /tmp/v9-run1/entry.png /tmp/v9-run2/entry.png entry.png
```

All three hashes should match — the committed `entry.png` is the
reference output.

## How it works

`main.py` composites the page from the twelve pictures committed
under `assets/` (AI-generated illustrations, one per story): a
newsprint masthead, then the 3x4 grid — picture on top of each cell
with a place tag, headline, and summary line below. Every story on
the page is a real event from 24 November 2026, cross-checked in
news sources; claims are hedged as claims ("TEHRAN CLAIMS",
"KYIV CLAIMS").

## The twelve stories

Every story below is a real event reported on 24 November 2026.
Figures were cross-checked against at least two independent reports;
one-sided claims stay labelled as claims on the page rather than
stated as fact.

1. **Bahrain** — Iran's Revolutionary Guard says its missiles and
   drones struck two radars of US Patriot batteries in Bahrain;
   Bahrain says the strike hit a civilian site on Sitra Island,
   wounding two. Sources: AFP, Al Jazeera, Middle East Eye.
2. **Kyiv** — Russian strikes on the Kyiv region killed at least 15
   people over the weekend, and the power grid faces months of repair
   as winter sets in. Sources: UN News, Euronews, Al Jazeera, AFP,
   Reuters.
3. **Antalya** — the COP31 climate talks collapsed without a deal
   after the draft pact left out any mention of fossil fuels.
   Sources: CNN, Le Monde, CNBC Africa.
4. **The Hague** — the International Court of Justice ruled 9–6
   that Myanmar committed genocide against the Rohingya, the first
   time the court has held a state responsible for genocide.
   Sources: Human Rights Watch, CNN, Le Monde, OHCHR.
5. **Shenzhen** — the first ever three-way meeting of Xi, Trump and
   Putin ended without a breakthrough on Ukraine or Iran. Sources:
   RFE/RL, AP.
6. **Turin** — Carlos Alcaraz beat Alexander Zverev 6–2, 7–6 to win
   his first ATP Finals title and a record $5.17M cheque. Sources:
   ATP Tour, BBC, The Times.
7. **Libya** — Kyiv claims a Russian warship was sunk off the
   Libyan coast; Moscow has said nothing about the claim.
8. **Seoul** — South Korea scrambled fighter jets after Russian
   aircraft entered its air defence identification zone.
9. **Java** — a fire at a candy factory killed 24 people, with 34
   more missing as crews fought the blaze.
10. **Colombia** — a car bomb struck the governor's office in Meta
    province; the toll was still feared to rise.
11. **Himalayas** — floods left 4 people dead and around 100
    missing as rivers burst their banks and swamped villages.
12. **Dhaka** — Bangladesh began vaccinating 50 million children
    against typhoid, the world's largest drive of its kind.

Stories 7–12 are wire-reported events from the same news day; the
page hedges the sinking claim (story 7) as Kyiv's claim, not as
established fact.

## Design notes

- One format, repeated twelve times: every cell is a picture on top
  (325x146), a place-tag chip in the corner, a bold headline of up
  to two lines, and a single summary line underneath. Same cell
  size, same fonts, same spacing — the grid, not any single story,
  carries the page.
- The pictures are matched to their stories, not decorative: a
  burning radar base under a fighter jet for Bahrain, rescuers in a
  dark Kyiv street, an empty COP31 hall, the court bench in The
  Hague, three leaders deadlocked in Shenzhen, Alcaraz lifting the
  trophy, and so on. All twelve are AI-generated illustrations
  committed under `assets/`; the footer says so plainly ("Pictures
  are AI-generated illustrations.").
- Density on purpose: three columns by four rows fill the 1024x1024
  page edge to edge, with a 10-pixel gutter and a thin frame around
  each cell. No story gets a bigger slot than any other — the photo
  grid is the point.
- Typography: DejaVu Serif Bold (40pt) for the masthead, DejaVu Sans
  Bold for headlines (shrinking from 17pt down to 13pt to fit two
  lines), DejaVu Sans for summaries (12pt down to 10pt, one line).
  Headline and summary text shrink to fit rather than wrapping or
  overflowing the cell.
