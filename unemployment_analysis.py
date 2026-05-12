
# =============================================================
# UNEMPLOYMENT ANALYSIS
# Author: Sanjai KV | GitHub: sanjaikv2255
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Styling ──────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#f9f9f9",
    "axes.grid": True,
    "grid.color": "#e0e0e0",
    "grid.alpha": 0.6,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

COVID_COLOR  = "#e74c3c"
PRE_COLOR    = "#2ecc71"
ACCENT_COLOR = "#3498db"
REGION_COLORS = {
    "North":     "#4C72B0",
    "South":     "#DD8452",
    "East":      "#55A868",
    "West":      "#C44E52",
    "Northeast": "#8172B2",
}

print("=" * 58)
print("  UNEMPLOYMENT ANALYSIS IN INDIA — CodeAlpha Internship")
print("=" * 58)

# ── 1. Load & Clean ───────────────────────────────────────────
df1 = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")
df2 = pd.read_csv("Unemployment_in_India.csv")

# Clean column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Rename for consistency
df1.rename(columns={
    "Estimated Unemployment Rate (%)": "Unemployment_Rate",
    "Estimated Employed":              "Employed",
    "Estimated Labour Participation Rate (%)": "Labour_Participation",
}, inplace=True)

df2.rename(columns={
    "Estimated Unemployment Rate (%)": "Unemployment_Rate",
    "Estimated Employed":              "Employed",
    "Estimated Labour Participation Rate (%)": "Labour_Participation",
}, inplace=True)

# Strip whitespace from region names
df1["Region"] = df1["Region"].str.strip()
df2["Region"] = df2["Region"].str.strip()

# Parse dates
df1["Date"] = pd.to_datetime(df1["Date"].str.strip(), format="%d-%m-%Y")
df2["Date"] = pd.to_datetime(df2["Date"].str.strip(), format="%d-%m-%Y")

# Drop empty rows (df2 has trailing blank rows)
df2.dropna(subset=["Region", "Unemployment_Rate"], inplace=True)

# Add period label for Covid analysis (df1 covers Jan–Nov 2020)
df1["Period"] = df1["Date"].apply(lambda d: "During COVID" if d >= pd.Timestamp("2020-03-01") else "Pre-COVID")

print(f"\n📌 Dataset 1 (State-level 2020): {df1.shape[0]} rows, {df1['Region'].nunique()} states")
print(f"📌 Dataset 2 (India Rural/Urban 2019-2020): {df2.shape[0]} rows, {df2['Region'].nunique()} states")
print(f"\n📌 Date range (df1): {df1['Date'].min().date()} → {df1['Date'].max().date()}")
print(f"📌 Date range (df2): {df2['Date'].min().date()} → {df2['Date'].max().date()}")
print(f"\n📌 Missing values (df1): {df1['Unemployment_Rate'].isna().sum()}")
print(f"📌 Missing values (df2): {df2['Unemployment_Rate'].isna().sum()}")

print("\n📌 National Monthly Avg Unemployment Rate (2020):")
monthly = df1.groupby("Date")["Unemployment_Rate"].mean().round(2)
print(monthly.to_string())

# ── 2. Plot 1 — National Trend Line Chart ─────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly.index, monthly.values, color=ACCENT_COLOR, linewidth=2.5, marker="o", markersize=6, zorder=3)

# Shade COVID lockdown period
ax.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-06-01"),
           alpha=0.15, color=COVID_COLOR, label="Lockdown Period (Mar–Jun 2020)")
ax.axvline(pd.Timestamp("2020-03-25"), color=COVID_COLOR, linestyle="--", linewidth=1.2, alpha=0.8)

# Annotate peak
peak_date = monthly.idxmax()
peak_val  = monthly.max()
ax.annotate(f"Peak: {peak_val:.1f}%\n({peak_date.strftime('%b %Y')})",
            xy=(peak_date, peak_val),
            xytext=(peak_date + pd.Timedelta(days=10), peak_val - 3),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
            fontsize=10, color="black")

