// Private administration project. Run in the Apps Script editor only.
// No web-app endpoint, no email sending, no student records embedded here.
function setupAssignmentForms() {
  const lock = LockService.getScriptLock(); lock.waitLock(10000);
  try {
    const props = PropertiesService.getScriptProperties();
    let destinationId = props.getProperty('responseSpreadsheetId');
    if (!destinationId) {
      const ss = SpreadsheetApp.create('North Star Summit 2026–27 — Assignment responses');
      destinationId = ss.getId(); props.setProperty('responseSpreadsheetId', destinationId);
      ss.getSheets()[0].setName('Form links').appendRow(['Assignment', 'Respondent URL', 'Editor URL', 'Status']);
    }
    const registry = SpreadsheetApp.openById(destinationId).getSheetByName('Form links');
    const result = {};
    ASSIGNMENTS.forEach((a,index) => {
      // A published native Form is managed in Google Forms, not recreated here.
      if (a.publishedUrl) {
        result[a.id] = a.publishedUrl;
        registry.getRange(index+2,1,1,4).setValues([[a.id,a.publishedUrl,'Managed in Google Forms','Already published — retain existing settings and response destination']]);
        return;
      }
      const key = 'form:' + a.id;
      let id = props.getProperty(key), form;
      if (!id) {
        form = FormApp.create('Summit 2026–27 · ' + a.id + ' · ' + a.title, false);
        id = form.getId(); props.setProperty(key, id);
      } else { form = FormApp.openById(id); }
      // Resume an interrupted setup only when the existing questions match this spec.
      const existing = form.getItems();
      existing.forEach((item,i)=>{if(!a.fields[i] || item.getTitle()!==a.fields[i].title)throw new Error('Review existing questions for '+a.id+' before rerunning.');});
      a.fields.slice(existing.length).forEach(field=>{
        const item = field.type==='paragraph'?form.addParagraphTextItem():form.addTextItem();
        item.setTitle(field.title).setRequired(field.required!==false);
        if(field.type==='email')item.setValidation(FormApp.createTextValidation().requireTextIsEmail().build());
        if(field.type==='url')item.setValidation(FormApp.createTextValidation().requireTextIsUrl().build());
      });
      const instructions = a.id==='questions' ? '\nSign in with your school Google account. Describe your question or tell us you are on track. Your answers are private to the course teaching team.' : '\nSign in with your school Google account. Enter your answers below; where requested, paste code and its result. A file link alone is not a submission. Keep your files restricted to you and your teachers. Submit again after revisions; the latest response is your current version.';
      form.setDescription(a.description+instructions);
      form.setCollectEmail(true).setLimitOneResponsePerUser(false).setAllowResponseEdits(false).setPublishingSummary(false).setShowLinkToRespondAgain(true);
      form.setConfirmationMessage('Your '+a.id+' answers have been submitted. Keep this confirmation as your receipt. Keep working in the same files; submit again after revisions.');
      // getDestinationId throws on a new Form that has no destination yet.
      let currentDestination = null; try { currentDestination = form.getDestinationId(); } catch (e) {}
      if(currentDestination!==destinationId){form.setDestination(FormApp.DestinationType.SPREADSHEET,destinationId);SpreadsheetApp.flush();}
      // A new destination can take a moment to register before Forms allows publishing.
      for (let attempt = 1; ; attempt++) {
        try {
          form = FormApp.openById(id);
          if(form.supportsAdvancedResponderPermissions())form.setPublished(true);else form.setAcceptingResponses(true);
          break;
        } catch (e) {
          if (attempt >= 4) throw e;
          console.log('Retrying publish for '+a.id+' after: '+e.message);
          Utilities.sleep(3000*attempt);
        }
      }
      if (form.getItems().length!==a.fields.length || !form.collectsEmail() || form.isPublishingSummary() || !form.isAcceptingResponses()) throw new Error('Form verification failed: '+a.id);
      console.log('CREATED '+JSON.stringify({id:a.id,editor:form.getEditUrl(),respondent:form.getPublishedUrl(),fields:form.getItems().length}));
      result[a.id]=form.getPublishedUrl();
      registry.getRange(index+2,1,1,4).setValues([[a.id,form.getPublishedUrl(),form.getEditUrl(),'Created — check responder access with a school account']]);
    });
    registry.setFrozenRows(1);registry.autoResizeColumns(1,4);
    console.log('FORM_LINKS='+JSON.stringify(result));
    console.log('TEACHER_RESPONSES=https://docs.google.com/spreadsheets/d/'+destinationId+'/edit');
  } finally {lock.releaseLock();}
}
