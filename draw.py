#!/usr/bin/env python3
"""Draw the news-image-20261118 front page: 'Wednesday 18 November 2026'.

One dense broadsheet, 1024x1024, built to the winning genre of the daily
news-image contests: masthead + 3 illustrated hero cards + 8 illustrated
medium cards + a numbered 12-30 list + a world map with numbered pins.

Every story was verified against real reporting of 18 November 2026
(AP / Reuters / AFP / BBC / Al Jazeera / CNBC / IMD / CSK).
The program draws the whole image with Pillow (flat procedural art, no
copied photograph) and writes entry.png next to this file.

Map land shapes: Natural Earth 110m admin-0 countries (public domain),
loaded from /tmp/ne110m.geojson at build time.
"""
import json
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
GEOJSON = "/tmp/ne110m.geojson"

W = H = 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
GREY = (110, 105, 92)
RULE = (201, 194, 176)
RED = (176, 42, 32)
CARD_BG = (255, 255, 255)
CARD_LINE = (205, 198, 182)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 58)
F_KICK = font("DejaVuSans-Bold.ttf", 14)
F_KICK_SM = font("DejaVuSans-Bold.ttf", 11)
F_HERO_H = font("DejaVuSerif-Bold.ttf", 20)
F_HERO_D = font("DejaVuSans.ttf", 12)
F_MED_H = font("DejaVuSerif-Bold.ttf", 14)
F_MED_D = font("DejaVuSans.ttf", 10)
F_LIST = font("DejaVuSans.ttf", 12)
F_LIST_N = font("DejaVuSans-Bold.ttf", 12)
F_FOOT = ImageFont.truetype(
    "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf", 11)
F_MAP_CAP = font("DejaVuSans.ttf", 11)
F_PIN = font("DejaVuSans-Bold.ttf", 11)

# ---------------------------------------------------------------- stories
# (headline, deck, kicker, colour) -- all verified from 18 Nov 2026 reporting
HEROES = [
    ("US and Iran trade fire over Bahrain",  # 1
     "Iranian drones target a US radar at Sheikh Isa base; Bahrain and US "
     "forces intercept them, and US jets hit a missile site on Qeshm Island.",
     "MIDDLE EAST", (211, 84, 0)),
    ("Ukraine collapses a span of the Crimea bridge",  # 2
     "A second day of strikes drops the road arch into the Kerch Strait; "
     "Russia hits Kyiv's two main bridges in reply.",
     "EUROPE", (125, 60, 152)),
    ("Trump in Manila for first Quad in two years",  # 3
     "He meets Modi, Takaichi and Albanese at the ASEAN sidelines, sees "
     "Marcos today, then heads to Shenzhen for APEC.",
     "ASIA", (30, 132, 73)),
]

MEDIUM = [
    ("Nvidia revenue more than doubles to $115.8bn",  # 4
     "First results since Huang resigned; data centre sales hit $107.6bn, "
     "and the board rules out his return.",
     "MARKETS", (36, 113, 163)),
    ("Cyclone Akvan bears down on India's east coast",  # 5
     "The Severe Cyclonic Storm heads for Andhra Pradesh and Odisha, with "
     "heavy rain from today and landfall on Friday.",
     "WEATHER", (30, 132, 73)),
    ("Knesset elects Kahana, a blow to Netanyahu",  # 6
     "Eisenkot's ally wins the speakership 66-52, replacing Likud's Ohana "
     "and taking control of the agenda.",
     "MIDDLE EAST", (211, 84, 0)),
    ("EU plans a \u20ac45bn loan for Ukraine",  # 7
     "Brussels would cover two-thirds of Kyiv's \u20ac70bn 2027 gap, likely "
     "through new joint borrowing.",
     "EUROPE", (125, 60, 152)),
    ("Britain sanctions settlement builders",  # 8
     "Eight Israeli construction firms and aid-blocking group Tzav 9 face "
     "asset freezes ahead of the E1 deadline.",
     "UNITED KINGDOM", (36, 113, 163)),
    ("China cuts tariffs for Canada as Xi meets Carney",  # 9
     "Tariff relief on pork and seafood as the two leaders extend trade "
     "deals ahead of the APEC summit.",
     "TRADE", (30, 132, 73)),
    ("Dhoni ends IPL playing career",  # 10
     "CSK name him Team Mentor for 2027 after five titles \u2014 with no "
     "farewell match after injury.",
     "SPORT", (211, 84, 0)),
    ("US loses measles elimination status",  # 11
     "The worst outbreak since 1991 ends three decades of elimination, "
     "health officials confirm.",
     "HEALTH", (125, 60, 152)),
]

