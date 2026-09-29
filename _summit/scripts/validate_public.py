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
assert len(c['modules']) == 9 and len(c['workshops']) == 8
assert hashlib.sha256((R / 'curriculum/data/mr_hayward_weight.csv').read_bytes()).hexdigest() == 'cbb89a848420e48b757563b0c42871a96d76bf5922c3ac9c64b101238b3d1f13'
page = R.parent / 'summit2026_2027/index.html'
assert page.read_bytes() == (R / 'hub/index.html').read_bytes()
for forbidden in ['student-directory', 'Choose your name', 'COURSE.students', 'research/private', '/*APP*/', '/*CONFIG*/', 'download=']:
    assert forbidden not in page.read_text(), forbidden
assert (page.parent / 'assets/north-star-academy.png').read_bytes() == (R / 'assets/brand/north-star-academy.png').read_bytes()
assert 'url=/summit2026_2027/' in (R.parent / 'summit/index.html').read_text()
# Check all assignment, feedback, checkpoint and live dates against the school calendar.
from datetime import date
blocks=json.loads((R/'curriculum/calendar-constraints.json').read_text())['avoid']
for m in c['modules']:
    for key in ['live','questionsDue','due','feedbackDue']:
        value=m[key]
        assert not any(b['start']<=value<=b['end'] for b in blocks),(m['id'],key,value)
    for point in m.get('checkpoints',[]):
        assert not any(b['start']<=point['date']<=b['end'] for b in blocks), point
assert c['endDate']=='2027-04-15'
assert next(m for m in c['modules'] if m['id']=='A01')['due']=='2026-12-03'
assert next(m for m in c['modules'] if m['id']=='A02')['live']=='2027-01-14'
assert 'data-complete' not in page.read_text()
assert (page.parent/'syllabus.pdf').read_bytes()==(R/'docs/syllabus.pdf').read_bytes()
assert c['links']['syllabusDoc'] and c['links']['syllabusDoc'] in page.read_text()
forms=json.loads((R/'curriculum/forms.json').read_text())
assert {f['id'] for f in forms}=={m['id'] for m in c['modules']}|{'questions'}
for f in forms:
    if f['id'] in ['A02','A03','A04','A05']:
        # Require code for calculations/charts; prose explanations get their own answer field.
        expected_code_fields={'A02':6,'A03':1,'A04':3,'A05':2}
        assert len([q for q in f['fields'] if 'paste the Python code' in q['title']])==expected_code_fields[f['id']]
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
print('PASS: nine lessons, eight workshops, pinned data, exact published assets, short-link target, no public directory, and roster rejection.')
