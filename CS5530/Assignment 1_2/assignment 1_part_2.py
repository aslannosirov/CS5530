import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Utility functions
plots_dir = Path("plots")
plots_dir.mkdir(parents=True, exist_ok=True)

def save_and_show(fig, fname):
    dpi = 300
    fig.set_size_inches(800/dpi, 600/dpi)
    fig.savefig(plots_dir / fname, dpi=dpi, bbox_inches="tight")
    plt.show()

# Step 1: Load Data
csv_path = Path("StudentsPerformance.csv")

if csv_path.exists():
    df = pd.read_csv(csv_path)
    print(f"Loaded dataset: {csv_path}")
else:
    print("No CSV found, using fallback sample dataset.")

# Step 2: Preprocessing

df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
score_cols = ["math_score","reading_score","writing_score"]

# Convert scores to numeric
for c in score_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Fill missing
for c in df.columns:
    if df[c].dtype == "object":
        df[c] = df[c].fillna(df[c].mode()[0])
    else:
        df[c] = df[c].fillna(df[c].mean())

# Normalize categories
df["test_preparation_course"] = df["test_preparation_course"].str.strip().str.lower()
df["lunch"] = df["lunch"].str.strip().str.lower()
df["gender"] = df["gender"].str.strip().str.lower()

# Add overall average
df["overall_avg"] = df[score_cols].mean(axis=1)

print("Preprocessing complete. Data shape:", df.shape)

# V1 — Gender boxplots (math vs reading)

fig1, ax1 = plt.subplots()
positions = []
labels = []
data_to_plot = []
pos = 1
for subj in ["math_score","reading_score"]:
    for g in df["gender"].unique():
        data_to_plot.append(df.loc[df["gender"]==g, subj].dropna().values)
        positions.append(pos)
        labels.append(f"{subj.split('_')[0].title()} ({g})")
        pos += 1
    pos += 0.5
ax1.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)
ax1.set_title("Gender differences: Math vs Reading")
ax1.set_ylabel("Score (0-100)")
ax1.set_xticks(positions)
ax1.set_xticklabels(labels, rotation=30, ha="right")
ax1.grid(axis="y", linestyle="--", linewidth=0.5)
save_and_show(fig1, "V1_gender_boxplots.png")

# V2 — Test prep impact on math

fig2, ax2 = plt.subplots()
prep_groups = df["test_preparation_course"].unique()
data_v2 = [df.loc[df["test_preparation_course"]==g, "math_score"].dropna().values for g in prep_groups]
ax2.boxplot(data_v2, labels=[g.title() for g in prep_groups], patch_artist=True)
ax2.set_title("Math scores by Test Preparation Course")
ax2.set_ylabel("Math score (0-100)")
ax2.grid(axis="y", linestyle="--", linewidth=0.5)
save_and_show(fig2, "V2_testprep_math.png")

# V3 — Lunch type and average performance

fig3, ax3 = plt.subplots()
lunch_groups = df["lunch"].unique()
means = [df.loc[df["lunch"]==lg, "overall_avg"].mean() for lg in lunch_groups]
x = np.arange(len(lunch_groups))
bars = ax3.bar(x, means, tick_label=[lg.title() for lg in lunch_groups])
ax3.set_title("Mean overall average score by Lunch type")
ax3.set_ylabel("Mean overall average (math, reading, writing)")
ax3.set_xlabel("Lunch type")
ax3.grid(axis="y", linestyle="--", linewidth=0.5)
for rect, m in zip(bars, means):
    ax3.annotate(f"{m:.1f}", xy=(rect.get_x() + rect.get_width()/2, rect.get_height()),
                 xytext=(0,3), textcoords="offset points", ha="center", va="bottom", fontsize=8)
save_and_show(fig3, "V3_lunch_mean_overall.png")

# V4 — Subject correlations

fig4, ax4 = plt.subplots()
corr = df[score_cols].corr()
cax = ax4.imshow(corr.values, vmin=-1, vmax=1, cmap="coolwarm")
ax4.set_xticks(range(len(score_cols)))
ax4.set_yticks(range(len(score_cols)))
ax4.set_xticklabels([c.split('_')[0].title() for c in score_cols])
ax4.set_yticklabels([c.split('_')[0].title() for c in score_cols])
for i in range(len(score_cols)):
    for j in range(len(score_cols)):
        ax4.text(j, i, f"{corr.values[i,j]:.2f}", ha="center", va="center", color="black")
ax4.set_title("Correlation heatmap: Math, Reading, Writing")
fig4.colorbar(cax, ax=ax4, fraction=0.046, pad=0.04)
save_and_show(fig4, "V4_subject_correlations.png")

# V5 — Math vs reading with trend lines by test prep

fig5, ax5 = plt.subplots()
colors = {"completed":"tab:blue", "none":"tab:orange"}
for g in df["test_preparation_course"].unique():
    sub = df[df["test_preparation_course"]==g]
    x = sub["reading_score"].values
    y = sub["math_score"].values
    ax5.scatter(x, y, label=f"{g.title()} (n={len(sub)})")
    if len(sub) >= 2:
        slope, intercept = np.polyfit(x, y, 1)
        xs = np.array([x.min(), x.max()])
        ys = slope*xs + intercept
        ax5.plot(xs, ys, linewidth=1.5)
ax5.set_xlabel("Reading score")
ax5.set_ylabel("Math score")
ax5.set_title("Math vs Reading with best-fit lines by Test Preparation Course")
ax5.legend()
ax5.grid(True, linestyle="--", linewidth=0.5)
save_and_show(fig5, "V5_math_vs_reading_trendlines.png")

print("All visualizations saved in 'plots' folder and also shown interactively.")