ALSO = [
    "Trump signs reciprocal trade deal with Thailand",
    "Pope Leo struck in the eye by a rosary thrown from a crowd in Peru",
    "Jordan and Iraq block Telegram over security concerns",
    "US presses UN agency over Taiwan flight curbs; China hits back",
    "Baidu chief warns of an AI \u2018bubble\u2019 ahead of APEC talks",
    "Amazon to invest $7bn in India\u2019s renewable energy",
    "India re-elected to ITU Council for 2027\u20132030",
    "Jay Shah re-elected ICC chairman for a second term",
    "UEFA backs France\u2019s Diallo to stand against Infantino in FIFA vote",
    "Modi offers free e-visas and maritime ties at ASEAN summit",
    "Pakistan and Iran stress engagement for regional stability",
    "Japan offers ASEAN nations access to energy storage",
    "UN: at least 372 civilians killed in Ukraine in October",
    "Sudan: UN confirms over 2,230 civilian deaths",
    "Gaza: WFP provides one hot meal every two days",
    "Latvia: confidence vote backs Kulbergs government",
    "US: Asif Merchant jailed for 27.5 years over murder plot",
    "Grammy nominations for 2027 announced",
    "SpaceX catches a falling Starship",
]

# pins: (lon, lat, dx, dy) -- dx/dy nudge the badge so neighbours do not clash
PINS = {
    1: (50.6, 26.2, 0, 0), 2: (33.9, 45.4, 0, 0), 3: (121.0, 14.6, 0, 0),
    4: (-122.0, 37.4, 0, 0), 5: (90.0, 18.0, 0, 0), 6: (35.2, 31.8, 0, 0),
    7: (4.4, 50.9, 0, 0), 8: (-0.1, 51.5, -13, -11), 9: (-75.7, 45.4, 0, 0),
    10: (80.3, 13.1, 0, 0), 11: (-84.4, 33.8, 0, 0),
}
PIN_COLOUR = {1: (211, 84, 0), 2: (125, 60, 152), 3: (30, 132, 73),
              4: (36, 113, 163), 5: (30, 132, 73), 6: (211, 84, 0),
              7: (125, 60, 152), 8: (125, 60, 152), 9: (36, 113, 163),
              10: (30, 132, 73), 11: (36, 113, 163)}


# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, width):
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


def badge(draw, x, y, n, colour, r=9):
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=colour)
    t = str(n)
    tw = draw.textlength(t, font=F_PIN)
    draw.text((x + r - tw / 2, y + r - 6), t, font=F_PIN, fill=(255, 255, 255))


def kicker_line(draw, x, y, n, label, colour):
    badge(draw, x, y - 2, n, colour, r=9)
    draw.text((x + 24, y), label, font=F_KICK_SM, fill=colour)


# ---------------------------------------------------------------- illustrations
def star(d, cx, cy, r, colour, points=5, rot=-math.pi / 2):
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * 0.42
        a = rot + i * math.pi / points
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=colour)


def illu_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 48))
    for i, (cx, cy, r) in enumerate([(w * 0.22, h * 0.42, 15), (w * 0.55, h * 0.30, 18),
                                     (w * 0.82, h * 0.48, 13)]):
        for k in range(10):
            a = k * math.pi / 5 + i * 0.4
            d.line([x + cx, y + cy, x + cx + r * 2.4 * math.cos(a),
                    y + cy + r * 2.4 * math.sin(a)], fill=(255, 170, 60), width=3)
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(255, 120, 30))
        d.ellipse([x + cx - r * 0.45, y + cy - r * 0.45, x + cx + r * 0.45,
                   y + cy + r * 0.45], fill=(255, 220, 130))
        for sx, sy, sr in [(cx - r * 1.4, cy - r * 0.9, 7), (cx + r * 1.3, cy + r, 6)]:
            d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                      fill=(70, 72, 80))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(10, 14, 26))
    for bx in (0.05, 0.30, 0.62, 0.85):
        bw, bh = w * 0.10, h * 0.16
        d.rectangle([x + w * bx, y + h * 0.78 - bh, x + w * bx + bw,
                     y + h * 0.78], fill=(8, 10, 20))
        for wy in range(2):
            d.rectangle([x + w * bx + 4, y + h * 0.78 - bh + 4 + wy * 9,
                         x + w * bx + bw - 4, y + h * 0.78 - bh + 8 + wy * 9],
                        fill=(255, 200, 90))
    # radar dish
    cx, cy = x + w * 0.5, y + h * 0.66
    d.arc([cx - 30, cy - 30, cx + 30, cy + 8], 180, 360, fill=(200, 210, 225),
          width=5)
    d.line([cx, cy, cx + 22, cy - 26], fill=(200, 210, 225), width=4)
    d.ellipse([cx + 19, cy - 29, cx + 25, cy - 23], fill=(255, 90, 60))
    d.line([cx - 4, cy + 2, cx - 4, y + h * 0.78], fill=(160, 170, 185), width=4)


