#!/usr/bin/env python3
import base64
import os
import sys

BASEDIR = os.path.join(os.path.dirname(__file__), "07_report")
os.makedirs(BASEDIR, exist_ok=True)

FILES = [
    ("varzaghan_employer_report_precise.pdf", "employer_report.b64"),
    ("ves_curves.png", "ves_curves.b64"),
    ("rho_histogram.png", "rho_histogram.b64"),
    ("qc_boxplot.png", "qc_boxplot.b64"),
]

for outname, b64name in FILES:
    src = os.path.join(os.path.dirname(__file__), b64name)
    out = os.path.join(BASEDIR, outname)
    try:
        with open(src, "r") as f:
            data = f.read()
        with open(out, "wb") as f:
            f.write(base64.b64decode(data))
        print(f"Decoded {outname} -> {out}")
    except FileNotFoundError:
        print(f"WARNING: {src} not found; skipping {outname}")
