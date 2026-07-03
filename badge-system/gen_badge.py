#!/usr/bin/env python3
"""
Openline OS — Badge Generator (sustainable, reusable)
-----------------------------------------------------
Renders flat "pill" badges that match the existing os-nav badge style:
  - rounded-pill shape, solid fill
  - small white line-icon on the left
  - bold white UPPERCASE text with letter-spacing
  - 34px tall (rendered at 3x then downsampled for crisp edges)

Usage:
  python3 gen_badge.py <label> <slug> [color] [icon]

  color: hex like #312E81  OR a named palette key (navy, gold, purple,
         emerald, cyan, violet, slate, rose, teal, orange)
  icon : a glyph name from ICONS (see below) or 'none'

Examples:
  python3 gen_badge.py "Read & Last Activity" badge-read-last-activity navy eye
  python3 gen_badge.py "Quick Actions" badge-quick-actions violet bolt

Batch: import build_badge() and call it in a loop (see gen_all.py).
"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
S = 3                      # supersample factor
H = 34                     # final height in px
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Palette sampled from the existing badges
PALETTE = {
    "navy":    "#312E81",  # indigo-900  (Executive / strategic)
    "gold":    "#B47809",  # amber-700   (tips / prod / why-this-exists)
    "purple":  "#86198F",  # fuchsia-800 (badge-system)
    "emerald": "#047857",  # emerald-700 (golden rule)
    "cyan":    "#0E7490",  # cyan-700    (ai agent)
    "violet":  "#6D28D9",  # violet-700  (how-it-works)
    "slate":   "#334155",
    "rose":    "#9F1239",
    "teal":    "#0F766E",
    "orange":  "#C2410C",
    "blue":    "#1D4ED8",
    "pink":    "#BE185D",
    # --- extended palette (deep, saturated, white-text safe) ---
    "red":       "#B91C1C",  # red-700
    "crimson":   "#9F1239",  # rose-800
    "maroon":    "#7F1D1D",  # red-900
    "amber":     "#B45309",  # amber-700
    "bronze":    "#92400E",  # amber-800
    "olive":     "#4D7C0F",  # lime-700
    "green":     "#15803D",  # green-700
    "forest":    "#166534",  # green-800
    "jade":      "#059669",  # emerald-600
    "turquoise": "#0D9488",  # teal-600
    "sky":       "#0369A1",  # sky-700
    "azure":     "#0284C7",  # sky-600
    "cobalt":    "#1E40AF",  # blue-800
    "indigo":    "#4338CA",  # indigo-700
    "iris":      "#4F46E5",  # indigo-600
    "grape":     "#7E22CE",  # purple-700
    "plum":      "#6B21A8",  # purple-800
    "magenta":   "#A21CAF",  # fuchsia-700
    "fuchsia":   "#C026D3",  # fuchsia-600
    "raspberry": "#BE123C",  # rose-700
    "coral":     "#EA580C",  # orange-600
    "rust":      "#9A3412",  # orange-800
    "charcoal":  "#1F2937",  # gray-800
    "steel":     "#475569",  # slate-600
    "gunmetal":  "#0F172A",  # slate-900
}

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ---- Minimal white line-icons drawn with primitives (scale-aware) ----
# Each fn draws into `d` inside a box (x0,y0,x1,y1) using stroke width lw.
def _eye(d, b, lw, col):
    x0,y0,x1,y1 = b; cx=(x0+x1)/2; cy=(y0+y1)/2; rw=(x1-x0)/2; rh=(y1-y0)/2.6
    # almond shape via two arcs -> approximate with ellipse outline
    d.ellipse([cx-rw, cy-rh, cx+rw, cy+rh], outline=col, width=lw)
    d.ellipse([cx-rh*0.6, cy-rh*0.6, cx+rh*0.6, cy+rh*0.6], fill=col)

def _bolt(d, b, lw, col):
    x0,y0,x1,y1 = b; w=x1-x0; h=y1-y0
    pts=[(x0+w*0.55,y0),(x0+w*0.15,y0+h*0.58),(x0+w*0.45,y0+h*0.58),
         (x0+w*0.35,y1),(x0+w*0.9,y0+h*0.4),(x0+w*0.55,y0+h*0.4)]
    d.polygon(pts, fill=col)

def _gear(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; cy=(y0+y1)/2; R=min(x1-x0,y1-y0)/2
    for i in range(8):
        a=math.radians(i*45)
        d.line([cx+math.cos(a)*R*0.55, cy+math.sin(a)*R*0.55,
                cx+math.cos(a)*R, cy+math.sin(a)*R], fill=col, width=lw)
    d.ellipse([cx-R*0.6,cy-R*0.6,cx+R*0.6,cy+R*0.6], outline=col, width=lw)

def _bulb(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; w=x1-x0; h=y1-y0
    d.ellipse([cx-w*0.35, y0, cx+w*0.35, y0+h*0.7], outline=col, width=lw)
    d.line([cx-w*0.18, y0+h*0.8, cx+w*0.18, y0+h*0.8], fill=col, width=lw)
    d.line([cx-w*0.13, y1, cx+w*0.13, y1], fill=col, width=lw)

def _dollar(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2
    fnt=ImageFont.truetype(FONT_PATH, int((y1-y0)*1.15))
    d.text((cx, (y0+y1)/2), "$", font=fnt, fill=col, anchor="mm")

def _search(d, b, lw, col):
    x0,y0,x1,y1=b; r=(x1-x0)*0.34
    d.ellipse([x0, y0, x0+2*r, y0+2*r], outline=col, width=lw)
    d.line([x0+2*r*0.78, y0+2*r*0.78, x1, y1], fill=col, width=int(lw*1.2))

def _mail(d, b, lw, col):
    x0,y0,x1,y1=b
    d.rectangle([x0,y0,x1,y1], outline=col, width=lw)
    d.line([x0,y0,(x0+x1)/2,(y0+y1)/2], fill=col, width=lw)
    d.line([x1,y0,(x0+x1)/2,(y0+y1)/2], fill=col, width=lw)

def _globe(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; cy=(y0+y1)/2
    d.ellipse([x0,y0,x1,y1], outline=col, width=lw)
    d.ellipse([cx-(x1-x0)*0.22,y0,cx+(x1-x0)*0.22,y1], outline=col, width=lw)
    d.line([x0,cy,x1,cy], fill=col, width=lw)

def _building(d, b, lw, col):
    x0,y0,x1,y1=b
    d.rectangle([x0,y0,x1,y1], outline=col, width=lw)
    for fy in (0.28,0.55,0.82):
        for fx in (0.28,0.62):
            yy=y0+(y1-y0)*fy; xx=x0+(x1-x0)*fx
            d.rectangle([xx-1.4*lw,yy-1.4*lw,xx+1.4*lw,yy+1.4*lw], fill=col)

def _rocket(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; w=x1-x0; h=y1-y0
    d.polygon([(cx,y0),(cx+w*0.3,y0+h*0.6),(cx-w*0.3,y0+h*0.6)], outline=col, width=lw)
    d.ellipse([cx-w*0.1,y0+h*0.25,cx+w*0.1,y0+h*0.45], fill=col)
    d.line([cx-w*0.18,y0+h*0.6,cx-w*0.3,y1], fill=col, width=lw)
    d.line([cx+w*0.18,y0+h*0.6,cx+w*0.3,y1], fill=col, width=lw)

def _code(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; cy=(y0+y1)/2
    d.line([(x0+ (x1-x0)*0.32,y0),(x0,cy),(x0+(x1-x0)*0.32,y1)], fill=col, width=lw, joint="curve")
    d.line([(x1-(x1-x0)*0.32,y0),(x1,cy),(x1-(x1-x0)*0.32,y1)], fill=col, width=lw, joint="curve")

def _plug(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2
    d.rectangle([cx-(x1-x0)*0.28,y0+ (y1-y0)*0.25,cx+(x1-x0)*0.28,y1-(y1-y0)*0.15], outline=col, width=lw)
    d.line([cx-(x1-x0)*0.12,y0,cx-(x1-x0)*0.12,y0+(y1-y0)*0.25], fill=col, width=lw)
    d.line([cx+(x1-x0)*0.12,y0,cx+(x1-x0)*0.12,y0+(y1-y0)*0.25], fill=col, width=lw)

def _puzzle(d, b, lw, col):
    x0,y0,x1,y1=b
    d.rectangle([x0,y0+(y1-y0)*0.15,x1,y1], outline=col, width=lw)
    d.ellipse([(x0+x1)/2-(x1-x0)*0.16,y0,(x0+x1)/2+(x1-x0)*0.16,y0+(y1-y0)*0.3], fill=col)

def _swap(d, b, lw, col):  # price comparison / swap arrows
    x0,y0,x1,y1=b; cy=(y0+y1)/2
    d.line([x0,y0+(y1-y0)*0.32,x1,y0+(y1-y0)*0.32], fill=col, width=lw)
    d.line([x1,y0+(y1-y0)*0.32,x1-(x1-x0)*0.25,y0], fill=col, width=lw)
    d.line([x1,y1-(y1-y0)*0.32,x0,y1-(y1-y0)*0.32], fill=col, width=lw)
    d.line([x0,y1-(y1-y0)*0.32,x0+(x1-x0)*0.25,y1], fill=col, width=lw)

def _file(d, b, lw, col):
    x0,y0,x1,y1=b
    d.polygon([(x0,y0),(x1-(x1-x0)*0.3,y0),(x1,y0+(y1-y0)*0.3),(x1,y1),(x0,y1)], outline=col, width=lw)
    for fy in (0.5,0.68,0.86):
        d.line([x0+(x1-x0)*0.2,y0+(y1-y0)*fy,x1-(x1-x0)*0.2,y0+(y1-y0)*fy], fill=col, width=max(1,int(lw*0.8)))

def _chart(d, b, lw, col):
    x0,y0,x1,y1=b
    d.line([x0,y0,x0,y1,x1,y1], fill=col, width=lw, joint="curve")
    bw=(x1-x0)/4.5
    for i,hf in enumerate((0.35,0.6,0.85)):
        bx=x0+(x1-x0)*0.18+i*bw*1.25
        d.rectangle([bx,y1-(y1-y0)*hf,bx+bw,y1], fill=col)

def _folder(d, b, lw, col):
    x0,y0,x1,y1=b
    d.polygon([(x0,y0+(y1-y0)*0.22),(x0+(x1-x0)*0.4,y0+(y1-y0)*0.22),
               (x0+(x1-x0)*0.52,y0),(x1,y0),(x1,y1),(x0,y1)], outline=col, width=lw)

def _users(d, b, lw, col):
    x0,y0,x1,y1=b; w=x1-x0; h=y1-y0
    d.ellipse([x0+w*0.05,y0,x0+w*0.45,y0+h*0.42], outline=col, width=lw)
    d.arc([x0+w*0.0,y0+h*0.5,x0+w*0.5,y1+h*0.5], 180,360, fill=col, width=lw)
    d.ellipse([x0+w*0.5,y0+h*0.08,x0+w*0.88,y0+h*0.46], outline=col, width=lw)
    d.arc([x0+w*0.45,y0+h*0.55,x0+w*0.95,y1+h*0.5], 180,360, fill=col, width=lw)

def _calendar(d, b, lw, col):
    x0,y0,x1,y1=b
    d.rectangle([x0,y0+(y1-y0)*0.16,x1,y1], outline=col, width=lw)
    d.line([x0,y0+(y1-y0)*0.38,x1,y0+(y1-y0)*0.38], fill=col, width=lw)
    d.line([x0+(x1-x0)*0.28,y0,x0+(x1-x0)*0.28,y0+(y1-y0)*0.28], fill=col, width=lw)
    d.line([x0+(x1-x0)*0.72,y0,x0+(x1-x0)*0.72,y0+(y1-y0)*0.28], fill=col, width=lw)

def _check(d, b, lw, col):
    x0,y0,x1,y1=b
    d.line([(x0+(x1-x0)*0.12,y0+(y1-y0)*0.55),(x0+(x1-x0)*0.4,y1),
            (x1,y0+(y1-y0)*0.12)], fill=col, width=int(lw*1.3), joint="curve")

def _check_circle(d, b, lw, col):
    x0,y0,x1,y1=b
    d.ellipse([x0,y0,x1,y1], outline=col, width=lw)
    d.line([(x0+(x1-x0)*0.28,(y0+y1)/2+(y1-y0)*0.02),(x0+(x1-x0)*0.44,y0+(y1-y0)*0.68),
            (x0+(x1-x0)*0.74,y0+(y1-y0)*0.32)], fill=col, width=lw, joint="curve")

def _tag(d, b, lw, col):
    x0,y0,x1,y1=b
    d.polygon([(x0,y0),(x0+(x1-x0)*0.55,y0),(x1,(y0+y1)/2),(x0+(x1-x0)*0.55,y1),(x0,y1)], outline=col, width=lw)
    d.ellipse([x0+(x1-x0)*0.14,(y0+y1)/2-(x1-x0)*0.09,x0+(x1-x0)*0.32,(y0+y1)/2+(x1-x0)*0.09], fill=col)

def _shield(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2
    d.polygon([(cx,y0),(x1,y0+(y1-y0)*0.22),(x1,y0+(y1-y0)*0.55),(cx,y1),
               (x0,y0+(y1-y0)*0.55),(x0,y0+(y1-y0)*0.22)], outline=col, width=lw)

def _star(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; cy=(y0+y1)/2; R=min(x1-x0,y1-y0)/2
    pts=[]
    for i in range(10):
        a=math.radians(-90+i*36); r=R if i%2==0 else R*0.42
        pts.append((cx+math.cos(a)*r, cy+math.sin(a)*r))
    d.polygon(pts, fill=col)

def _clock(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; cy=(y0+y1)/2
    d.ellipse([x0,y0,x1,y1], outline=col, width=lw)
    d.line([cx,cy,cx,y0+(y1-y0)*0.28], fill=col, width=lw)
    d.line([cx,cy,x0+(x1-x0)*0.72,cy], fill=col, width=lw)

def _link(d, b, lw, col):
    x0,y0,x1,y1=b; cy=(y0+y1)/2
    d.arc([x0,y0+(y1-y0)*0.18,x0+(x1-x0)*0.6,y1-(y1-y0)*0.18],90,270,fill=col,width=lw)
    d.arc([x1-(x1-x0)*0.6,y0+(y1-y0)*0.18,x1,y1-(y1-y0)*0.18],270,90,fill=col,width=lw)
    d.line([x0+(x1-x0)*0.32,cy,x1-(x1-x0)*0.32,cy], fill=col, width=lw)

def _layers(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; w=x1-x0
    def dia(yc):
        d.polygon([(cx,yc-(y1-y0)*0.13),(x1,yc),(cx,yc+(y1-y0)*0.13),(x0,yc)], outline=col, width=lw)
    dia(y0+(y1-y0)*0.22); dia((y0+y1)/2); dia(y1-(y1-y0)*0.22)

def _database(d, b, lw, col):
    x0,y0,x1,y1=b
    d.ellipse([x0,y0,x1,y0+(y1-y0)*0.28], outline=col, width=lw)
    d.line([x0,y0+(y1-y0)*0.14,x0,y1-(y1-y0)*0.14], fill=col, width=lw)
    d.line([x1,y0+(y1-y0)*0.14,x1,y1-(y1-y0)*0.14], fill=col, width=lw)
    d.arc([x0,y1-(y1-y0)*0.28,x1,y1],0,180,fill=col,width=lw)
    d.arc([x0,y0+(y1-y0)*0.22,x1,y0+(y1-y0)*0.5],0,180,fill=col,width=lw)

def _server(d, b, lw, col):
    x0,y0,x1,y1=b
    for fy in (0.0,0.55):
        d.rectangle([x0,y0+(y1-y0)*fy,x1,y0+(y1-y0)*(fy+0.4)], outline=col, width=lw)
        d.ellipse([x0+(x1-x0)*0.72,y0+(y1-y0)*(fy+0.14),x0+(x1-x0)*0.82,y0+(y1-y0)*(fy+0.26)], fill=col)

def _book(d, b, lw, col):
    # clean closed book: cover rectangle + spine line + a couple page lines
    x0,y0,x1,y1=b
    d.rectangle([x0,y0,x1,y1], outline=col, width=lw)
    d.line([x0+(x1-x0)*0.26,y0,x0+(x1-x0)*0.26,y1], fill=col, width=lw)
    for fy in (0.35,0.6):
        d.line([x0+(x1-x0)*0.42,y0+(y1-y0)*fy,x1-(x1-x0)*0.12,y0+(y1-y0)*fy], fill=col, width=max(1,int(lw*0.85)))

def _flag(d, b, lw, col):
    x0,y0,x1,y1=b
    d.line([x0,y0,x0,y1], fill=col, width=lw)
    d.polygon([(x0,y0),(x1,y0+(y1-y0)*0.14),(x0,y0+(y1-y0)*0.5)], outline=col, width=lw)

def _bell(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2
    d.arc([x0,y0,x1,y1+(y1-y0)*0.6],180,360,fill=col,width=lw)
    d.line([x0,y1-(y1-y0)*0.28,x1,y1-(y1-y0)*0.28], fill=col, width=lw)
    d.ellipse([cx-(x1-x0)*0.08,y1-(y1-y0)*0.16,cx+(x1-x0)*0.08,y1], fill=col)

def _target(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; cy=(y0+y1)/2
    d.ellipse([x0,y0,x1,y1], outline=col, width=lw)
    d.ellipse([x0+(x1-x0)*0.28,y0+(y1-y0)*0.28,x1-(x1-x0)*0.28,y1-(y1-y0)*0.28], outline=col, width=lw)
    d.ellipse([cx-(x1-x0)*0.08,cy-(y1-y0)*0.08,cx+(x1-x0)*0.08,cy+(y1-y0)*0.08], fill=col)

def _wrench(d, b, lw, col):
    x0,y0,x1,y1=b
    d.ellipse([x0,y0,x0+(x1-x0)*0.42,y0+(y1-y0)*0.42], outline=col, width=lw)
    d.line([x0+(x1-x0)*0.34,y0+(y1-y0)*0.34,x1,y1], fill=col, width=int(lw*1.4))

def _home(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2
    d.polygon([(cx,y0),(x1,y0+(y1-y0)*0.45),(x0,y0+(y1-y0)*0.45)], outline=col, width=lw)
    d.rectangle([x0+(x1-x0)*0.16,y0+(y1-y0)*0.45,x1-(x1-x0)*0.16,y1], outline=col, width=lw)

def _cloud(d, b, lw, col):
    x0,y0,x1,y1=b
    d.arc([x0,y0+(y1-y0)*0.2,x0+(x1-x0)*0.55,y1],90,360,fill=col,width=lw)
    d.arc([x0+(x1-x0)*0.35,y0,x1,y1-(y1-y0)*0.1],180,360,fill=col,width=lw)
    d.line([x0+(x1-x0)*0.18,y1,x1-(x1-x0)*0.1,y1], fill=col, width=lw)

def _trash(d, b, lw, col):
    x0,y0,x1,y1=b
    d.line([x0,y0+(y1-y0)*0.16,x1,y0+(y1-y0)*0.16], fill=col, width=lw)
    d.rectangle([x0+(x1-x0)*0.14,y0+(y1-y0)*0.16,x1-(x1-x0)*0.14,y1], outline=col, width=lw)
    d.rectangle([x0+(x1-x0)*0.36,y0,x1-(x1-x0)*0.36,y0+(y1-y0)*0.16], outline=col, width=lw)
    for fx in (0.36,0.5,0.64):
        d.line([x0+(x1-x0)*fx,y0+(y1-y0)*0.3,x0+(x1-x0)*fx,y1-(y1-y0)*0.12], fill=col, width=max(1,int(lw*0.8)))

def _archive(d, b, lw, col):
    x0,y0,x1,y1=b
    d.rectangle([x0,y0,x1,y0+(y1-y0)*0.3], outline=col, width=lw)
    d.rectangle([x0+(x1-x0)*0.06,y0+(y1-y0)*0.3,x1-(x1-x0)*0.06,y1], outline=col, width=lw)
    d.line([x0+(x1-x0)*0.35,y0+(y1-y0)*0.55,x0+(x1-x0)*0.65,y0+(y1-y0)*0.55], fill=col, width=lw)

def _refresh(d, b, lw, col):
    x0,y0,x1,y1=b
    d.arc([x0,y0,x1,y1],40,320,fill=col,width=lw)
    d.polygon([(x1-(x1-x0)*0.1,y0),(x1,y0+(y1-y0)*0.28),(x1-(x1-x0)*0.32,y0+(y1-y0)*0.22)], fill=col)

def _handshake(d, b, lw, col):
    # two interlocking chevrons meeting in the middle = clasped hands, reads clean
    x0,y0,x1,y1=b; cx=(x0+x1)/2; cy=(y0+y1)/2
    d.line([(x0,y0+(y1-y0)*0.3),(cx,cy),(x0,y1-(y1-y0)*0.3)], fill=col, width=lw, joint="curve")
    d.line([(x1,y0+(y1-y0)*0.3),(cx,cy),(x1,y1-(y1-y0)*0.3)], fill=col, width=lw, joint="curve")
    d.ellipse([cx-lw,cy-lw,cx+lw,cy+lw], fill=col)

def _play(d, b, lw, col):
    x0,y0,x1,y1=b
    d.ellipse([x0,y0,x1,y1], outline=col, width=lw)
    d.polygon([(x0+(x1-x0)*0.4,y0+(y1-y0)*0.3),(x0+(x1-x0)*0.4,y1-(y1-y0)*0.3),
               (x1-(x1-x0)*0.3,(y0+y1)/2)], fill=col)

def _list(d, b, lw, col):
    x0,y0,x1,y1=b
    for fy in (0.12,0.5,0.88):
        yy=y0+(y1-y0)*fy
        d.ellipse([x0,yy-(y1-y0)*0.07,x0+(y1-y0)*0.14,yy+(y1-y0)*0.07], fill=col)
        d.line([x0+(x1-x0)*0.28,yy,x1,yy], fill=col, width=lw)

def _compass(d, b, lw, col):
    x0,y0,x1,y1=b; cx=(x0+x1)/2; cy=(y0+y1)/2
    d.ellipse([x0,y0,x1,y1], outline=col, width=lw)
    d.polygon([(cx,cy),(x0+(x1-x0)*0.66,y0+(y1-y0)*0.34),(cx,cy)], outline=col, width=lw)
    d.polygon([(cx,cy),(cx-(x1-x0)*0.06,cy-(y1-y0)*0.06),(x0+(x1-x0)*0.66,y0+(y1-y0)*0.34),(cx+(x1-x0)*0.06,cy+(y1-y0)*0.06)], fill=col)

ICONS = {
    "eye": _eye, "bolt": _bolt, "gear": _gear, "bulb": _bulb, "dollar": _dollar,
    "search": _search, "mail": _mail, "globe": _globe, "building": _building,
    "rocket": _rocket, "code": _code, "plug": _plug, "puzzle": _puzzle,
    "swap": _swap, "file": _file,
    # extended set
    "chart": _chart, "folder": _folder, "users": _users, "calendar": _calendar,
    "check": _check, "check_circle": _check_circle, "tag": _tag, "shield": _shield,
    "star": _star, "clock": _clock, "link": _link, "layers": _layers,
    "database": _database, "server": _server, "book": _book, "flag": _flag,
    "bell": _bell, "target": _target, "wrench": _wrench, "home": _home,
    "cloud": _cloud, "trash": _trash, "archive": _archive, "refresh": _refresh,
    "handshake": _handshake, "play": _play, "list": _list, "compass": _compass,
}

def build_badge(label, slug, color="navy", icon="none", out_dir=OUT_DIR):
    fill = PALETTE.get(color, color)
    rgb = hex2rgb(fill)
    text = label.upper()

    h = H * S
    pad_x = 11 * S
    icon_box = 12 * S
    icon_gap = 6 * S
    tracking = 0.4 * S           # letter-spacing
    radius = 6 * S            # gentle rounded-rectangle corners (was h/2 full pill)

    font_size = 12 * S
    font = ImageFont.truetype(FONT_PATH, font_size)

    # measure text width with tracking
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)
    def text_w(s):
        w = 0
        for ch in s:
            bb = td.textbbox((0, 0), ch, font=font)
            w += (bb[2] - bb[0]) + tracking
        return w - tracking if s else 0
    tw = text_w(text)
    ascent, descent = font.getmetrics()

    has_icon = icon in ICONS
    left = pad_x
    content_w = (icon_box + icon_gap if has_icon else 0) + tw
    w = int(left * 2 + content_w)

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=rgb + (255,))

    cx = left
    if has_icon:
        iy0 = (h - icon_box) / 2
        ICONS[icon](d, (cx, iy0, cx + icon_box, iy0 + icon_box), max(2, int(2.0 * S)), (255, 255, 255, 255))
        cx += icon_box + icon_gap

    # draw text with tracking, vertically centered
    ty = (h - (ascent + descent)) / 2
    for ch in text:
        d.text((cx, ty), ch, font=font, fill=(255, 255, 255, 255))
        bb = td.textbbox((0, 0), ch, font=font)
        cx += (bb[2] - bb[0]) + tracking

    final = img.resize((round(w / S), H), Image.LANCZOS)
    path = os.path.join(out_dir, slug + ".png")
    final.save(path)
    return path, final.size

if __name__ == "__main__":
    label = sys.argv[1]
    slug = sys.argv[2]
    color = sys.argv[3] if len(sys.argv) > 3 else "navy"
    icon = sys.argv[4] if len(sys.argv) > 4 else "none"
    p, sz = build_badge(label, slug, color, icon)
    print("wrote", p, sz)
