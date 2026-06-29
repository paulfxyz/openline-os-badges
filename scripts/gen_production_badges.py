"""Generate section badges for the OS > Production page tabs (2 sections, 7 tabs)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import make

PAL = {
    "violet":  (109, 40, 217),   "indigo":  (49, 46, 129),
    "blue":    (29, 78, 216),    "cyan":    (14, 116, 144),
    "teal":    (13, 92, 92),     "emerald": (4, 120, 87),
    "green":   (26, 92, 58),     "lime":    (77, 124, 15),
    "amber":   (180, 120, 9),    "orange":  (194, 84, 16),
    "rust":    (154, 52, 18),    "red":     (153, 27, 27),
    "rose":    (159, 18, 57),    "pink":    (157, 23, 77),
    "fuchsia": (134, 25, 143),   "slate":   (51, 65, 95),
    "purple":  (109, 40, 217),
}

BADGES = [
    # Infrastructure & Assets
    ("badge-prod-accounts.png",       PAL["amber"],   "key-round",    "Accounts"),
    ("badge-prod-domains.png",        PAL["cyan"],    "globe",        "Domains"),
    ("badge-prod-servers.png",        PAL["teal"],    "server",       "Servers & Databases"),
    ("badge-prod-access.png",         PAL["emerald"], "shield-check", "Access Confirmations"),
    # Automation & Systems
    ("badge-prod-automations.png",    PAL["violet"],  "workflow",     "Automations"),
    ("badge-prod-systems.png",        PAL["indigo"],  "puzzle",       "Systems"),
    ("badge-prod-auto-databases.png", PAL["blue"],    "database",     "Automation Databases"),
]

made = []
for fn, color, icon, label in BADGES:
    made.append(make("section", color, icon, label, fn, autowidth=True))
for p in made:
    print(p)