def illu_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 178, 190))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(74, 102, 128))
    for i in range(30):
        d.line([x + i * w / 30, y + h * 0.62 + (i % 3),
                x + i * w / 30 + 14, y + h * 0.62 + (i % 3)],
               fill=(120, 150, 175), width=2)
    # smoke
    for cx, cy, r in [(w * 0.30, h * 0.20, 13), (w * 0.38, h * 0.13, 16),
                      (w * 0.48, h * 0.19, 11)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(96, 98, 102))
    # bridge deck: left span, collapsed middle, right span
    d.rectangle([x, y + h * 0.50, x + w * 0.38, y + h * 0.56], fill=(52, 54, 60))
    d.polygon([(x + w * 0.38, y + h * 0.50), (x + w * 0.52, y + h * 0.62),
               (x + w * 0.56, y + h * 0.60), (x + w * 0.44, y + h * 0.50)],
              fill=(52, 54, 60))
    d.rectangle([x + w * 0.62, y + h * 0.50, x + w, y + h * 0.56],
                fill=(52, 54, 60))
    # arch + towers
    d.arc([x + w * 0.08, y + h * 0.30, x + w * 0.36, y + h * 0.62], 180, 360,
          fill=(120, 124, 130), width=6)
    d.line([x + w * 0.08, y + h * 0.46, x + w * 0.08, y + h * 0.52],
           fill=(120, 124, 130), width=6)
    d.line([x + w * 0.36, y + h * 0.46, x + w * 0.36, y + h * 0.52],
           fill=(120, 124, 130), width=6)
    for tx in (0.12, 0.86):
        d.rectangle([x + w * tx, y + h * 0.30, x + w * tx + 6, y + h * 0.56],
                    fill=(70, 72, 78))
    d.ellipse([x + w * 0.47, y + h * 0.60, x + w * 0.55, y + h * 0.66],
              fill=(230, 235, 240))


