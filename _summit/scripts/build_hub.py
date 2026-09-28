"""Build both delivery formats from the same course and UI sources."""
from pathlib import Path
import json, shutil, base64, csv
R=Path(__file__).resolve().parents[1]
c=json.loads((R/'curriculum/course.json').read_text())
# This configuration is shipped to every visitor. Never store a roster here.
if 'students' in c or 'roster' in c:
 raise ValueError('Keep the roster and assigned student file links in private Google Drive, not course.json.')
with (R/'curriculum/schedule.csv').open('w',newline='') as f:
 writer=csv.writer(f,lineterminator="\n");writer.writerow(['Assignment','Live date tentative','Due date tentative','Topic','Deliverable'])
 for m in c['modules']:writer.writerow([m['id'],m['live'],m['due'] or '',m['title'],m['deliverable']])
rows=list(csv.DictReader((R/'curriculum/data/mr_hayward_weight.csv').open()))
data={'count':len(rows),'columns':list(rows[0]),'preview':rows[:6]}
style=(R/'scripts/hub.css').read_text();js=(R/'scripts/hub.js').read_text();template=(R/'scripts/hub.html').read_text()
logo=R/'assets/brand/north-star-academy.png'
def build(embedded):
 config='window.COURSE='+json.dumps(c,ensure_ascii=False)+';window.DATA='+json.dumps(data)+';'
 logo_url='data:image/png;base64,'+base64.b64encode(logo.read_bytes()).decode() if embedded else 'assets/north-star-academy.png'
 return template.replace('BRAND_LOGO',logo_url).replace('/*STYLE*/',style).replace('/*CONFIG*/',config.replace('</','<\\/')).replace('/*APP*/',js)
(R/'hub/assets').mkdir(parents=True,exist_ok=True)
shutil.copy2(logo,R/'hub/assets/north-star-academy.png')
# Student work lives in Google. The source CSV and notebook stay in curriculum/.
for name in ('summit-2026-27.ipynb','mr_hayward_weight.csv'):
 (R/'hub/downloads'/name).unlink(missing_ok=True)
(R/'hub/index.html').write_text(build(False))
(R/'apps-script').mkdir(exist_ok=True)
(R/'apps-script/Index.html').write_text(build(True))
(R/'apps-script/Code.gs').write_text('function doGet() {\n  return HtmlService.createHtmlOutputFromFile("Index")\n    .setTitle("North Star Summit — Data Science with Mr. Hayward")\n    .addMetaTag("viewport", "width=device-width, initial-scale=1");\n}\n')
(R/'apps-script/appsscript.json').write_text(json.dumps({'timeZone':'America/New_York','runtimeVersion':'V8','exceptionLogging':'STACKDRIVER','oauthScopes':[]},indent=2))
print('Built static hub and self-contained Apps Script package')
