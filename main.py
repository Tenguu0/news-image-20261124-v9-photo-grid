#!/usr/bin/env python3
"""The World in One Page - Photo Grid, 24 November 2026.

A make.fun entry for news-image-20261124: twelve real stories from
Tuesday 24 November 2026 on one 1024x1024 newspaper front page, as a
photo grid - three columns by four rows. Every cell is led by a
picture that shows what the story is about (a radar base under fire,
a sinking warship, a tennis champion lifting his trophy, a flooded
mountain village...), then a bold headline and one summary line.

The twelve pictures are AI-generated illustrations committed with
this repo under assets/; this program composites the page from them.
No network, no randomness, no clock - every run writes the same
bytes, so entry.png is byte-identical across runs.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
Writes out/entry.png (1024x1024 PNG). Exits 2 with a loud error on
stderr when MAKEFUN_OUTPUT_DIR is not set or an asset is missing.
"""

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

PAGE_W = 1024
PAGE_H = 1024
PAPER = (251, 248, 241)
INK = (17, 17, 17)
MUTED = (96, 90, 78)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

# (asset file, tag, headline, summary) - all twelve stories are real
# events reported on 24 November 2026; claims are hedged as claims.
STORIES = [
    ("img01-bahrain.webp", "BAHRAIN",
     "IRGC CLAIMS PATRIOT RADARS HIT IN BAHRAIN",
     "Tehran says 2 radars struck; 20th MQ-1 downed."),
    ("img02-kyiv.webp", "KYIV",
     "15 DEAD AS KYIV REGION IS HIT AGAIN",
     "Power grid may take months to repair."),
    ("img03-cop31.webp", "ANTALYA",
     "COP31 COLLAPSES WITHOUT A DEAL",
     "Antalya pact rejected over fossil fuels."),
    ("img04-icj.webp", "THE HAGUE",
     "MYANMAR GUILTY OF GENOCIDE, ICJ RULES 9-6",
     "Court finds Rohingya genocide; act, it says."),
    ("img05-trilateral.webp", "SHENZHEN",
     "XI-TRUMP-PUTIN SUMMIT ENDS IN DEADLOCK",
     "Shenzhen talks agree on oil, little else."),
    ("img06-alcaraz.webp", "TURIN",
     "ALCARAZ WINS FIRST ATP FINALS TITLE",
     "Beats Zverev 6-2, 7-6; record $5.17M."),
    ("img07-warship.webp", "LIBYA",
     "KYIV CLAIMS RUSSIAN WARSHIP SUNK OFF LIBYA",
     "Moscow silent on Kyiv's sinking claim."),
    ("img08-jets.webp", "SEOUL",
     "SEOUL SCRAMBLES JETS AS RUSSIAN PLANES ENTER ZONE",
     "Fighters meet incursion in defence zone."),
    ("img09-factory-fire.webp", "JAVA",
     "JAVA CANDY FACTORY FIRE KILLS 24",
     "34 missing as crews battle the blaze."),
    ("img10-carbomb.webp", "COLOMBIA",
     "CAR BOMB HITS GOVERNOR'S OFFICE IN COLOMBIA",
     "Blast in Meta province; toll feared."),
    ("img11-flood.webp", "HIMALAYAS",
     "HIMALAYAN FLOODS LEAVE 4 DEAD, ~100 MISSING",
     "Villages swamped as rivers burst banks."),
    ("img12-vaccine.webp", "DHAKA",
     "BANGLADESH VACCINATES 50M CHILDREN VS TYPHOID",
     "World's biggest typhoid drive under way."),
]

