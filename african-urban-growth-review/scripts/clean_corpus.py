#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_corpus.py — build the analytical dataset from the raw reviewer corpus.

Reads the raw screening workbook (`urban_abstracts_reviewed_updated_new_9.xlsm`,
sheet "Papers"), keeps the rows marked Include, and writes the 42-column
analytical CSV used by the R analysis (`data/urban_growth_cleaned.csv`).

Usage:
    python scripts/clean_corpus.py data/urban_abstracts_reviewed_updated_new_9.xlsm \
                                   data/urban_growth_cleaned.csv

Design notes
------------
* The workbook is the single source of truth. Every analytical field is derived
  from it by the deterministic rules below, so the CSV can be rebuilt from the
  corpus at any time.
* Four fields carry the dual-review team's *final* method/accuracy classification,
  which in a handful of records differs from a purely mechanical read of the
  workbook's coarse auto-labels (e.g. a study whose task label reads
  "Artificial Intelligence" but was adjudicated Traditional on the method name).
  Those adjudicated cells are listed explicitly in `scripts/review_coding.csv`
  and applied after the mechanical pass. This keeps the pipeline reproducible
  while preserving the coding reported in the manuscript.
* Rows are emitted in workbook order; `study_id` is assigned 1..N in that order.
  All downstream analyses aggregate and are order-independent.

