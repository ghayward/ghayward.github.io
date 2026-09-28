from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
cells=[]
def md(s):cells.append(dict(cell_type='markdown',metadata={},source=s.splitlines(True)))
def code(s):cells.append(dict(cell_type='code',metadata={},execution_count=None,outputs=[],source=s.splitlines(True)))
md('''# North Star Summit 2026–27
## Your data science notebook
Use **File → Save a copy in Drive** once, unless your teacher has already assigned you a personal notebook. Rename your copy `Summit 2026-27 - Your Name`. Keep this same copy all year and save its link in the hub’s **My work** section.

Work in the assignment sections below. Run cells from the top after reconnecting. Keep your code, outputs and explanation together. Submit the link through **the answer Form for each assignment** in the class hub. Sharing the link does not automatically grant access: confirm your teachers can open your copy.

You may use documentation, classmates and AI to learn. Explain your own code, check the output, and note help you received.

The dataset is Mr. Hayward's already-published teaching dataset. No student weight or other personal measurements are requested.
''')
md('## Setup\nRun the next cell to load the teaching data directly from GitHub. You do not need to download a file. The pinned URL keeps this year’s exercises reproducible. If your school blocks this connection, ask your teacher for help. The same data is already in your Google Sheet’s Data tab.')
code('''import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

DATA_URL = "https://raw.githubusercontent.com/ghayward/hayward_public_data/e2443fa8eb4b91f526657deeceedf5ce81616327/data/mr_hayward_weight.csv"
df = pd.read_csv(DATA_URL)
df["date"] = pd.to_datetime(df["date"], errors="raise")
df = df.sort_values("date").reset_index(drop=True)
assert len(df) == 2001, "Check that you loaded the course dataset."
assert pd.api.types.is_bool_dtype(df["is_weekend"])
assert pd.api.types.is_bool_dtype(df["is_holiday"])
df.head()
''')
code('print("Observations:", len(df))\nprint("Columns:", list(df.columns))\n')
md('''## A01 Start with a spreadsheet
Open your personal Google Sheet from the hub’s My work section. Its Data tab already contains the dataset. Use formulas referencing that tab to calculate count, median, mean, minimum, maximum and weekend average. Add your Sheet link below. You will start Python after finishing the spreadsheet phase.

**My Sheet link:**

**One formula I can explain:**
''')
md('''## A02 From formulas to Python
Here are two examples. Use the same pattern to answer the six independent questions below.
''')
code('print("Median:", df["weight"].median())\nprint("Mean:", round(df["weight"].mean(), 2))\n')
for q in ['2A What is the lowest weight?','2B What is the highest weight?','2C What is max minus min? Round the computed answer to zero decimal places.','3A What is the earliest date?','3B What is the latest date?','3C What is the latest date where is_holiday is True? The CSV has no holiday-name column; identifying its name is an optional lookup.']:
 md('### '+q);code('# Write and run your code here.\n')