GRID_X = 14
GRID_Y = 104
GRID_W = 996
GRID_H = 896
COLS = 3
ROWS = 4
GUTTER_X = 10
GUTTER_Y = 8
CELL_W = (GRID_W - (COLS - 1) * GUTTER_X) // COLS
CELL_H = (GRID_H - (ROWS - 1) * GUTTER_Y) // ROWS
IMG_H = 146
TEXT_PAD = 6


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_text(draw, text, names, sizes, max_width, max_lines):
    """Pick the largest font size whose wrap fits max_lines.

    Returns (font, lines). Sizes are tried from large to small.
    """
    for size in sizes:
        fnt = font(names, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(names, sizes[-1])
    return fnt, wrap(draw, text, fnt, max_width)


def build_page(base_dir):
    assets = base_dir / "assets"
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead.
    masthead = font("DejaVuSerif-Bold.ttf", 40)
    title = "THE WORLD IN ONE PAGE"
    tw = draw.textlength(title, font=masthead)
    draw.text(((PAGE_W - tw) / 2, 12), title, font=masthead, fill=INK)
    dateline = font("DejaVuSans.ttf", 13)
    sub = "TUESDAY, 24 NOVEMBER 2026  -  TWELVE STORIES IN PICTURES"
    sw = draw.textlength(sub, font=dateline)
    draw.text(((PAGE_W - sw) / 2, 62), sub, font=dateline, fill=MUTED)
    draw.line([(GRID_X, 90), (PAGE_W - GRID_X, 90)], fill=INK, width=2)
    draw.line([(GRID_X, 94), (PAGE_W - GRID_X, 94)], fill=INK, width=1)

    # Photo grid, 3 columns x 4 rows.
    for index, (asset_name, tag, headline, summary) in enumerate(STORIES):
        row, col = divmod(index, COLS)
        x = GRID_X + col * (CELL_W + GUTTER_X)
        y = GRID_Y + row * (CELL_H + GUTTER_Y)

        # Picture on top of the cell, centre-cropped to the box.
        with Image.open(assets / asset_name) as photo:
            picture = ImageOps.fit(
                photo.convert("RGB"), (CELL_W, IMG_H), Image.LANCZOS
            )
        page.paste(picture, (x, y))

        # Tag chip on the picture, top left.
        tag_font = font("DejaVuSans-Bold.ttf", 11)
        tag_w = draw.textlength(tag, font=tag_font)
        chip_w = int(tag_w) + 12
        chip_h = 18
        draw.rectangle([x, y, x + chip_w, y + chip_h], fill=INK)
        draw.text((x + 6, y + 3), tag, font=tag_font, fill=(255, 255, 255))

        # Headline, bold, up to two lines, shrinking to fit.
        text_w = CELL_W - 2 * TEXT_PAD
        head_font, head_lines = fit_text(
            draw, headline, "DejaVuSans-Bold.ttf",
            [17, 16, 15, 14, 13], text_w, 2,
        )
        ty = y + IMG_H + 6
        for line in head_lines:
            draw.text((x + TEXT_PAD, ty), line, font=head_font, fill=INK)
            ty += head_font.size + 3

        # Summary, one line, shrinking to fit.
        sum_font, sum_lines = fit_text(
            draw, summary, "DejaVuSans.ttf", [12, 11, 10], text_w, 1,
        )
        draw.text((x + TEXT_PAD, ty + 2), sum_lines[0], font=sum_font,
                  fill=MUTED)

        # Thin frame around the whole cell.
        draw.rectangle(
            [x, y, x + CELL_W - 1, y + CELL_H - 1], outline=INK, width=1
        )

    # Footer.
    foot = font("DejaVuSans.ttf", 10)
    note = "All stories reported 24 November 2026. Pictures are AI-generated illustrations."
    fw = draw.textlength(note, font=foot)
    draw.text(((PAGE_W - fw) / 2, 1008), note, font=foot, fill=MUTED)
    return page


def publish() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 2
    base_dir = Path(__file__).resolve().parent
    assets = base_dir / "assets"
    for asset_name, _, _, _ in STORIES:
        if not (assets / asset_name).is_file():
            print(f"error: missing asset: assets/{asset_name}",
                  file=sys.stderr)
            return 2
    page = build_page(base_dir)
    os.makedirs(out_dir, exist_ok=True)
    page.save(os.path.join(out_dir, "entry.png"))
    return 0


raise SystemExit(publish())
