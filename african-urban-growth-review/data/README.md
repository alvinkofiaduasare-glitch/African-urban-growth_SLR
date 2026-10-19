# Data dictionary — `urban_growth_cleaned.csv`

One row per included study (**n = 183**). Fields were coded by the authors from the full text of each study following the coding framework described in Methods §Analysis approach.

## Variables

| Column | Type | Description |
|---|---|---|
| `study_id` | integer | Unique within-corpus identifier (1 – 183) |
| `authors` | character | Author list, semicolon-separated surname + initials |
| `title` | character | Article title |
| `source_title` | character | Journal name |
| `pub_year` | integer | Publication year (2015 – 2025) |
| `doi` | character | DOI (bare, no URL prefix) |
| `country` | character | Primary country of the study area |
| `city` | character | Primary city or study-area name |
| `population` | numeric | Reported or inferred population of the primary study area |
| `latitude` | numeric | Primary study-area centroid latitude (WGS84) |
| `longitude` | numeric | Primary study-area centroid longitude (WGS84) |
| `specific_region` | character | African sub-region: Western / Eastern / Northern / Southern / Middle Africa |
| `informal_dev` | character | "Yes" / "No" — explicitly focused on informal settlement development |
| `informal_dev_bin` | integer | 1 if `informal_dev == "Yes"`, else 0 |
| `urban_growth_focus` | character | "Yes" / "No" — explicitly focused on urban growth |
| `urban_prediction` | character | "Yes" / "No" — includes predictive modelling of urban growth |
| `urban_prediction_bin` | integer | 1 if `urban_prediction == "Yes"`, else 0 |
| `informal_prediction` | character | "Yes" / "No" — includes predictive modelling of informal settlement |
| `method` | character | High-level methodological orientation: Quantitative / Mixed / Qualitative |
| `mapping_method_type` | character | Traditional / Machine learning / Deep learning (for mapping tasks) |
| `projection_method_type` | character | Traditional / Machine learning / Deep learning (for projection tasks) |
| `specific_methodology` | character | Specific method name (e.g., "Maximum likelihood classification"; "CA-ANN") |
| `satellite` | character | Primary satellite platform(s), semicolon-separated |
| `period_duration` | numeric | Length of the observation window in years |
| `accuracy_pct` | numeric | Reported overall accuracy or kappa coefficient (0 – 100 %) |
| `expansion_clean` | numeric | Annual urban expansion rate (%/yr), harmonised across studies |
| `spatial_form` | character | Spatial typology reported in the study |
| `primary_driver` | character | Primary driver of urban growth as identified by the study |
| `has_demography` | integer | 1 if demography named as a driver |
| `has_migration` | integer | 1 if migration named as a driver |
| `has_planning` | integer | 1 if planning named as a driver |
| `has_roads` | integer | 1 if road/transport expansion named as a driver |
| `has_conflict` | integer | 1 if conflict/displacement named as a driver |
| `has_economy` | integer | 1 if economic development named as a driver |
| `scenario_count` | integer | Number of distinct scenarios the study constructs (1 if not multi-scenario) |
| `scenario_theme` | character | Scenario themes present, semicolon-separated |
| `scenario_year` | character | Scenario horizon years, semicolon-separated |

## Values that need harmonising

- `country` includes two multi-country labels — "Africa/Multiple" and "West Africa" — for continental-scale and regional-scale studies. These are filtered out of country-level maps and tables.
- `specific_region` includes an uncommon compound label "Western Africa, Middle Africa" that is recoded to "Unknown" in the analytical scripts.
- `scenario_theme` canonical values: `BAU`, `Planning, policy and infrastructure`, `Ecological protection`, `Population-driven / unconstrained`. Multiple themes per study are semicolon-separated.
- `population` is coded as the latest reported figure available at the time of the study; it reflects urban extent of the study area rather than the whole city when the two differ.

## Provenance

The dataset was built by the author team from the full text of each of the 183 included studies between October 2025 and January 2026. The underlying bibliography (Web of Science and Scopus) was exported on **27 October 2025**. See Methods §Literature search and selection for the complete search string and screening flow.
