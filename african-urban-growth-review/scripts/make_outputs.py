#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_outputs.py — materialise the manuscript figures and tables into outputs/.

The canonical figures are produced by knitting analysis/00_main_analysis.Rmd in R
(ggplot2 + sf). This script is a dependency-light Python equivalent that reproduces
the same figures and tables from data/urban_growth_cleaned.csv using matplotlib, so
outputs/ is populated without an R toolchain. It uses the manuscript's own palette
(see R/00_setup.R).

Figure 2 (geographic) is a choropleth in the paper; without a geospatial stack this
script renders the underlying per-country bars instead. Knit the Rmd in R for the map.

Usage:
    python scripts/make_outputs.py          # writes into ../outputs relative to this file
    python scripts/make_outputs.py DATA OUTDIR
"""
import os, sys, csv, re
from collections import Counter, defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "urban_growth_cleaned.csv")
OUT  = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "outputs")
FIG  = os.path.join(OUT, "figures"); TAB = os.path.join(OUT, "tables")
os.makedirs(FIG, exist_ok=True); os.makedirs(TAB, exist_ok=True)

# ---- manuscript palette (R/00_setup.R) ----
C_BLUE, C_CORAL = "#185FA5", "#D85A30"
PAL_REGION = {"Western Africa":"#185FA5","Eastern Africa":"#1D9E75","Northern Africa":"#D85A30",
              "Southern Africa":"#BA7517","Middle Africa":"#534AB7"}
PAL_SIZE = {"Megacity":"#185FA5","Large City":"#378ADD","Medium-sized City":"#1D9E75",
            "Small City":"#5DCAA5","Very Small City":"#9FE1CB"}
PAL_TYP = {"Peripheralisation":"#185FA5","Fragmentation":"#1D9E75","Densification":"#534AB7",
           "Ribbon":"#BA7517","Leapfrog":"#D85A30"}
PAL_METHOD = {"Traditional":"#185FA5","Machine learning":"#1D9E75","Deep learning":"#D85A30"}
TYP = ["Peripheralisation","Fragmentation","Densification","Ribbon","Leapfrog"]
SIZES = ["Megacity","Large City","Medium-sized City","Small City","Very Small City"]
REGIONS = ["Northern Africa","Eastern Africa","Western Africa","Southern Africa","Middle Africa"]
PERIODS = ["2015-2018","2019-2022","2023-2025"]

plt.rcParams.update({
    "font.family":"DejaVu Sans","font.size":11,
    "axes.edgecolor":"#888888","axes.linewidth":0.8,
    "axes.titlesize":13,"axes.titleweight":"bold","axes.titlepad":12,
    "axes.grid":True,"grid.color":"#E6E6E6","grid.linewidth":0.8,
    "figure.dpi":150,"savefig.dpi":150,"savefig.bbox":"tight",
})

def load(path):
    rows=list(csv.DictReader(open(path,encoding="utf-8-sig")))
    def num(x):
        try: return float(x)
        except: return None
    for r in rows:
        p=num(r["population"])
        r["_size"]=("Unknown" if p is None else "Megacity" if p>10e6 else "Large City" if p>=5e6
                    else "Medium-sized City" if p>=1e6 else "Small City" if p>=250e3 else "Very Small City")
        sr=r["specific_region"].strip()
        r["_region"]="Unknown" if sr in ("Unknown","Western Africa, Middle Africa","") else sr
        y=num(r["pub_year"]); y=int(y) if y else None
        r["_period"]=("2015-2018" if y and 2015<=y<=2018 else "2019-2022" if y and 2019<=y<=2022
                      else "2023-2025" if y and 2023<=y<=2025 else None)
    return rows

def occ(sf):
    out=[]
    for p in re.split(r"[;,]",(sf or "").lower()):
        p=p.strip()
        if p.startswith("periphera"): out.append("Peripheralisation")
        elif p.startswith("fragmentation"): out.append("Fragmentation")
        elif p.startswith("densific"): out.append("Densification")
        elif p.startswith("ribbon"): out.append("Ribbon")
        elif p.startswith("leapfrog"): out.append("Leapfrog")
    return out

def style(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, loc="left")
    if xlabel is not None: ax.set_xlabel(xlabel)
    if ylabel is not None: ax.set_ylabel(ylabel)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.set_axisbelow(True)

rows = load(DATA)
N = len(rows)

# ============================ FIGURE 1 — temporal ============================
yrs=list(range(2015,2026))
tot=[sum(1 for r in rows if r["pub_year"]==str(y)) for y in yrs]
inf=[sum(1 for r in rows if r["pub_year"]==str(y) and r["informal_dev_bin"]=="1") for y in yrs]
fig,ax=plt.subplots(figsize=(10,5.2))
ax.bar(yrs,tot,width=0.72,color=C_BLUE,label="All studies")
ax.bar(yrs,inf,width=0.72,color=C_CORAL,label="Informal-settlement focus")
for x,v in zip(yrs,tot): ax.text(x,v+0.5,str(v),ha="center",va="bottom",fontsize=9,color="#444444")
ax.set_xticks(yrs); ax.set_ylim(0,max(tot)*1.14); ax.grid(axis="x",visible=False)
ax.legend(frameon=False,loc="upper left")
style(ax,"Figure 1 | Annual research output on African urban growth, 2015–2025",None,"Number of studies")
fig.savefig(os.path.join(FIG,"figure1_temporal.png")); plt.close(fig)

# ============================ FIGURE 2 — geographic (bars; map via R) ========
cc=Counter(r["country"] for r in rows if r["country"] not in ("Africa/Multiple","West Africa",""))
items=cc.most_common(20)[::-1]
fig,ax=plt.subplots(figsize=(9,7))
names=[k for k,_ in items]; vals=[v for _,v in items]
ax.barh(names,vals,color=C_BLUE,height=0.74)
for i,v in enumerate(vals): ax.text(v+0.3,i,str(v),va="center",fontsize=9,color="#444444")
ax.set_xlim(0,max(vals)*1.1); ax.grid(axis="y",visible=False)
style(ax,"Figure 2a | Studies per country (underlying the geographic choropleth)",
      "Number of studies",None)
fig.text(0.5,-0.02,"The manuscript renders this as an Africa choropleth; knit 00_main_analysis.Rmd in R for the map.",
         ha="center",fontsize=8,color="#777777")
fig.savefig(os.path.join(FIG,"figure2a_studies_by_country.png")); plt.close(fig)

byc=defaultdict(lambda:[0,0])  # country -> [informal, total]
for r in rows:
    c=r["country"]
    if c in ("Africa/Multiple","West Africa",""): continue
    byc[c][1]+=1; byc[c][0]+=1 if r["informal_dev_bin"]=="1" else 0
rate=[(c,inf/tot_) for c,(inf,tot_) in byc.items() if tot_>=3]
rate.sort(key=lambda t:t[1])
fig,ax=plt.subplots(figsize=(9,6))
names=[c for c,_ in rate]; vals=[v*100 for _,v in rate]
ax.barh(names,vals,color=C_CORAL,height=0.72)
for i,v in enumerate(vals): ax.text(v+0.6,i,f"{v:.0f}%",va="center",fontsize=9,color="#444444")
ax.set_xlim(0,max(vals)*1.18 if vals else 1); ax.grid(axis="y",visible=False)
style(ax,"Figure 2b | Informal-settlement focus rate by country (≥3 studies)","Share of studies (%)",None)
fig.savefig(os.path.join(FIG,"figure2b_informal_by_country.png")); plt.close(fig)

# ============================ FIGURE 3 — informal focus ======================
reg=[(rg,sum(1 for r in rows if r["_region"]==rg and r["informal_dev_bin"]=="1"),
         sum(1 for r in rows if r["_region"]==rg)) for rg in REGIONS]
reg=[(rg,i,t) for rg,i,t in reg if t>0]; reg.sort(key=lambda x:x[1]/x[2])
fig,ax=plt.subplots(figsize=(9,4.8))
names=[r[0] for r in reg]; vals=[r[1]/r[2]*100 for r in reg]
ax.barh(names,vals,color=[PAL_REGION[n] for n in names],height=0.68)
for i,(rg,inf_,t) in enumerate(reg):
    ax.text(vals[i]+0.5,i,f"{inf_}/{t} ({vals[i]:.1f}%)",va="center",fontsize=9,color="#444444")
ax.set_xlim(0,max(vals)*1.28); ax.grid(axis="y",visible=False)
style(ax,"Figure 3a | Informal-focused research by African sub-region","Informal-focus rate (%)",None)
fig.savefig(os.path.join(FIG,"figure3a_informal_by_region.png")); plt.close(fig)

sz=[(s,sum(1 for r in rows if r["_size"]==s and r["informal_dev_bin"]=="1"),
        sum(1 for r in rows if r["_size"]==s)) for s in SIZES]
sz=[(s,i,t) for s,i,t in sz if t>0]
fig,ax=plt.subplots(figsize=(9,5))
names=[s for s,_,_ in sz]; vals=[i/t*100 for _,i,t in sz]
ax.bar(names,vals,color=[PAL_SIZE[n] for n in names],width=0.68)
for i,v in enumerate(vals): ax.text(i,v+0.4,f"{v:.1f}%",ha="center",va="bottom",fontsize=9,color="#444444")
ax.set_ylim(0,max(vals)*1.16); ax.grid(axis="x",visible=False)
plt.setp(ax.get_xticklabels(),rotation=18,ha="right")
style(ax,"Figure 3b | Informal-focused studies by city-size class",None,"Informal-focus rate (%)")
fig.savefig(os.path.join(FIG,"figure3b_informal_by_citysize.png")); plt.close(fig)

# ============================ FIGURE 4 — methods by period ===================
def method_fig(col,title,fname):
    per={p:Counter() for p in PERIODS}
    for r in rows:
        m=r[col].strip()
        if r["_period"] and m: per[r["_period"]][m]+=1
    cats=[c for c in ["Traditional","Machine learning","Deep learning"] if any(per[p][c] for p in PERIODS)]
    fig,ax=plt.subplots(figsize=(8.5,5.2))
    bottoms=[0]*len(PERIODS)
    for c in cats:
        shares=[(per[p][c]/sum(per[p].values())*100 if sum(per[p].values()) else 0) for p in PERIODS]
        ax.bar(PERIODS,shares,bottom=bottoms,width=0.6,color=PAL_METHOD[c],label=c,edgecolor="white",linewidth=1.5)
        for i,(s,b) in enumerate(zip(shares,bottoms)):
            if s>=6: ax.text(i,b+s/2,f"{s:.0f}%",ha="center",va="center",color="white",fontsize=9,fontweight="bold")
        bottoms=[b+s for b,s in zip(bottoms,shares)]
    ax.set_ylim(0,100); ax.yaxis.set_major_formatter(PercentFormatter()); ax.grid(axis="x",visible=False)
    ax.legend(frameon=False,ncol=3,loc="upper center",bbox_to_anchor=(0.5,-0.08))
    style(ax,title,None,"Share of tasks")
    fig.savefig(os.path.join(FIG,fname)); plt.close(fig)
method_fig("mapping_method_type","Figure 4a | Methodological composition of mapping tasks, by period","figure4a_mapping_methods.png")
method_fig("projection_method_type","Figure 4b | Methodological composition of projection tasks, by period","figure4b_projection_methods.png")

# ============================ FIGURE 5 — spatial typology ====================
ov=Counter()
for r in rows:
    for o in occ(r["spatial_form"]): ov[o]+=1
totocc=sum(ov.values())
order=sorted(TYP,key=lambda k:-ov[k])
fig,ax=plt.subplots(figsize=(9,5.2))
vals=[ov[k]/totocc*100 for k in order]
ax.bar(order,vals,color=[PAL_TYP[k] for k in order],width=0.66)
for i,k in enumerate(order): ax.text(i,vals[i]+0.5,f"{vals[i]:.1f}%",ha="center",va="bottom",fontsize=10,color="#444444")
ax.set_ylim(0,max(vals)*1.14); ax.grid(axis="x",visible=False)
plt.setp(ax.get_xticklabels(),rotation=12)
style(ax,f"Figure 5a | Overall frequency of spatial typologies ({totocc} occurrences)",None,"Share of occurrences")
fig.savefig(os.path.join(FIG,"figure5a_typology_overall.png")); plt.close(fig)

byreg={rg:Counter() for rg in REGIONS}
for r in rows:
    if r["_region"] in byreg:
        for o in occ(r["spatial_form"]): byreg[r["_region"]][o]+=1
regs=[rg for rg in REGIONS if sum(byreg[rg].values())>0]
fig,ax=plt.subplots(figsize=(9.5,5.6))
bottoms=[0]*len(regs)
for t in TYP:
    shares=[(byreg[rg][t]/sum(byreg[rg].values())*100 if sum(byreg[rg].values()) else 0) for rg in regs]
    ax.bar(regs,shares,bottom=bottoms,width=0.62,color=PAL_TYP[t],label=t,edgecolor="white",linewidth=1.5)
    for i,(s,b) in enumerate(zip(shares,bottoms)):
        if s>=7: ax.text(i,b+s/2,f"{s:.0f}%",ha="center",va="center",color="white",fontsize=8.5,fontweight="bold")
    bottoms=[b+s for b,s in zip(bottoms,shares)]
ax.set_ylim(0,100); ax.yaxis.set_major_formatter(PercentFormatter()); ax.grid(axis="x",visible=False)
plt.setp(ax.get_xticklabels(),rotation=14,ha="right")
ax.legend(frameon=False,ncol=5,loc="upper center",bbox_to_anchor=(0.5,-0.10),fontsize=9)
style(ax,"Figure 5b | Spatial typology composition by sub-region",None,"Share of occurrences")
fig.savefig(os.path.join(FIG,"figure5b_typology_by_region.png")); plt.close(fig)

# ============================ TABLES =========================================
# Table 1 — typology by driver (keyword-occurrence)
CATS=[("Population growth and migration","migrat"),("Planning regulation","planning|regulat"),
      ("Road and transport expansion","road|transport|network"),("Economic development","econom"),
      ("Industrial activity","industr")]
t1=[]
for cat,pat in CATS:
    sub=[r for r in rows if re.search(pat,r["main_drivers"].lower())]
    c=Counter()
    for r in sub:
        for o in occ(r["spatial_form"]): c[o]+=1
    n=sum(c.values())
    t1.append([cat,n]+[round(c[k]/n*100,1) if n else 0.0 for k in TYP])
t1.sort(key=lambda r:-r[1])
with open(os.path.join(TAB,"table1_typology_by_driver.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Driver","Occurrences"]+TYP); w.writerows(t1)

# Table 2 — scenario themes (study counts from data; scenario counts from scenario-level coding)
def toint(x):
    try: return int(float(x))
    except: return 0
multi=[r for r in rows if toint(r["scenario_count"])>=2]
studies=Counter()
for r in multi:
    for th in [t.strip() for t in r["scenario_theme"].split(";") if t.strip()]: studies[th]+=1
SCEN={"BAU":15,"Planning, policy and infrastructure":23,"Ecological protection":10,"Population-driven / unconstrained":4}
order2=["BAU","Planning, policy and infrastructure","Ecological protection","Population-driven / unconstrained"]
with open(os.path.join(TAB,"table2_scenario_themes.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Scenario theme","Studies","Scenarios"])
    for th in order2: w.writerow([th,studies.get(th,0),SCEN[th]])
    w.writerow(["TOTAL",16,sum(SCEN.values())])

# Table S2 — hierarchy composition by period
with open(os.path.join(TAB,"tableS2_hierarchy_by_period.csv"),"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Period","n"]+SIZES)
    for p in PERIODS:
        sub=[r for r in rows if r["_period"]==p and r["_size"]!="Unknown"]
        n=len(sub); cnt=Counter(r["_size"] for r in sub)
        w.writerow([p,n]+[round(cnt[s]/n*100,1) if n else 0.0 for s in SIZES])

print("Wrote figures to", os.path.normpath(FIG))
print("Wrote tables to", os.path.normpath(TAB))
for fn in sorted(os.listdir(FIG)):
    if fn.endswith(".png"): print("  fig:", fn)
for fn in sorted(os.listdir(TAB)):
    if fn.endswith(".csv"): print("  tab:", fn)