def illu_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 186, 138))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(122, 84, 52))
    d.rectangle([x, y + h * 0.55, x + w, y + h * 0.60], fill=(96, 64, 40))
    for i in range(4):
        fx = x + w * (0.10 + i * 0.22)
        d.line([fx, y + h * 0.10, fx, y + h * 0.62], fill=(60, 45, 30), width=3)
        fw, fh = 34, 20
        if i == 0:  # United States: stripes + blue canton
            for s in range(7):
                d.rectangle([fx, y + h * 0.10 + s * fh / 7,
                             fx + fw, y + h * 0.10 + (s + 1) * fh / 7],
                            fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, y + h * 0.10, fx + 14, y + h * 0.10 + fh * 4 / 7],
                        fill=(30, 50, 110))
            star(d, fx + 7, y + h * 0.10 + fh * 2 / 7, 3, (255, 255, 255))
        elif i == 1:  # India: saffron / white / green
            d.rectangle([fx, y + h * 0.10, fx + fw, y + h * 0.10 + fh / 3],
                        fill=(255, 153, 51))
            d.rectangle([fx, y + h * 0.10 + fh / 3, fx + fw,
                         y + h * 0.10 + 2 * fh / 3], fill=(255, 255, 255))
            d.rectangle([fx, y + h * 0.10 + 2 * fh / 3, fx + fw,
                         y + h * 0.10 + fh], fill=(19, 136, 8))
            d.ellipse([fx + 13, y + h * 0.10 + fh / 3 + 2, fx + 21,
                       y + h * 0.10 + 2 * fh / 3 - 2], outline=(0, 56, 147))
        elif i == 2:  # Japan: white field, red disc
            d.rectangle([fx, y + h * 0.10, fx + fw, y + h * 0.10 + fh],
                        fill=(255, 255, 255))
            d.ellipse([fx + 11, y + h * 0.10 + 4, fx + 23,
                       y + h * 0.10 + fh - 4], fill=(188, 0, 45))
        else:  # Australia: blue field, canton, gold star
            d.rectangle([fx, y + h * 0.10, fx + fw, y + h * 0.10 + fh],
                        fill=(0, 40, 104))
            d.rectangle([fx, y + h * 0.10, fx + 14, y + h * 0.10 + fh / 2],
                        fill=(255, 255, 255))
            d.line([fx + 7, y + h * 0.10, fx + 7, y + h * 0.10 + fh / 2],
                   fill=(200, 16, 46), width=2)
            d.line([fx, y + h * 0.10 + fh / 4, fx + 14,
                    y + h * 0.10 + fh / 4], fill=(200, 16, 46), width=2)
            star(d, fx + 26, y + h * 0.10 + fh * 0.68, 4, (255, 215, 0))
    # seated figures
    for i, suit in enumerate([(40, 44, 66), (70, 60, 50), (50, 70, 90),
                             (90, 50, 40)]):
        px = x + w * (0.13 + i * 0.23)
        d.ellipse([px - 9, y + h * 0.42, px + 9, y + h * 0.60], fill=(232, 190, 150))
        d.rounded_rectangle([px - 16, y + h * 0.58, px + 16, y + h * 0.86],
                            radius=8, fill=suit)
        d.polygon([(px - 4, y + h * 0.58), (px + 4, y + h * 0.58),
                   (px, y + h * 0.70)], fill=(255, 255, 255))


def illu_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 40, 28))
    for i in range(5):
        d.line([x + w * 0.08, y + h * (0.15 + i * 0.16),
                x + w * 0.30, y + h * (0.15 + i * 0.16)], fill=(60, 160, 110),
               width=2)
        d.line([x + w * 0.70, y + h * (0.15 + i * 0.16),
                x + w * 0.92, y + h * (0.15 + i * 0.16)], fill=(60, 160, 110),
               width=2)
    pts = [(x + w * 0.10, y + h * 0.86), (x + w * 0.35, y + h * 0.70),
           (x + w * 0.60, y + h * 0.74), (x + w * 0.90, y + h * 0.42)]
    d.line(pts, fill=(255, 210, 60), width=4, joint="curve")
    d.polygon([(pts[-1][0] - 12, pts[-1][1] + 2), (pts[-1][0] - 2, pts[-1][1] - 8),
               (pts[-1][0] - 2, pts[-1][1] + 10)], fill=(255, 210, 60))
    cx, cy, s = x + w * 0.5, y + h * 0.5, min(w, h) * 0.30
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=8,
                        fill=(20, 90, 60), outline=(140, 220, 170), width=3)
    d.rounded_rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55,
                         cy + s * 0.55], radius=5, fill=(118, 185, 0))
    d.text((cx - 8, cy - 9), "NV", font=font("DejaVuSans-Bold.ttf", 16),
           fill=(255, 255, 255))


def illu_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 92, 128))
    cx, cy = x + w * 0.45, y + h * 0.52
    for k in range(5):
        r = 12 + k * 9
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8],
              200 + k * 55, 200 + k * 55 + 250,
              fill=(255, 255, 255) if k % 2 else (190, 220, 235), width=6)
    d.ellipse([cx - 10, cy - 8, cx + 10, cy + 8], fill=(255, 240, 200))
    # coastline
    d.polygon([(x + w * 0.72, y), (x + w, y), (x + w, y + h),
               (x + w * 0.78, y + h), (x + w * 0.70, y + h * 0.6)],
              fill=(214, 196, 150))
    for i in range(6):
        rx = x + w * (0.05 + i * 0.10)
        d.line([rx, y + h * 0.12, rx - 6, y + h * 0.30], fill=(160, 200, 225),
               width=2)


