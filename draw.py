#!/usr/bin/env python3
"""Draw the news-image-20261118 front page, v2: 'Wednesday 18 November 2026'.

A dense broadsheet, 1024x1024, in the genre the daily news-image leaders
use: dark navy masthead with the date and a one-line promise, three
illustrated lead cards with caption strips, eight medium cards with a small
square picture at the left, a BY THE NUMBERS strip, a dotted world map with
numbered pins, and a two-column list of the rest of the day. 36 verified
stories in all.

Every story was checked against real reporting of 18 November 2026
(AP / Reuters / AFP / BBC / Al Jazeera / CNBC / IMD / CSK, plus the market
close, the APEC opening and the An-12, Tokyo-jets and Apple-outage reports
of the day). Contested claims are attributed in the text. The image is
drawn with Pillow (flat procedural art, no copied photograph) and written
to entry.png next to this file.

The dotted map is built from Natural Earth 110m admin-0 countries (public
domain), loaded from /tmp/ne110m.geojson at build time.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
GEOJSON = "/tmp/ne110m.geojson"

W = H = 1024
PAPER = (247, 243, 232)
NAVY = (18, 32, 62)
NAVY_SOFT = (200, 210, 225)
GOLD = (212, 175, 90)
INK = (17, 17, 17)
BODY = (45, 42, 36)
GREY = (110, 105, 92)
RULE = (201, 194, 176)
RED = (176, 42, 32)
CARD = (255, 255, 255)
CARD_EDGE = (205, 198, 182)
MAP_SEA = (221, 233, 242)
DOT = (105, 115, 105)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
NOTO = "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_KICK = font("DejaVuSans-Bold.ttf", 14)
F_DATE = font("DejaVuSerif-Bold.ttf", 54)
F_DECK = ImageFont.truetype(NOTO, 13)
F_CAP = font("DejaVuSans-Bold.ttf", 10)
F_KICK2 = font("DejaVuSans-Bold.ttf", 11)
F_HERO_H = font("DejaVuSerif-Bold.ttf", 20)
F_HERO_D = font("DejaVuSans.ttf", 12)
F_MED_K = font("DejaVuSans-Bold.ttf", 10)
F_MED_H = font("DejaVuSerif-Bold.ttf", 14)
F_MED_D = font("DejaVuSans.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 20)
F_NUM_C = font("DejaVuSans.ttf", 10)
F_ALSO_N = font("DejaVuSans-Bold.ttf", 9)
F_ALSO_L = font("DejaVuSans-Bold.ttf", 9)
F_ALSO_D = font("DejaVuSans.ttf", 9)
F_FOOT = ImageFont.truetype(NOTO, 11)
F_MAP_CAP = font("DejaVuSans.ttf", 10)
F_PIN = font("DejaVuSans-Bold.ttf", 11)

# ---------------------------------------------------------------- stories
# heroes: (headline, deck, kicker, caption strip, accent)
HEROES = [
    ("US and Iran trade fire over Bahrain",
     "Iranian drones target a US radar at Sheikh Isa base; Bahrain and US "
     "forces intercept them, and US jets hit a missile site on Qeshm Island.",
     "MIDDLE EAST \u00b7 CONFLICT", "SHEIKH ISA BASE \u00b7 QESHM ISLAND",
     (211, 84, 0)),
    ("A span of the Crimea bridge falls into the sea",
     "Kyiv says a second strike in two days destroyed the road arch; "
     "Moscow says it downed 1,441 drones, and the rail arch stands.",
     "EUROPE \u00b7 WAR IN UKRAINE", "KERCH STRAIT \u00b7 19 KM CROSSING",
     (125, 60, 152)),
    ("Trump in Manila for first Quad in two years",
     "He meets Modi, Takaichi and Albanese at the ASEAN sidelines, sees "
     "Marcos today, then heads to Shenzhen for APEC.",
     "ASIA \u00b7 DIPLOMACY", "MANILA \u00b7 FIRST QUAD IN TWO YEARS",
     (30, 132, 73)),
]

# mediums: (headline, deck, kicker, accent)
MEDIUM = [
    ("Nvidia revenue doubles to $115.8bn",
     "First results since Huang resigned; data centre sales hit $107.6bn.",
     "MARKETS \u00b7 TECHNOLOGY", (36, 113, 163)),
    ("Cyclone Akvan bears down on India's coast",
     "Heads for Andhra Pradesh and Odisha; heavy rain from today, "
     "landfall Friday.",
     "ASIA \u00b7 WEATHER", (30, 132, 73)),
    ("Knesset elects Kahana, a blow to Netanyahu",
     "Eisenkot's ally wins 66-52, replacing Likud's Ohana and taking "
     "the agenda.",
     "MIDDLE EAST \u00b7 POLITICS", (211, 84, 0)),
    ("EU plans a \u20ac45bn loan for Ukraine",
     "Brussels would cover two-thirds of Kyiv's \u20ac70bn 2027 gap.",
     "EUROPE \u00b7 UKRAINE AID", (125, 60, 152)),
    ("APEC opens in Shenzhen with Xi keynote",
     "Leaders of 21 Pacific economies meet; Xi urges free trade as "
     "Trump arrives.",
     "CHINA \u00b7 SUMMIT", (160, 60, 120)),
    ("China cuts tariffs for Canada as Xi meets Carney",
     "Tariff relief on pork and seafood as the leaders extend trade "
     "deals.",
     "TRADE \u00b7 CHINA\u2013CANADA", (30, 132, 73)),
    ("Wall Street slides as the Dow drops 849 points",
     "The S&P 500 closed at its lowest since July in a fourth straight "
     "fall.",
     "MARKETS \u00b7 UNITED STATES", (36, 113, 163)),
    ("US loses measles elimination status",
     "The worst outbreak since 1991 ends three decades of elimination.",
     "HEALTH \u00b7 UNITED STATES", (125, 60, 152)),
]

# also: (bold lead, deck) -- numbers 12..36, one short line each
ALSO = [
    ("Thailand deal", "Trump signs trade pact"),
    ("Pope Leo", "hit in the eye by a rosary"),
    ("Telegram blocked", "Jordan, Iraq cite security"),
    ("Taiwan curbs", "US presses UN, China hits back"),
    ("AI bubble", "Baidu chief warns before APEC"),
    ("Amazon", "$7bn for India's renewables"),
    ("ITU Council", "India re-elected to 2030"),
    ("ICC", "Jay Shah re-elected chairman"),
    ("FIFA vote", "UEFA backs Diallo vs Infantino"),
    ("ASEAN", "Modi offers free e-visas, sea ties"),
    ("Pakistan\u2013Iran", "stress regional engagement"),
    ("ASEAN energy", "Japan offers storage access"),
    ("Ukraine toll", "UN: 372 civilians killed in Oct"),
    ("Sudan toll", "UN confirms 2,230 deaths"),
    ("Gaza aid", "WFP: one meal every two days"),
    ("Latvia", "confidence vote backs Kulbergs"),
    ("Asif Merchant", "jailed 27.5 years over plot"),
    ("Grammys", "2027 nominations announced"),
    ("Starship", "SpaceX catches a falling booster"),
    ("Dhoni", "ends IPL career, mentors CSK"),
    ("Settler sanctions", "Britain freezes 8 firms"),
    ("Siberia crash", "all 19 aboard An-12 killed"),
    ("Tokyo jets", "two suspected Russian planes"),
    ("Apple outage", "hits iCloud, App Store"),
    ("NSA outage", "reports of a network failure"),
]

# numbers strip: (big value, caption)
NUMBERS = [
    ("66\u201352", "Kahana's margin for speaker"),
    ("$115.8bn", "Nvidia revenue, up 103%"),
    ("145 km/h", "Akvan gusts at landfall"),
    ("200,000", "Odisha moves from the coast"),
    ("1,441", "drones Moscow says it downed"),
    ("849", "Dow points lost"),
]

# map pins: story number -> (lon, lat, dx, dy) nudge for the cluster
PINS = {
    1: (50.6, 26.2, 10, 8), 2: (33.9, 45.4, 4, -14), 3: (121.0, 14.6, 0, 0),
    4: (-122.0, 37.4, 0, 0), 5: (90.0, 18.0, 0, 0),
    6: (35.2, 31.8, -18, 10), 7: (4.4, 50.9, -16, -10),
    8: (114.1, 22.5, 0, 0), 9: (-75.7, 45.4, -16, -14),
    10: (-74.0, 40.7, 14, 6), 11: (-84.4, 33.8, -12, 14),
}


# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def pin_badge(draw, x, y, n, colour, r=9):
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=colour)
    t = str(n)
    tw = draw.textlength(t, font=F_PIN)
    draw.text((x + r - tw / 2, y + r - 6), t, font=F_PIN,
              fill=(255, 255, 255))


def kicker_line(draw, x, y, n, label, colour):
    pin_badge(draw, x, y - 2, n, colour, r=9)
    draw.text((x + 24, y), label, font=F_KICK2, fill=colour)


def caption_strip(draw, x, y, w, text):
    """Dark label bar across the bottom of a hero picture."""
    draw.rectangle([x, y, x + w, y + 18], fill=(10, 14, 26))
    draw.text((x + 8, y + 3), text, font=F_CAP, fill=(255, 255, 255))


def star5(d, cx, cy, r, colour, rot=-math.pi / 2):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = rot + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=colour)


# ---------------------------------------------------------------- hero pictures
def hero_bahrain(d, x, y, w, h):
    """Night over the Gulf: radar dome, jet silhouette, moon, dark sea."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 24, 48))
    # stars
    for sx, sy in [(0.08, 0.12), (0.30, 0.07), (0.52, 0.14), (0.70, 0.08),
                   (0.90, 0.16), (0.18, 0.28), (0.62, 0.26)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1,
                   y + h * sy + 1], fill=(220, 225, 240))
    # moon
    d.ellipse([x + w * 0.84, y + h * 0.08, x + w * 0.94, y + h * 0.26],
              fill=(245, 238, 200))
    # radar dome, centre left -- big and pale so it reads at small size
    cx, cy = x + w * 0.30, y + h * 0.60
    d.arc([cx - 46, cy - 46, cx + 46, cy + 14], 180, 360,
          fill=(200, 210, 225), width=7)
    d.line([cx, cy, cx + 34, cy - 40], fill=(200, 210, 225), width=5)
    d.ellipse([cx + 30, cy - 44, cx + 38, cy - 36], fill=(255, 90, 60))
    d.rectangle([cx - 4, cy + 2, cx + 4, y + h * 0.80], fill=(160, 170, 185))
    # jet silhouette, upper right, bigger, with a red trail
    jx, jy = x + w * 0.58, y + h * 0.28
    d.polygon([(jx, jy), (jx + 62, jy + 8), (jx + 14, jy + 14),
               (jx + 30, jy + 22), (jx + 6, jy + 16)], fill=(8, 10, 18))
    d.line([jx - 78, jy + 8, jx - 6, jy + 8], fill=(255, 90, 60), width=3)
    d.line([jx - 60, jy + 15, jx - 2, jy + 13], fill=(255, 150, 80), width=2)
    # interception flash over the sea, right side
    fx, fy = x + w * 0.82, y + h * 0.66
    star5(d, fx, fy, 10, (255, 160, 60))
    star5(d, fx, fy, 5, (255, 90, 40))
    # sea band with lit windows
    d.rectangle([x, y + h * 0.80, x + w, y + h], fill=(10, 14, 26))
    for bx in (0.06, 0.52, 0.78):
        d.rectangle([x + w * bx, y + h * 0.80, x + w * bx + w * 0.10,
                     y + h * 0.80 + 8], fill=(8, 10, 20))
        d.rectangle([x + w * bx + 3, y + h * 0.80 + 2, x + w * bx + w * 0.10 - 3,
                     y + h * 0.80 + 5], fill=(255, 200, 90))
    caption_strip(d, x, y + h - 18, w, HEROES[0][3])


