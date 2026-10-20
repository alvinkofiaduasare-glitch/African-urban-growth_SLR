# Data — `urban_growth_cleaned.csv`

**183 rows × 42 columns.** One row per included study, after PRISMA screening of 14,282 records retrieved from Web of Science and Scopus on 27 October 2025.

Built from `urban_abstracts_reviewed_updated_new_8.xlsm` (source corpus, not included in this repository to keep the public release at the published analytical layer) by `scripts/clean_corpus.py`. The cleaning step reconciles spelling (Peripheralisation vs peripheralization), capitalisation (Densification vs densification), typos (Tradiitional → Traditional), DOI prefixes (strips repeated `https://doi.org/`) and normalises list-valued fields to semicolons.

## Variables

### Bibliographic

| Column | Type | Description |
|---|---|---|
| `study_id` | integer | Sequential within-corpus identifier (1–183) |
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
| `latitude` | numeric | Centroid latitude (WGS84) |
| `longitude` | numeric | Centroid longitude (WGS84) |
| `specific_region` | character | African sub-region: `Western Africa` / `Eastern Africa` / `Northern Africa` / `Southern Africa` / `Middle Africa` / `Unknown` |

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
| `mapping_method_type` | character | Mapping task method: `Traditional` / `Machine learning` / `Deep learning` |
| `projection_method_type` | character | Projection task method: `Traditional` / `Machine learning` / `Deep learning` |
| `specific_methodology` | character | Specific method name (e.g., `Maximum likelihood classification`, `CA-ANN`) |
| `satellite` | character | Primary satellite platform(s), comma-separated |
| `period_duration` | integer | Length of the observation window in years (parsed from `YYYY-YYYY` strings) |
| `accuracy_pct` | numeric | Reported overall accuracy or kappa coefficient (0–100 %) — study-level |
| `mapping_accuracy` | numeric | Mapping-task-specific accuracy (0–100 %) |
| `projection_accuracy` | numeric | Projection-task-specific accuracy (0–100 %) |
| `expansion_clean` | numeric | Annual urban expansion rate (%/yr), harmonised across studies |

### Spatial typology

| Column | Type | Description |
|---|---|---|
| `spatial_form` | character | Overall spatial typology, semicolon-separated when multiple (`Peripheralisation; Densification`) |
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
| `has_economy` | integer | 1 if economic/industrial activity named as a driver |

### Scenarios

| Column | Type | Description |
|---|---|---|
| `scenario_present` | character | `Yes` / `No` — study constructs one or more future scenarios |
| `scenario_count` | numeric | Number of distinct scenarios (0 if none) |
| `scenario_theme` | character | Scenario themes present, semicolon-separated — canonical values: `BAU`, `Planning, policy and infrastructure`, `Ecological protection`, `Population-driven / unconstrained` |
| `scenario_year` | character | Scenario horizon years, semicolon-separated (e.g., `2030; 2050`) |

## Reconciled sanity checks against the manuscript

The cleaning script `scripts/clean_corpus.py` validates against the following manuscript values after loading. If any diverge, re-run the cleaning.

| Metric | Expected | Source |
|---|---|---|
| Included studies | 183 | Methods §Literature search |
| Informal-settlement-focused studies | 21 | Methods §Analysis approach |
| Multi-scenario studies | 16 | Results §Scenarios |
| Country top-8 (Nigeria 34, Ethiopia 29, Egypt 24, Ghana 20, Algeria 14, South Africa 11, Tanzania 11, Morocco 9) | 154 | Results §Geographic concentration |
| Peripheralisation share of 129 typology occurrences | 76 / 129 = 58.9 % | Results §Spatial typologies |

## Data availability

The structured dataset `urban_growth_cleaned.csv` is released with this repository under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The underlying 183 primary studies are the publicly available peer-reviewed sources listed in the manuscript's reference list.

## Rebuilding the dataset from the raw corpus

If you have the raw `.xlsm` corpus, you can reproduce `urban_growth_cleaned.csv` with:

```bash
pip install openpyxl
python scripts/clean_corpus.py /path/to/corpus.xlsm data/urban_growth_cleaned.csv
```

The script applies all the normalisations listed above and runs the sanity checks before writing.
