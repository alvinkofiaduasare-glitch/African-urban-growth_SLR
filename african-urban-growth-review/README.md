# African Urban Growth Research — Systematic Review

Code and data companion to:

> **Adu-Asare, Alvin & Sharifi, Ayyoob.** *Urban growth research across Africa shows persistent geographic and methodological gaps* (2026). Submitted to *Nature Cities*.

[![R](https://img.shields.io/badge/R-%E2%89%A54.2-blue)](https://www.r-project.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRISMA 2020](https://img.shields.io/badge/PRISMA-2020-brightgreen)](https://www.prisma-statement.org/)
[![Corpus: v9](https://img.shields.io/badge/corpus-v9-informational)](data/README.md)

---

## Overview

This repository contains the full analytical pipeline for a PRISMA-compliant systematic review of African urban growth research published between January 2015 and October 2025. From an initial 14,282 records retrieved from Web of Science and Scopus, 183 peer-reviewed studies met the inclusion criteria. The analyses map the field across four dimensions:

1. **Temporal, geographic and urban-hierarchy distribution** of the research base
2. **Methodological landscape** — traditional, machine-learning and deep-learning approaches
3. **Dominant spatial typologies** of African urban growth and their drivers
4. **Future-oriented scenarios** and their treatment of informal settlements

The code reproduces every figure, table and statistical test reported in the paper (Figures 1–6, Tables 1–2, Tables S1–S2) and includes the exploratory analyses performed during the review that are not reported in the final manuscript.



## Repository structure

```
African-urban-growth_SLR/
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CITATION.cff                    # Citation metadata (GitHub-aware)
├── DESCRIPTION                     # R package-style metadata and dependencies
├── .gitignore                      # Standard R / RStudio ignore patterns
│
├── R/
│   ├── README.md
│   └── 00_setup.R                  # Shared theme, palettes, city-size classifier, load_corpus()
│
├── analysis/
│   ├── 00_main_analysis.Rmd        # Analyses reported in the manuscript
│   └── 01_exploratory_analysis.Rmd # Additional analyses (expansion rates, regressions)
│
├── scripts/
│   ├── clean_corpus.py             # Rebuilds the cleaned CSV from the raw corpus workbook
│   └── review_coding.csv           # Dual-review method/accuracy adjudications applied by the script
│
├── data/
│   ├── README.md                   # Data dictionary, variable definitions, v8→v9 change log
│   ├── urban_abstracts_reviewed_updated_new_9.xlsm  # Raw reviewer corpus (source of truth)
│   └── urban_growth_cleaned.csv    # Primary analytical dataset (183 studies)
│
├── outputs/
│   ├── figures/                    # Figures generated at knit time
│   └── tables/                     # Tables generated at knit time
│
└── docs/
    └── reproduce.md                # Step-by-step reproduction guide
```

## Data

The analytical dataset (`data/urban_growth_cleaned.csv`) contains one row per included study (n = 183) with coded fields covering bibliographic metadata, geographic focus, urban-hierarchy classification (per the UN population thresholds — see Methods), satellite platform, modelling approach and reported accuracy, spatial typology, driver, scenario theme, and informal-settlement focus. It is built from the raw reviewer workbook by `scripts/clean_corpus.py`. See [`data/README.md`](data/README.md) for the full variable dictionary and the rebuild command.

**Data availability**: both the raw reviewer corpus (`data/urban_abstracts_reviewed_updated_new_9.xlsm`) and the derived analytical dataset are included in this repository. The underlying 183 primary studies are the publicly available peer-reviewed sources cited in the manuscript's reference list.

## Reproducing the analyses

### Requirements

- R ≥ 4.2 and the packages listed in `DESCRIPTION` (install with `install.packages()` or `renv::restore()`)
- Python ≥ 3.9 with `openpyxl` (only needed to rebuild the CSV from the raw workbook)

### Rebuild the dataset from the raw corpus (optional)

```bash
pip install openpyxl
python scripts/clean_corpus.py data/urban_abstracts_reviewed_updated_new_9.xlsm \
                               data/urban_growth_cleaned.csv
```

The script normalises the raw fields, applies the dual-review method/accuracy adjudications in `scripts/review_coding.csv`, and runs sanity checks against the manuscript's v9 values before writing.

### One-shot run

```r
# From the repository root:
rmarkdown::render("analysis/00_main_analysis.Rmd")
rmarkdown::render("analysis/01_exploratory_analysis.Rmd")
```

Both documents knit to HTML and PDF by default. All figures land in `outputs/figures/` and all tables in `outputs/tables/`.

See [`docs/reproduce.md`](docs/reproduce.md) for a full step-by-step walkthrough.

## How the code maps to the manuscript

| Manuscript element | Rmd section |
|---|---|
| Figure 1 — Temporal distribution of studies | `00_main_analysis.Rmd` §Temporal trends |
| Figure 2 — Geographic distribution of research | `00_main_analysis.Rmd` §Geographic distribution |
| Figure 3 — Informal-settlement focus by region & hierarchy | `00_main_analysis.Rmd` §Informal settlement analysis |
| Figure 4 — Methodological landscape (mapping & projection) | `00_main_analysis.Rmd` §Methodological landscape |
| Figure 5 — Spatial typologies (overall & by sub-region) | `00_main_analysis.Rmd` §Spatial typologies |
| Figure 6 — PRISMA flow | Not reproduced in code (methods diagram) |
| Table 1 — Typology by driver | `00_main_analysis.Rmd` §Spatial typologies |
| Table 2 — Scenario themes | `00_main_analysis.Rmd` §Scenario analysis |
| Table S1 — Search string | Documented in `docs/reproduce.md` |
| Table S2 — Urban hierarchy by period | `00_main_analysis.Rmd` §Temporal trends |

## Statistical tests reported in the manuscript

| Test | Variables | Where |
|---|---|---|
| Pearson χ² with Cramér's V | Period × urban hierarchy | §Temporal trends |
| Pearson χ² with Cramér's V | Urban hierarchy × informal-settlement focus | §Informal settlement analysis |

Both reproduce exactly under v9 (χ²(8) = 18.24, *p* = 0.020, *n* = 164, V = 0.24; and χ²(4) = 12.86, *p* = 0.012, *n* = 164, V = 0.28). Additional exploratory tests (Kruskal-Wallis, ANOVA, logistic and linear regression, Spearman correlation, Fisher's exact) are performed in `01_exploratory_analysis.Rmd`. These informed the review but are not reported in the manuscript.

## Citing this work

If you use this code or dataset, please cite the paper and the repository. The `CITATION.cff` file provides machine-readable metadata that GitHub renders as a "Cite this repository" widget.

## Contributing

Issues and pull requests are welcome. Please open an issue first to discuss substantive changes.

## License

Code is released under the [MIT License](LICENSE). The analytical dataset is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — you may share and adapt it with attribution.

## Contact

**Alvin Adu-Asare** — alvinkofiaduasare@gmail.com
**Ayyoob Sharifi** (corresponding author)
