#!/usr/bin/env python3
"""Draw the news-image-20261118 front page, v3: 'Wednesday 18 November 2026'.

A dense broadsheet, 1024x1024, rebuilt on the structure the 17 November
final winners used (see news-image-20261117-final-winners-study.md):
cream paper, a masthead that counts the stories, a UTC timeline strip
across the day, FOUR large illustrated leads, TWELVE medium cards with a
picture strip on top, a BY THE NUMBERS strip, a dotted world map with
numbered pins and a region legend, a three-column briefs list, and an
explicit DATE CHECK box naming what was left out on purpose. 60 verified
stories in all.

Every story was checked against real reporting of 18 November 2026
(Reuters / AP / AFP / BBC / Al Jazeera / CNBC / IMD / CSK, plus the APEC
opening, the Xi-Putin meeting, the Alaska Senate result, the Anthropic
offering and the Board of Peace report of the day). Contested claims are
attributed in the text. Drawn with Pillow (flat procedural art, no copied
photograph); written to entry.png next to this file.

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
F_UTC_T = font("DejaVuSans-Bold.ttf", 10)
F_UTC_E = font("DejaVuSans.ttf", 9)
F_HERO_H = font("DejaVuSerif-Bold.ttf", 17)
F_HERO_D = font("DejaVuSans.ttf", 11)
F_MED_K = font("DejaVuSans-Bold.ttf", 8)
F_MED_H = font("DejaVuSerif-Bold.ttf", 12)
F_MED_D = font("DejaVuSans.ttf", 9)
F_NUM = font("DejaVuSans-Bold.ttf", 20)
F_NUM_C = font("DejaVuSans.ttf", 10)
F_ALSO_N = font("DejaVuSans-Bold.ttf", 9)
F_ALSO_L = font("DejaVuSans-Bold.ttf", 9)
F_ALSO_D = font("DejaVuSans.ttf", 9)
F_FOOT = ImageFont.truetype(NOTO, 11)
F_MAP_CAP = font("DejaVuSans.ttf", 10)
F_LEG = font("DejaVuSans.ttf", 9)
F_PIN = font("DejaVuSans-Bold.ttf", 11)
F_DC = font("DejaVuSans.ttf", 10)
F_DC_B = font("DejaVuSans-Bold.ttf", 10)

# ---------------------------------------------------------------- stories
# leads: (headline, deck, kicker, caption strip, accent)
LEADS = [
    ("US and Iran trade fire over Bahrain",
     "Iranian drones target a US radar in Bahrain; US jets hit Qeshm Island.",
     "MIDDLE EAST \u00b7 CONFLICT", "SHEIKH ISA BASE \u00b7 QESHM ISLAND",
     (211, 84, 0)),
    ("A span of the Crimea bridge falls into the sea",
     "Second strike in two days destroys the road arch; rail arch stands.",
     "EUROPE \u00b7 WAR IN UKRAINE", "KERCH STRAIT \u00b7 19 KM CROSSING",
     (125, 60, 152)),
    ("Trump in Manila for first Quad in two years",
     "Meets Modi, Takaichi and Albanese; sees Marcos, then flies to Shenzhen.",
     "ASIA \u00b7 DIPLOMACY", "MANILA \u00b7 FIRST QUAD IN TWO YEARS",
     (30, 132, 73)),
    ("Xi and Putin meet ahead of Thursday talks",
     "They tout stable ties and attack protectionism; Trump arrives Thursday.",
     "ASIA \u00b7 DIPLOMACY", "SHENZHEN \u00b7 APEC SUMMIT",
     (188, 0, 45)),
]

# mediums: (headline, deck, kicker, accent) -- numbers 5..16
MEDIUM = [
    ("Nvidia revenue doubles to $115.8bn",
     "First results since Huang resigned.",
     "MARKETS \u00b7 TECHNOLOGY", (36, 113, 163)),
    ("Cyclone Akvan bears down on India's coast",
     "Heads for Andhra Pradesh and Odisha.",
     "ASIA \u00b7 WEATHER", (30, 132, 73)),
    ("Knesset elects Kahana, a blow to Netanyahu",
     "Eisenkot's ally wins 66-52.",
     "MIDDLE EAST \u00b7 POLITICS", (211, 84, 0)),
    ("EU plans a \u20ac45bn loan for Ukraine",
     "Brussels covers two-thirds of Kyiv's gap.",
     "EUROPE \u00b7 UKRAINE AID", (125, 60, 152)),
    ("APEC opens in Shenzhen with Xi keynote",
     "Leaders of 21 economies meet in Shenzhen.",
     "CHINA \u00b7 SUMMIT", (160, 60, 120)),
    ("China cuts tariffs for Canada as Xi meets Carney",
     "Tariff relief on pork and seafood.",
     "TRADE \u00b7 CHINA\u2013CANADA", (30, 132, 73)),
    ("Wall Street slides as the Dow drops 849 points",
     "S&P 500 at its lowest since July.",
     "MARKETS \u00b7 UNITED STATES", (36, 113, 163)),
    ("US loses measles elimination status",
     "Worst outbreak since 1991; status lost.",
     "HEALTH \u00b7 UNITED STATES", (125, 60, 152)),
    ("Peltola wins Alaska as Democrats take the Senate",
     "Democrat Mary Peltola beats Dan Sullivan.",
     "AMERICAS \u00b7 POLITICS", (36, 113, 163)),
    ("US sinks five Iranian tankers as Iran hits back",
     "US sank five tankers; Iran hit ten ships.",
     "MIDDLE EAST \u00b7 CONFLICT", (211, 84, 0)),
    ("Trump's Board of Peace faults Israel and Hamas",
     "Both sides failed Gaza truce terms.",
     "MIDDLE EAST \u00b7 DIPLOMACY", (0, 128, 128)),
    ("Anthropic raises $81.3bn in record offering",
     "Largest stock offering on record.",
     "MARKETS \u00b7 TECHNOLOGY", (36, 113, 163)),
]

# briefs: (bold lead, deck) -- numbers 17..50, one short line each
BRIEFS = [
    ("Thailand deal", "signs trade"),
    ("Pope Leo", "hit by a rosary"),
    ("Telegram blocked", "Jordan, Iraq"),
    ("Taiwan curbs", "US presses UN"),
    ("AI bubble", "Baidu chief warns"),
    ("Amazon", "$7bn for renewables"),
    ("ITU Council", "India re-elected"),
    ("ICC", "Jay Shah re-elected"),
    ("FIFA vote", "UEFA backs Diallo"),
    ("ASEAN", "Modi offers e-visas"),
    ("Pakistan\u2013Iran", "regional talks"),
    ("ASEAN energy", "Japan storage deal"),
    ("Ukraine toll", "UN: 372 killed"),
    ("Sudan toll", "UN confirms 2,230"),
    ("Gaza aid", "one meal per two days"),
    ("Latvia", "confidence vote backs"),
    ("Asif Merchant", "jailed 27.5 years"),
    ("Grammys", "2027 nominations out"),
    ("Starship", "booster catch"),
    ("Dhoni", "ends IPL career"),
    ("Settler sanctions", "UK freezes 8"),
    ("Siberia crash", "all 19 killed"),
    ("Tokyo jets", "two Russian planes"),
    ("Apple outage", "iCloud, App Store"),
    ("NSA outage", "network failure"),
    ("COP31", "144 items disputed"),
    ("Gaza cold", "UN warns of deaths"),
    ("Sudan\u2013Ethiopia", "tensions rise"),
    ("\u0130mamo\u011flu", "jailed, banned"),
    ("OpenAI", "GPT-6.2 Astra, Sol"),
    ("Bond", "Pattinson is new 007"),
    ("Nvidia board", "rejects Huang"),
    ("Quad patrols", "patrols, AI plan"),
    ("South China Sea", "'not concerned'"),
    # v4: ten more stories, all first reported Wednesday 18 November 2026
    # (numbers 51..60) -- IAEA on Yongbyon, EU-Indonesia CEPA/IPA, UNICEF
    # Yemen toll, Xiaomi 18 Paris launch, Slay the Spire 2 sales, Ondas-Aston
    # Martin F1, Novig's 7 NHL deals, Alcaraz at the ATP Finals, Santner
    # out of the India Tests, India joins the Pax Silica pact.
    ("North Korea", "Yongbyon plant grows"),
    ("EU\u2013Indonesia", "trade deals approved"),
    ("Yemen toll", "64 children killed"),
    ("Xiaomi 18", "global launch in Paris"),
    ("Slay the Spire 2", "8m sold on Steam"),
    ("Ondas", "Aston Martin F1 deal"),
    ("Novig", "7 NHL team deals"),
    ("Alcaraz", "beats Tiafoe 6\u20132, 6\u20132"),
    ("Santner", "out of India series"),
    ("Pax Silica", "India joins US pact"),
]

# UTC strip: (time label, event)
UTC = [
    ("Overnight", "US sinks five tankers"),
    ("~03:00 UTC", "Kerch Bridge hit again"),
    ("~06:00 UTC", "Xi and Putin in Shenzhen"),
    ("~10:00 UTC", "Trump meets Marcos"),
    ("Day", "Peltola wins Alaska"),
    ("Evening", "Anthropic raises $81.3bn"),
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

# region colours for map pins + legend
REG = {
    "americas": (176, 42, 32),
    "europe": (36, 113, 163),
    "mideast": (211, 84, 0),
    "asia": (125, 60, 152),
    "africa": (30, 132, 73),
    "oceania": (0, 128, 128),
}
# map pins: story number -> (lon, lat, dx, dy, region)
PINS = {
    1: (50.6, 26.2, 0, 0, "mideast"),
    2: (33.9, 45.4, 0, 0, "europe"),
    3: (121.0, 14.6, 0, 0, "asia"),
    4: (114.1, 22.5, -16, -12, "asia"),
    5: (-122.0, 37.4, 0, 0, "americas"),
    6: (90.0, 18.0, 0, 0, "asia"),
    7: (35.2, 31.8, 0, 0, "mideast"),
    8: (4.4, 50.9, 0, 0, "europe"),
    9: (114.1, 22.5, 16, 10, "asia"),
    10: (-75.7, 45.4, 0, 0, "americas"),
    11: (-74.0, 40.7, 0, 0, "americas"),
    12: (-77.0, 38.9, -18, 12, "americas"),
    13: (-134.4, 58.3, 0, 0, "americas"),
    14: (58.0, 24.0, 0, 0, "mideast"),
    15: (34.4, 31.5, 16, 10, "mideast"),
    16: (-122.4, 37.8, -14, -12, "americas"),
}

DATE_CHECK = (
    "Left out on purpose because they broke before today: Kerch Bridge first "
    "hit (17 Nov) \u2014 today's lead is the second strike; FAA ground stop "
    "(13 Nov); Huang quitting Nvidia (12\u201313 Nov); Costa Rica reporter "
    "shot dead (16 Nov). Not yet: the Xi\u2013Trump\u2013Putin trilateral, due "
    "Thursday 19 Nov; COP31 ends Friday 20 Nov."
)

FOOT = ("Every story here happened or was first reported on Wednesday 18 "
        "November 2026. CLAIM = one side's account, not independently "
        "confirmed. Sources: Reuters, AP, AFP, BBC, Al Jazeera, CNBC, IMD, "
        "CSK.")


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


def star5(d, cx, cy, r, colour, rot=-math.pi / 2):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = rot + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=colour)


def pin_badge(draw, x, y, n, colour, r=9):
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=colour)
    t = str(n)
    tw = draw.textlength(t, font=F_PIN)
    draw.text((x + r - tw / 2, y + r - 6), t, font=F_PIN,
              fill=(255, 255, 255))


def caption_strip(draw, x, y, w, text):
    """Dark label bar across the bottom of a hero picture."""
    draw.rectangle([x, y, x + w, y + 18], fill=(10, 14, 26))
    draw.text((x + 8, y + 3), text, font=F_CAP, fill=(255, 255, 255))


# ---------------------------------------------------------------- lead pictures
def hero_bahrain(d, x, y, w, h):
    """Night over the Gulf: radar dome, jet silhouette, moon, dark sea."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 24, 48))
    for sx, sy in [(0.08, 0.12), (0.30, 0.07), (0.52, 0.14), (0.70, 0.08),
                   (0.90, 0.16), (0.18, 0.28), (0.62, 0.26)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1,
                   y + h * sy + 1], fill=(220, 225, 240))
    d.ellipse([x + w * 0.84, y + h * 0.08, x + w * 0.94, y + h * 0.26],
              fill=(245, 238, 200))
    cx, cy = x + w * 0.30, y + h * 0.60
    d.arc([cx - 40, cy - 40, cx + 40, cy + 12], 180, 360,
          fill=(200, 210, 225), width=6)
    d.line([cx, cy, cx + 30, cy - 34], fill=(200, 210, 225), width=4)
    d.ellipse([cx + 26, cy - 38, cx + 34, cy - 30], fill=(255, 90, 60))
    d.rectangle([cx - 3, cy + 2, cx + 3, y + h * 0.80], fill=(160, 170, 185))
    jx, jy = x + w * 0.58, y + h * 0.28
    d.polygon([(jx, jy), (jx + 52, jy + 7), (jx + 12, jy + 12),
               (jx + 26, jy + 19), (jx + 5, jy + 14)], fill=(8, 10, 18))
    d.line([jx - 64, jy + 7, jx - 5, jy + 7], fill=(255, 90, 60), width=3)
    d.line([jx - 50, jy + 13, jx - 2, jy + 11], fill=(255, 150, 80), width=2)
    fx, fy = x + w * 0.82, y + h * 0.66
    star5(d, fx, fy, 9, (255, 160, 60))
    star5(d, fx, fy, 4, (255, 90, 40))
    d.rectangle([x, y + h * 0.80, x + w, y + h], fill=(10, 14, 26))
    for bx in (0.06, 0.52, 0.78):
        d.rectangle([x + w * bx, y + h * 0.80, x + w * bx + w * 0.10,
                     y + h * 0.80 + 8], fill=(8, 10, 20))
        d.rectangle([x + w * bx + 3, y + h * 0.80 + 2, x + w * bx + w * 0.10 - 3,
                     y + h * 0.80 + 5], fill=(255, 200, 90))
    caption_strip(d, x, y + h - 18, w, LEADS[0][3])


