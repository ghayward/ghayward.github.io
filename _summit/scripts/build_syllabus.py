"""Render the syllabus (HTML, Markdown and PDF) from curriculum/syllabus-table.json."""
from html import escape
from pathlib import Path
import json
import base64
import subprocess

R = Path(__file__).resolve().parents[1]
s = json.loads((R / 'curriculum/syllabus-table.json').read_text())
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SECTIONS = [('October to December 2026: Spreadsheets', 'fall'), ('January to April 2027: Python, Gemini and presentations', 'spring')]
LOGO = 'data:image/png;base64,' + base64.b64encode((R / 'assets/brand/north-star-academy.png').read_bytes()).decode()
NOTES = [('How to submit', 'submission'), ('Breaks', 'breaks'), ('Gemini', 'gemini'), ('Privacy', 'privacy')]


def table(rows):
    body = ''.join(f'<tr><td>{escape(a)}</td><td>{escape(b)}</td><td>{escape(c)}</td></tr>' for a, b, c in rows)
    return ('<table><thead><tr><th>Assignment or activity</th><th>Meeting</th><th>Due or feedback</th></tr></thead>'
            f'<tbody>{body}</tbody></table>')


def notes(pairs):
    return ''.join(f'<p><b>{escape(t)}:</b> {escape(s[k])}</p>' for t, k in pairs)


(fall_title, fall), (spring_title, spring) = SECTIONS
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>North Star Summit 2026-27 Syllabus</title><style>
@page {{ size: letter; margin: 0.6in 0.65in; }}
body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10pt; color: #1f2933; line-height: 1.4; }}
.logo {{ height: 30pt; display: block; margin: 0 0 12pt; }}
h1 {{ font-size: 18pt; margin: 0 0 2pt; color: #12355b; }}
.byline {{ color: #52606d; margin: 0 0 10pt; }}
h2 {{ font-size: 12.5pt; color: #12355b; margin: 16pt 0 6pt; break-after: avoid; }}
table {{ width: 100%; border-collapse: collapse; margin-bottom: 6pt; }}
th, td {{ border: 1px solid #cbd2d9; padding: 5pt 7pt; text-align: left; vertical-align: top; }}
th {{ background: #e8eef5; font-size: 9.5pt; }}
th:nth-child(2), td:nth-child(2) {{ width: 17%; white-space: nowrap; }}
th:nth-child(3), td:nth-child(3) {{ width: 23%; }}
tr {{ break-inside: avoid; }}
tbody tr:nth-child(even) td {{ background: #f7f9fb; }}
p {{ margin: 6pt 0; }}
a {{ color: #1d5fa8; }}
.spring {{ break-before: page; }}
</style></head><body>
<img class="logo" src="{LOGO}" alt="Uncommon Schools North Star">
<h1>North Star Summit 2026-27: Data Science</h1>
<p class="byline">Syllabus and schedule · Mr. Hayward · george@haywarddatascience.com<br>{escape(s['intro'])}</p>
<p>{escape(s['setup'])}</p>
<p><b>How it works:</b> {escape(s['rhythm'])}</p>
<h2>{escape(fall_title)}</h2>{table(s[fall])}
{notes(NOTES[:2])}
<h2 class="spring">{escape(spring_title)}</h2>{table(s[spring])}
{notes(NOTES[2:])}
<p><b>Course website:</b> <a href="https://www.haywarddatascience.com/summit">haywarddatascience.com/summit</a></p>
</body></html>'''
(R / 'docs/syllabus.html').write_text(html)

md = ['# North Star Summit 2026-27 syllabus', '', s['intro'], '', s['setup'], '', s['rhythm'], '']
for title, key in SECTIONS:
    md += ['', f'## {title}', '', '| Assignment or activity | Meeting | Due or feedback |', '|---|---|---|']
    md += [f'| {a} | {b} | {c} |' for a, b, c in s[key]]
for title, key in NOTES:
    md += ['', f'## {title}', '', s[key]]
(R / 'docs/syllabus-and-lesson-plans.md').write_text('\n'.join(md) + '\n')

subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                f'--print-to-pdf={R / "docs/syllabus.pdf"}', (R / 'docs/syllabus.html').as_uri()],
               check=True, capture_output=True)
print('Wrote docs/syllabus.html, docs/syllabus-and-lesson-plans.md and docs/syllabus.pdf')
