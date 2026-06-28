"""Generate compact section-label badges (34px tall, like badge-how-it-works)
for use INSIDE the Guidebook callout boxes — smaller than the 50px nav buttons.
Uses each section's own theme color + page icon, matching the design system."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import make

# Section theme colors (from build_all.py C{})
C = {
    "plan": (74, 26, 122), "develop": (184, 74, 16),
    "operate": (13, 92, 92), "grow": (122, 16, 16), "executive": (30, 46, 90),
    "production": (26, 92, 58), "team": (26, 92, 58), "guidebook": (122, 90, 16),
    "archives": (40, 54, 90),
}

# filename, color_key, icon, label
NEW = [
    ("mini-plan.png",        "plan",       "plan",       "Plan"),
    ("mini-develop.png",     "develop",    "develop",    "Develop"),
    ("mini-operate.png",     "operate",    "operate",    "Operate"),
    ("mini-grow.png",        "grow",       "grow",       "Grow"),
    ("mini-team.png",        "team",       "team",       "Team"),
    ("mini-executive.png",   "executive",  "executive",  "Executive HQ"),
    ("mini-production.png",  "production", "production", "Production"),
    ("mini-archives.png",    "archives",   "archives",   "Archives"),
]

made = []
for fn, key, icon, label in NEW:
    made.append(make("section", C[key], icon, label, fn, autowidth=True))

for p in made:
    print(p)
