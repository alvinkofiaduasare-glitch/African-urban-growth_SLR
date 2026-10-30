# Reproduction guide

A step-by-step walkthrough to regenerate every figure, table and statistical test in the manuscript (corpus v9).

## Software prerequisites

- **R ≥ 4.2** (tested on R 4.3.2 on macOS 14 and Ubuntu 22.04)
- **Pandoc ≥ 2.19** (bundled with RStudio ≥ 2022.07)
- **Python ≥ 3.9** with `openpyxl` — only needed if you want to rebuild the CSV from the raw workbook
- Approximately 1 GB free disk for `rnaturalearth` map data on first run

## 1. Clone the repository

```bash
git clone https://github.com/alvinkofiaduasare-glitch/African-urban-growth_SLR.git
cd African-urban-growth_SLR
```

## 2. Install R dependencies

### Option A — plain install

```r
pkgs <- c(
  "tidyverse", "scales", "knitr", "kableExtra",
  "broom", "car", "rstatix", "effectsize", "corrplot",
  "sf", "rnaturalearth", "rnaturalearthdata",
  "viridis", "RColorBrewer", "ggrepel", "rmarkdown"
)
install.packages(pkgs)
```

### Option B — reproducible with `renv`

```r
install.packages("renv")
renv::init(bare = TRUE)
renv::install(pkgs)
renv::snapshot()
```

## 3. The dataset is already in place

`data/urban_growth_cleaned.csv` ships with the repository, so you can go straight to knitting. To rebuild it from the raw reviewer corpus (e.g. after editing the workbook):

```bash
pip install openpyxl
python scripts/clean_corpus.py data/urban_abstracts_reviewed_updated_new_9.xlsm \
                               data/urban_growth_cleaned.csv
```

The script normalises the raw fields, applies the dual-review adjudications in `scripts/review_coding.csv`, prints the sanity checks (see `data/README.md`) and writes the CSV. The expected schema is in [`data/README.md`](../data/README.md).

## 4. Knit the main analysis

```r
rmarkdown::render("analysis/00_main_analysis.Rmd")
```

Or from the command line:

```bash
Rscript -e "rmarkdown::render('analysis/00_main_analysis.Rmd')"
```

Outputs:

- `analysis/00_main_analysis.html` — HTML report
- `outputs/figures/fig1-temporal-1.png`, `fig2a-studies-map-1.png`, `fig5a-typology-1.png`, …
- All tables inline in the HTML (also copyable to Word/LaTeX via `kableExtra::save_kable()`)

## 4b. Populate outputs/ without R (optional)

A rendered copy of every figure and table is already committed under `outputs/`. To regenerate them without an R toolchain:

```bash
pip install matplotlib
python scripts/make_outputs.py
```

This writes `outputs/figures/figure1_temporal.png` … `figure5b_typology_by_region.png` and `outputs/tables/table1_typology_by_driver.csv`, `table2_scenario_themes.csv`, `tableS2_hierarchy_by_period.csv`, all from `data/urban_growth_cleaned.csv` using the manuscript palette. Figure 2's choropleth maps need the R `sf`/`rnaturalearth` stack; the script renders Figure 2 as the underlying per-country bars instead.

## 5. Knit the exploratory analysis (optional)

```r
rmarkdown::render("analysis/01_exploratory_analysis.Rmd")
```

Chunks that depend on harmonised study-level accuracy guard their inputs and skip when the data is too thin, so the document always knits.

## 6. Verify against the manuscript (corpus v9)

The main-analysis report cross-prints the manuscript's reported statistics next to each test. Key values to match:

