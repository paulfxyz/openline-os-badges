"""
Unified Openline OS image generator.
Produces a consistent family: solid rounded pill + clean Lucide icon (light tint
of fill) + bold white Lato Black label.

Types:
  mini    : 200x52  (nav grid badge)
  button  : 560x100 (nav button / hero banner)  -> label left, big
  section : 160x64  (small badge above an inline database)
  header  : custom black pill for "QUICK NAVIGATION GUIDE"

Usage: python gen.py  (reads SPEC list at bottom, writes to OUT dir)
"""
import cairosvg, io, os, re
from PIL import Image, ImageDraw, ImageFont

LUCIDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lucide")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out_images")
os.makedirs(OUT, exist_ok=True)
SS = 4
FONT_PATH = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"

# size presets: (W, H, radius, font_px, text_x, icon_cx, icon_cy, icon_px)
# COMPACT sizing: Notion renders standalone images at intrinsic pixel width,
# so smaller px = smaller on-page. Heroes ~360w, section badges ~120-130w.
PRESETS = {
    "mini":    (200, 52, 7, 14, 48, 25, 26, 18),
    "button":  (280, 50, 10, 16, 48, 26, 25, 22),
    "section": (96, 34, 7, 11, 30, 17, 17, 14),
}


def light_tint(rgb, f=0.72):
    return tuple(int(c + (255 - c) * f) for c in rgb)


def render_icon(icon_name, stroke_rgb, px):
    svg = open(os.path.join(LUCIDE, icon_name + ".svg")).read()
    hexcol = "#%02x%02x%02x" % stroke_rgb
    svg = svg.replace('stroke="currentColor"', f'stroke="{hexcol}"')
    if 'stroke="' not in svg:
        svg = svg.replace("<svg", f'<svg stroke="{hexcol}"', 1)
    svg = re.sub(r'stroke-width="[\d.]+"', 'stroke-width="2.25"', svg)
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=px, output_height=px)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def make(preset, fill, icon_name, label, outfile, autowidth=False, pad_right=18):
    label = label.upper()  # ALL-CAPS design system
    W, H, R, FPX, TX, ICX, ICY, IPX = PRESETS[preset]
    font = ImageFont.truetype(FONT_PATH, FPX)
    # Always ensure the pill is wide enough for the (uppercased) label so text
    # never overflows. autowidth lets it grow beyond the preset width.
    bb0 = font.getbbox(label)
    tw = bb0[2] - bb0[0]
    needed = TX + tw + pad_right
    if autowidth:
        W = max(W, needed)
    else:
        W = max(W, needed)
    base = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([0, 0, W * SS - 1, H * SS - 1], radius=R * SS, fill=fill + (255,))
    icon = render_icon(icon_name, light_tint(fill), IPX * SS)
    base.alpha_composite(icon, (ICX * SS - icon.width // 2, ICY * SS - icon.height // 2))
    badge = base.resize((W, H), Image.LANCZOS)
    dd = ImageDraw.Draw(badge)
    bb = font.getbbox(label)
    # vertically center text: cap height ~ (bb[3]-bb[1]); center on H/2
    text_h = bb[3] - bb[1]
    draw_y = (H - text_h) // 2 - bb[1]
    dd.text((TX, draw_y), label, font=font, fill=(255, 255, 255, 255))
    path = os.path.join(OUT, outfile)
    badge.save(path)
    return path


def make_header(label, outfile, fill=(26, 26, 26), icon_name="compass"):
    """Black quick-nav header pill, compass icon, 360x64."""
    label = label.upper()
    W, H, R, FPX = 360, 64, 12, 19
    font = ImageFont.truetype(FONT_PATH, FPX)
    bb0 = font.getbbox(label)
    W = max(W, 58 + (bb0[2] - bb0[0]) + 24)
    base = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([0, 0, W * SS - 1, H * SS - 1], radius=R * SS, fill=fill + (255,))
    icon = render_icon(icon_name, (236, 236, 236), 24 * SS)
    base.alpha_composite(icon, (34 * SS - icon.width // 2, 32 * SS - icon.height // 2))
    badge = base.resize((W, H), Image.LANCZOS)
    dd = ImageDraw.Draw(badge)
    bb = font.getbbox(label)
    th = bb[3] - bb[1]
    dd.text((58, (H - th) // 2 - bb[1]), label, font=font, fill=(255, 255, 255, 255))
    badge.save(os.path.join(OUT, outfile))
    return os.path.join(OUT, outfile)


COLORS = {
    "home": (247, 144, 9), "plan": (74, 26, 122), "develop": (184, 74, 16),
    "operate": (13, 92, 92), "grow": (122, 16, 16), "executive": (30, 46, 90),
    "production": (26, 92, 58), "team": (26, 92, 58), "guidebook": (122, 90, 16),
    "archives": (40, 54, 90),
}

if __name__ == "__main__":
    import sys
    print("generator ready; import and call make()/make_header()")
