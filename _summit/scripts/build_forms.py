"""Build a private, editor-run Forms setup script; never deploy it as the hub."""
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1];c=json.loads((r/'curriculum/course.json').read_text());spec=[]
for m in c['modules']:
 fields=[{'title':'Your name','type':'text'}]
 for i,q in enumerate(m['questions'],1):
  title=q+' Include your result and the Sheet formula you used.' if m['id']=='A01' and i<=6 else q
  fields.append({'title':title,'type':'paragraph'})
  if (m['id']=='A02' and i<=6) or (m['id']=='A03' and i==1) or (m['id']=='A04') or (m['id']=='A05' and i in [1,3]):
   fields.append({'title':f'Question {i}: paste the Python code you ran, then its output or result.','type':'paragraph'})
 if m['id']=='A03R':fields.append({'title':'Paste your complete 150–250 word letter to your teacher here (include subject and greeting).','type':'paragraph'})
 if m['workKind']:fields.append({'title':'Your Google Sheet link' if m['workKind']=='sheet' else 'Your Colab notebook link','type':'url'})
 if m['id']=='AI':fields += [{'title':'Link to your AI-assisted Doc, Sheet or notebook section','type':'url'},{'title':'Independent check 1: AI claim, your calculation and result','type':'paragraph'},{'title':'Independent check 2: AI claim, your calculation and result','type':'paragraph'}]
 if m['id']=='A06':fields.append({'title':'Your final Google Slides link','type':'url'})
 if m['id']=='A01':fields.append({'title':'Optional bonus work: explain your streak or VLOOKUP result','type':'paragraph','required':False})
 fields.append({'title':'What would you like help with? (Optional)','type':'paragraph','required':False})
 if m['id']!='welcome':fields.insert(1,{'title':'Submission stage: first attempt, final submission or revision','type':'text'})
 spec.append({'id':m['id'],'title':m['title'],'description':m['deliverable'],'fields':fields,'publishedUrl':m.get('submissionUrl')})
spec.append({'id':'questions','title':'Questions and weekly check-in','description':'Send questions about your current assignment, or say that you are on track. This is not your homework submission.','fields':[{'title':'Your name','type':'text'},{'title':'Assignment or topic','type':'text'},{'title':'What have you tried, and where are you stuck? Paste relevant code if helpful.','type':'paragraph'},{'title':'Your Sheet or Colab link (optional)','type':'url','required':False}]})
(r/'curriculum/forms.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
base=(r/'scripts/forms_setup.gs').read_text()
(r/'apps-script-admin/FormsSetup.gs').write_text('const ASSIGNMENTS = '+json.dumps(spec,ensure_ascii=False)+';\n'+base)
print('Built nine assignment Forms and one questions/check-in Form specification')
