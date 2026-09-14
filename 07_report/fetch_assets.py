#!/usr/bin/env python3
"""
fetch_assets.py — Download the final employer deliverables for the
Varzaghan geoelectrical interpretation project.

The reference files (report PDF + QC charts) are hosted on the project
CDN (my.smart98.ir) because the API used for this repo cannot store
binary blobs losslessly. This script fetches them, verifies SHA-256
checksums, and writes them into 07_report/.

Usage:
    python3 fetch_assets.py            # download all assets
    python3 fetch_assets.py --verify   # only verify existing files

Requires: requests (or falls back to urllib).
"""
import hashlib
import os
import sys
import urllib.request

BASE_URL = "https://my.smart98.ir/f/"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

ASSETS = {
    "varzaghan_employer_report_precise.pdf": {
        "id": "file_GoXFu1hhiAEz",
        "sha256": "6fef2a0b725effc85c6b75c9255e51170dbeede362505c4708984a85056399ab",
    },
    "ves_curves.png": {
        "id": "file_BkzlvsNsDkqd",
        "sha256": "6662a3b39b9ff91bfcedb0422f0fb53faa6e65f039559d1dc6bd36c5b285cade",
    },
    "rho_histogram.png": {
        "id": "file_GSJa2RmVkGw9",
        "sha256": "f58eb7831b3890eceb60f391917d415b3ddd964a95de10c35e0c38403cea91dd",
    },
    "qc_boxplot.png": {
        "id": "file_RXfb8Ssk861H",
        "sha256": "4c42848add1df6bf521cef271304af364f30de4a1da697c8c96fbd72629a044d",
    },
}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: str) -> None:
    print(f"Downloading {os.path.basename(dest)} ...")
    urllib.request.urlretrieve(url, dest)


def main() -> int:
    verify_only = "--verify" in sys.argv
    failures = 0
    for name, meta in ASSETS.items():
        dest = os.path.join(OUT_DIR, name)
        if not verify_only and not os.path.exists(dest):
            download(BASE_URL + meta["id"], dest)
        if os.path.exists(dest):
            actual = sha256(dest)
            ok = actual == meta["sha256"]
            print(f"[{'OK ' if ok else 'BAD'}] {name}  sha256={actual[:16]}...")
            failures += 0 if ok else 1
        else:
            print(f"[MISS] {name} not present")
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())