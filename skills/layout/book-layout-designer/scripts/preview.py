"""Render a PDF into contact sheets (JPG grids) for visual QA.

  python preview.py book.pdf outdir [--dpi 50] [--per 12] [--cols 4] [--pages 1-12]
Look at every sheet before delivering: split figures, orphaned callout labels,
near-empty pages, overflowing tables and clipped text are easy to spot here.
"""
import argparse, glob, os, subprocess, tempfile
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("pdf"); ap.add_argument("outdir")
ap.add_argument("--dpi", type=int, default=50); ap.add_argument("--per", type=int, default=12)
ap.add_argument("--cols", type=int, default=4); ap.add_argument("--pages")
a = ap.parse_args()
os.makedirs(a.outdir, exist_ok=True)
tmp = tempfile.mkdtemp()
cmd = ["pdftoppm", "-jpeg", "-r", str(a.dpi)]
if a.pages:
    f, l = a.pages.split("-")
    cmd += ["-f", f, "-l", l]
subprocess.run(cmd + [a.pdf, os.path.join(tmp, "p")], check=True)
files = sorted(glob.glob(os.path.join(tmp, "*.jpg")))
first = int(a.pages.split("-")[0]) if a.pages else 1
sheets = []
for s in range(0, len(files), a.per):
    ims = [Image.open(f) for f in files[s:s + a.per]]
    w, h = max(i.width for i in ims), max(i.height for i in ims)
    rows = (len(ims) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * (w + 10) + 10, rows * (h + 10) + 10), (120, 120, 120))
    for k, im in enumerate(ims):
        x, y = 10 + (k % a.cols) * (w + 10), 10 + (k // a.cols) * (h + 10)
        sheet.paste(im, (x, y))
        ImageDraw.Draw(sheet).text((x + 4, y + 2), str(first + s + k), fill=(220, 0, 0))
    out = os.path.join(a.outdir, f"sheet_{s // a.per + 1:02d}.jpg")
    sheet.save(out, quality=85)
    sheets.append(out)
print("\n".join(sheets))
