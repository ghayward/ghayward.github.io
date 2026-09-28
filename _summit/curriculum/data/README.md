# Teaching dataset

`mr_hayward_weight.csv` is copied from George's existing local `hayward_public_data/data/mr_hayward_weight.csv`. The class already uses the public version at https://github.com/ghayward/hayward_public_data .

Pinned upstream version: `e2443fa8eb4b91f526657deeceedf5ce81616327` (October 2, 2024).

SHA-256: `cbb89a848420e48b757563b0c42871a96d76bf5922c3ac9c64b101238b3d1f13`.

2,001 rows; October 10, 2017 through September 29, 2024; no duplicate dates or null fields found.

| Column | Meaning |
|---|---|
| date | Date of recorded measurement; parse as a date before plotting |
| weight | George's recorded weight in pounds |
| day_of_week | English weekday label |
| is_weekend | Boolean weekend flag |
| is_holiday | Boolean holiday flag; no holiday name is included |

An observation is a recorded measurement, not proof of uninterrupted daily tracking. The data is an educational example; students do not supply their own measurements. Do not infer diet, exercise, or causes from the available fields alone.
