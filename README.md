<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/paulfxyz/openline-brand-assets/main/logo/png/openline-logo-white.png" />
  <img src="https://raw.githubusercontent.com/paulfxyz/openline-brand-assets/main/logo/png/openline-logo-color.png" alt="Openline" width="120" height="120" />
</picture>

# Openline OS · Badge System

**The badging system for the Openline OS Notion workspace — the source of truth and public image host for every badge, nav button, and hero banner embedded across the OS.**

[![Purpose](https://img.shields.io/badge/purpose-OS%20badge%20system-0F766E?style=flat-square)](#what-this-repo-is)
[![Badges](https://img.shields.io/badge/badges-generated%20from%20JSON-6D28D9?style=flat-square)](#the-badge-system-badge-system)
[![Images](https://img.shields.io/badge/os--nav%20images-122-0E9CA8?style=flat-square)](#image-inventory)
[![Visibility](https://img.shields.io/badge/visibility-public%20(required)-F38020?style=flat-square)](#-why-this-repo-must-stay-public)
[![Mirror](https://img.shields.io/badge/mirror-openline--audit--shots-9333EA?style=flat-square)](#mirror--url-safety-net)
[![Backup](https://img.shields.io/badge/backup-restore%20ready-22C55E?style=flat-square)](#backup--restore)
[![Website](https://img.shields.io/badge/openline.com-Visit-FF6A00?style=flat-square)](https://openline.com)

</div>

---

> **Openline** is an eSIM provider that always gets the best signal — instant data in **190+ countries**, multi-carrier Tier-1 networks, automatic switching, no roaming bills.
>
> This repository is the **badging system for the Openline OS** — the shared operating workspace in Notion. It holds the generator that produces every badge, nav button, and hero banner, and it hot-hosts those PNGs straight into Notion pages via `raw.githubusercontent.com` URLs.
>
> It also keeps the original UI/UX **audit screenshots** of `openline.com` as a point-in-time archive (`shots/`), since that is where this repo started — but the badge system is now its primary job.

---

## ⚠️ Why this repo must stay public

Every badge and hero image in the Openline OS is embedded with a **`raw.githubusercontent.com`** URL like:

```
https://raw.githubusercontent.com/paulfxyz/openline-os-badges/main/os-nav/badge-tasks.png
```

`raw.githubusercontent.com` **only serves files from public repositories.** If this repo is flipped to **private**, every one of those URLs returns `404` and **all badges, nav buttons, and hero banners across the entire OS (Executive, Team, Plan, Develop, Operate, Grow, Production, Guidebook, Archives, plus every staff dashboard and the HR Resources hub) break instantly.**

> **Bottom line: keep this repo `public`.** It contains no secrets — only decorative PNGs and the generator that makes them. The whole point is that GitHub serves the images for free, at a stable URL.

---

## Mirror & URL safety net

This repo was renamed from **`openline-audit-shots`** → **`openline-os-badges`** to match what it actually does now. Because `raw.githubusercontent.com` does **not** follow GitHub's repo-rename redirect, a public **mirror** is kept at the old name so historical embeds never break:

| Repo | Role | Raw URL base |
| --- | --- | --- |
| **`openline-os-badges`** | ✅ Primary / canonical — edit here | `raw.githubusercontent.com/paulfxyz/openline-os-badges/main/…` |
| `openline-audit-shots` | 🪞 Public mirror — do not edit directly | `raw.githubusercontent.com/paulfxyz/openline-audit-shots/main/…` |

Both serve byte-identical files. New work references the **primary** repo; the mirror exists purely so any old `openline-audit-shots` URL still resolves. Keep them in sync with [`scripts/sync-mirror.sh`](#keeping-the-mirror-in-sync) after every push. **Both must stay public.**

---

## Table of contents

- [What this repo is](#what-this-repo-is)
- [Repository layout](#repository-layout)
- [The badge system (`badge-system/`)](#the-badge-system-badge-system)
- [Image inventory](#image-inventory)
- [Hot-link URLs (raw GitHub)](#hot-link-urls-raw-github)
- [Add or restyle a badge](#add-or-restyle-a-badge)
- [The publishing loop](#the-publishing-loop)
- [Keeping the mirror in sync](#keeping-the-mirror-in-sync)
- [Backup & restore](#backup--restore)
- [The image cache trap](#the-image-cache-trap)
- [Audit archive (`shots/`)](#audit-archive-shots)
- [Contributing & maintenance](#contributing--maintenance)
- [Changelog](#changelog)

---

## What this repo is

| Layer | What it holds | Who reads it |
| --- | --- | --- |
| **Badge system** | `badge-system/` — `badges.json` (source of truth) + `gen_badge.py` + `build_all.py` | Anyone making/restyling a badge |
| **OS images** | `os-nav/` — 122 badges, nav buttons, and hero banners for the Notion OS | Notion (hot-linked) |
| **Staff images** | `staff/` — hero + section images for staff dashboards | Notion (hot-linked) |
| **Audit archive** | `shots/` — 36 annotated UI/UX audit screenshots of `openline.com` | Reference only (frozen) |
| **Ops** | `scripts/` — sync-mirror + backup/restore helpers | Maintainers |
| **Docs** | [`BADGE-SYSTEM.md`](BADGE-SYSTEM.md), [`CONTEXT.md`](CONTEXT.md), this README | Maintainers |

---

## Repository layout

```
openline-os-badges/
├── README.md                ← you are here
├── BADGE-SYSTEM.md          ← design system + full generator reference
├── CONTEXT.md               ← how images reach Notion + full inventory + pages
│
├── badge-system/            ← ★ the live badge generator (source of truth)
│   ├── badges.json          ← every badge: slug, label, color, icon, group
│   ├── gen_badge.py         ← renderer — draws one flat pill badge
│   ├── build_all.py         ← reads badges.json, renders the whole set
│   ├── gen_chain.py         ← one-off composite/diagram generator
│   └── preview.png          ← contact sheet of the current set
│
├── os-nav/                  ← 122 published OS images (hot-linked into Notion)
│   ├── badge-*.png          ← section badges (auto×34px flat pills)
│   └── button-*.png         ← nav buttons & section heroes
│
├── staff/                   ← staff-dashboard images (hot-linked into Notion)
│
├── shots/                   ← 36 annotated UI/UX audit screenshots (frozen archive)
│
└── scripts/                 ← ops helpers
    ├── sync-mirror.sh       ← push primary → public mirror (openline-audit-shots)
    ├── backup.sh            ← snapshot the repo to a timestamped bundle + tarball
    └── restore.sh           ← restore from a bundle/tarball
```

---

## The badge system (`badge-system/`)

Badges are **generated programmatically**, not hand-designed or AI-generated. That gives:

- **Perfectly consistent style** (color, shape, font, spacing) every time
- **No hallucinated text** — the label is rendered from a string
- **One source of truth** — edit [`badge-system/badges.json`](badge-system/badges.json), re-run, commit
- **Global restyle** — re-render *every* badge at once if the style ever changes

**The look:** a flat rectangle with tiny rounded corners, a solid fill from the Openline palette, a white line-icon on the left, and a bold **ALL-CAPS** white label. Rendered at 3× then downsampled (Lanczos) for crisp edges. Full spec, palette, icons, and presets are in [`BADGE-SYSTEM.md`](BADGE-SYSTEM.md).

```bash
cd badge-system
python3 build_all.py --dir ../os-nav     # renders every badge straight into os-nav/
```

---

## Image inventory

- **`os-nav/`** — 122 PNGs: section badges (`badge-*`, auto×34 flat pills, above inline databases) and nav buttons / section heroes (`button-*`). Covers every OS section plus the **HR Resources** hub (`badge-hr-*`).
- **`staff/`** — staff-dashboard hero + section badges, same generator and embed pattern.
- **`shots/`** — 36 frozen audit screenshots (see [Audit archive](#audit-archive-shots)).

Full per-image listing lives in [`CONTEXT.md`](CONTEXT.md).

---

## Hot-link URLs (raw GitHub)

Notion embeds reference the **primary** repo on `main`:

```
https://raw.githubusercontent.com/paulfxyz/openline-os-badges/main/os-nav/<slug>.png
```

Because pages reference badges by **stable slug on `main`**, committing a restyled PNG over the old one updates **every page at once** — no Notion edits required for a pure restyle. To force past caches when you *do* need an immediate refresh, append a cache-buster token (`?c=<short-sha>`) — see [the image cache trap](#the-image-cache-trap).

> These resolve **only while the repo is public.** The mirror serves the same files at `…/openline-audit-shots/main/…` for any legacy URL.

---

## Add or restyle a badge

1. Add or edit an entry in [`badge-system/badges.json`](badge-system/badges.json):
   ```json
   { "slug": "badge-my-thing", "label": "My Thing", "color": "teal", "icon": "eye" }
   ```
2. Render the full set:
   ```bash
   cd badge-system && python3 build_all.py --dir ../os-nav
   ```
3. **Preview before committing** — open `badge-system/preview.png` (or build a stacked sheet) and check for text overflow, wrong icon, or a color clashing with a sibling.
4. Reference it in Notion:
   ```
   ![](https://raw.githubusercontent.com/paulfxyz/openline-os-badges/main/os-nav/badge-my-thing.png)
   ```

Palette and icon names are documented in [`BADGE-SYSTEM.md`](BADGE-SYSTEM.md).

---

## The publishing loop

```bash
# 1. Edit badges.json / gen_badge.py, then re-render
cd badge-system && python3 build_all.py --dir ../os-nav && cd ..

# 2. Commit as Paul & push to the primary repo
git add badge-system os-nav staff *.md
git -c user.email="hello@paulfleury.com" -c user.name="Paul Fleury" commit -m "Describe the change"
git push origin main

# 3. Sync the public mirror so legacy URLs stay identical
bash scripts/sync-mirror.sh

# 4. (Only if you need an instant refresh past caches) bump the ?c= token in the Notion embeds
```

---

## Keeping the mirror in sync

After every push to the primary repo, run:

```bash
bash scripts/sync-mirror.sh
```

It force-pushes the primary `main` to `openline-audit-shots` so both raw hosts serve identical bytes. The mirror is **never edited directly** — it only ever receives what the primary already has.

---

## Backup & restore

Two helpers snapshot and rebuild the whole repo independently of GitHub:

```bash
# Create a timestamped backup (git bundle = full history + a plain tarball of files)
bash scripts/backup.sh              # writes to ./backups/openline-os-badges-<UTC>.{bundle,tar.gz}

# Restore from a backup into a fresh directory
bash scripts/restore.sh backups/openline-os-badges-<UTC>.bundle ./restored-repo
```

- The **`.bundle`** is a complete, self-contained clone of all branches and history — `git clone backup.bundle` reconstructs the repo exactly.
- The **`.tar.gz`** is a flat copy of the working tree (images + scripts) for quick file recovery without git.
- Keep backups off GitHub (local disk / cloud storage) so the repo can be rebuilt even if the remote is lost.

---

## The image cache trap

Two cache layers sit between a pushed PNG and what a Notion viewer sees:

1. **GitHub raw CDN** caches each path `max-age=300` and **ignores query strings** — a `?c=` bump alone does *not* bypass it.
2. **Notion's image proxy** caches per proxied URL; restarting Notion does not clear it.

**Reliable refresh:** wait ~5 min for the GitHub CDN to expire (or verify the served blob SHA via the GitHub contents API), *then* point Notion at a **brand-new** `?c=<short-sha>` token that has never been proxied before. Verify each raw URL returns `200` with the new bytes before considering it done.

---

## Audit archive (`shots/`)

The repo started as the host for the `openline.com` UI/UX audit. `shots/` holds **36 annotated screenshots** captured during that audit — numbered and named for the issue or surface each documents. They are a **point-in-time artifact**: not regenerated, kept for reference and traceability. They no longer drive the repo's purpose but stay here as history.

---

## Contributing & maintenance

This repo is **actively maintained** alongside the Openline OS.

- **Adding a section/hub to the OS?** Add its badge to `badges.json`, render, preview, push, sync the mirror, then embed the raw URL in Notion.
- **Spotted a broken badge in Notion?** It's almost always a stale token or a private-repo URL — confirm **both** repos are still **public** and the slug exists in `os-nav/`.
- **New audit screenshots?** They're frozen; only add to `shots/` if you're extending the original audit.

### Don'ts

- ❌ Don't make either repo private — it breaks every OS badge ([why](#-why-this-repo-must-stay-public)).
- ❌ Don't edit the mirror (`openline-audit-shots`) directly — only sync into it.
- ❌ Don't store anything secret here — both repos are public by design.

### Maintainer

- **[@paulfxyz](https://github.com/paulfxyz)** — repository owner.

---

## Changelog

### 2026-07-12

- 🔁 **Renamed** `openline-audit-shots` → `openline-os-badges` to reflect its real purpose (the OS badge system), and re-oriented all docs around it.
- 🪞 **Added a public mirror** at the old name so legacy `raw.githubusercontent.com/.../openline-audit-shots/...` URLs never break.
- 💾 **Added backup/restore + mirror-sync scripts** (`scripts/backup.sh`, `scripts/restore.sh`, `scripts/sync-mirror.sh`).
- 🧑‍🤝‍🧑 Added the **HR Resources** badge set (`badge-hr-*`) for the new OS ⟩ Team hub.

### Earlier

- Added the OS badge system (`badge-system/`, `os-nav/`, `staff/`) and the [`BADGE-SYSTEM.md`](BADGE-SYSTEM.md) / [`CONTEXT.md`](CONTEXT.md) references.
- Initial drop: 36 UI/UX audit screenshots of `openline.com` (`shots/`).

---

<div align="center">

<sub>© Openline · <a href="https://openline.com">openline.com</a> · Keep this repo <strong>public</strong></sub>

</div>