def hero_bridge(d, x, y, w, h):
    """Pale sky, a bridge arch with its middle span dropped into the sea."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 206, 214))
    d.ellipse([x + w * 0.80, y + h * 0.06, x + w * 0.90, y + h * 0.22],
              fill=(240, 220, 140))
    # smoke over the gap
    for cx, cy, r in [(0.46, 0.16, 12), (0.54, 0.10, 15), (0.62, 0.17, 10)]:
        d.ellipse([x + w * cx - r, y + h * cy - r, x + w * cx + r,
                   y + h * cy + r], fill=(110, 112, 116))
    # sea
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(74, 102, 128))
    for i in range(24):
        d.line([x + i * w / 24, y + h * 0.62 + (i % 3),
                x + i * w / 24 + 16, y + h * 0.62 + (i % 3)],
               fill=(120, 150, 175), width=2)
    # arch over the left span, thick so it reads at small size
    d.arc([x + w * 0.06, y + h * 0.20, x + w * 0.40, y + h * 0.60], 180, 360,
          fill=(110, 114, 120), width=8)
    # deck: left span, fallen middle, right span
    d.rectangle([x, y + h * 0.48, x + w * 0.38, y + h * 0.54],
                fill=(52, 54, 60))
    d.polygon([(x + w * 0.38, y + h * 0.48), (x + w * 0.50, y + h * 0.62),
               (x + w * 0.55, y + h * 0.60), (x + w * 0.44, y + h * 0.48)],
              fill=(52, 54, 60))
    d.rectangle([x + w * 0.64, y + h * 0.48, x + w, y + h * 0.54],
                fill=(52, 54, 60))
    # towers
    for tx in (0.10, 0.88):
        d.rectangle([x + w * tx, y + h * 0.28, x + w * tx + 6, y + h * 0.54],
                    fill=(70, 72, 78))
    # debris in the water
    d.ellipse([x + w * 0.50, y + h * 0.62, x + w * 0.58, y + h * 0.68],
              fill=(230, 235, 240))
    caption_strip(d, x, y + h - 18, w, HEROES[1][3])


def hero_summit(d, x, y, w, h):
    """Warm dusk, a city skyline and four flags over a table."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 186, 138))
    d.ellipse([x + w * 0.84, y + h * 0.06, x + w * 0.94, y + h * 0.24],
              fill=(245, 225, 150))
    # skyline
    for bx, bw, bh in [(0.02, 0.12, 0.34), (0.16, 0.10, 0.46),
                       (0.28, 0.14, 0.30), (0.44, 0.10, 0.52),
                       (0.56, 0.13, 0.38), (0.71, 0.11, 0.48),
                       (0.84, 0.12, 0.34)]:
        d.rectangle([x + w * bx, y + h * (0.78 - bh), x + w * (bx + bw),
                     y + h * 0.78], fill=(30, 40, 60))
        for wy in range(2):
            for wx in range(2):
                d.rectangle([x + w * (bx + 0.02 + wx * 0.04),
                             y + h * (0.78 - bh + 0.06 + wy * 0.12),
                             x + w * (bx + 0.04 + wx * 0.04),
                             y + h * (0.78 - bh + 0.10 + wy * 0.12)],
                            fill=(255, 210, 90))
    # four flags on poles
    for i in range(4):
        fx = x + w * (0.10 + i * 0.22)
        d.line([fx, y + h * 0.08, fx, y + h * 0.62], fill=(60, 45, 30),
               width=3)
        fw, fh = 34, 20
        if i == 0:  # United States
            for s in range(7):
                d.rectangle([fx, y + h * 0.08 + s * fh / 7,
                             fx + fw, y + h * 0.08 + (s + 1) * fh / 7],
                            fill=(178, 34, 52) if s % 2 == 0
                            else (255, 255, 255))
            d.rectangle([fx, y + h * 0.08, fx + 14,
                         y + h * 0.08 + fh * 4 / 7], fill=(30, 50, 110))
            star5(d, fx + 7, y + h * 0.08 + fh * 2 / 7, 3, (255, 255, 255))
        elif i == 1:  # India
            d.rectangle([fx, y + h * 0.08, fx + fw, y + h * 0.08 + fh / 3],
                        fill=(255, 153, 51))
            d.rectangle([fx, y + h * 0.08 + fh / 3, fx + fw,
                         y + h * 0.08 + 2 * fh / 3], fill=(255, 255, 255))
            d.rectangle([fx, y + h * 0.08 + 2 * fh / 3, fx + fw,
                         y + h * 0.08 + fh], fill=(19, 136, 8))
            d.ellipse([fx + 13, y + h * 0.08 + fh / 3 + 2, fx + 21,
                       y + h * 0.08 + 2 * fh / 3 - 2],
                      outline=(0, 56, 147))
        elif i == 2:  # Japan
            d.rectangle([fx, y + h * 0.08, fx + fw, y + h * 0.08 + fh],
                        fill=(255, 255, 255))
            d.ellipse([fx + 11, y + h * 0.08 + 4, fx + 23,
                       y + h * 0.08 + fh - 4], fill=(188, 0, 45))
        else:  # Australia
            d.rectangle([fx, y + h * 0.08, fx + fw, y + h * 0.08 + fh],
                        fill=(0, 40, 104))
            d.rectangle([fx, y + h * 0.08, fx + 14, y + h * 0.08 + fh / 2],
                        fill=(255, 255, 255))
            d.line([fx + 7, y + h * 0.08, fx + 7, y + h * 0.08 + fh / 2],
                   fill=(200, 16, 46), width=2)
            d.line([fx, y + h * 0.08 + fh / 4, fx + 14,
                    y + h * 0.08 + fh / 4], fill=(200, 16, 46), width=2)
            star5(d, fx + 26, y + h * 0.08 + fh * 0.68, 4, (255, 215, 0))
    # table band with seated figures, kept clear of the caption strip
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(122, 84, 52))
    for i, suit in enumerate([(40, 44, 66), (70, 60, 50), (50, 70, 90),
                              (90, 50, 40)]):
        px = x + w * (0.13 + i * 0.23)
        d.ellipse([px - 9, y + h * 0.34, px + 9, y + h * 0.52],
                  fill=(232, 190, 150))
        d.rounded_rectangle([px - 16, y + h * 0.50, px + 16, y + h * 0.76],
                            radius=8, fill=suit)
        d.polygon([(px - 4, y + h * 0.50), (px + 4, y + h * 0.50),
                   (px, y + h * 0.62)], fill=(255, 255, 255))
    caption_strip(d, x, y + h - 18, w, HEROES[2][3])


