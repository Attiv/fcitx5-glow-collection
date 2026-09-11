#!/usr/bin/env python3
"""Trim and compress the preview PNGs produced by build-guest-previews.cjs.

Playwright screenshots a fixed viewport, leaving a wide border of background
around the candidate panel. This crops every shot to its content bounding box
(plus a small margin) and re-encodes it so the repository stays small.

Usage:
    python3 glow-studio/trim-previews.py            # trim + compress all
    python3 glow-studio/trim-previews.py --check    # report only, no writes
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

PACK = Path(__file__).resolve().parent
SHOTS = PACK / 'screenshots'
MARGIN = 18          # px of padding kept around the content
BG_TOLERANCE = 18    # channel distance from the corner colour that still counts as background


def content_bbox(im, tolerance=BG_TOLERANCE):
    """Bounding box of everything that differs from the top-left pixel."""
    a = np.asarray(im.convert('RGB')).astype(np.int16)
    bg = a[0, 0]
    mask = np.abs(a - bg).sum(axis=2) > tolerance
    if not mask.any():
        return None
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def trim(path, check=False):
    before = path.stat().st_size
    im = Image.open(path)
    box = content_bbox(im)
    if not box:
        return before, before, None
    w, h = im.size
    left = max(0, box[0] - MARGIN)
    top = max(0, box[1] - MARGIN)
    right = min(w, box[2] + MARGIN)
    bottom = min(h, box[3] + MARGIN)
    cropped = im.crop((left, top, right, bottom))
    if check:
        return before, before, cropped.size
    # Palette-quantise the UI shots: flat colours survive 256 colours cleanly while
    # the file shrinks by an order of magnitude.
    out = cropped.convert('RGB').quantize(colors=256, method=Image.MEDIANCUT, dither=Image.NONE)
    out.save(path, optimize=True)
    return before, path.stat().st_size, cropped.size


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    targets = sorted(SHOTS.glob('guest-*.png')) + \
              sorted((SHOTS / 'families').glob('*.png')) + \
              sorted((SHOTS / 'themes').glob('*.png'))
    if not targets:
        raise SystemExit('No preview images found; run build-guest-previews.cjs first.')
    total_before = total_after = 0
    for p in targets:
        before, after, size = trim(p, check=args.check)
        total_before += before
        total_after += after
        print(f'{p.relative_to(PACK)!s:44} {before/1024:9.1f}K -> {after/1024:8.1f}K  {size}')
    print(f'\n{len(targets)} files: {total_before/1048576:.1f}MB -> {total_after/1048576:.1f}MB')


if __name__ == '__main__':
    main()
