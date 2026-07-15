#!/usr/bin/env python3
"""Regenerate the staff-dashboard badge family in HD (2x export), coherent palette."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_badge import build_badge

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "staff")
os.makedirs(OUT, exist_ok=True)

# Coherent cool "personal workspace" family: blue -> teal -> indigo -> purple.
STAFF = [
    # slug, label, color, icon, preset
    ("staff-button-dashboard",        "Dashboard",          "iris",      "home",      "button"),
    ("staff-badge-tasks",             "Tasks",              "blue",      "check",     "badge"),
    ("staff-badge-recurring-ops",     "Recurring Ops",      "teal",      "refresh",   "badge"),
    ("staff-badge-projects",          "Projects",           "indigo",    "folder",    "badge"),
    ("staff-badge-objectives",        "Objectives",         "grape",     "target",    "badge"),
    ("staff-badge-key-results",       "Key Results",        "turquoise", "chart",     "badge"),
    ("staff-badge-sops-and-workflows","SOPs & Workflows",   "cobalt",    "book",      "badge"),
    ("staff-badge-staff-dashboards",  "Staff Dashboards",   "iris",      "users",     "badge"),
]

results = []
for slug, label, color, icon, preset in STAFF:
    path, size = build_badge(label, slug, color=color, icon=icon,
                             out_dir=OUT, preset=preset, export_scale=1)
    results.append((slug, label, color, icon, preset, size))
    print(f"{slug:34s} {str(size):12s} [{color}/{icon}/{preset}]  {label}")

# Register in badges.json as the single source of truth (folder=staff, scale=2)
bj = os.path.join(os.path.dirname(os.path.abspath(__file__)), "badges.json")
d = json.load(open(bj))
existing = {it.get("slug") for it in d["badges"]}
for slug, label, color, icon, preset, size in results:
    entry = {"slug": slug, "label": label, "color": color, "icon": icon,
             "preset": preset, "folder": "staff",
             "page": "Team / Staff Dashboard"}
    # replace if present, else append
    d["badges"] = [it for it in d["badges"] if it.get("slug") != slug]
    d["badges"].append(entry)
json.dump(d, open(bj, "w"), indent=2, ensure_ascii=False)
print("registered", len(results), "staff badges in badges.json")