md('Explain a Boolean filter you used. Why is == different from =?')
md('''## A03 Which weekday tends to have the lowest weight?
Compare all seven weekdays. Choose a statistic that answers “tends to,” and justify it. Show counts as well as the results. A single lowest observation and the lowest average need not occur on the same weekday.

The example below starts with Monday. You can adapt it for the other days or explore `groupby`.
''')
code('monday = df[df["day_of_week"] == "Monday"]\nprint("Count:", len(monday))\nprint("Mean:", monday["weight"].mean())\nprint("Min:", monday["weight"].min())\nprint("Max:", monday["weight"].max())\n')
code('# Compare all seven days here.\n')
md('''### A03R Your work email
Write a 150–250 word work email to Mr. Hayward. Include a subject and greeting, then the finding, supporting numbers, a limitation, and a next question. Paste it into the assignment Form; you do not need to email it. Label hypotheses as hypotheses. The dataset does not tell us what caused any pattern.

**Subject and greeting:**

**Finding:**

**Evidence:**

**Limitation:**

**What I would investigate next:**
''')
md('''## A04 Make a weekend histogram
First run the weekday example, then adapt it for weekends. Give your plot a useful title, label the units, and explain what you see.
''')
code('''weekday = df.loc[~df["is_weekend"], "weight"]
weekend = df.loc[df["is_weekend"], "weight"]
# Use the same bin edges when comparing the two groups.
bin_edges = np.linspace(df["weight"].min(), df["weight"].max(), 21)
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(weekday, bins=bin_edges)
ax.set(title="Weight on weekdays", xlabel="Weight (lb)", ylabel="Observations")
plt.show()
print("Weekday observations:", len(weekday))
print("Weekend observations:", len(weekend))
''')
code('# Make a labeled WEEKEND histogram here.\n')
md('''### Compare the distributions
The groups have different observation counts. Do not confuse lower raw bar heights with lower weight. Keep bin edges the same; try `density=True` for comparing distribution shapes. If you use density, label the y-axis `Density`, not `Observations`.

What changes if you use 10, 20 or 50 bins? Describe one difference, one similarity, and one limitation.
''')
code('# Optional: make a normalized comparison chart here.\n')
md('''## A05 Why is the average not the whole story?
Run this time-series example. Notice that setup parses actual dates and sorts them. The horizontal spacing therefore represents elapsed time rather than just row order.
''')
code('''fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["date"], df["weight"], linewidth=1)
ax.set(title="Mr. Hayward's weight over time", xlabel="Date", ylabel="Weight (lb)")
locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
fig.tight_layout()
plt.show()
''')
code('# Calculate the overall mean here.\n')
md('''What is the overall mean? Why might reporting only that number be misleading? Describe a time period visible in the chart and identify what further information you would need before explaining a cause.

**My explanation:**
''')
md('''## AI Can AI help? Check its work.
Revisit one question you have already solved. Use the school-approved free AI tool your teachers make available, such as Gemini. Give it the public GitHub CSV URL from Setup, or a teacher-provided excerpt if the URL is inaccessible. Ask what rows and columns it actually read.

Ask for a useful artifact: a clearer chart, a summary document, a table or improved code. Export to a Google Doc or Sheet if that feature is available. Otherwise paste its response into a Doc or this notebook and label it AI-generated. If individual AI access is unavailable, critique a teacher-provided AI response.

**The earlier question I chose:**

**AI tool and exact prompt:**

**Original AI response or artifact link:**

**Check 1 — claim, my independent calculation, result:**

**Check 2 — claim, my independent calculation, result:**

**What was correct:**

**What was wrong, incomplete or uncertain (or what I checked if I found no error):**

**My corrections:**

**What saved time, what still needed my judgment, and when I would not rely on AI:**

Keep the original output and your revision distinguishable. Submit the artifact link and your critique in the AI answer Form. Use only the public teaching dataset.
''')
code('# Use your own code to check at least two AI claims here.\n')
md('''## A06 Show us what you learned
Prepare four slides:
1. Cover and your analysis question.
2. One clear visualization, short interpretation and a code excerpt you can explain.
3. What AI helped with, what you verified or corrected, and a limitation.
4. Three tips for students learning to code.

**My presentation link:**

**My final memo or speaker notes:**

Before submitting: restart and run all; verify the numbers and labels; confirm teacher access; submit the notebook and presentation links using the final assignment Form. Presentations finish in April. Include an evidence-based next step in your explanation.

## Optional challenge
Define a weight-gain streak carefully. Do you mean consecutive recorded observations or consecutive calendar days? What should happen if a day is missing or weight stays equal? State your rule before writing code.
''')
n={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
for i,c in enumerate(n['cells']):c['id']=f'summit-{i:03}'
(R/'curriculum/notebooks/summit-2026-27.ipynb').write_text(json.dumps(n,indent=2,ensure_ascii=False))
print('Built',len(cells),'notebook cells')
