#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ===== FORCE ARIAL BLACK, SIZE 10 =====
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["font.weight"] = "black"
mpl.rcParams["font.size"] = 10
mpl.rcParams["axes.labelweight"] = "black"
mpl.rcParams["axes.titleweight"] = "black"
mpl.rcParams["axes.titlesize"] = 10
mpl.rcParams["axes.labelsize"] = 10
mpl.rcParams["xtick.labelsize"] = 10
mpl.rcParams["ytick.labelsize"] = 10

INFILE = "results/tables/merops_family_top25.tsv"
OUTPNG = "results/figures/MEROPS_family_barplot_top25_familyColors_ArialBlack_1000dpi.png"
OUTPDF = "results/figures/MEROPS_family_barplot_top25_familyColors_ArialBlack.pdf"

df = pd.read_csv(INFILE, sep="\t")

# Sort ascending so the largest ends up on top in barh
df = df.sort_values("Count", ascending=True).reset_index(drop=True)

# Labels shown on y-axis
df["Label"] = df["Family"].astype(str) + " (" + df["Catalytic_type"].astype(str) + ")"

# ---- Color map: one color per family (categorical) ----
families = df["Family"].astype(str).tolist()

# tab20 has 20 distinct colors; for >20 families we cycle
cmap = plt.get_cmap("tab20")
family_to_color = {fam: cmap(i % cmap.N) for i, fam in enumerate(sorted(set(families)))}
colors = [family_to_color[f] for f in families]

plt.figure(figsize=(10, 7))
bars = plt.barh(df["Label"], df["Count"], color=colors)

plt.xlabel("Number of proteins")
plt.ylabel("MEROPS family (catalytic type)")
plt.title("MEROPS peptidase family composition (Top 25)")

# Optional: add a compact legend mapping family -> color
# For Top 25, legend can get crowded; comment out if you don't want it.
handles = []
labels = []
for fam in sorted(set(families)):
    handles.append(mpl.patches.Patch(color=family_to_color[fam]))
    labels.append(fam)
plt.legend(handles, labels, title="MEROPS family", fontsize=8, title_fontsize=9,
           loc="lower right", frameon=False)

plt.tight_layout()
plt.savefig(OUTPNG, dpi=1000, bbox_inches="tight")
plt.savefig(OUTPDF, bbox_inches="tight")
plt.close()

print(f"Wrote: {OUTPNG}")
print(f"Wrote: {OUTPDF}")
