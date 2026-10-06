"""Check that everything the build needs is available and print fixes for what is missing."""
import importlib, os, shutil, subprocess, sys, json, warnings
warnings.filterwarnings("ignore")

ok = True
def need(cond, name, fix):
    global ok
    print(("  OK   " if cond else "  MISS ") + name + ("" if cond else f"   -> {fix}"))
    ok &= bool(cond)

print("Python modules")
for m, pip in [("pypdf", "pypdf"), ("pdfplumber", "pdfplumber"), ("PIL", "pillow"), ("yaml", "pyyaml")]:
    try:
        importlib.import_module(m); need(True, m, "")
    except ImportError:
        need(False, m, f"pip install {pip} (add --break-system-packages if pip refuses)")
print("Node & packages")
node = shutil.which("node")
need(node, "node", "install Node.js 18+")
if node:
    root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env = dict(os.environ, NODE_PATH=os.pathsep.join(filter(None, [os.environ.get("NODE_PATH"), root])))
    for pkg in ["docx", "playwright"]:
        r = subprocess.run([node, "-e", f"require('{pkg}')"], env=env, capture_output=True)
        need(r.returncode == 0, f"npm {pkg}", f"npm install -g {pkg}" + (" (Chromium: npx playwright install chromium)" if pkg == "playwright" else ""))
print("Tools")
need(shutil.which("pdftoppm"), "pdftoppm (poppler)", "apt-get install poppler-utils  — only needed for previews")
lo = shutil.which("soffice") or shutil.which("libreoffice")
print(("  OK   " if lo else "  OPT  ") + "LibreOffice" + ("" if lo else "   -> optional: without it the DOCX TOC has no cached page numbers (Word fills them on open)"))
print("\nREADY" if ok else "\nFix the MISS items above, then rerun.")
sys.exit(0 if ok else 1)
