# 🎨 Openline Badge System — Reference & Prompting Guide

The single source of truth for generating the section badges, nav buttons, and hero
banners used across the Openline OS Notion workspace. Read this first, then copy one of
the **ready-to-run prompts** at the bottom to make new badges flawlessly.

---

## 1. What a badge is

A **badge** is a solid rounded pill with:

- a **flat color fill** (from the Openline palette),
- a clean **Lucide icon** rendered in a light tint of the fill color (auto-derived),
- an **ALL-CAPS** label in **Lato Black**, white, vertically centered.

They sit above inline databases / at the top of tabs to label a section. The look is
consistent everywhere because every badge is produced by the same generator: `badge-system/build_all.py` (reading `badge-system/badges.json`).

---

## 2. Repo & layout

- **Primary repo:** `paulfxyz/openline-os-badges` (https://github.com/paulfxyz/openline-os-badges)
- **Public mirror:** `paulfxyz/openline-audit-shots` — byte-identical, keeps legacy URLs alive. Never edited directly (see the README's *Mirror & URL safety net*).
- **Generator (source of truth):** `badge-system/badges.json` + `badge-system/gen_badge.py` + `badge-system/build_all.py`
- **Published badges:** `os-nav/` — committed PNGs served raw to Notion
- **Legacy generator:** `scripts/gen.py` + `scripts/gen_*.py` (older per-batch flow, kept for reference; new work goes through `badge-system/`)

Notion embeds badges via the **raw GitHub URL on `main`**, referencing a stable slug:

```
https://raw.githubusercontent.com/paulfxyz/openline-os-badges/main/os-nav/<file>.png
```

Referencing `main` by **stable slug** means a restyle (same slug, new PNG) updates every page at once. When you need an *immediate* refresh past caches, append a `?c=<short-sha>` token — see the README's *image cache trap*.

---

## 3. The generator API

```python
make(preset, fill, icon_name, label, outfile, autowidth=True, pad_right=18)
```

| Arg         | Meaning                                                                 |
|-------------|-------------------------------------------------------------------------|
| `preset`    | `"section"` (the badge family), `"mini"`, or `"button"`                 |
| `fill`      | RGB tuple from the palette, e.g. `(29, 78, 216)`                        |
| `icon_name` | a Lucide icon filename (without `.svg`) present in `scripts/lucide/`    |
| `label`     | text; auto-uppercased                                                   |
| `outfile`   | output filename, e.g. `"badge-arch-files.png"`                          |
| `autowidth` | keep `True` so the pill grows to fit the label (no text overflow)       |

### Presets — `(W, H, radius, font_px, text_x, icon_cx, icon_cy, icon_px)`

| Preset    | Size (W×H)      | Use                                            |
|-----------|-----------------|------------------------------------------------|
| `section` | 96×**34** (grows)| **Section badges** — the standard tab/db badge |
| `mini`    | 200×52          | nav grid badge                                 |
| `button`  | 280×50          | nav button / hero banner                       |

> **The badge family = `section` preset, 34px tall.** Always use `preset="section"` and
> `autowidth=True` for tab/section badges so they match every other badge on the pages.

`make_header(label, outfile, fill=(26,26,26), icon_name="compass")` makes the black
360×64 "QUICK NAVIGATION GUIDE" header pill — rarely needed.

---

## 4. The Openline palette (`PAL`)

Use these named RGB tuples for `fill`. Pick a color that fits the section's meaning and
stays distinct from its neighbors.

| Name      | RGB                | Name      | RGB                |
|-----------|--------------------|-----------|--------------------|
| violet    | `(109, 40, 217)`   | purple    | `(109, 40, 217)`   |
| indigo    | `(49, 46, 129)`    | blue      | `(29, 78, 216)`    |
| cyan      | `(14, 116, 144)`   | teal      | `(13, 92, 92)`     |
| emerald   | `(4, 120, 87)`     | green     | `(26, 92, 58)`     |
| lime      | `(77, 124, 15)`    | amber     | `(180, 120, 9)`    |
| orange    | `(194, 84, 16)`    | rust      | `(154, 52, 18)`    |
| red       | `(153, 27, 27)`    | rose      | `(159, 18, 57)`    |
| pink      | `(157, 23, 77)`    | fuchsia   | `(134, 25, 143)`   |
| slate     | `(51, 65, 95)`     |           |                    |

The icon tint is computed automatically (`light_tint(fill, 0.72)`) — never set it by hand.

---

## 5. Icons

59 Lucide icons are already vendored in `scripts/lucide/`. Common ones:

`archive · archives · boxes · folder-archive · trash-2 · files · package · database ·
server · globe · key-round · shield-check · workflow · puzzle · search · library ·
layout-grid · book-marked · book-open · layers · life-buoy · link-2 · list-checks ·
compass · home · lightbulb · runbook · sop · tasks · projects · team · people · contacts ·
departments · objectives · key-results · okrs · investors · rounds · deals · executive ·
founder · production · operate · develop · grow · plan · guidebook · overview · dashboards`

**Need a new icon?** Download from Lucide first:

```bash
cd scripts/lucide
curl -fsSL "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/<name>.svg" -o <name>.svg
```

Browse names at https://lucide.dev/icons . Pick a 2px-stroke outline icon (the generator
forces stroke-width 2.25 for consistency).

---

## 6. Established badge sets (for reference / matching)

**Archives tabs** (`badge-arch-*`):
| Tab          | Color  | Icon            |
|--------------|--------|-----------------|
| All / Browse | indigo | search          |
| Files        | orange | files           |
| OS Hubs      | blue   | boxes           |
| Resources    | violet | folder-archive  |
| Other        | slate  | archive         |
| Trash        | red    | trash-2         |

**Production tabs** (`badge-prod-*`):
| Tab                  | Color   | Icon          |
|----------------------|---------|---------------|
| Accounts             | amber   | key-round     |
| Domains              | cyan    | globe         |
| Servers & Databases  | teal    | server        |
| Access Confirmations | emerald | shield-check  |
| Automations          | violet  | workflow      |
| Systems              | indigo  | puzzle        |
| Automation Databases | blue    | database      |

> **Tip:** group a section's tabs into one color family, then give each tab a distinct
> hue within it (e.g. Production "Infra" = amber/cyan/teal/emerald; "Automation" = violet/indigo/blue).

---

## 7. Full workflow (copy/paste)

### a. Write a batch script

`scripts/gen_<area>_badges.py`:

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import make

PAL = {
    "violet": (109,40,217), "indigo": (49,46,129), "blue": (29,78,216),
    "cyan": (14,116,144), "teal": (13,92,92), "emerald": (4,120,87),
    "green": (26,92,58), "lime": (77,124,15), "amber": (180,120,9),
    "orange": (194,84,16), "rust": (154,52,18), "red": (153,27,27),
    "rose": (159,18,57), "pink": (157,23,77), "fuchsia": (134,25,143),
    "slate": (51,65,95), "purple": (109,40,217),
}

BADGES = [
    # (outfile,                 color,          icon,        label)
    ("badge-x-overview.png",    PAL["blue"],    "overview",  "Overview"),
    ("badge-x-tasks.png",       PAL["emerald"], "tasks",     "Tasks"),
]

for fn, color, icon, label in BADGES:
    print(make("section", color, icon, label, fn, autowidth=True))
```

### b. Generate + preview

```bash
cd scripts && python3 gen_<area>_badges.py
# composite previews into /tmp/*.png and visually inspect BEFORE committing
```

**Always preview** — check for text overflow, color/label clarity, right icon.

### c. Publish

```bash
cd /home/user/workspace/openline-os-badges
cp out_images/badge-x-*.png os-nav/
git -c user.email="hello@paulfleury.com" -c user.name="Paul Fleury" \
    add os-nav/badge-x-*.png scripts/gen_<area>_badges.py scripts/lucide/<any-new>.svg
git -c user.email="hello@paulfleury.com" -c user.name="Paul Fleury" \
    commit -q -m "Add <area> section badges"
git push origin HEAD          # uses the github credential
git rev-parse HEAD            # <-- copy this SHA
```

### d. Verify the raw URL is live (expect 200)

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://raw.githubusercontent.com/paulfxyz/openline-os-badges/main/os-nav/badge-x-overview.png"
```

### e. Embed in Notion

In the target tab/section, place the image right above the inline database:

```
![](https://raw.githubusercontent.com/paulfxyz/openline-os-badges/main/os-nav/badge-x-overview.png)
```

---

## 8. Rules / gotchas

- **Family = `section` preset, 34px tall, `autowidth=True`.** Don't change H.
- **Reference `main` by stable slug** (current convention) so a restyle updates every page at once; use a `?c=<short-sha>` token only when you need to bust caches immediately.
- **Preview before committing** — overflow and wrong-icon mistakes are easy to miss.
- Inline color/`<color:>` and `<page>` mention tags **do not render** inside Notion callout
  text via the API (they get escaped) — style links with a leading `→` and bold + `↗` instead.
- Inline `<database>` creation via markdown does **not** work — use the create-database tool.
- One commit per badge batch; keep the `gen_*.py` script in the repo so future edits are reproducible.

---

## 9. Ready-to-run prompt templates

> **New badge set for a page's tabs:**
> "Make section badges for the tabs on `<Notion page/URL>`, matching the Openline badge
> family (BADGE-SYSTEM.md): `section` preset, 34px, Lato-Black caps, Lucide icon in a light
> tint. Pick a coherent color family from PAL with a distinct hue per tab. Generate, preview
> them for me, then commit + push to `openline-os-badges` (and sync the mirror), verify the raw URLs are 200, and
> embed each badge above its content via the `main` slug URL."

> **Single new badge:**
> "Add one section badge `badge-<name>.png`, color `<PAL name>`, icon `<lucide name>`,
> label `<TEXT>` — same family as the others. Preview, push, give me the raw URL."

> **New icon needed:**
> "Download the Lucide `<name>` icon into `scripts/lucide/`, then make the badge as above."