HERO_ILLU = [hero_bahrain, hero_bridge, hero_summit]


# ---------------------------------------------------------------- medium icons
def icon_chip(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(16, 40, 28))
    for i in range(4):
        d.line([x + 4, y + s * (0.18 + i * 0.2), x + s * 0.30,
                y + s * (0.18 + i * 0.2)], fill=(60, 160, 110), width=2)
        d.line([x + s * 0.70, y + s * (0.18 + i * 0.2), x + s - 4,
                y + s * (0.18 + i * 0.2)], fill=(60, 160, 110), width=2)
    cx, cy, r = x + s / 2, y + s / 2, s * 0.26
    d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=5,
                        fill=(20, 90, 60), outline=(140, 220, 170), width=2)
    d.text((cx - 7, cy - 8), "NV", font=font("DejaVuSans-Bold.ttf", 13),
           fill=(255, 255, 255))
    pts = [(x + s * 0.10, y + s * 0.88), (x + s * 0.38, y + s * 0.72),
           (x + s * 0.62, y + s * 0.76), (x + s * 0.90, y + s * 0.40)]
    d.line(pts, fill=(255, 210, 60), width=3, joint="curve")
    d.polygon([(pts[-1][0] - 9, pts[-1][1] + 2), (pts[-1][0] - 1, pts[-1][1] - 6),
               (pts[-1][0] - 1, pts[-1][1] + 8)], fill=(255, 210, 60))