def illu_knesset(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 210, 225))
    bx, by, bw, bh = x + w * 0.14, y + h * 0.30, w * 0.72, h * 0.55
    d.rectangle([bx, by, bx + bw, by + bh], fill=(232, 228, 216))
    d.polygon([(bx - 8, by), (bx + bw / 2, by - h * 0.22), (bx + bw + 8, by)],
              fill=(200, 195, 180))
    d.ellipse([bx + bw / 2 - 14, by - h * 0.16, bx + bw / 2 + 14, by + h * 0.06],
              fill=(120, 160, 200))
    for i in range(5):
        cx = bx + bw * (0.12 + i * 0.19)
        d.rectangle([cx - 5, by + h * 0.08, cx + 5, by + bh], fill=(250, 248, 240))
    d.rectangle([x + w * 0.78, y + h * 0.10, x + w * 0.94, y + h * 0.34],
                fill=(255, 255, 255))
    d.rectangle([x + w * 0.78, y + h * 0.10, x + w * 0.94, y + h * 0.18],
                fill=(0, 56, 147))
    d.rectangle([x + w * 0.78, y + h * 0.26, x + w * 0.94, y + h * 0.34],
                fill=(0, 56, 147))
    # gavel: head + handle, lower left
    d.rounded_rectangle([x + w * 0.05, y + h * 0.68, x + w * 0.22, y + h * 0.78],
                        radius=4, fill=(120, 80, 40))
    d.line([x + w * 0.13, y + h * 0.73, x + w * 0.30, y + h * 0.90],
           fill=(90, 60, 30), width=4)


def illu_euro(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    cx, cy, r = x + w * 0.5, y + h * 0.52, min(w, h) * 0.36
    for k in range(12):
        a = k * math.pi / 6 - math.pi / 2
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.polygon([(sx, sy - 6), (sx + 2, sy - 2), (sx + 6, sy), (sx + 2, sy + 2),
                   (sx, sy + 6), (sx - 2, sy + 2), (sx - 6, sy), (sx - 2, sy - 2)],
                  fill=(255, 215, 0))
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(255, 255, 255))
    d.text((cx - 15, cy - 20), "\u20ac", font=font("DejaVuSans-Bold.ttf", 34),
           fill=(0, 40, 104))
    d.polygon([(x, y + h), (x + w * 0.35, y + h * 0.82), (x + w * 0.65, y + h),
               ], fill=(0, 91, 187))
    d.polygon([(x + w * 0.35, y + h * 0.82), (x + w, y + h),
               (x + w * 0.65, y + h)], fill=(255, 213, 0))


def illu_sanction(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 222, 208))
    d.rectangle([x + w * 0.18, y + h * 0.12, x + w * 0.82, y + h * 0.88],
                fill=(255, 255, 255), outline=(120, 115, 100), width=2)
    for i in range(3):
        d.line([x + w * 0.26, y + h * (0.24 + i * 0.10),
                x + w * 0.74, y + h * (0.24 + i * 0.10)], fill=(150, 145, 130),
               width=3)
    d.rounded_rectangle([x + w * 0.26, y + h * 0.58, x + w * 0.74, y + h * 0.80],
                        radius=6, fill=(255, 255, 255), outline=(188, 30, 25), width=3)
    d.text((x + w * 0.33, y + h * 0.63), "FROZEN", font=font("DejaVuSans-Bold.ttf", 13),
           fill=(188, 30, 25))
    # union jack corner
    jx, jy, jw, jh = x + w * 0.62, y + h * 0.06, w * 0.30, h * 0.16
    d.rectangle([jx, jy, jx + jw, jy + jh], fill=(1, 33, 105))
    d.line([jx, jy, jx + jw, jy + jh], fill=(255, 255, 255), width=3)
    d.line([jx + jw, jy, jx, jy + jh], fill=(255, 255, 255), width=3)
    d.line([jx + jw / 2, jy, jx + jw / 2, jy + jh], fill=(200, 16, 46), width=4)
    d.line([jx, jy + jh / 2, jx + jw, jy + jh / 2], fill=(200, 16, 46), width=4)