Version: 2.0.0 — tracks corpus v9 (urban_abstracts_reviewed_updated_new_9.xlsm),
in which the spatial typology of informal-settlement growth for 13 non-informal-
focused studies was moved into the overall `Spatial forms` field (see
data/README.md, "Change log: v8 -> v9").
"""
import sys
import os
import re
import csv
import argparse

try:
    import openpyxl
except ImportError:
    sys.exit("This script needs openpyxl:  pip install openpyxl")

SHEET = "Papers"
BLANKS = {"", "na", "n/a", "none", "null", "nan"}

# ----------------------------------------------------------------------------- helpers
def s(v):
    """Cell -> trimmed string; workbook blanks ('NA','None',...) -> ''."""
    if v is None:
        return ""
    t = str(v).strip()
    return "" if t.lower() in BLANKS else t

def strip_doi(v):
    t = s(v)
    # collapse accidental repeated prefixes, then drop any resolver prefix; keep case
    t = re.sub(r'(https?://)?(dx\.)?doi\.org/', '', t, flags=re.I)
    return t.strip()

def yesno(v):
    t = s(v).lower()
    if t in ("yes", "y", "true", "1"):
        return "Yes"
    if t in ("no", "n", "false", "0"):
        return "No"
    return s(v)

def to_bin(yn):
    return 1 if s(yn).lower() == "yes" else 0

def num_or_blank(v):
    """Keep an integer as an integer, a decimal as given; non-numeric -> ''."""
    t = s(v)
    if re.fullmatch(r'-?\d+', t):
        return t
    if re.fullmatch(r'-?\d*\.\d+', t):
        return t
    return ""

def bare_accuracy(v):
    """Task accuracy: keep a plain number only; percentage strings / text -> ''."""
    t = s(v)
    return t if re.fullmatch(r'\d+(\.\d+)?', t) else ""

def lead_num(v):
    """Leading numeric of an expansion string ('2.2 increase' -> '2.2'); else ''."""
    t = s(v)
    m = re.match(r'-?\d+(\.\d+)?', t)
    return m.group(0) if m else ""

def period_years(v):
    """'1985-2010' (any dash) -> 25; needs exactly the first two 4-digit years."""
    t = s(v)
    yrs = re.findall(r'(19|20)\d{2}', t)
    if len(yrs) >= 2:
        a = int(re.findall(r'(?:19|20)\d{2}', t)[0])
        b = int(re.findall(r'(?:19|20)\d{2}', t)[1])
        if b >= a:
            return str(b - a)
    return ""

# --- spatial typology -------------------------------------------------------------
TYPO_MAP = {
    "peripheralization": "Peripheralisation",
    "peripheralisation": "Peripheralisation",
    "densification": "Densification",
    "fragmentation": "Fragmentation",
    "ribbon": "Ribbon",
    "leapfrog": "Leapfrog",
}
def norm_spatial(v):
    t = s(v)
    if not t:
        return ""
    out = []
    for tok in re.split(r'[;,]', t):
        key = tok.strip().lower()
        if key in TYPO_MAP:
            lab = TYPO_MAP[key]
            if lab not in out:
                out.append(lab)
    return "; ".join(out)

# --- method type ------------------------------------------------------------------
METHOD_MAP = {
    "traditional": "Traditional",
    "traditional method": "Traditional",
    "tradiitional": "Traditional",            # workbook typo
    "machine learning": "Machine learning",
    "artificial intelligence": "Deep learning",
}
def norm_method(v):
    return METHOD_MAP.get(s(v).lower(), "")

# --- scenario theme ---------------------------------------------------------------
# Raw theme names contain commas, so match canonical phrases by position and keep
# source order. Canonical labels follow the manuscript / Table 2.
THEME_PATTERNS = [
    (re.compile(r'business[\s-]*as[\s-]*usual|bau', re.I),              "BAU"),
    (re.compile(r'planning,?\s*policy\s*and\s*infrastructur', re.I),     "Planning, policy and infrastructure"),
    (re.compile(r'ecological', re.I),                                    "Ecological protection"),
    (re.compile(r'population[\s-]*driven', re.I),                        "Population-driven / unconstrained"),
]
def norm_theme(v):
    # Emit present themes in the manuscript's canonical order
    # (BAU; Planning, policy and infrastructure; Ecological protection;
    #  Population-driven / unconstrained), independent of source order.
    t = s(v)
    if not t:
        return ""
    ordered = []
    for pat, label in THEME_PATTERNS:
        if pat.search(t) and label not in ordered:
            ordered.append(label)
    return "; ".join(ordered)

def norm_years(v):
    t = s(v)
    if not t:
        return ""
    ys = [y for y in re.split(r'[;,]', t)]
    out = []
    for y in ys:
        y = y.strip()
        if y and y not in out:
            out.append(y)
    return "; ".join(out)

# --- drivers ----------------------------------------------------------------------
def driver_flags(main_drivers):
    low = main_drivers.lower()
    return dict(
        has_demography = 1 if "demograph" in low else 0,
        has_migration  = 1 if "migration" in low else 0,
        has_planning   = 1 if "planning"  in low else 0,
        has_roads      = 1 if "road"       in low else 0,
        has_conflict   = 1 if "conflict"   in low else 0,
        # economy = explicit economic/industrial drivers plus 'job opportunities'
        has_economy    = 1 if ("economic" in low or "industr" in low or "job" in low) else 0,
    )

OUT_COLUMNS = [
    "study_id","authors","title","source_title","pub_year","doi","country","city",
    "population","latitude","longitude","specific_region","informal_dev","informal_dev_bin",
    "urban_growth_focus","urban_prediction","urban_prediction_bin","informal_prediction",
    "method","mapping_method_type","projection_method_type","specific_methodology","satellite",
    "period_duration","accuracy_pct","mapping_accuracy","projection_accuracy","expansion_clean",
    "spatial_form","spatial_form_informal","primary_driver","main_drivers",
    "has_demography","has_migration","has_planning","has_roads","has_conflict","has_economy",
    "scenario_present","scenario_count","scenario_theme","scenario_year",
]

# ----------------------------------------------------------------------------- load
def read_workbook(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    if SHEET not in wb.sheetnames:
        sys.exit(f"Sheet '{SHEET}' not found in {path} (have: {wb.sheetnames})")
    ws = wb[SHEET]
    it = ws.iter_rows(values_only=True)
    header = list(next(it))
    # the workbook reuses the header 'Method type' twice (mapping, then projection)
    mt = [i for i, h in enumerate(header) if h == "Method type"]
    idx = {h: i for i, h in enumerate(header)}      # first occurrence wins; that's fine
    rows = [r for r in it if not all(c is None for c in r)]
    return header, idx, mt, rows

def load_overrides(sidecar):
    by_doi, by_title = {}, {}
    if not os.path.exists(sidecar):
        return by_doi, by_title
    with open(sidecar, encoding="utf-8-sig") as f:
        for rec in csv.DictReader(f):
            payload = {k: rec.get(k, "") for k in
                       ("mapping_method_type", "projection_method_type",
                        "mapping_accuracy", "projection_accuracy")}
            if rec.get("match_doi", "").strip():
                by_doi[rec["match_doi"].strip().lower()] = payload
            elif rec.get("match_title", "").strip():
                by_title[re.sub(r'\s+', ' ', rec["match_title"]).strip().lower()] = payload
    return by_doi, by_title

# ----------------------------------------------------------------------------- build
def build(xlsm_path, sidecar):
    header, idx, mt, rows = read_workbook(xlsm_path)
    col = lambda name: idx[name]
    by_doi, by_title = load_overrides(sidecar)

    out = []
    sid = 0
    for r in rows:
        if s(r[col("Screening decision")]).lower() != "include":
            continue
        sid += 1
        main_drivers = s(r[col("Main Drivers")])
        primary = main_drivers.split(",")[0].strip() if main_drivers else ""
        rec = {
            "study_id": sid,
            "authors": s(r[col("Authors")]),
            "title": s(r[col("Article Title")]),
            "source_title": s(r[col("Source Title")]),
            "pub_year": s(r[col("Publication Year")]),
            "doi": strip_doi(r[col("DOI Link")]),
            "country": s(r[col("country")]),
            "city": s(r[col("City")]),
            "population": num_or_blank(r[col("Population")]),
            "latitude": num_or_blank(r[col("Latitude")]),         # 'Not specified' etc. -> blank
            "longitude": num_or_blank(r[col("Longitude")]),
            # workbook spelling; missing region is recorded as the literal 'Unknown'
            "specific_region": (s(r[col("Specifc regions")]) or "Unknown"),
            "informal_dev": yesno(r[col("Focused on informal development")]),
            "urban_growth_focus": yesno(r[col("Focused on urban growth")]),
            "urban_prediction": yesno(r[col("Focused on urban growth  prediction")]),
            "informal_prediction": yesno(r[col("Focused on predicting growth in the context of informal development")]),
            "method": s(r[col("Method")]),
            "mapping_method_type": norm_method(r[mt[0]]),
            "projection_method_type": norm_method(r[mt[1]]),
            "specific_methodology": s(r[col("Specific methodology")]),
            "satellite": s(r[col("Satellite imagery used")]),
            "period_duration": period_years(r[col("Period under consideration")]),
            "accuracy_pct": "",                                   # study-level accuracy not harmonised across the corpus
            "mapping_accuracy": bare_accuracy(r[col("Urban Expansion Accuracy 1")]),
            "projection_accuracy": bare_accuracy(r[col("Urban forecasting Accuracy 2")]),
            # annual expansion rate (%/yr): leading number of the reviewers' expansion field
            "expansion_clean": lead_num(r[col("change of expansion or change")]),
            "spatial_form": norm_spatial(r[col("Spatial forms")]),
            "spatial_form_informal": norm_spatial(r[col("Spatial pattern of informal growth")]),
            "primary_driver": primary,
            "main_drivers": main_drivers,
            "scenario_present": yesno(r[col(" scenario present")]),   # leading space in header
            "scenario_count": (num_or_blank(r[col("Number of scenarios")]) or "0"),
            "scenario_theme": norm_theme(r[col("Scenario theme")]),
            "scenario_year": norm_years(r[col("Year of scenarios")]),
        }
        rec["informal_dev_bin"] = to_bin(rec["informal_dev"])
        rec["urban_prediction_bin"] = to_bin(rec["urban_prediction"])
        rec.update(driver_flags(main_drivers))

        # apply dual-review final coding for the adjudicated cells
        ov = by_doi.get(rec["doi"].lower()) or by_title.get(re.sub(r'\s+', ' ', rec["title"]).strip().lower())
        if ov:
            for k, v in ov.items():
                rec[k] = v
        out.append(rec)
    return out

# ----------------------------------------------------------------------------- checks
def sanity(rows):
    """Validate against the manuscript's reported v9 values; warn on divergence."""
    n = len(rows)
    def count(pred): return sum(1 for r in rows if pred(r))
    checks = []
    checks.append(("included studies", n, 183))
    checks.append(("informal-focused (informal_dev=Yes)",
                   count(lambda r: r["informal_dev"] == "Yes"), 21))
    checks.append(("prediction studies (urban_prediction=Yes)",
                   count(lambda r: r["urban_prediction"] == "Yes"), 108))
    checks.append(("multi-scenario studies (scenario_count>=2)",
                   count(lambda r: (r["scenario_count"] or "0").isdigit()
                                   and int(r["scenario_count"]) >= 2), 16))
    # spatial typology occurrences (overall) under v9
    occ = 0
    for r in rows:
        occ += len([t for t in r["spatial_form"].split(";") if t.strip()])
    checks.append(("spatial-form occurrences (overall)", occ, 137))
    # informal-growth typology studies under v9
    inf = count(lambda r: r["spatial_form_informal"].strip() != "")
    checks.append(("informal-typology studies", inf, 13))

    ok = True
    print("\nSanity checks (value vs expected v9):")
    for name, got, exp in checks:
        flag = "OK " if got == exp else "!! "
        if got != exp:
            ok = False
        print(f"  [{flag}] {name:42s} {got:>5}  (expect {exp})")
    if not ok:
        print("  WARNING: one or more checks diverged from the manuscript's v9 values.")
    return ok

def main():
    ap = argparse.ArgumentParser(description="Build urban_growth_cleaned.csv from the raw corpus workbook.")
    ap.add_argument("xlsm", help="path to urban_abstracts_reviewed_updated_new_9.xlsm")
    ap.add_argument("out", help="output CSV path (e.g. data/urban_growth_cleaned.csv)")
    ap.add_argument("--sidecar", default=os.path.join(os.path.dirname(__file__), "review_coding.csv"),
                    help="reviewer method/accuracy adjudication sheet")
    args = ap.parse_args()

    rows = build(args.xlsm, args.sidecar)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in OUT_COLUMNS})
    print(f"Wrote {len(rows)} studies x {len(OUT_COLUMNS)} columns -> {args.out}")
    sanity(rows)

if __name__ == "__main__":
    main()
