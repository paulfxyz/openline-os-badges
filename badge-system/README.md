# Openline OS — Badge System

Sustainable, replicable generator for the `os-nav/` pill badges used across the
Openline OS Notion pages (Executive, Production, etc.).

## Why

Badges are **generated programmatically**, not hand-designed or AI-generated.
That means:

- Perfectly consistent style (color, shape, font, spacing) every time
- No hallucinated text — the label is rendered from a string
- One source of truth: edit [`badges.json`](./badges.json), re-run, commit
- Re-render **every** badge at once if the style ever changes

## Files

| File            | Purpose                                                        |
| --------------- | ------------------------------------------------------------- |
| `badges.json`   | Source of truth — every badge (slug, label, color, icon, page) |
| `gen_badge.py`  | Renderer — draws one pill badge (shape, icon, text)           |
| `build_all.py`  | Reads `badges.json` and renders all badges                    |
| `preview.png`   | Contact sheet of the current badge set                        |

## Regenerate everything

```bash
cd badge-system
python3 build_all.py --dir ../os-nav   # writes PNGs straight into os-nav/
git add ../os-nav/*.png preview.png
git commit -m "Regenerate badges"
git push
```

Because pages reference badges by stable slug via raw GitHub URL
(`https://raw.githubusercontent.com/paulfxyz/openline-os-badges/main/os-nav/<slug>.png`),
committing new PNGs over the old ones updates **every page at once** — no Notion
edits required for a pure restyle.

## Add a new badge

1. Add an entry to `badges.json`:
   ```json
   { "slug": "badge-my-thing", "label": "My Thing", "color": "navy", "icon": "eye", "page": "..." }
   ```
2. `python3 build_all.py --dir ../os-nav`
3. Reference it in Notion:
   `![](https://raw.githubusercontent.com/paulfxyz/openline-os-badges/main/os-nav/badge-my-thing.png)`

## Style spec

- Rounded pill, 34px tall, transparent background (RGBA PNG)
- Solid fill, bold uppercase white text with letter-spacing
- Small white line-icon on the left
- Rendered at 3× then downsampled (Lanczos) for crisp edges

### Palette (sampled from the original badges)

`navy #312E81` · `gold #B47809` · `purple #86198F` · `emerald #047857` ·
`cyan #0E7490` · `violet #6D28D9` · `slate #334155` · `rose #9F1239` ·
`teal #0F766E` · `orange #C2410C` · `blue #1D4ED8` · `pink #BE185D`
(or pass any `#hex`)

### Icons

`eye · bolt · gear · bulb · dollar · search · mail · globe · building ·
rocket · code · plug · puzzle · swap · file · none`

## Requirements

`Pillow` and the Liberation Sans Bold font
(`/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf`).
