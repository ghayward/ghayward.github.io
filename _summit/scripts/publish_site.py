"""Build the public course in the surrounding ghayward.github.io checkout.

Run from website/_summit. This only stages files; it does not commit or push.
"""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT.parent
if ROOT.name != '_summit' or not (SITE / 'CNAME').is_file():
    raise SystemExit('Run the copy of this script in ghayward.github.io/_summit.')
subprocess.run([sys.executable, str(ROOT / 'scripts/build_hub.py')], check=True)
destination = SITE / 'summit2026_2027'
destination.mkdir(exist_ok=True)
(destination / 'assets').mkdir(exist_ok=True)
for filename in ['index.html', 'assets/north-star-academy.png']:
    shutil.copy2(ROOT / 'hub' / filename, destination / filename)
alias = SITE / 'summit'
alias.mkdir(exist_ok=True)
(alias / 'index.html').write_text('''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>North Star Summit — Data Science with Mr. Hayward</title>
<meta http-equiv="refresh" content="0; url=/summit2026_2027/">
<link rel="canonical" href="https://www.haywarddatascience.com/summit2026_2027/">
</head><body><p><a href="/summit2026_2027/">Open North Star Summit 2026–27</a></p></body></html>
''')
print('Prepared /summit2026_2027/ and /summit/ in the website checkout.')
