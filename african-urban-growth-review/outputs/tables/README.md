# Tables

These CSVs are **committed** and reproduce the manuscript's tables (corpus v9).
Regenerate with `python scripts/make_outputs.py`, or knit `analysis/00_main_analysis.Rmd`
in R (which prints the same tables inline and can export them via `kableExtra::save_kable()`).

| File | Manuscript table |
|---|---|
| `table1_typology_by_driver.csv` | Table 1 — spatial typology by driver (occurrence shares) |
| `table2_scenario_themes.csv` | Table 2 — scenario themes. `Studies` is computed from the data; `Scenarios` (15 / 23 / 10 / 4; 52 total) is the scenario-level coding from the workbook, which a study can contribute to more than once |
| `tableS2_hierarchy_by_period.csv` | Table S2 — urban-hierarchy composition by period (row %) |
