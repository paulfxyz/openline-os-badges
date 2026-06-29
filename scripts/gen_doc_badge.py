"""Generate the Documentation badge in the section-badge family."""
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
}

p = make("section", PAL["fuchsia"], "book-marked", "Documentation",
         "badge-documentation.png", autowidth=True)
print(p)
