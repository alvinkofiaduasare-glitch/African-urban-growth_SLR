# R/ — shared helper code

`00_setup.R` holds the project-wide theme, palettes, city-size classifier and `load_corpus()` helper. Both Rmd files source what they need from this file so visualisation style and data transformations stay consistent across the two reports.

Source it from any script with:

```r
source("R/00_setup.R")
df <- load_corpus()
```