def icon_cyclone(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(38, 92, 128))
    cx, cy = x + s * 0.45, y + s * 0.52
    for k in range(5):
        r = 8 + k * 6
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8],
              200 + k * 55, 200 + k * 55 + 250,
              fill=(255, 255, 255) if k % 2 else (190, 220, 235), width=4)
    d.ellipse([cx - 7, cy - 6, cx + 7, cy + 6], fill=(255, 240, 200))
    d.polygon([(x + s * 0.72, y), (x + s, y), (x + s, y + s),
               (x + s * 0.78, y + s), (x + s * 0.70, y + s * 0.6)],
              fill=(214, 196, 150))


def icon_knesset(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(196, 210, 225))
    bx, by, bw, bh = x + s * 0.14, y + s * 0.32, s * 0.72, s * 0.52
    d.rectangle([bx, by, bx + bw, by + bh], fill=(120, 130, 145))
    d.polygon([(bx - 6, by), (bx + bw / 2, by - s * 0.20), (bx + bw + 6, by)],
              fill=(90, 100, 118))
    for i in range(5):
        cx = bx + bw * (0.12 + i * 0.19)
        d.rectangle([cx - 4, by + s * 0.08, cx + 4, by + bh],
                    fill=(245, 243, 235))
    d.rounded_rectangle([x + s * 0.06, y + s * 0.70, x + s * 0.24,
                         y + s * 0.80], radius=3, fill=(120, 80, 40))


