"""
Generate staff-dashboard images in the NEW compact design system, ALL-CAPS.
Matches OS pages: hero uses 'button' preset (280x50), section badges use
'section' preset (autowidth x34). Varied colors from the OS palette for variety.
Writes into out_images/ with the SAME filenames used on staff pages.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import make, OUT
from PIL import Image

# Varied palette (same as OS build_all.py PAL)
PAL = {
    "violet":  (109, 40, 217),   "indigo":  (49, 46, 129),
    "blue":    (29, 78, 216),    "cyan":    (14, 116, 144),
    "teal":    (13, 92, 92),     "emerald": (4, 120, 87),
    "green":   (26, 92, 58),     "lime":    (77, 124, 15),
    "amber":   (180, 120, 9),    "orange":  (194, 84, 16),
    "rust":    (154, 52, 18),    "red":     (153, 27, 27),
    "rose":    (159, 18, 57),    "pink":    (157, 23, 77),
    "fuchsia": (134, 25, 143),   "slate":   (51, 65, 95),
}

# Hero: red theme (staff dashboard identity), 'button' preset
HERO_COLOR = (192, 28, 28)   # deep red

# Section badges -> distinct varied colors
THEME = {
    "tasks":              (PAL["rust"],    "tasks",       "Tasks"),
    "recurring-ops":      (PAL["teal"],    "recurring",   "Recurring Ops"),
    "projects":           (PAL["orange"],  "projects",    "Projects"),
    "objectives":         (PAL["fuchsia"], "objectives",  "Objectives"),
    "key-results":        (PAL["cyan"],    "key-results", "Key Results"),
    "sops-and-workflows": (PAL["indigo"],  "sop",         "SOPs & Workflows"),
    "staff-dashboards":   (PAL["lime"],    "people",      "Staff Dashboards"),
}


if __name__ == "__main__":
    made = []
    # Hero (button preset = 280x50, autowidth so longer labels fit)
    p = make("button", HERO_COLOR, "dashboards", "Dashboard",
             "staff-button-dashboard.png", autowidth=True)
    made.append(os.path.basename(p))
    # Section badges (section preset = x34, autowidth)
    for key, (fill, icon, label) in THEME.items():
        p = make("section", fill, icon, label, f"staff-badge-{key}.png", autowidth=True)
        made.append(os.path.basename(p))
    # contact sheet
    imgs = [Image.open(os.path.join(OUT, n)).convert("RGBA") for n in made]
    gap = 12
    sheet_w = max(i.width for i in imgs) + 2 * gap
    sheet_h = sum(i.height for i in imgs) + gap * (len(imgs) + 1)
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (245, 245, 245, 255))
    y = gap
    for i in imgs:
        sheet.alpha_composite(i, (gap, y)); y += i.height + gap
    sheet.save(os.path.join(OUT, "_staff_sheet.png"))
    for n in made:
        im = Image.open(os.path.join(OUT, n))
        print(f"  {n}: {im.size[0]}x{im.size[1]}")
    print("staff done")