def hero_bridge(d, x, y, w, h):
    """Pale sky, a bridge arch with its middle span dropped into the sea."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 206, 214))
    d.ellipse([x + w * 0.80, y + h * 0.06, x + w * 0.90, y + h * 0.22],
              fill=(240, 220, 140))
    for cx, cy, r in [(0.46, 0.16, 11), (0.54, 0.10, 13), (0.62, 0.17, 9)]:
        d.ellipse([x + w * cx - r, y + h * cy - r, x + w * cx + r,
                   y + h * cy + r], fill=(110, 112, 116))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(74, 102, 128))
    for i in range(24):
        d.line([x + i * w / 24, y + h * 0.62 + (i % 3),
                x + i * w / 24 + 16, y + h * 0.62 + (i % 3)],
               fill=(120, 150, 175), width=2)
    d.arc([x + w * 0.06, y + h * 0.20, x + w * 0.40, y + h * 0.60], 180, 360,
          fill=(110, 114, 120), width=7)
    d.rectangle([x, y + h * 0.48, x + w * 0.38, y + h * 0.54],
                fill=(52, 54, 60))
    d.polygon([(x + w * 0.38, y + h * 0.48), (x + w * 0.50, y + h * 0.62),
               (x + w * 0.55, y + h * 0.60), (x + w * 0.44, y + h * 0.48)],
              fill=(52, 54, 60))
    d.rectangle([x + w * 0.64, y + h * 0.48, x + w, y + h * 0.54],
                fill=(52, 54, 60))
    for tx in (0.10, 0.88):
        d.rectangle([x + w * tx, y + h * 0.28, x + w * tx + 6, y + h * 0.54],
                    fill=(70, 72, 78))
    d.ellipse([x + w * 0.50, y + h * 0.62, x + w * 0.58, y + h * 0.68],
              fill=(230, 235, 240))
    caption_strip(d, x, y + h - 18, w, LEADS[1][3])


def hero_summit(d, x, y, w, h):
    """Warm dusk, a city skyline and four flags over a table."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 186, 138))
    d.ellipse([x + w * 0.84, y + h * 0.06, x + w * 0.94, y + h * 0.24],
              fill=(245, 225, 150))
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
    for i in range(4):
        fx = x + w * (0.10 + i * 0.22)
        d.line([fx, y + h * 0.08, fx, y + h * 0.62], fill=(60, 45, 30),
               width=3)
        fw, fh = 30, 18
        if i == 0:  # United States
            for s in range(7):
                d.rectangle([fx, y + h * 0.08 + s * fh / 7,
                             fx + fw, y + h * 0.08 + (s + 1) * fh / 7],
                            fill=(178, 34, 52) if s % 2 == 0
                            else (255, 255, 255))
            d.rectangle([fx, y + h * 0.08, fx + 13,
                         y + h * 0.08 + fh * 4 / 7], fill=(30, 50, 110))
            star5(d, fx + 6, y + h * 0.08 + fh * 2 / 7, 3, (255, 255, 255))
        elif i == 1:  # India
            d.rectangle([fx, y + h * 0.08, fx + fw, y + h * 0.08 + fh / 3],
                        fill=(255, 153, 51))
            d.rectangle([fx, y + h * 0.08 + fh / 3, fx + fw,
                         y + h * 0.08 + 2 * fh / 3], fill=(255, 255, 255))
            d.rectangle([fx, y + h * 0.08 + 2 * fh / 3, fx + fw,
                         y + h * 0.08 + fh], fill=(19, 136, 8))
            d.ellipse([fx + 11, y + h * 0.08 + fh / 3 + 2, fx + 19,
                       y + h * 0.08 + 2 * fh / 3 - 2],
                      outline=(0, 56, 147))
        elif i == 2:  # Japan
            d.rectangle([fx, y + h * 0.08, fx + fw, y + h * 0.08 + fh],
                        fill=(255, 255, 255))
            d.ellipse([fx + 10, y + h * 0.08 + 4, fx + 20,
                       y + h * 0.08 + fh - 4], fill=(188, 0, 45))
        else:  # Australia
            d.rectangle([fx, y + h * 0.08, fx + fw, y + h * 0.08 + fh],
                        fill=(0, 40, 104))
            d.rectangle([fx, y + h * 0.08, fx + 13, y + h * 0.08 + fh / 2],
                        fill=(255, 255, 255))
            d.line([fx + 6, y + h * 0.08, fx + 6, y + h * 0.08 + fh / 2],
                   fill=(200, 16, 46), width=2)
            d.line([fx, y + h * 0.08 + fh / 4, fx + 13,
                    y + h * 0.08 + fh / 4], fill=(200, 16, 46), width=2)
            star5(d, fx + 23, y + h * 0.08 + fh * 0.68, 3, (255, 215, 0))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(122, 84, 52))
    for i, suit in enumerate([(40, 44, 66), (70, 60, 50), (50, 70, 90),
                              (90, 50, 40)]):
        px = x + w * (0.13 + i * 0.23)
        d.ellipse([px - 8, y + h * 0.34, px + 8, y + h * 0.52],
                  fill=(232, 190, 150))
        d.rounded_rectangle([px - 14, y + h * 0.50, px + 14, y + h * 0.76],
                            radius=7, fill=suit)
        d.polygon([(px - 3, y + h * 0.50), (px + 3, y + h * 0.50),
                   (px, y + h * 0.62)], fill=(255, 255, 255))
    caption_strip(d, x, y + h - 18, w, LEADS[2][3])