def icon_euro(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(0, 40, 104))
    cx, cy, r = x + s / 2, y + s / 2, s * 0.34
    for k in range(12):
        a = k * math.pi / 6 - math.pi / 2
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        star5(d, sx, sy, 3, (255, 215, 0))
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 255, 255))
    d.text((cx - 9, cy - 12), "\u20ac", font=font("DejaVuSans-Bold.ttf", 20),
           fill=(0, 40, 104))


def icon_apec(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(0, 96, 96))
    cx, cy, r = x + s / 2, y + s / 2, s * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 210, 210))
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(0, 96, 96), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(0, 96, 96), width=2)
    for px, py in [(0.38, 0.38), (0.62, 0.42), (0.55, 0.62), (0.70, 0.58)]:
        d.ellipse([x + s * px - 3, y + s * py - 3, x + s * px + 3,
                   y + s * py + 3], fill=(188, 30, 25))
    d.text((x + 4, y + s - 14), "21", font=font("DejaVuSans-Bold.ttf", 11),
           fill=(255, 255, 255))


def icon_trade(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(240, 236, 222))
    d.rectangle([x + s * 0.08, y + s * 0.16, x + s * 0.48, y + s * 0.56],
                fill=(222, 41, 16))
    star5(d, x + s * 0.16, y + s * 0.28, 6, (255, 222, 0))
    star5(d, x + s * 0.34, y + s * 0.24, 3, (255, 222, 0))
    d.rectangle([x + s * 0.54, y + s * 0.16, x + s * 0.92, y + s * 0.56],
                fill=(255, 255, 255), outline=(200, 16, 46), width=2)
    d.rectangle([x + s * 0.54, y + s * 0.16, x + s * 0.64, y + s * 0.56],
                fill=(255, 0, 0))
    d.rectangle([x + s * 0.82, y + s * 0.16, x + s * 0.92, y + s * 0.56],
                fill=(255, 0, 0))
    mx, my = x + s * 0.73, y + s * 0.36
    d.polygon([(mx, my - 10), (mx + 3, my - 4), (mx + 8, my - 7),
               (mx + 5, my), (mx + 9, my + 2), (mx + 4, my + 4),
               (mx + 4, my + 10), (mx, my + 6), (mx - 4, my + 10),
               (mx - 4, my + 4), (mx - 9, my + 2), (mx - 5, my),
               (mx - 8, my - 7), (mx - 3, my - 4)], fill=(255, 0, 0))


