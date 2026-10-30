# R/ — shared helper code

`00_setup.R` holds the project-wide theme, palettes, city-size classifier and `load_corpus()` helper. The two Rmd reports are self-contained (they define the theme and palettes inline so they knit from the `analysis/` directory), but `00_setup.R` gives you the same look and the `load_corpus()` transformations for interactive work at the R console.

Source it from any script with:

```r
source("R/00_setup.R")
df <- load_corpus()
```
