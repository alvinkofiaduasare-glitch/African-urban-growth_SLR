# Figures

These PNGs are **committed** and reproduce the manuscript's figures (corpus v9).
There are two ways to regenerate them:

- **R (canonical).** Knit `analysis/00_main_analysis.Rmd`; the ggplot2 chunks write
  here via `knitr`'s `fig.path`. This path also produces the **Figure 2 choropleth
  maps** (via `sf` + `rnaturalearth`).
- **Python (no R toolchain needed).** `python scripts/make_outputs.py` rebuilds every
  figure from `data/urban_growth_cleaned.csv` with matplotlib, using the manuscript
  palette. Because the geospatial stack is optional, **Figure 2 is rendered here as the
  underlying per-country bars**; knit the Rmd in R for the actual map.

| File | Manuscript figure |
|---|---|
| `figure1_temporal.png` | Figure 1 — annual research output |
| `figure2a_studies_by_country.png` | Figure 2a — studies per country (bar form of the choropleth) |
| `figure2b_informal_by_country.png` | Figure 2b — informal-focus rate per country (bar form) |
| `figure3a_informal_by_region.png` | Figure 3a — informal focus by sub-region |
| `figure3b_informal_by_citysize.png` | Figure 3b — informal focus by city-size class |
| `figure4a_mapping_methods.png` | Figure 4a — mapping method composition by period |
| `figure4b_projection_methods.png` | Figure 4b — projection method composition by period |
| `figure5a_typology_overall.png` | Figure 5a — overall spatial-typology frequency |
| `figure5b_typology_by_region.png` | Figure 5b — spatial typology by sub-region |