def icon_chart(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(24, 24, 30))
    pts = [(x + s * 0.10, y + s * 0.30), (x + s * 0.34, y + s * 0.42),
           (x + s * 0.58, y + s * 0.38), (x + s * 0.88, y + s * 0.72)]
    d.line(pts, fill=(230, 60, 50), width=3, joint="curve")
    d.polygon([(pts[-1][0] - 8, pts[-1][1] - 2), (pts[-1][0] + 2, pts[-1][1] + 6),
               (pts[-1][0] - 8, pts[-1][1] + 8)], fill=(230, 60, 50))
    d.text((x + 6, y + s - 18), "-849", font=font("DejaVuSans-Bold.ttf", 14),
           fill=(255, 255, 255))
    d.line([x + 6, y + s * 0.16, x + s - 6, y + s * 0.16],
           fill=(90, 90, 100), width=1)


def icon_virus(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(238, 226, 220))
    for i, (fx, fy, r) in enumerate([(0.28, 0.32, 11), (0.70, 0.30, 13),
                                     (0.50, 0.68, 12)]):
        cx, cy = x + s * fx, y + s * fy
        for k in range(8):
            a = k * math.pi / 4
            d.line([cx + r * math.cos(a), cy + r * math.sin(a),
                    cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a)],
                   fill=(178, 34, 34), width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(198, 60, 50))
        d.ellipse([cx - r * 0.4, cy - r * 0.4, cx + r * 0.2, cy + r * 0.2],
                  fill=(230, 120, 110))


