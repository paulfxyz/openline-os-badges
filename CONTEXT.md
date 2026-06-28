# Openline OS — Badge & Hero Image System

This repo hosts every pill/badge/hero image used across the **Openline OS** Notion
workspace (OS section pages + staff dashboards). Images are referenced from Notion
via pinned-SHA `raw.githubusercontent.com` URLs so they never break.

---

## 1. How images are served

Raw URL pattern (always pin a commit SHA, never use `main`):

```
https://raw.githubusercontent.com/paulfxyz/openline-audit-shots/<SHA>/<folder>/<file>.png
```

| Folder     | Used by                          | Current SHA  |
|------------|----------------------------------|--------------|
| `os-nav/`  | OS section pages (Plan, Develop…) | `216b739b`   |
| `staff/`   | Staff dashboards + templates      | `4dcdcdd`    |

> When you regenerate images and push, the SHA changes. You must then update the
> SHA in the Notion pages that reference them (see section 5).

---

## 2. Design system

All images share one look: solid rounded pill + Lucide icon (light tint of the
fill color) + bold **ALL-CAPS** white label (Lato Black).

### Size presets (`scripts/gen.py` → `PRESETS`)

| Preset    | Size (W×H) | Use                                   |
|-----------|-----------|----------------------------------------|
| `button`  | 280×50    | Section heroes / "Overview" banners    |
| `section` | auto×34   | Small badges above an inline database  |
| `mini`    | 200×52    | (legacy) mini nav badges               |

Notion renders a standalone image at its intrinsic pixel width, so **smaller PNG =
smaller on page**. Heroes are 280×50; inside badges are 34px tall (auto width).

### Color palette (`scripts/build_all.py` → `PAL`, RGB)

| Name    | RGB             | Name    | RGB             |
|---------|-----------------|---------|-----------------|
| violet  | (109, 40, 217)  | emerald | (4, 120, 87)    |
| indigo  | (49, 46, 129)   | green   | (26, 92, 58)    |
| blue    | (29, 78, 216)   | lime    | (77, 124, 15)   |
| cyan    | (14, 116, 144)  | amber   | (180, 120, 9)   |
| teal    | (13, 92, 92)    | orange  | (194, 84, 16)   |
| rust    | (154, 52, 18)   | red     | (153, 27, 27)   |
| rose    | (159, 18, 57)   | pink    | (157, 23, 77)   |
| fuchsia | (134, 25, 143)  | slate   | (51, 65, 95)    |

**Rule of thumb:**
- **Overview heroes** keep their *page-theme* color (Plan = purple, Develop =
  orange, Operate = teal, Grow = red, Team/Production = green, Guidebook = amber,
  Executive/Archives = navy).
- **Inside badges** (non-overview) use *varied* colors from `PAL` for visual
  variety — no two adjacent badges should share a color.

---

## 3. Image inventory

### `os-nav/` (OS section pages)

**Section heroes — 280×50, page-theme colored:**
`button-plan-overview`, `button-overview-orange` (Develop),
`button-overview-teal` (Operate), `button-overview-red` (Grow),
`button-overview-green` (Team), `button-overview-amber` (Guidebook),
`button-overview-archives`.

**Home nav buttons — 280×50:** `button-plan`, `button-launch` (Develop),
`button-operate`, `button-grow`, `button-production`, `button-team`,
`button-guidebook`, `button-executive-hq`, `button-archives`.

**Inside badges — auto×34, varied colors:**
`badge-objectives`, `badge-key-results`, `badge-projects`, `badge-tasks`,
`badge-deals`, `badge-closed`, `badge-departments`, `badge-staff-dashboards`,
`badge-strategic-tasks`, `badge-what-youll-find`, `badge-why-this-exists`,
`badge-founder-office`, `button-exec-priorities`, `button-exec-projects`,
`sec-exec-okrs`, `sec-plan-okrs`, `sec-plan-key-results`,
`button-plan-quarterly-overview`.

**Guidebook buttons — 280×50:** `button-guidebook-how-it-works`,
`button-guidebook-loom-video`, `button-guidebook-tips-best-practices`.

### `staff/` (staff dashboards + templates)

**Hero — 280×50, deep red:** `staff-button-dashboard`.

**Section badges — auto×34, varied colors:**
`staff-badge-tasks` (rust), `staff-badge-recurring-ops` (teal),
`staff-badge-projects` (orange), `staff-badge-objectives` (fuchsia),
`staff-badge-key-results` (cyan), `staff-badge-sops-and-workflows` (indigo),
`staff-badge-staff-dashboards` (lime).

---

## 4. How to generate / regenerate images

Requirements: Python 3 with `Pillow` and `cairosvg`, plus the **Lato Black**
font installed at `/usr/share/fonts/truetype/lato/Lato-Black.ttf`
(the Lucide SVG icons are bundled in `scripts/lucide/`).

```bash
pip install Pillow cairosvg

# 1. OS section images  -> writes to ../out_images/
python scripts/build_all.py

# 2. Staff dashboard images -> writes to ../out_images/
python scripts/make_staff.py
```

To **add a new badge**: edit the relevant list in `scripts/build_all.py`
(`SECTION`, `HEROES`, `NAV_BUTTONS`) or the `THEME` dict in
`scripts/make_staff.py`, pick a `PAL` color + a Lucide icon name (must exist in
`scripts/lucide/`), then re-run the script.

To **change a size**: edit `PRESETS` in `scripts/gen.py`.

---

## 5. Publishing changes (the full loop)

```bash
# after regenerating into out_images/
cp out_images/<changed>.png os-nav/      # or staff/
git add os-nav staff scripts CONTEXT.md
git commit -m "Describe the change"
git push origin main
git rev-parse HEAD                        # <- this is your new SHA
```

Then in Notion, update the referencing pages to the new SHA. Easiest is a
find-and-replace of the old SHA → new SHA inside each page's image URLs.

**Pages that reference these images:**
- OS pages: Plan, Develop, Operate, Grow, Team, Guidebook, Executive, Archives,
  Staff Dashboards index, Openline OS (Home).
- Staff: every page in the **People (Staff)** database, plus the two database
  templates ("New Staff Dashboard" = default, "New Staff (V2)").

> Tip: keep the OS folder and staff folder on independent SHAs — you can re-push
> one without disturbing the other, as long as you only update the affected pages.