ax.set_title("National Unemployment Rate Trend — India 2020", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Unemployment Rate (%)", fontsize=11)
ax.legend(fontsize=10)
ax.fill_between(monthly.index, monthly.values, alpha=0.1, color=ACCENT_COLOR)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("plots/01_national_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n✅ Plot 1 saved: National Trend")

# ── 3. Plot 2 — Pre-COVID vs During COVID Bar Chart ───────────
pre   = df1[df1["Period"] == "Pre-COVID"]["Unemployment_Rate"].mean()
post  = df1[df1["Period"] == "During COVID"]["Unemployment_Rate"].mean()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: National comparison bar
ax = axes[0]
bars = ax.bar(["Pre-COVID\n(Jan–Feb 2020)", "During COVID\n(Mar–Nov 2020)"],
              [pre, post], color=[PRE_COLOR, COVID_COLOR], width=0.45, edgecolor="white")
for bar, val in zip(bars, [pre, post]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{val:.1f}%", ha="center", fontsize=13, fontweight="bold")
ax.set_title("National Avg: Pre vs During COVID", fontsize=12, fontweight="bold")
ax.set_ylabel("Avg Unemployment Rate (%)", fontsize=10)
ax.set_ylim(0, post * 1.3)

# Right: State-level comparison
state_comp = df1.groupby(["Region", "Period"])["Unemployment_Rate"].mean().unstack()
state_comp = state_comp.sort_values("During COVID", ascending=True).tail(12)

x = np.arange(len(state_comp))
w = 0.35
ax2 = axes[1]
ax2.barh(x - w/2, state_comp["Pre-COVID"], height=w, color=PRE_COLOR, alpha=0.85, label="Pre-COVID")
ax2.barh(x + w/2, state_comp["During COVID"], height=w, color=COVID_COLOR, alpha=0.85, label="During COVID")
ax2.set_yticks(x)
ax2.set_yticklabels(state_comp.index, fontsize=8)
ax2.set_xlabel("Avg Unemployment Rate (%)", fontsize=10)
ax2.set_title("Top 12 States: COVID Impact", fontsize=12, fontweight="bold")
ax2.legend(fontsize=9)

fig.suptitle("COVID-19 Impact on Unemployment", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("plots/02_covid_impact.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Plot 2 saved: COVID Impact")

# ── 4. Plot 3 — State-wise Avg Unemployment Bar Chart ─────────
state_avg = df1.groupby("Region")["Unemployment_Rate"].mean().sort_values(ascending=True)
region_map = df1[["Region", "Region.1"]].drop_duplicates().set_index("Region")["Region.1"].to_dict() \
    if "Region.1" in df1.columns else {}

fig, ax = plt.subplots(figsize=(12, 9))
colors = [REGION_COLORS.get(region_map.get(s, "North"), "#7f8c8d") for s in state_avg.index]
bars = ax.barh(state_avg.index, state_avg.values, color=colors, edgecolor="white", height=0.65)
for bar, val in zip(bars, state_avg.values):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=8.5)
ax.set_xlabel("Average Unemployment Rate (%)", fontsize=11)
ax.set_title("State-wise Average Unemployment Rate — 2020", fontsize=13, fontweight="bold", pad=12)
ax.axvline(state_avg.mean(), color="red", linestyle="--", linewidth=1.2, alpha=0.7, label=f"National Avg ({state_avg.mean():.1f}%)")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("plots/03_statewise_avg.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Plot 3 saved: State-wise Average")

# ── 5. Plot 4 — Monthly Heatmap (State × Month) ───────────────
pivot = df1.pivot_table(index="Region", columns="Date", values="Unemployment_Rate", aggfunc="mean")
pivot.columns = [d.strftime("%b %Y") for d in pivot.columns]

fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax,
            linewidths=0.3, annot_kws={"size": 7.5},
            cbar_kws={"label": "Unemployment Rate (%)", "shrink": 0.7})
ax.set_title("State × Month Unemployment Rate Heatmap", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Month", fontsize=10)
ax.set_ylabel("State", fontsize=10)
ax.tick_params(axis="x", rotation=30, labelsize=9)
ax.tick_params(axis="y", labelsize=8)
plt.tight_layout()
plt.savefig("plots/04_heatmap_state_month.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Plot 4 saved: Heatmap")

# ── 6. Plot 5 — Rural vs Urban Comparison (df2) ───────────────
if "Area" in df2.columns:
    ru = df2.groupby(["Date", "Area"])["Unemployment_Rate"].mean().unstack()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(ru.index, ru.get("Rural", []), color="#27ae60", linewidth=2.2, marker="o", markersize=5, label="Rural")
    ax.plot(ru.index, ru.get("Urban", []), color="#8e44ad", linewidth=2.2, marker="s", markersize=5, label="Urban")
    ax.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-06-01"),
               alpha=0.12, color=COVID_COLOR, label="Lockdown Period")
    ax.set_title("Rural vs Urban Unemployment Rate Trend", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Avg Unemployment Rate (%)", fontsize=11)
    ax.legend(fontsize=10)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("plots/05_rural_vs_urban.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✅ Plot 5 saved: Rural vs Urban")

# ── 7. Plot 6 — Labour Participation Rate vs Unemployment ─────
fig, ax = plt.subplots(figsize=(9, 6))
region_col = "Region.1" if "Region.1" in df1.columns else "Region"
unique_regions = df1[region_col].unique() if "Region.1" in df1.columns else ["All"]

scatter_colors = [REGION_COLORS.get(r, "#7f8c8d") for r in df1[region_col]] \
    if "Region.1" in df1.columns else [ACCENT_COLOR] * len(df1)

sc = ax.scatter(df1["Labour_Participation"], df1["Unemployment_Rate"],
                c=scatter_colors, alpha=0.65, s=45, edgecolors="white", linewidths=0.4)

# Regression line
z = np.polyfit(df1["Labour_Participation"].dropna(), df1["Unemployment_Rate"].dropna(), 1)
p = np.poly1d(z)
x_line = np.linspace(df1["Labour_Participation"].min(), df1["Labour_Participation"].max(), 100)
ax.plot(x_line, p(x_line), color="black", linestyle="--", linewidth=1.5, alpha=0.7, label="Trend")

if "Region.1" in df1.columns:
    patches = [mpatches.Patch(color=REGION_COLORS.get(r, "#7f8c8d"), label=r) for r in REGION_COLORS]
    ax.legend(handles=patches, title="Region", fontsize=9, title_fontsize=9)

ax.set_xlabel("Labour Participation Rate (%)", fontsize=11)
ax.set_ylabel("Unemployment Rate (%)", fontsize=11)
ax.set_title("Labour Participation vs Unemployment Rate", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("plots/06_participation_vs_unemployment.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Plot 6 saved: Participation vs Unemployment")

# ── 8. Summary ────────────────────────────────────────────────
print("\n" + "=" * 58)
print("  KEY INSIGHTS")
print("=" * 58)
print(f"\n  📈 Pre-COVID avg unemployment:    {pre:.2f}%")
print(f"  📈 During-COVID avg unemployment: {post:.2f}%")
print(f"  📈 COVID spike:                   +{post-pre:.2f} percentage points")
print(f"\n  🏆 Highest avg unemployment: {state_avg.idxmax()} ({state_avg.max():.1f}%)")
print(f"  ✅ Lowest avg unemployment:  {state_avg.idxmin()} ({state_avg.min():.1f}%)")
print(f"\n  📅 Peak national unemployment: {peak_date.strftime('%B %Y')} ({peak_val:.1f}%)")
print("\n  📌 All 6 plots saved to /plots/")
print("\n  ✅ Task 2 Complete! Ready for GitHub.\n")
