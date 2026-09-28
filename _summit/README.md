# North Star Summit 2026–27

Public course source in the existing Hayward Data Science website repository.

- Course: https://www.haywarddatascience.com/summit2026_2027/
- Short address: https://www.haywarddatascience.com/summit/
- Title: North Star Summit — Data Science with Mr. Hayward

## Update the course

Edit `curriculum/course.json` for lessons, dates and public assignment Form links.
Edit `scripts/hub.html`, `scripts/hub.css` and `scripts/hub.js` for the website.
From this directory run:

```sh
python3 scripts/publish_site.py
python3 scripts/validate_public.py
```

Review the diff, then commit `_summit/`, `summit2026_2027/` and `summit/` to the website's master branch. The existing GitHub Pages build publishes them. No separate North Star remote repository is needed. The underscore source directory is excluded by the site's default Jekyll build, but everything committed here is visible in the public GitHub repository.

The public page uses no analytics or external JavaScript. Personal work shortcuts stay in the current browser. They are not a roster or verified submission record. On a shared computer, students should clear their saved shortcuts when finished.

## Private student work

Never commit names, school emails, assigned student file URLs, responses, grades, teacher answer keys or historical correspondence. There is no public student directory. Keep the roster and assignment responses in restricted Google Sheets. Share each personal Sheet and Colab only with its student, George and the two confirmed teachers. Deliver those two links privately; the student saves them in My work. Google account permissions protect the files.

`apps-script-admin/FormsSetup.gs` contains only the assignment questions and setup code, not responses. Run it in its separate owner-only Apps Script project, not as a public web app. Keep any populated enrollment configuration outside this repository. The original workspace retains private research and enrollment tools locally.

## Launch status

The course is ready for teacher review. Eight live meetings run October–mid-April, with nine sequential lessons. Dates and meeting times require school confirmation. The nine assignment Form URLs and a questions/check-in Form are not yet active; the page labels them unreleased. Google authorization, current-year enrollment, teacher access, school-account access checks and syncing the revised Colab master remain separate setup tasks. No student copies have been provisioned.

The earlier Apps Script hub remains an outdated secondary preview; website updates do not automatically update that deployment. Use the website address for sharing going forward.

## Data and teaching materials

The frozen CSV and starter notebook are in `curriculum/`. The notebook continues reading the pinned public dataset from `ghayward/hayward_public_data`; it is a separate existing data repository. The course uses browser-based Sheets and Colab, not downloads. Build a revised notebook with `python3 scripts/build_notebook.py` and sync it to the private Google master before creating student copies.

The syllabus source is `docs/syllabus-and-lesson-plans.md`. Form specifications are `curriculum/forms.json`; regenerate the setup script with `python3 scripts/build_forms.py` from this directory.

The editable Google syllabus is linked from `course.json`. After editing it, export and visually check `docs/syllabus.pdf`; the publish script copies it to the website.

2026–27 opening deck: new Google Slides copy saved in the business account, with the three historical student-profile slides and all speaker notes removed. Its view-sharing setting remains pending because native Chrome stopped responding. The hub links the checked clean PDF until Google viewer access is confirmed.