ICONS = {4: icon_chip, 5: icon_cyclone, 6: icon_knesset, 7: icon_euro,
         8: icon_apec, 9: icon_trade, 10: icon_chart, 11: icon_virus}


# ---------------------------------------------------------------- dotted map
def draw_map(d, x, y, w, h):
    """Dot-matrix world map from the Natural Earth polygons, red pins 1-11."""
    d.rectangle([x, y, x + w, y + h], fill=MAP_SEA)
    lat_min, lat_max, lon_min, lon_max = -58, 84, -180, 180

    def px(lon, lat):
        return (x + (lon - lon_min) / (lon_max - lon_min) * w,
                y + (lat_max - lat) / (lat_max - lat_min) * h)

    try:
        data = json.load(open(GEOJSON))
        mask = Image.new("L", (w, h), 0)
        md = ImageDraw.Draw(mask)
        for feat in data["features"]:
            geom = feat["geometry"]
            if geom is None:
                continue
            if geom["type"] == "Polygon":
                polys = [geom["coordinates"]]
            elif geom["type"] == "MultiPolygon":
                polys = geom["coordinates"]
            else:
                continue
            for poly in polys:
                for ring in poly:
                    xs = [p[0] for p in ring]
                    if max(xs) - min(xs) > 300:
                        continue
                    # mask coords are relative to the map box, not the page
                    pts = [((lon - lon_min) / (lon_max - lon_min) * w,
                            (lat_max - lat) / (lat_max - lat_min) * h)
                           for lon, lat in ring]
                    md.polygon(pts, fill=255)
        step = 7
        for gy in range(step // 2, h, step):
            for gx in range(step // 2, w, step):
                if mask.getpixel((gx, gy)):
                    d.ellipse([x + gx - 2, y + gy - 2, x + gx + 2,
                               y + gy + 2], fill=DOT)
    except FileNotFoundError:
        d.text((x + 10, y + 10), "world map data unavailable",
               font=F_MAP_CAP, fill=GREY)
    d.rectangle([x, y, x + w, y + h], outline=(150, 142, 122), width=1)
    for n, (lon, lat, dx, dy) in PINS.items():
        bx, by = px(lon, lat)
        bx += dx
        by += dy
        if dx or dy:
            ox, oy = px(lon, lat)
            d.line([ox, oy, bx, by], fill=(60, 55, 45), width=1)
            d.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=(60, 55, 45))
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        t = str(n)
        tw = d.textlength(t, font=F_PIN)
        d.text((bx - tw / 2, by - 6), t, font=F_PIN, fill=(255, 255, 255))


# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead: dark navy band --------------------------------------
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.text((24, 12), "THE DAY IN WORLD NEWS", font=F_KICK, fill=GOLD)
    right = "36 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE"
    d.text((W - 24 - d.textlength(right, font=F_KICK), 12), right,
           font=F_KICK, fill=GOLD)
    d.text((24, 32), "Wednesday 18 November 2026", font=F_DATE,
           fill=(255, 255, 255))
    d.text((24, 94), "Every story below happened, or was first reported, "
           "on this day.", font=F_DECK, fill=NAVY_SOFT)
    d.rectangle([0, 116, W, 118], fill=GOLD)

    # ---- heroes ---------------------------------------------------------
    hy, hw, hgap = 130, 317, 12
    for i, (head, deck, kick, cap, col) in enumerate(HEROES):
        cx = 24 + i * (hw + hgap)
        HERO_ILLU[i](d, cx, hy, hw, 102)
        kicker_line(d, cx, hy + 110, i + 1, kick, col)
        yy = hy + 128
        for line in wrap(d, head, F_HERO_H, hw)[:3]:
            d.text((cx, yy), line, font=F_HERO_H, fill=INK)
            yy += 23
        yy += 4
        for line in wrap(d, deck, F_HERO_D, hw)[:3]:
            d.text((cx, yy), line, font=F_HERO_D, fill=BODY)
            yy += 15
    d.rectangle([24, 392, W - 24, 393], fill=INK)

    # ---- medium grid: 2 rows x 4, icon at left --------------------------
    my, mh, mw = 404, 126, 238
    for row in range(2):
        for ci in range(4):
            idx = row * 4 + ci
            head, deck, kick, col = MEDIUM[idx]
            n = idx + 4
            cx = 24 + ci * (mw + 8)
            cy = my + row * (mh + 8)
            d.rectangle([cx, cy, cx + mw, cy + mh], fill=CARD,
                        outline=CARD_EDGE, width=1)
            ICONS[n](d, cx + 7, cy + 7, 56)
            tx = cx + 70
            d.text((tx, cy + 9), kick, font=F_MED_K, fill=col)
            yy = cy + 25
            for line in wrap(d, head, F_MED_H, mw - 78)[:3]:
                d.text((tx, yy), line, font=F_MED_H, fill=INK)
                yy += 16
            yy += 2
            for line in wrap(d, deck, F_MED_D, mw - 78)[:3]:
                d.text((tx, yy), line, font=F_MED_D, fill=BODY)
                yy += 12.5
    d.rectangle([24, 672, W - 24, 673], fill=INK)

    # ---- by the numbers --------------------------------------------------
    d.rectangle([24, 682, W - 24, 732], fill=NAVY)
    for i, (val, cap) in enumerate(NUMBERS):
        bx = 24 + i * 163 + 8
        d.text((bx, 690), val, font=F_NUM, fill=GOLD)
        d.text((bx, 714), cap, font=F_NUM_C, fill=(255, 255, 255))

    # ---- bottom: dotted map (left) + also list (right, 2 cols) ----------
    by = 744
    d.text((24, by), "WHERE IT HAPPENED", font=F_KICK, fill=RED)
    d.rectangle([24, by + 20, 488, by + 21], fill=RED)
    d.text((512, by), "ALSO ON WEDNESDAY 18 NOVEMBER \u2014 25 MORE STORIES",
           font=F_KICK, fill=RED)
    d.rectangle([512, by + 20, W - 24, by + 21], fill=RED)
    draw_map(d, 24, by + 28, 464, 196)
    d.text((24, by + 230), "Numbered dots mark stories 1\u201311.",
           font=F_MAP_CAP, fill=GREY)
    ly = by + 28
    for i, (lead, deck) in enumerate(ALSO):
        n = i + 12
        col = 0 if i < 13 else 1
        cx = 512 + col * 250
        col_w = 246 if col == 0 else 236
        yy = ly + (i if i < 13 else i - 13) * 16.2
        num = str(n) + "."
        num_w = d.textlength(num, font=F_ALSO_N)
        # trim the deck until lead + deck fits the column
        shown, trimmed = deck, False
        lead_w = d.textlength(lead, font=F_ALSO_L)
        while True:
            tail = " \u2014 " + shown + ("\u2026" if trimmed else "")
            if lead_w + d.textlength(tail, font=F_ALSO_D) \
                    <= col_w - num_w - 8:
                break
            if " " not in shown:
                break
            shown = shown.rsplit(" ", 1)[0]
            trimmed = True
        d.text((cx, yy), num, font=F_ALSO_N, fill=RED)
        nx = cx + num_w + 4
        d.text((nx, yy), lead, font=F_ALSO_L, fill=INK)
        lx = nx + d.textlength(lead, font=F_ALSO_L) + 4
        d.text((lx, yy), "\u2014 " + shown + ("\u2026" if trimmed else ""),
               font=F_ALSO_D, fill=BODY)

    # footer
    foot = ("Every story was reported on Wednesday 18 November 2026; "
            "disputed claims are attributed. Sources: Reuters, AP, AFP, "
            "BBC, Al Jazeera, CNBC, IMD, CSK.")
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, 1004), foot,
           font=F_FOOT, fill=GREY)

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes", img.size)


if __name__ == "__main__":
    main()
