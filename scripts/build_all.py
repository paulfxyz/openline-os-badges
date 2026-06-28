"""
Build ALL Openline OS navigation + hero/heading images.
Reuses the design system in gen.py (Lato Black + Lucide, light-tint icons).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import make, make_header, COLORS, render_icon, light_tint, OUT, FONT_PATH, SS, PRESETS
from PIL import Image, ImageDraw, ImageFont

# ---------- Section color themes (RGB) ----------
C = {
    "home": (247, 144, 9), "plan": (74, 26, 122), "develop": (184, 74, 16),
    "operate": (13, 92, 92), "grow": (122, 16, 16), "executive": (30, 46, 90),
    "production": (26, 92, 58), "team": (26, 92, 58), "guidebook": (122, 90, 16),
    "archives": (40, 54, 90),
}

# ===========================================================
# 1) LARGE NAV BUTTONS (Home Quick OS Navigation) 560x100
#    color = destination section ; icon = destination page icon
#    filename, fill_key, icon, label
# ===========================================================
NAV_BUTTONS = [
    ("button-plan.png",         "plan",       "plan",      "Plan"),
    ("button-launch.png",       "develop",    "develop",   "Develop"),
    ("button-operate.png",      "operate",    "operate",   "Operate"),
    ("button-grow.png",         "grow",       "grow",      "Grow"),
    ("button-production.png",   "production", "production","Production"),
    ("button-team.png",         "team",       "team",      "Team"),
    ("button-guidebook.png",    "guidebook",  "guidebook", "Guidebook"),
    ("button-executive-hq.png", "executive",  "executive", "Executive HQ"),
    ("button-archives.png",     "archives",   "archives",  "Archives"),
]

# ===========================================================
# 2) HERO "OVERVIEW" BANNERS  560x100 ; color = own page
#    filename, fill_key, icon, label
# ===========================================================
HEROES = [
    ("button-plan-overview.png", "plan",      "overview", "Overview"),
    ("button-overview-orange.png","develop",  "overview", "Overview"),
    ("button-overview-teal.png", "operate",   "overview", "Overview"),
    ("button-overview-red.png",  "grow",      "overview", "Overview"),
    ("button-overview-green.png","team",      "overview", "Overview"),
    ("button-overview-amber.png","guidebook", "overview", "Overview"),
    ("button-overview-archives.png","archives", "overview", "Overview"),
]

# ===========================================================
# 3) SECTION BADGES above inline databases (compact)
#    VARIED colors (not page-theme) for visual variety.
#    filename, RGB color, icon, label
# ===========================================================
# Curated varied palette (distinct, harmonious)
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
SECTION = [
    # PLAN page badges
    ("sec-plan-okrs.png",               PAL["violet"],  "okrs",         "OKRs"),
    ("sec-plan-key-results.png",        PAL["blue"],    "key-results",  "Key Results"),
    ("badge-objectives.png",            PAL["fuchsia"], "objectives",   "Objectives"),
    ("badge-key-results.png",           PAL["cyan"],    "key-results",  "Key Results"),
    ("button-plan-quarterly-overview.png",PAL["indigo"],"quarterly",    "Quarterly"),
    # DEVELOP page badges
    ("badge-projects.png",              PAL["orange"],  "projects",     "Projects"),
    ("badge-tasks.png",                 PAL["rust"],    "tasks",        "Tasks"),
    # GROW page badges
    ("badge-deals.png",                 PAL["rose"],    "rounds",       "Deals"),
    ("badge-closed.png",                PAL["red"],     "decisions",    "Closed"),
    # TEAM page badges
    ("badge-departments.png",           PAL["emerald"], "departments",  "Departments"),
    ("badge-staff-dashboards.png",      PAL["lime"],    "people",       "Staff"),
    # EXECUTIVE page badges
    ("badge-strategic-tasks.png",       PAL["indigo"],  "strategic",    "Strategic Tasks"),
    ("badge-what-youll-find.png",       PAL["teal"],    "overview",     "What You'll Find"),
    ("badge-why-this-exists.png",       PAL["amber"],   "decisions",    "Why This Exists"),
    ("badge-founder-office.png",        PAL["slate"],   "founder",      "Founder Office"),
    ("button-exec-priorities.png",      PAL["pink"],    "strategic",    "Priorities"),
    ("button-exec-projects.png",        PAL["blue"],    "projects",     "Projects"),
    ("sec-exec-okrs.png",               PAL["violet"],  "okrs",         "OKRs"),
]

# ===========================================================
# 4) GUIDEBOOK nav buttons  560x100 (amber)
# ===========================================================
GUIDEBOOK_BTN = [
    ("button-guidebook-how-it-works.png",      "guidebook", "book-open",   "How It Works"),
    ("button-guidebook-loom-video.png",        "guidebook", "circle-play", "Loom Video"),
    ("button-guidebook-tips-best-practices.png","guidebook","lightbulb",   "Tips & Best Practices"),
]

def gen_all():
    made = []
    for fn, key, icon, label in NAV_BUTTONS:
        made.append(make("button", C[key], icon, label, fn)); 
    for fn, key, icon, label in HEROES:
        made.append(make("button", C[key], icon, label, fn))
    for fn, color, icon, label in SECTION:
        made.append(make("section", color, icon, label, fn, autowidth=True))
    for fn, key, icon, label in GUIDEBOOK_BTN:
        made.append(make("button", C[key], icon, label, fn))
    # Quick-nav header (black)
    made.append(make_header("QUICK NAVIGATION GUIDE", "button-quick-nav-black.png"))
    return made

if __name__ == "__main__":
    m = gen_all()
    print(f"Generated {len(m)} images into {OUT}")
    for p in m:
        print(" ", os.path.basename(p))