| Element | Manuscript value (v9) |
|---|---|
| Period × urban hierarchy | χ²(8) = 18.24, *p* = 0.020, *n* = 164, Cramér's V = 0.24 |
| Urban hierarchy × informal focus | χ²(4) = 12.86, *p* = 0.012, *n* = 164, Cramér's V = 0.28 |
| Top-8 countries | 152 / 183 = 83.1 % |
| Spatial typology — peripheralisation | 59.9 % (82 / 137) |
| Spatial typology — fragmentation | 15.3 % |
| Spatial typology — densification | 10.2 % |
| Spatial typology — ribbon / leapfrog | 7.3 % each |
| Peripheralisation in Northern Africa | 71.1 % |
| Peripheralisation in Eastern Africa | 63.6 % |
| Peripheralisation in Western Africa | 50.0 % |
| Peripheralisation in Southern Africa | 37.5 % (now leads) |
| Informal-growth typology | 13 studies, 16 occurrences (peripheralisation 56.3 %, densification 37.5 %, ribbon 6.3 %) |

### Table 1 (typology by driver, v9)

| Driver | Occ | Periph | Frag | Densif | Ribbon | Leapfrog |
|---|---|---|---|---|---|---|
| Population growth and migration | 20 | 50.0 | 15.0 | 20.0 | 15.0 | 0.0 |
| Planning regulation | 17 | 58.8 | 11.8 | 5.9 | 5.9 | 17.6 |
| Road and transport expansion | 14 | 42.9 | 28.6 | 0.0 | 14.3 | 14.3 |
| Economic development | 10 | 80.0 | 20.0 | 0.0 | 0.0 | 0.0 |
| Industrial activity | 10 | 80.0 | 10.0 | 10.0 | 0.0 | 0.0 |

> The submitted manuscript's Table 1 carries two stale cells from v8 — Population/Fragmentation (15.8) and Industrial/Densification (11.1). The code computes the correct v9 values (15.0 and 10.0); update the manuscript to match.

### Table 2 (scenario themes, v9)

`00_main_analysis.Rmd` reports the **number of studies** each theme appears in (BAU 15, Planning/policy 11, Ecological 9, Population-driven 4, across the 16 multi-scenario studies). The manuscript's Table 2 also reports a per-theme **scenario** count, which comes from the scenario-level coding in the workbook (`Scenarios used` / `Scenario theme`) and totals 52:

| Scenario theme | Studies | Scenarios |
|---|---|---|
| Business-as-usual (BAU) | 15 | 15 |
| Planning, policy and infrastructure | 11 | 23 |
| Ecological / ecosystem protection | 9 | 10 |
| Population-driven / unconstrained | 4 | 4 |

Scenario horizons (terminal, per multi-scenario study): 2030 (8), 2035 (3), 2050 (2), and single studies at 2025, 2038 and 2076.

### A note on the Figure 4 method shares

Figure 4 shows the method composition of **mapping** and **projection** tasks separately, by period. The manuscript's headline "≈67 % traditional" pools the two task types; the per-task figures the chunk plots are: mapping — 71 traditional / 46 machine learning / 3 deep learning (of 120 coded); projection — 55 traditional / 22 deep learning (of 77 coded). CA-Markov is the most common single projection method (see `01_exploratory_analysis.Rmd`).

Divergence beyond rounding suggests the dataset drifted from the v9 analytical snapshot — rebuild with `scripts/clean_corpus.py` and re-knit.

## Table S1 — search string

The full Web of Science / Scopus search string and the Boolean operators are reported in the manuscript's Supplementary Methods. Record counts: 14,282 retrieved → 183 included after PRISMA screening (Figure 6).

## Troubleshooting

- **`rnaturalearth` download fails** on first use: `install.packages("rnaturalearthhires", repos = "https://ropensci.r-universe.dev")` and retry.
- **`sf` fails to load** on Linux: `sudo apt-get install libgdal-dev libproj-dev libgeos-dev`.
- **Figures do not land in `outputs/figures/`**: check that `knitr::opts_chunk$set(fig.path = "../outputs/figures/")` is active in the first setup chunk. Use `rmarkdown::render()` from the repository root rather than the RStudio Knit button.

## Reporting issues

Please open an issue on GitHub with the output of `sessionInfo()` and the error message.
