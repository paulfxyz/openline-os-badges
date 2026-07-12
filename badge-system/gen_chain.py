#!/usr/bin/env python3
"""
Golden Rule chain image — four colored word-badges joined by arrows:
  OBJECTIVE → KEY RESULT → PROJECT → TASK

Reuses the exact badge style (flat rounded rect, white bold caps text) from
gen_badge.build_badge, then composes them onto one transparent canvas with
crisp arrow connectors between each pill. Rendered at 3x then downsampled.
"""
import os
from PIL import Image, ImageDraw
from gen_badge import build_badge, PALETTE, hex2rgb

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
S = 3  # supersample

# The four links, each its own color (icons match the concept)
STEPS = [
    ("Objective",  "grape",   "target"),   # top of chain — the ambition
    ("Key Result", "cyan",    "chart"),     # measurable
    ("Project",    "amber",   "layers"),    # initiative
    ("Task",       "emerald", "check"),     # the doable step
]

ARROW_GAP = 22        # horizontal space reserved for each arrow (final px)
SIDE_PAD  = 6         # tiny breathing room at the far edges
ARROW_COL = "#64748B" # slate-500 — neutral connector, reads on light + dark
PRESET    = "button"  # bigger pills (52px tall) for a crisp hero look

def render():
    # 1) render each pill badge to a temp slug, load as image
    pills = []
    for i, (label, color, icon) in enumerate(STEPS):
        slug = f"_chain_pill_{i}"
        path, size = build_badge(label, slug, color, icon, out_dir=OUT_DIR, preset=PRESET)
        img = Image.open(path).convert("RGBA")
        pills.append(img)
        os.remove(path)

    ph = pills[0].height  # all badges share height (button preset = 52)
    gap = ARROW_GAP
    total_w = SIDE_PAD * 2 + sum(p.width for p in pills) + gap * (len(pills) - 1)
    H = ph

    # Compose at the pills' native resolution (no re-downsample → no quality loss),
    # then scale the whole thing up 2x with LANCZOS so it renders crisp in Notion.
    canvas = Image.new("RGBA", (total_w, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)

    arrow_rgb = hex2rgb(ARROW_COL)
    cy = H / 2
    x = SIDE_PAD
    for i, p in enumerate(pills):
        canvas.alpha_composite(p, (int(x), int((H - p.height) / 2)))
        x += p.width
        if i < len(pills) - 1:
            gx0 = x + gap * 0.16
            gx1 = x + gap * 0.80
            lw = 3
            d.line([gx0, cy, gx1, cy], fill=arrow_rgb + (255,), width=lw)
            hs = gap * 0.34
            d.polygon([
                (gx1, cy),
                (gx1 - hs, cy - hs * 0.60),
                (gx1 - hs, cy + hs * 0.60),
            ], fill=arrow_rgb + (255,))
            x += gap

    final = canvas
    out = os.path.join(OUT_DIR, "chain-golden-rule.png")
    final.save(out)
    print("wrote", out, final.size)
    return out

if __name__ == "__main__":
    render()
