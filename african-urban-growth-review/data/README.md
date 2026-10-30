# Data — `urban_growth_cleaned.csv`

**183 rows × 42 columns.** One row per included study, after PRISMA screening of 14,282 records retrieved from Web of Science and Scopus on 27 October 2025.

Built from `urban_abstracts_reviewed_updated_new_9.xlsm` (the raw reviewer corpus, included in this repository) by [`scripts/clean_corpus.py`](../scripts/clean_corpus.py). The cleaning step reconciles spelling (Peripheralisation vs peripheralization), capitalisation (Densification vs densification), method-type labels, DOI prefixes (strips repeated `https://doi.org/`) and normalises list-valued fields to semicolons. A small set of dual-review method/accuracy adjudications is applied from [`scripts/review_coding.csv`](../scripts/review_coding.csv).

Rebuild it at any time with:

```bash
pip install openpyxl
python scripts/clean_corpus.py data/urban_abstracts_reviewed_updated_new_9.xlsm \
                               data/urban_growth_cleaned.csv
```

The script runs the sanity checks below before writing and emits rows in workbook order (`study_id` 1..183); all analyses aggregate and are order-independent.

## Variables

### Bibliographic

| Column | Type | Description |
|---|---|---|
| `study_id` | integer | Sequential within-corpus identifier (1–183), in workbook order |
| `authors` | character | Author list, semicolon-separated surnames + initials |
| `title` | character | Article title |
| `source_title` | character | Journal name |
| `pub_year` | integer | Publication year (2015–2025) |
| `doi` | character | Bare DOI (`10.xxxx/yyyy`), no URL prefix |

### Geographic focus

| Column | Type | Description |
|---|---|---|
| `country` | character | Primary country of the study area. Values `Africa/Multiple` and `West Africa` are multi-country labels — filter them out for country-level maps |
| `city` | character | Primary city or study-area name |
| `population` | numeric | Reported population of the primary study area |
| `latitude` | numeric | Centroid latitude (WGS84); blank when the study area is not a single point |
| `longitude` | numeric | Centroid longitude (WGS84); blank when the study area is not a single point |
| `specific_region` | character | African sub-region: `Western Africa` / `Eastern Africa` / `Northern Africa` / `Southern Africa` / `Middle Africa` / `Western Africa, Middle Africa` (hybrid) / `Unknown`. Missing values are recorded as `Unknown` |

### Study classification

| Column | Type | Description |
|---|---|---|
| `informal_dev` | character | `Yes` / `No` — study explicitly focused on informal settlement development |
| `informal_dev_bin` | integer | 1 if `informal_dev == "Yes"`, else 0 |
| `urban_growth_focus` | character | `Yes` / `No` — study explicitly focused on urban growth |
| `urban_prediction` | character | `Yes` / `No` — study includes predictive modelling of urban growth |
| `urban_prediction_bin` | integer | 1 if `urban_prediction == "Yes"`, else 0 |
| `informal_prediction` | character | `Yes` / `No` — study includes predictive modelling of informal settlement |

### Method

| Column | Type | Description |
|---|---|---|
| `method` | character | High-level orientation: `Quantitative` / `Mixed` / `Qualitative` |
| `mapping_method_type` | character | Mapping task method: `Traditional` / `Machine learning` / `Deep learning` (blank if no mapping task) |
| `projection_method_type` | character | Projection task method: `Traditional` / `Machine learning` / `Deep learning` (blank if no projection task) |
| `specific_methodology` | character | Specific method name (e.g., `Maximum likelihood classification`, `CA-ANN`) |
| `satellite` | character | Primary satellite platform(s), comma-separated |
| `period_duration` | integer | Length of the observation window in years (parsed from `YYYY-YYYY` strings) |
| `accuracy_pct` | numeric | **Not harmonised** — study-level accuracy is reported per task and on mixed scales across studies, so this column is left blank in the public release. See the two task-level columns below |
| `mapping_accuracy` | numeric | Mapping-task accuracy where reported as a plain number (sparse) |
| `projection_accuracy` | numeric | Projection-task accuracy where reported as a plain number (sparse) |
| `expansion_clean` | numeric | Annual urban expansion rate (%/yr), the leading numeric of the reviewers' expansion field (populated for 143 of 183 studies) |

### Spatial typology

