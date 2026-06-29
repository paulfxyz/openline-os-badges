"""Generate the Trash tab badge in the section-badge family."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import make

PAL = {"red": (153, 27, 27)}

p = make("section", PAL["red"], "trash-2", "Trash", "badge-arch-trash.png", autowidth=True)
print(p)
