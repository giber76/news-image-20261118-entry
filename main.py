#!/usr/bin/env python3
"""news-image-20261118 entry (Python 3.13, standard library only).

The entry image is the entry.png beside this file; the program copies it
to /output/entry.png. The image itself was drawn by draw.py in this
repository (Pillow, flat procedural art, no copied photograph): a dense
broadsheet front page for Wednesday 18 November 2026 -- 3 illustrated
hero cards, 8 illustrated medium cards, a numbered 12-30 list and a
world map with numbered pins, 30 verified stories in all.

Run it with:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT_DIR, "entry.png"))
print("wrote", os.path.join(OUT_DIR, "entry.png"))
