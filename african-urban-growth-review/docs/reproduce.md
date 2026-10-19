# Reproduction guide

A step-by-step walkthrough to regenerate every figure, table and statistical test in the manuscript.

## Software prerequisites

- **R ≥ 4.2** (tested on R 4.3.2 on macOS 14 and Ubuntu 22.04)
- **Pandoc ≥ 2.19** (bundled with RStudio ≥ 2022.07)
- Approximately 1 GB free disk for `rnaturalearth` map data on first run

## 1. Clone the repository

```bash
git clone https://github.com/<USER>/african-urban-growth-review.git
cd african-urban-growth-review
```

## 2. Install R dependencies

Two options:

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

A snapshot `renv.lock` can be committed to pin exact versions.

## 3. Place the dataset

Copy the project CSV to `data/urban_growth_cleaned.csv`.
The expected schema is in [`data/README.md`](../data/README.md).
Delete the `urban_growth_cleaned.csv.PLACEHOLDER` file once the real one is in place.

## 4. Knit the main analysis

From R:

```r
rmarkdown::render("analysis/00_main_analysis.Rmd")
```

Or from the command line:

```bash
Rscript -e "rmarkdown::render('analysis/00_main_analysis.Rmd')"
```

Outputs:

- `analysis/00_main_analysis.html` — HTML report
- `outputs/figures/fig2-temporal-1.png`, `fig3a-studies-map-1.png`, …
- All tables inline in the HTML (also copyable to Word/LaTeX via `kableExtra::save_kable()`)

## 5. Knit the exploratory analysis (optional)

```r
rmarkdown::render("analysis/01_exploratory_analysis.Rmd")
```

Outputs:

- `analysis/01_exploratory_analysis.html`
- `outputs/figures/exploratory_*.png`

## 6. Verify against the manuscript

The main-analysis report cross-prints the manuscript's reported statistics next to each test so you can spot any divergence. Key manuscript values to match:

| Test | Manuscript value |
|---|---|
| Period × urban hierarchy | χ²(8) = 18.24, *p* = 0.020, *n* = 164, Cramér's V = 0.24 |
| Urban hierarchy × informal focus | χ²(4) = 12.86, *p* = 0.012, *n* = 164, Cramér's V = 0.28 |
| Peripheralisation share | 58.9 % of occurrences |
| Fragmentation share | 15.5 % |
| Densification share | 10.1 % |
| Ribbon / Leapfrog share | 7.8 % each |
| Peripheralisation in Northern Africa | 69.8 % |
| Peripheralisation in Eastern Africa | 63.4 % |
| Peripheralisation in Western Africa | 51.4 % |

Divergence > 0.1 percentage point suggests the dataset drifted from the manuscript's analytical snapshot — re-sync and re-knit.

## Troubleshooting

- **`rnaturalearth` download fails** on first use: `install.packages("rnaturalearthhires", repos = "https://ropensci.r-universe.dev")` and retry.
- **`sf` fails to load** on Linux: `sudo apt-get install libgdal-dev libproj-dev libgeos-dev`.
- **Figures do not land in `outputs/figures/`**: check that `knitr::opts_chunk$set(fig.path = "../outputs/figures/")` is active in the first setup chunk. RStudio sometimes resets the working directory when knitting; use `rmarkdown::render()` from the repository root rather than the RStudio Knit button.

## Reporting issues

Please open an issue on GitHub with the output of `sessionInfo()` and the error message.