def illu_trade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 222))
    # China flag
    d.rectangle([x + w * 0.06, y + h * 0.18, x + w * 0.46, y + h * 0.60],
                fill=(222, 41, 16))
    star(d, x + w * 0.14, y + h * 0.31, 9, (255, 222, 0))
    star(d, x + w * 0.30, y + h * 0.26, 4, (255, 222, 0))
    star(d, x + w * 0.35, y + h * 0.34, 4, (255, 222, 0))
    # Canada flag
    d.rectangle([x + w * 0.54, y + h * 0.18, x + w * 0.94, y + h * 0.60],
                fill=(255, 255, 255), outline=(200, 16, 46), width=2)
    d.rectangle([x + w * 0.54, y + h * 0.18, x + w * 0.66, y + h * 0.60],
                fill=(255, 0, 0))
    d.rectangle([x + w * 0.82, y + h * 0.18, x + w * 0.94, y + h * 0.60],
                fill=(255, 0, 0))
    mx, my = x + w * 0.74, y + h * 0.39
    d.polygon([(mx, my - 17), (mx + 5, my - 7), (mx + 13, my - 11),
               (mx + 9, my - 1), (mx + 15, my + 3), (mx + 6, my + 7),
               (mx + 7, my + 17), (mx, my + 11), (mx - 7, my + 17),
               (mx - 6, my + 7), (mx - 15, my + 3), (mx - 9, my - 1),
               (mx - 13, my - 11), (mx - 5, my - 7)], fill=(255, 0, 0))
    d.line([x + w * 0.46, y + h * 0.78, x + w * 0.54, y + h * 0.78],
           fill=(120, 115, 100), width=3)
    d.text((x + w * 0.30, y + h * 0.72), "Tariff relief", font=font("DejaVuSans-Bold.ttf", 11),
           fill=(60, 55, 45))


def illu_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
    d.rectangle([x + w * 0.42, y, x + w * 0.58, y + h], fill=(210, 190, 140))
    for sx in (0.44, 0.49, 0.54):
        d.rectangle([x + w * sx, y + h * 0.14, x + w * sx + 4, y + h * 0.34],
                    fill=(255, 214, 64))
    d.rectangle([x + w * 0.44, y + h * 0.12, x + w * 0.58, y + h * 0.15],
                fill=(255, 214, 64))
    # bat
    d.rounded_rectangle([x + w * 0.60, y + h * 0.45, x + w * 0.72, y + h * 0.82],
                        radius=5, fill=(190, 150, 100))
    d.line([x + w * 0.66, y + h * 0.45, x + w * 0.78, y + h * 0.22],
           fill=(120, 85, 50), width=5)
    d.ellipse([x + w * 0.24, y + h * 0.66, x + w * 0.34, y + h * 0.78],
              fill=(178, 34, 34), outline=(255, 255, 255), width=2)


def illu_virus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 220))
    random.seed(11)
    for i in range(6):
        cx = x + w * (0.12 + (i % 3) * 0.34)
        cy = y + h * (0.30 if i < 3 else 0.72)
        r = 11 if i % 2 else 14
        for k in range(8):
            a = k * math.pi / 4
            d.line([cx + r * math.cos(a), cy + r * math.sin(a),
                    cx + (r + 7) * math.cos(a), cy + (r + 7) * math.sin(a)],
                   fill=(178, 34, 34), width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(198, 60, 50))
        d.ellipse([cx - r * 0.4, cy - r * 0.4, cx + r * 0.2, cy + r * 0.2],
                  fill=(230, 120, 110))


ILLU = {1: illu_bahrain, 2: illu_bridge, 3: illu_summit, 4: illu_chip,
        5: illu_cyclone, 6: illu_knesset, 7: illu_euro, 8: illu_sanction,
        9: illu_trade, 10: illu_cricket, 11: illu_virus}


# ---------------------------------------------------------------- map
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(221, 233, 242))
    lat_min, lat_max, lon_min, lon_max = -58, 84, -180, 180

    def px(lon, lat):
        return (x + (lon - lon_min) / (lon_max - lon_min) * w,
                y + (lat_max - lat) / (lat_max - lat_min) * h)

    try:
        data = json.load(open(GEOJSON))
        for feat in data["features"]:
            geom = feat["geometry"]
            if geom is None:
                continue
            geoms = [geom["coordinates"]] if geom["type"] == "Polygon" \
                else geom["coordinates"] if geom["type"] == "MultiPolygon" \
                else []
            for poly in geoms:
                for ring in poly:
                    xs = [p[0] for p in ring]
                    if max(xs) - min(xs) > 300:
                        continue
                    pts = [px(lon, lat) for lon, lat in ring]
                    d.polygon(pts, fill=(228, 220, 196), outline=(150, 142, 122))
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
        col = PIN_COLOUR[n]
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=col,
                  outline=(255, 255, 255), width=2)
        t = str(n)
        tw = d.textlength(t, font=F_PIN)
        d.text((bx - tw / 2, by - 6), t, font=F_PIN, fill=(255, 255, 255))


# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top kicker
    d.text((24, 14), "THE WORLD\u2019S NEWS IN ONE PICTURE", font=F_KICK,
           fill=RED)
    right = "30 STORIES \u00b7 6 CONTINENTS"
    d.text((W - 24 - d.textlength(right, font=F_KICK), 14), right, font=F_KICK,
           fill=GREY)
    # masthead
    d.text((24, 34), "Wednesday 18 November 2026", font=F_MAST, fill=INK)
    d.rectangle([24, 100, W - 24, 103], fill=INK)
    d.rectangle([24, 106, W - 24, 107], fill=INK)

    # ---- heroes ------------------------------------------------------
    hy, hw, hgap = 114, 317, 12
    for i, (head, deck, kick, col) in enumerate(HEROES):
        cx = 24 + i * (hw + hgap)
        ILLU[i + 1](d, cx, hy, hw, 104)
        kicker_line(d, cx, hy + 112, i + 1, kick, col)
        yy = hy + 132
        for line in wrap(d, head, F_HERO_H, hw)[:3]:
            d.text((cx, yy), line, font=F_HERO_H, fill=INK)
            yy += 23
        yy += 3
        for line in wrap(d, deck, F_HERO_D, hw)[:3]:
            d.text((cx, yy), line, font=F_HERO_D, fill=(45, 42, 36))
            yy += 15
    d.rectangle([24, 388, W - 24, 389], fill=INK)

    # ---- medium grid --------------------------------------------------
    my, mh, mgap = 398, 143, 10
    mw = 238
    for row in range(2):
        for col_i in range(4):
            idx = row * 4 + col_i
            head, deck, kick, col = MEDIUM[idx]
            n = idx + 4
            cx = 24 + col_i * (mw + 8)
            cy = my + row * (mh + mgap)
            d.rectangle([cx, cy, cx + mw, cy + mh], fill=CARD_BG,
                        outline=CARD_LINE, width=1)
            ILLU[n](d, cx + 1, cy + 1, mw - 2, 46)
            kicker_line(d, cx + 8, cy + 51, n, kick, col)
            yy = cy + 71
            for line in wrap(d, head, F_MED_H, mw - 16)[:2]:
                d.text((cx + 8, yy), line, font=F_MED_H, fill=INK)
                yy += 16
            yy += 1
            for line in wrap(d, deck, F_MED_D, mw - 16)[:3]:
                d.text((cx + 8, yy), line, font=F_MED_D, fill=(45, 42, 36))
                yy += 12.5
    d.rectangle([24, 700, W - 24, 701], fill=INK)

    # ---- bottom: list (left) + map (right) ---------------------------
    by = 710
    d.text((24, by), "ALSO ON WEDNESDAY 18 NOVEMBER", font=F_KICK, fill=RED)
    d.rectangle([24, by + 20, 488, by + 21], fill=RED)
    yy = by + 28
    for i, item in enumerate(ALSO):
        n = i + 12
        d.text((24, yy), str(n), font=F_LIST_N, fill=RED)
        d.text((52, yy), item, font=F_LIST, fill=(30, 28, 24))
        yy += 13.8
    d.text((512, by), "WHERE IT HAPPENED", font=F_KICK, fill=RED)
    d.rectangle([512, by + 20, W - 24, by + 21], fill=RED)
    draw_map(d, 512, by + 28, 488, 224)
    legend_y = by + 262
    d.text((512, legend_y), "Numbers match the stories above.",
           font=F_MAP_CAP, fill=GREY)
    lx = 512
    ly = legend_y + 18
    for label, col in [("N. America", (36, 113, 163)),
                       ("Europe", (125, 60, 152)),
                       ("Middle East", (211, 84, 0)),
                       ("Asia", (30, 132, 73))]:
        d.ellipse([lx, ly + 2, lx + 9, ly + 11], fill=col)
        d.text((lx + 13, ly), label, font=F_MAP_CAP, fill=(45, 42, 36))
        lx += 13 + d.textlength(label, font=F_MAP_CAP) + 18

    # footer
    foot = ("The world\u2019s news for Wednesday 18 November 2026 \u00b7 Sources: "
            "AP, Reuters, AFP, BBC, Al Jazeera, CNBC, IMD, CSK.")
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, 1004), foot,
           font=F_FOOT, fill=GREY)

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes", img.size)


if __name__ == "__main__":
    main()