def hero_shenzhen(d, x, y, w, h):
    """Dusk over Shenzhen: towers, two flags, a long table, APEC banner."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 42, 74))
    d.ellipse([x + w * 0.86, y + h * 0.06, x + w * 0.95, y + h * 0.22],
              fill=(245, 225, 150))
    for bx, bw, bh in [(0.03, 0.09, 0.40), (0.14, 0.07, 0.55),
                       (0.23, 0.11, 0.34), (0.36, 0.08, 0.62),
                       (0.46, 0.10, 0.44), (0.58, 0.08, 0.58),
                       (0.68, 0.11, 0.38), (0.81, 0.09, 0.50),
                       (0.91, 0.08, 0.36)]:
        d.rectangle([x + w * bx, y + h * (0.72 - bh), x + w * (bx + bw),
                     y + h * 0.72], fill=(12, 20, 38))
        for wy in range(3):
            d.rectangle([x + w * (bx + 0.02), y + h * (0.72 - bh + 0.06 + wy * 0.12),
                         x + w * (bx + 0.04), y + h * (0.72 - bh + 0.10 + wy * 0.12)],
                        fill=(255, 210, 90))
    # two flags: China left, Russia right
    for i, flag in enumerate(("china", "russia")):
        fx = x + w * (0.16 + i * 0.52)
        d.line([fx, y + h * 0.06, fx, y + h * 0.58], fill=(200, 200, 210),
               width=3)
        fw, fh = 34, 20
        if flag == "china":
            d.rectangle([fx, y + h * 0.06, fx + fw, y + h * 0.06 + fh],
                        fill=(222, 41, 16))
            star5(d, fx + 8, y + h * 0.06 + fh * 0.32, 5, (255, 222, 0))
            star5(d, fx + 24, y + h * 0.06 + fh * 0.22, 2, (255, 222, 0))
            star5(d, fx + 27, y + h * 0.06 + fh * 0.55, 2, (255, 222, 0))
        else:
            d.rectangle([fx, y + h * 0.06, fx + fw, y + h * 0.06 + fh / 3],
                        fill=(255, 255, 255))
            d.rectangle([fx, y + h * 0.06 + fh / 3, fx + fw,
                         y + h * 0.06 + 2 * fh / 3], fill=(0, 57, 166))
            d.rectangle([fx, y + h * 0.06 + 2 * fh / 3, fx + fw,
                         y + h * 0.06 + fh], fill=(213, 0, 50))
    # table band with two seated figures
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(90, 60, 40))
    for i, suit in enumerate([(40, 44, 66), (120, 30, 30)]):
        px = x + w * (0.28 + i * 0.44)
        d.ellipse([px - 8, y + h * 0.36, px + 8, y + h * 0.54],
                  fill=(232, 190, 150))
        d.rounded_rectangle([px - 15, y + h * 0.52, px + 15, y + h * 0.78],
                            radius=7, fill=suit)
        d.polygon([(px - 3, y + h * 0.52), (px + 3, y + h * 0.52),
                   (px, y + h * 0.64)], fill=(255, 255, 255))
    caption_strip(d, x, y + h - 18, w, LEADS[3][3])


HERO_ILLU = [hero_bahrain, hero_bridge, hero_summit, hero_shenzhen]


# ---------------------------------------------------------------- medium strips
# Each strip fills the top of a medium card (156 x 46): a flat scene with
# one clear pictogram, drawn wide so it reads at small size.
def strip_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 40, 28))
    for i in range(4):
        d.line([x + 6, y + h * (0.18 + i * 0.2), x + w * 0.30,
                y + h * (0.18 + i * 0.2)], fill=(60, 160, 110), width=2)
        d.line([x + w * 0.70, y + h * (0.18 + i * 0.2), x + w - 6,
                y + h * (0.18 + i * 0.2)], fill=(60, 160, 110), width=2)
    cx, cy = x + w / 2, y + h / 2
    d.rounded_rectangle([cx - 22, cy - 14, cx + 22, cy + 14], radius=5,
                        fill=(20, 90, 60), outline=(140, 220, 170), width=2)
    d.text((cx - 8, cy - 8), "NV", font=font("DejaVuSans-Bold.ttf", 13),
           fill=(255, 255, 255))
    pts = [(x + w * 0.06, y + h * 0.86), (x + w * 0.34, y + h * 0.70),
           (x + w * 0.60, y + h * 0.74), (x + w * 0.94, y + h * 0.34)]
    d.line(pts, fill=(255, 210, 60), width=3, joint="curve")


def strip_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 92, 128))
    cx, cy = x + w * 0.42, y + h * 0.54
    for k in range(5):
        r = 7 + k * 5
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8],
              200 + k * 55, 200 + k * 55 + 250,
              fill=(255, 255, 255) if k % 2 else (190, 220, 235), width=4)
    d.ellipse([cx - 6, cy - 5, cx + 6, cy + 5], fill=(255, 240, 200))
    d.polygon([(x + w * 0.80, y), (x + w, y), (x + w, y + h),
               (x + w * 0.86, y + h), (x + w * 0.78, y + h * 0.6)],
              fill=(214, 196, 150))


def strip_knesset(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 210, 225))
    bx, by, bw, bh = x + w * 0.30, y + h * 0.30, w * 0.40, h * 0.56
    d.rectangle([bx, by, bx + bw, by + bh], fill=(120, 130, 145))
    d.polygon([(bx - 5, by), (bx + bw / 2, by - h * 0.20), (bx + bw + 5, by)],
              fill=(90, 100, 118))
    for i in range(4):
        cx = bx + bw * (0.14 + i * 0.24)
        d.rectangle([cx - 3, by + h * 0.06, cx + 3, by + bh],
                    fill=(245, 243, 235))
    d.rounded_rectangle([x + w * 0.06, y + h * 0.66, x + w * 0.22,
                         y + h * 0.78], radius=3, fill=(120, 80, 40))
    d.text((x + w * 0.72, y + h * 0.60), "66-52",
           font=font("DejaVuSans-Bold.ttf", 12), fill=(40, 40, 60))


def strip_euro(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    cx, cy, r = x + w * 0.30, y + h / 2, h * 0.34
    for k in range(12):
        a = k * math.pi / 6 - math.pi / 2
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        star5(d, sx, sy, 2.5, (255, 215, 0))
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 255, 255))
    d.text((cx - 7, cy - 10), "\u20ac", font=font("DejaVuSans-Bold.ttf", 16),
           fill=(0, 40, 104))
    d.text((x + w * 0.56, y + h * 0.28), "\u20ac45bn",
           font=font("DejaVuSans-Bold.ttf", 14), fill=(255, 215, 0))
    d.text((x + w * 0.56, y + h * 0.60), "for Kyiv",
           font=font("DejaVuSans.ttf", 10), fill=(255, 255, 255))


def strip_apec(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 96, 96))
    cx, cy, r = x + w * 0.28, y + h / 2, h * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 210, 210))
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(0, 96, 96), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(0, 96, 96), width=2)
    for px, py in [(0.38, 0.38), (0.62, 0.42), (0.55, 0.62)]:
        d.ellipse([x + w * px - 3, y + h * py - 3, x + w * px + 3,
                   y + h * py + 3], fill=(188, 30, 25))
    d.text((x + w * 0.58, y + h * 0.24), "APEC",
           font=font("DejaVuSans-Bold.ttf", 15), fill=(255, 255, 255))
    d.text((x + w * 0.58, y + h * 0.58), "21 economies",
           font=font("DejaVuSans.ttf", 9), fill=(200, 235, 235))


def strip_trade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 222))
    d.rectangle([x + w * 0.08, y + h * 0.18, x + w * 0.44, y + h * 0.78],
                fill=(222, 41, 16))
    star5(d, x + w * 0.16, y + h * 0.34, 6, (255, 222, 0))
    star5(d, x + w * 0.32, y + h * 0.28, 3, (255, 222, 0))
    d.rectangle([x + w * 0.52, y + h * 0.18, x + w * 0.90, y + h * 0.78],
                fill=(255, 255, 255), outline=(200, 16, 46), width=2)
    d.rectangle([x + w * 0.52, y + h * 0.18, x + w * 0.60, y + h * 0.78],
                fill=(255, 0, 0))
    d.rectangle([x + w * 0.82, y + h * 0.18, x + w * 0.90, y + h * 0.78],
                fill=(255, 0, 0))
    mx, my = x + w * 0.71, y + h * 0.48
    d.polygon([(mx, my - 9), (mx + 3, my - 3), (mx + 7, my - 6),
               (mx + 4, my), (mx + 8, my + 2), (mx + 3, my + 3),
               (mx + 3, my + 9), (mx, my + 5), (mx - 3, my + 9),
               (mx - 3, my + 3), (mx - 8, my + 2), (mx - 4, my),
               (mx - 7, my - 6), (mx - 3, my - 3)], fill=(255, 0, 0))


def strip_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 30))
    pts = [(x + w * 0.08, y + h * 0.28), (x + w * 0.32, y + h * 0.40),
           (x + w * 0.56, y + h * 0.36), (x + w * 0.90, y + h * 0.74)]
    d.line(pts, fill=(230, 60, 50), width=3, joint="curve")
    d.polygon([(pts[-1][0] - 8, pts[-1][1] - 2), (pts[-1][0] + 2, pts[-1][1] + 6),
               (pts[-1][0] - 8, pts[-1][1] + 8)], fill=(230, 60, 50))
    d.text((x + w * 0.06, y + h * 0.60), "-849",
           font=font("DejaVuSans-Bold.ttf", 15), fill=(255, 255, 255))


def strip_virus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 220))
    for fx, fy, r in [(0.28, 0.50, 12), (0.68, 0.46, 14)]:
        cx, cy = x + w * fx, y + h * fy
        for k in range(8):
            a = k * math.pi / 4
            d.line([cx + r * math.cos(a), cy + r * math.sin(a),
                    cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a)],
                   fill=(178, 34, 34), width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(198, 60, 50))
        d.ellipse([cx - r * 0.4, cy - r * 0.4, cx + r * 0.2, cy + r * 0.2],
                  fill=(230, 120, 110))


def strip_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 38, 74))
    cx = x + w * 0.30
    d.rectangle([cx - 26, y + h * 0.62, cx + 26, y + h * 0.86],
                fill=(220, 222, 230))
    d.arc([cx - 18, y + h * 0.30, cx + 18, y + h * 0.66], 180, 360,
          fill=(220, 222, 230), width=4)
    d.rectangle([cx - 2, y + h * 0.18, cx + 2, y + h * 0.34],
                fill=(220, 222, 230))
    star5(d, cx, y + h * 0.14, 4, (255, 215, 0))
    for i in range(4):
        d.rectangle([cx - 22 + i * 12, y + h * 0.66, cx - 18 + i * 12,
                     y + h * 0.86], fill=(180, 184, 195))
    d.text((x + w * 0.56, y + h * 0.24), "56\u201344",
           font=font("DejaVuSans-Bold.ttf", 15), fill=(255, 215, 0))
    d.text((x + w * 0.56, y + h * 0.58), "Senate flips",
           font=font("DejaVuSans.ttf", 10), fill=(255, 255, 255))


def strip_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 30, 52))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(10, 18, 34))
    hx, hy = x + w * 0.30, y + h * 0.52
    d.rectangle([hx - 34, hy - 8, hx + 34, hy + 6], fill=(90, 96, 110))
    d.rectangle([hx + 18, hy - 20, hx + 30, hy - 8], fill=(70, 76, 90))
    d.line([hx + 24, hy - 20, hx + 24, hy - 30], fill=(160, 165, 175), width=2)
    fx, fy = x + w * 0.74, y + h * 0.40
    star5(d, fx, fy, 12, (255, 160, 60))
    star5(d, fx, fy, 6, (255, 90, 40))
    d.text((x + w * 0.06, y + h * 0.08), "5 TANKERS SUNK",
           font=font("DejaVuSans-Bold.ttf", 9), fill=(255, 200, 90))


def strip_peace(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 96, 96))
    cx, cy = x + w * 0.30, y + h * 0.52
    d.polygon([(cx - 22, cy + 2), (cx - 4, cy - 10), (cx + 8, cy - 12),
               (cx + 22, cy - 4), (cx + 6, cy + 2), (cx + 14, cy + 10),
               (cx - 2, cy + 8), (cx - 12, cy + 12)], fill=(255, 255, 255))
    d.polygon([(cx + 8, cy - 12), (cx + 16, cy - 20), (cx + 20, cy - 12)],
              fill=(255, 255, 255))
    for i in range(3):
        d.ellipse([cx + 24 + i * 7, cy + 6 + i * 3, cx + 30 + i * 7,
                   cy + 12 + i * 3], fill=(60, 160, 110))
    d.text((x + w * 0.58, y + h * 0.26), "BOTH SIDES",
           font=font("DejaVuSans-Bold.ttf", 11), fill=(255, 255, 255))
    d.text((x + w * 0.58, y + h * 0.58), "faulted",
           font=font("DejaVuSans.ttf", 10), fill=(200, 235, 235))


def strip_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 34))
    rx, ry = x + w * 0.30, y + h * 0.52
    d.polygon([(rx, ry - 16), (rx + 7, ry - 2), (rx + 5, ry + 12),
               (rx - 5, ry + 12), (rx - 7, ry - 2)], fill=(230, 235, 240))
    d.ellipse([rx - 4, ry - 8, rx + 4, ry], fill=(188, 30, 25))
    d.polygon([(rx - 3, ry + 12), (rx - 8, ry + 20), (rx - 1, ry + 14)],
              fill=(255, 150, 60))
    d.polygon([(rx + 3, ry + 12), (rx + 8, ry + 20), (rx + 1, ry + 14)],
              fill=(255, 150, 60))
    d.text((x + w * 0.52, y + h * 0.24), "$81.3bn",
           font=font("DejaVuSans-Bold.ttf", 14), fill=(255, 210, 60))
    d.text((x + w * 0.52, y + h * 0.58), "record offering",
           font=font("DejaVuSans.ttf", 10), fill=(255, 255, 255))


STRIPS = [strip_chip, strip_cyclone, strip_knesset, strip_euro, strip_apec,
          strip_trade, strip_chart, strip_virus, strip_capitol, strip_tanker,
          strip_peace, strip_rocket]


# ---------------------------------------------------------------- dotted map
def draw_map(d, x, y, w, h):
    """Dot-matrix world map from the Natural Earth polygons, colour pins."""
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
                    pts = [((lon - lon_min) / (lon_max - lon_min) * w,
                            (lat_max - lat) / (lat_max - lat_min) * h)
                           for lon, lat in ring]
                    md.polygon(pts, fill=255)
        step = 6
        for gy in range(step // 2, h, step):
            for gx in range(step // 2, w, step):
                if mask.getpixel((gx, gy)):
                    d.ellipse([x + gx - 2, y + gy - 2, x + gx + 2,
                               y + gy + 2], fill=DOT)
    except FileNotFoundError:
        d.text((x + 10, y + 10), "world map data unavailable",
               font=F_MAP_CAP, fill=GREY)
    d.rectangle([x, y, x + w, y + h], outline=(150, 142, 122), width=1)
    for n, (lon, lat, dx, dy, region) in PINS.items():
        colour = REG[region]
        bx, by = px(lon, lat)
        bx += dx
        by += dy
        if dx or dy:
            ox, oy = px(lon, lat)
            d.line([ox, oy, bx, by], fill=(60, 55, 45), width=1)
            d.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=(60, 55, 45))
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=colour,
                  outline=(255, 255, 255), width=2)
        t = str(n)
        tw = d.textlength(t, font=F_PIN)
        d.text((bx - tw / 2, by - 6), t, font=F_PIN, fill=(255, 255, 255))


# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead: dark navy band --------------------------------------
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((24, 10), "THE DAY IN WORLD NEWS", font=F_KICK, fill=GOLD)
    right = "60 STORIES \u00b7 6 CONTINENTS \u00b7 EVERY ONE FROM THIS WEDNESDAY"
    d.text((W - 24 - d.textlength(right, font=F_KICK), 10), right,
           font=F_KICK, fill=GOLD)
    d.text((24, 28), "Wednesday 18 November 2026", font=F_DATE,
           fill=(255, 255, 255))
    d.text((24, 86), "Every story below happened, or was first reported, "
           "on this day.", font=F_DECK, fill=NAVY_SOFT)
    d.rectangle([0, 104, W, 106], fill=GOLD)

    # ---- UTC timeline strip ---------------------------------------------
    uy = 112
    d.rectangle([24, uy, 132, uy + 24], fill=RED)
    d.text((32, uy + 5), "THE DAY IN UTC", font=F_UTC_T,
           fill=(255, 255, 255))
    slot_w = (W - 48 - 120) // 6
    for i, (t, ev) in enumerate(UTC):
        sx = 140 + i * slot_w
        d.text((sx, uy), t, font=F_UTC_T, fill=RED)
        for j, line in enumerate(wrap(d, ev, F_UTC_E, slot_w - 8)[:2]):
            d.text((sx, uy + 12 + j * 11), line, font=F_UTC_E, fill=BODY)
        if i:
            d.line([sx - 5, uy + 2, sx - 5, uy + 22], fill=RULE, width=1)

    # ---- leads: 4 across -------------------------------------------------
    ly, lw, lgap, lh = 144, 236, 10, 84
    for i, (head, deck, kick, cap, col) in enumerate(LEADS):
        cx = 24 + i * (lw + lgap)
        HERO_ILLU[i](d, cx, ly, lw, lh)
        pin_badge(d, cx, ly + lh + 6, i + 1, col, r=9)
        d.text((cx + 24, ly + lh + 8), kick, font=F_KICK2, fill=col)
        yy = ly + lh + 26
        for line in wrap(d, head, F_HERO_H, lw)[:2]:
            d.text((cx, yy), line, font=F_HERO_H, fill=INK)
            yy += 20
        yy += 3
        for line in wrap(d, deck, F_HERO_D, lw)[:3]:
            d.text((cx, yy), line, font=F_HERO_D, fill=BODY)
            yy += 14
    d.rectangle([24, 338, W - 24, 339], fill=INK)

    # ---- medium grid: 2 rows x 6, picture strip on top ------------------
    my, mh, mw, mgap = 346, 136, 156, 8
    for row in range(2):
        for ci in range(6):
            idx = row * 6 + ci
            head, deck, kick, col = MEDIUM[idx]
            n = idx + 5
            cx = 24 + ci * (mw + mgap)
            cy = my + row * (mh + mgap)
            d.rectangle([cx, cy, cx + mw, cy + mh], fill=CARD,
                        outline=CARD_EDGE, width=1)
            STRIPS[idx](d, cx + 1, cy + 1, mw - 2, 46)
            tx = cx + 7
            d.text((tx, cy + 52), kick, font=F_MED_K, fill=col)
            yy = cy + 66
            for line in wrap(d, head, F_MED_H, mw - 14)[:3]:
                d.text((tx, yy), line, font=F_MED_H, fill=INK)
                yy += 15
            yy += 2
            for line in wrap(d, deck, F_MED_D, mw - 14)[:2]:
                d.text((tx, yy), line, font=F_MED_D, fill=BODY)
                yy += 12
    d.rectangle([24, 626, W - 24, 627], fill=INK)

    # ---- by the numbers --------------------------------------------------
    d.rectangle([24, 634, W - 24, 676], fill=NAVY)
    for i, (val, cap) in enumerate(NUMBERS):
        bx = 24 + i * 163 + 8
        d.text((bx, 642), val, font=F_NUM, fill=GOLD)
        d.text((bx, 664), cap, font=F_NUM_C, fill=(255, 255, 255))

    # ---- bottom: dotted map (left) + briefs (right, 3 cols) -------------
    by = 686
    d.text((24, by), "WHERE IT HAPPENED", font=F_KICK, fill=RED)
    d.rectangle([24, by + 20, 344, by + 21], fill=RED)
    d.text((368, by), "ALSO ON WEDNESDAY 18 NOVEMBER \u2014 44 MORE STORIES",
           font=F_KICK, fill=RED)
    d.rectangle([368, by + 20, W - 24, by + 21], fill=RED)
    draw_map(d, 24, by + 28, 320, 190)
    d.text((24, by + 224), "Numbered dots mark stories 1\u201316.",
           font=F_MAP_CAP, fill=GREY)
    lx = 24
    for name, colour in [("Americas", REG["americas"]),
                         ("Europe", REG["europe"]),
                         ("Middle East", REG["mideast"]),
                         ("Asia", REG["asia"]),
                         ("Africa", REG["africa"]),
                         ("Oceania", REG["oceania"])]:
        d.ellipse([lx, by + 242, lx + 8, by + 250], fill=colour)
        d.text((lx + 11, by + 240), name, font=F_LEG, fill=BODY)
        lx += 11 + d.textlength(name, font=F_LEG) + 10
    ly = by + 28
    for i, (lead, deck) in enumerate(BRIEFS):
        n = i + 17
        col = i // 15
        cx = 368 + col * 212
        col_w = 208
        yy = ly + (i % 15) * 15.0
        num = str(n) + "."
        num_w = d.textlength(num, font=F_ALSO_N)
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
        lx2 = nx + d.textlength(lead, font=F_ALSO_L) + 4
        d.text((lx2, yy), "\u2014 " + shown + ("\u2026" if trimmed else ""),
               font=F_ALSO_D, fill=BODY)

    # ---- DATE CHECK box --------------------------------------------------
    dy = 946
    d.rectangle([24, dy, W - 24, dy + 40], outline=RED, width=2)
    d.rectangle([24, dy, 132, dy + 40], fill=RED)
    d.text((32, dy + 12), "DATE CHECK", font=F_DC_B, fill=(255, 255, 255))
    yy = dy + 4
    for line in wrap(d, DATE_CHECK, F_DC, W - 24 - 140 - 8)[:3]:
        d.text((140, yy), line, font=F_DC, fill=BODY)
        yy += 12

    # footer
    d.text(((W - d.textlength(FOOT, font=F_FOOT)) / 2, 1002), FOOT,
           font=F_FOOT, fill=GREY)

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes", img.size)


if __name__ == "__main__":
    main()
