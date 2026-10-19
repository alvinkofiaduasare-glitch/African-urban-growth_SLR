# 00_setup.R — shared project setup
# Sourced from the top of both Rmd files to keep theme and palette consistent.
# You can also source it directly in a plain R session for interactive work.

suppressPackageStartupMessages({
  library(tidyverse)
  library(scales)
  library(knitr)
  library(kableExtra)
  library(rstatix)
  library(effectsize)
})

# -----------------------------------------------------------------------------
# City-size classifier (UN 2025 thresholds)
# -----------------------------------------------------------------------------
classify_city <- function(pop) {
  dplyr::case_when(
    is.na(pop)   ~ "Unknown",
    pop > 10e6   ~ "Megacity",
    pop >= 5e6   ~ "Large City",
    pop >= 1e6   ~ "Medium-sized City",
    pop >= 250e3 ~ "Small City",
    TRUE         ~ "Very Small City"
  )
}

# -----------------------------------------------------------------------------
# Palettes
# -----------------------------------------------------------------------------
pal_blue  <- c("#185FA5", "#378ADD", "#85B7EB", "#B5D4F4", "#E6F1FB")
pal_teal  <- c("#085041", "#0F6E56", "#1D9E75", "#5DCAA5", "#9FE1CB")
pal_coral <- c("#993C1D", "#D85A30", "#F0997B", "#F5C4B3")
pal_amber <- c("#854F0B", "#BA7517", "#EF9F27", "#FAC775")

pal_region <- c(
  "Western Africa"  = "#185FA5",
  "Eastern Africa"  = "#1D9E75",
  "Northern Africa" = "#D85A30",
  "Southern Africa" = "#BA7517",
  "Middle Africa"   = "#534AB7"
)

pal_size <- c(
  "Megacity"          = "#185FA5",
  "Large City"        = "#378ADD",
  "Medium-sized City" = "#1D9E75",
  "Small City"        = "#5DCAA5",
  "Very Small City"   = "#9FE1CB"
)

pal_typology <- c(
  "Peripheralisation" = "#185FA5",
  "Fragmentation"     = "#1D9E75",
  "Densification"     = "#534AB7",
  "Ribbon"            = "#BA7517",
  "Leapfrog"          = "#D85A30"
)

pal_method <- c(
  "Traditional"      = "#185FA5",
  "Machine learning" = "#1D9E75",
  "Deep learning"    = "#D85A30"
)

# -----------------------------------------------------------------------------
# ggplot theme
# -----------------------------------------------------------------------------
ggplot2::theme_set(
  ggplot2::theme_minimal(base_size = 12) +
    ggplot2::theme(
      plot.title    = ggplot2::element_text(face = "bold", size = 13),
      plot.subtitle = ggplot2::element_text(colour = "grey40", size = 11),
      legend.position = "right",
      panel.grid.minor = ggplot2::element_blank()
    )
)

# -----------------------------------------------------------------------------
# Load and lightly transform the analytical dataset
# -----------------------------------------------------------------------------
load_corpus <- function(path = "data/urban_growth_cleaned.csv") {
  df <- readr::read_csv(path, show_col_types = FALSE)
  stopifnot(nrow(df) == 183)

  df %>%
    dplyr::mutate(
      city_size = factor(
        classify_city(population),
        levels = c("Megacity", "Large City", "Medium-sized City",
                   "Small City", "Very Small City", "Unknown")
      ),
      lat_num = suppressWarnings(as.numeric(latitude)),
      lon_num = suppressWarnings(as.numeric(longitude)),
      region  = ifelse(specific_region %in%
                         c("Unknown", "Western Africa, Middle Africa"),
                       "Unknown", specific_region),
      period = dplyr::case_when(
        pub_year %in% 2015:2018 ~ "2015-2018",
        pub_year %in% 2019:2022 ~ "2019-2022",
        pub_year %in% 2023:2025 ~ "2023-2025",
        TRUE                    ~ NA_character_
      )
    )
}