| Column | Type | Description |
|---|---|---|
| `spatial_form` | character | Overall spatial typology, semicolon-separated when multiple (`Peripheralisation; Densification`). Canonical values: Peripheralisation, Fragmentation, Densification, Ribbon, Leapfrog |
| `spatial_form_informal` | character | Spatial typology specifically reported for informal-settlement growth |

### Drivers

| Column | Type | Description |
|---|---|---|
| `primary_driver` | character | First driver listed in the raw Main Drivers field |
| `main_drivers` | character | Full driver list, comma-separated as reported in the source |
| `has_demography` | integer | 1 if demography named as a driver |
| `has_migration` | integer | 1 if migration named as a driver |
| `has_planning` | integer | 1 if planning/regulation named as a driver |
| `has_roads` | integer | 1 if road/transport expansion named as a driver |
| `has_conflict` | integer | 1 if conflict/displacement named as a driver |
| `has_economy` | integer | 1 if economic activity named as a driver (economic development, industrial activity, or job opportunities) |

### Scenarios

| Column | Type | Description |
|---|---|---|
| `scenario_present` | character | `Yes` / `No` — study constructs one or more future scenarios |
| `scenario_count` | numeric | Number of distinct scenarios (0 if none) |
| `scenario_theme` | character | Scenario themes present, semicolon-separated in canonical order — `BAU`, `Planning, policy and infrastructure`, `Ecological protection`, `Population-driven / unconstrained` |
| `scenario_year` | character | Scenario horizon years, semicolon-separated (e.g., `2030; 2050`) |

## Reconciled sanity checks against the manuscript (corpus v9)

`scripts/clean_corpus.py` validates against the following after loading; if any diverge it prints a warning.

| Metric | Expected (v9) | Source |
|---|---|---|
| Included studies | 183 | Methods §Literature search |
| Informal-settlement-focused studies | 21 | Methods §Analysis approach |
| Prediction studies (`urban_prediction = Yes`) | 108 | Results §Scenarios |
| Multi-scenario studies | 16 | Results §Scenarios |
| Country top-8 (Nigeria 34, Ethiopia 29, Egypt 24, Ghana 20, Algeria 14, South Africa 11, Tanzania 11, Morocco 9) | 152 (83.1 %) | Results §Geographic concentration |
| Overall spatial-typology occurrences | 137 | Results §Spatial typologies |
| Peripheralisation share of occurrences | 82 / 137 = 59.9 % | Results §Spatial typologies |
| Informal-growth typology studies | 13 | Results §Informal settlement |

## Change log: v8 → v9

The dataset previously tracked corpus v8 (`urban_abstracts_reviewed_updated_new_8.xlsm`). No study was added or removed (183 in both). The differences are:

1. **Informal-settlement typology recoding (the substantive change).** The spatial typology of informal-settlement growth for 13 non-informal-focused studies was moved out of `spatial_form_informal` and into the overall `spatial_form` field. As a result:
   - `spatial_form_informal` now covers **13** studies (16 occurrences), down from 26 studies (29 occurrences) in v8.
   - Overall `spatial_form` occurrences rise from **129 to 137**, so the overall peripheralisation share becomes 59.9 % (82 / 137), up from 58.9 % (76 / 129).
   - Within-region typology shifts accordingly; notably, **peripheralisation now leads in every sub-region**, including Southern Africa (37.5 %), where under v8 it did not lead.
2. **Field completions / corrections in v9.** v9 fills in or corrects cells that were blank in v8 for a small number of studies: `city` (1), `specific_region` (7, mostly Unknown → a named sub-region), `method` (2), `specific_methodology` (6), `satellite` (7), `primary_driver` / `main_drivers` (4, with consequent `has_*` flags), and one `scenario_year`.
3. **`expansion_clean` populated.** Previously blank; now the parsed annual expansion rate (143 of 183 studies).

Every number reported in the manuscript was re-verified against v9 and holds, except two stale cells in the submitted Table 1 (Population/Fragmentation 15.8 → 15.0 %, Industrial/Densification 11.1 → 10.0 %) that should be corrected to the v9 values the code computes.

## Data availability

Both the raw reviewer corpus (`urban_abstracts_reviewed_updated_new_9.xlsm`) and the derived analytical dataset (`urban_growth_cleaned.csv`) are released with this repository. The CSV is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The underlying 183 primary studies are the publicly available peer-reviewed sources listed in the manuscript's reference list.
