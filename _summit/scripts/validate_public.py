"""Check the public publication boundary and course artifacts before a push."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

R = Path(__file__).resolve().parents[1]
c = json.loads((R / 'curriculum/course.json').read_text())
assert 'students' not in c and 'roster' not in c
assert len(c['modules']) == 9 and len(c['workshops']) == 7
assert hashlib.sha256((R / 'curriculum/data/mr_hayward_weight.csv').read_bytes()).hexdigest() == 'cbb89a848420e48b757563b0c42871a96d76bf5922c3ac9c64b101238b3d1f13'
page = R.parent / 'summit2026_2027/index.html'
assert page.read_bytes() == (R / 'hub/index.html').read_bytes()
for forbidden in ['student-directory', 'Choose your name', 'COURSE.students', 'research/private', '/*APP*/', '/*CONFIG*/', 'download=']:
    assert forbidden not in page.read_text(), forbidden
assert (page.parent / 'assets/north-star-academy.png').read_bytes() == (R / 'assets/brand/north-star-academy.png').read_bytes()
assert 'url=/summit2026_2027/' in (R.parent / 'summit/index.html').read_text()
# A future accidental roster must fail before any generated files can be written.
with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    (root / 'scripts').mkdir()
    (root / 'curriculum').mkdir()
    (root / 'scripts/build_hub.py').write_bytes((R / 'scripts/build_hub.py').read_bytes())
    (root / 'curriculum/course.json').write_text(json.dumps({**c, 'students': [{'displayName': 'PRIVACY_TEST_CANARY'}]}))
    result = subprocess.run([sys.executable, str(root / 'scripts/build_hub.py')], capture_output=True, text=True)
    assert result.returncode != 0 and 'Keep the roster' in result.stderr
    assert not (root / 'hub').exists()
print('PASS: nine lessons, seven workshops, pinned data, exact published assets, short-link target, no public directory, and roster rejection.')
