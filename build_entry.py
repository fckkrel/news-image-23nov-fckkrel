#!/usr/bin/env python3
"""Build entry.png: a dense one-page world front page for Monday 23 November 2026.

Written for the MakeFun news-image bounty. Draws everything with Pillow from the
story list below; no network, no randomness. Run:  python3 build_entry.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"
SERIF_B = FONT_DIR + "LiberationSerif-Bold.ttf"

INK = (17, 17, 17)
PAPER = (250, 247, 240)
GREY = (85, 85, 85)
WHITE = (255, 255, 255)

DATE = "MONDAY 23 NOVEMBER 2026"

LEAD = {
    "kicker": "UKRAINE  ·  OFF LIBYA",
    "head": "Ukraine sinks Russian warship off Libya",
    "deck": "Sea drones sink the corvette Merkury 2,400 km from the front; cargo ship hit, helicopter destroyed, Kyiv says. NATO meets on the missiles in Poland.",
}

# (region label, colour, [headlines])
COLUMNS = [
    [
        ("EUROPE", (27, 73, 140), [
            "NATO meets on Monday over 3 Russian missiles in Poland",
            "COP31 blame game: Australia pressed to sack Bowen",
            "Thousands rally in Istanbul against media takeover",
            "Belgian airports shut in austerity strike",
            "Denmark: Russia plotted to kill rapper Kyivstoner",
        ]),
        ("MIDDLE EAST", (160, 60, 20), [
            "Trump: Iran ships testing blockade end at sea bottom",
            "Iran vows 'every means' against US blockade",
            "Houthis claim Saudi refinery hit; Saudi strikes Hodeida",
            "Netanyahu-Eisenkot coalition talks end with no deal",
            "Gaza war left widespread contamination, experts say",
        ]),
    ],
    [
        ("ASIA-PACIFIC", (150, 25, 45), [
            "Cikande fire: 24 dead confirmed, 30 still missing",
            "Nepal PM Balen Shah meets Modi in New Delhi",
            "India 3rd in Asia Power Index, ahead of Japan",
            "Nikkei falls 5.06% as AI sell-off spreads in Asia",
            "South Korea education minister quits over exam scandal",
            "China sentences official to death for spying",
        ]),
        ("AFRICA", (20, 110, 60), [
            "Drone attacks kill five children in Khartoum",
            "Eastern Libya seeks UN inquiry into ship attacks",
            "Kenya and DR Congo agree to restore ties",
            "Ethiopia violence strains health system, WHO warns",
            "EU seeks answers over Sudan chemical attacks",
        ]),
    ],
    [
        ("NORTH AMERICA", (60, 60, 110), [
            "Democrats reach 258 House seats, most since 1992",
            "Trump signs law ending the penny after 232 years",
            "Delta outage delays 1,600 flights for Thanksgiving",
            "Trump to confront Newsom over 548 death-row sparings",
            "Trump urges Nvidia to rehire Jensen Huang",
        ]),
        ("LATIN AMERICA", (120, 75, 10), [
            "Bolsonaro still in intensive care, hospital says",
            "Peru aftershocks continue after Friday's M6.7 quake",
            "Plus Ultra halts flights to South America",
        ]),
        ("MARKETS · SCIENCE · SPORT", (40, 40, 40), [
            "Marquez wins eighth MotoGP title in Portugal",
            "49ers rout Vikings 35-10 in Mexico City return",
            "Lions, Bears both 8-2 before Thanksgiving clash",
            "TCU fires coach Sonny Dykes after five seasons",
        ]),
    ],
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def column_height(draw, col, fnt, lh, text_w):
    h = 0
    for _label, _colour, heads in col:
        h += 26 + 6
        for head in heads:
            h += len(wrap(draw, head, fnt, text_w)) * lh + 7
        h += 6
    return h


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    n_stories = 1 + sum(len(h) for col in COLUMNS for _, _, h in col)
    n_regions = 7

    # masthead
    centred(d, 6, "THE WORLD", font(SERIF_B, 70), INK)
    d.rectangle([0, 86, W, 132], fill=INK)
    centred(d, 90, DATE, font(SANS_B, 36), WHITE)
    centred(d, 137, f"ONE DAY IN THE NEWS  ·  {n_stories} STORIES  ·  {n_regions} REGIONS  ·  ALL DATED 23 NOV 2026",
            font(SANS_B, 14), GREY)
    d.line([24, 160, W - 24, 160], fill=INK, width=2)

    # lead story
    y = 166
    d.text((24, y), LEAD["kicker"], font=font(SANS_B, 14), fill=(20, 110, 60))
    y += 20
    lead_size = 44
    while d.textlength(LEAD["head"], font=font(SERIF_B, lead_size)) > W - 48:
        lead_size -= 1  # keep the lead headline on one line
    lead_f = font(SERIF_B, lead_size)
    d.text((24, y), LEAD["head"], font=lead_f, fill=INK)
    y += lead_size + 6
    deck_f = font(SANS, 17)
    for line in wrap(d, LEAD["deck"], deck_f, W - 48):
        d.text((24, y + 2), line, font=deck_f, fill=GREY)
        y += 22
    y += 8
    d.line([24, y, W - 24, y], fill=INK, width=2)
    top = y + 8

    # three columns of region sections
    gutter, margin = 18, 20
    col_w = (W - 2 * margin - 2 * gutter) // 3
    text_w = col_w - 16
    avail = H - 24 - top
    size = 20
    while size > 11:
        fnt, lh = font(SANS_B, size), size + 3
        if max(column_height(d, c, fnt, lh, text_w) for c in COLUMNS) <= avail:
            break
        size -= 1
    else:
        raise SystemExit("stories do not fit")
    label_f = font(SANS_B, 15)
    for i, col in enumerate(COLUMNS):
        x = margin + i * (col_w + gutter)
        cy = top
        # share this column's spare room between its stories so columns end level
        spare = avail - column_height(d, col, fnt, lh, text_w)
        n_heads = sum(len(h) for _, _, h in col)
        pad = min(14, spare // n_heads)
        for label, colour, heads in col:
            d.rectangle([x, cy, x + col_w, cy + 24], fill=colour)
            d.text((x + 8, cy + 4), label, font=label_f, fill=WHITE)
            cy += 26 + 6
            for head in heads:
                d.rectangle([x + 2, cy + size // 2 - 3, x + 8, cy + size // 2 + 3], fill=colour)
                for line in wrap(d, head, fnt, text_w):
                    d.text((x + 16, cy), line, font=fnt, fill=INK)
                    cy += lh
                cy += 7 + pad
            cy += 6
        assert cy <= H - 22, (i, cy)
        if i:
            d.line([x - gutter // 2, top, x - gutter // 2, H - 26], fill=(190, 185, 175), width=1)

    # footer
    d.line([24, H - 22, W - 24, H - 22], fill=INK, width=1)
    centred(d, H - 18, "The World  ·  Monday 23 November 2026  ·  news of this one day only", font(SANS, 12), GREY)

    out = img.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    path = os.path.join(HERE, "entry.png")
    out.save(path, format="PNG", optimize=True)
    print("font size", size, "stories", n_stories, "bytes", os.path.getsize(path))


if __name__ == "__main__":
    build()
