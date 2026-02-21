
import sys


import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120


# ==============================================================================
# SECTION 1 – LOAD
# ==============================================================================

RAW_DATA_PATH   = "DataScience_salaries_2025.csv"
CLEAN_DATA_PATH = "clean_salary_dataset.csv"

print("=" * 70)
print(" CareerScout | Data Preparation & EDA")
print("=" * 70)

print(f"\n[1/5] Loading raw data from '{RAW_DATA_PATH}' ...")
df = pd.read_csv(RAW_DATA_PATH)

print(f"      Raw dataset shape : {df.shape[0]:,} rows × {df.shape[1]} columns")


# ==============================================================================
# SECTION 2 – INITIAL INSPECTION
# ==============================================================================

print("\n[2/5] Running initial dataset inspection ...")


print("\n── Schema ──────────────────────────────────────────────────────────────")
df.info()


print("\n── Descriptive Statistics ──────────────────────────────────────────────")
print(df.describe())

# --- Missing values -----------------------------------------------------------
missing     = df.isnull().sum()
pct_missing = (missing / len(df)) * 100

missing_report = pd.DataFrame({
    "Missing Values" : missing,
    "Percentage (%)" : pct_missing.round(2)
}).sort_values(by="Percentage (%)", ascending=False)

print("\n── Missing Values Report ───────────────────────────────────────────────")
print(missing_report)


# --- Salary range before cleaning --------------------------------------------
print("\n── Salary Summary (Before Cleaning) ───────────────────────────────────")
print(df["salary_in_usd"].describe())


# ==============================================================================
# SECTION 3 – DATA CLEANING  (Outlier Removal)
# ==============================================================================

print("\n[3/5] Cleaning data ...")

SALARY_CAP = 500_000   # USD – removes extreme outliers at the upper tail

rows_before = len(df)
df = df[df["salary_in_usd"] <= SALARY_CAP].reset_index(drop=True)
rows_after  = len(df)

print(f"      Rows removed (salary > ${SALARY_CAP:,}) : {rows_before - rows_after:,}")
print(f"      Clean dataset shape                     : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"      Max salary after cleaning               : ${df['salary_in_usd'].max():,}")


# ==============================================================================
# SECTION 4 – EXPLORATORY DATA ANALYSIS  (GroupBy Summaries)
# ==============================================================================

print("\n[4/5] Running EDA groupby analyses ...")

# --- 4a. Average salary by job title (Top 10) --------------------------------
top_jobs_by_salary = (
    df.groupby("job_title")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .round(0)
)
print("\n── Top 10 Highest-Paying Job Titles (Average USD) ──────────────────────")
print(top_jobs_by_salary.to_string())

# --- 4b. Average salary by experience level ----------------------------------
salary_by_experience = (
    df.groupby("experience_level")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .round(0)
)
print("\n── Average Salary by Experience Level ──────────────────────────────────")
print(salary_by_experience.to_string())
print("  (EN = Entry, MI = Mid, SE = Senior, EX = Executive)")

# --- 4c. Average salary by remote ratio --------------------------------------
salary_by_remote = (
    df.groupby("remote_ratio")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .round(0)
)
print("\n── Average Salary by Remote Ratio ──────────────────────────────────────")
print(salary_by_remote.to_string())
print("  (0 = On-site, 50 = Hybrid, 100 = Fully Remote)")

# --- 4d. Average salary by company location (Top 10) -------------------------
salary_by_location = (
    df.groupby("company_location")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .round(0)
)
print("\n── Top 10 Highest-Paying Company Locations (Average USD) ───────────────")
print(salary_by_location.to_string())


# ==============================================================================
# SECTION 5 – VISUALIZATIONS  (4 Figures)
# ==============================================================================

print("\n[5/5] Generating visualisations (4 plots) ...")

# ── Figure 1 : Salary Distribution Histogram ─────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(10, 5))

ax1.hist(df["salary_in_usd"], bins=50, color="steelblue", edgecolor="white")
ax1.set_title("Salary Distribution (USD)", fontsize=14, fontweight="bold")
ax1.set_xlabel("Salary (USD)")
ax1.set_ylabel("Frequency")
ax1.xaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x:,.0f}")
)

plt.tight_layout()
plt.savefig("fig1_salary_distribution.png")
plt.show()
print("      ✓ Figure 1 saved → fig1_salary_distribution.png")

# ── Figure 2 : Experience Level Count (Bar Chart) ────────────────────────────
fig2, ax2 = plt.subplots(figsize=(8, 5))

exp_counts = df["experience_level"].value_counts()
exp_counts.plot(kind="bar", ax=ax2, color="coral", edgecolor="white")

# Annotate bars with raw counts for quick reading
for bar in ax2.patches:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 200,
        f"{int(bar.get_height()):,}",
        ha="center", va="bottom", fontsize=9
    )

ax2.set_title("Experience Level Distribution", fontsize=14, fontweight="bold")
ax2.set_xlabel("Experience Level  (EN=Entry · MI=Mid · SE=Senior · EX=Executive)")
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.savefig("fig2_experience_level_count.png")
plt.show()
print("      ✓ Figure 2 saved → fig2_experience_level_count.png")

# ── Figure 3 : Top 10 Highest-Paying Job Titles (Bar Chart) ──────────────────
fig3, ax3 = plt.subplots(figsize=(12, 6))

top_jobs_by_salary.sort_values().plot(
    kind="barh", ax=ax3, color="mediumseagreen", edgecolor="white"
)

ax3.set_title("Top 10 Highest-Paying Job Titles", fontsize=14, fontweight="bold")
ax3.set_xlabel("Average Salary (USD)")
ax3.set_ylabel("Job Title")
ax3.xaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x:,.0f}")
)

plt.tight_layout()
plt.savefig("fig3_top10_jobs.png")
plt.show()
print("      ✓ Figure 3 saved → fig3_top10_jobs.png")

# ── Figure 4 : Salary vs. Experience Level (Box Plot) ────────────────────────
# Define a logical sort order for the x-axis labels
exp_order = ["EN", "MI", "SE", "EX"]

fig4, ax4 = plt.subplots(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="experience_level",
    y="salary_in_usd",
    order=exp_order,
    hue="experience_level",
    palette="Set2",
    legend=False,
    ax=ax4
)

ax4.set_title("Salary vs. Experience Level", fontsize=14, fontweight="bold")
ax4.set_xlabel("Experience Level  (EN=Entry · MI=Mid · SE=Senior · EX=Executive)")
ax4.set_ylabel("Salary (USD)")
ax4.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda y, _: f"${y:,.0f}")
)

plt.tight_layout()
plt.savefig("fig4_salary_vs_experience.png")
plt.show()
print("      ✓ Figure 4 saved → fig4_salary_vs_experience.png")


# ==============================================================================
# SECTION 6 – EXPORT CLEANED DATASET
# ==============================================================================

df.to_csv(CLEAN_DATA_PATH, index=False)
print(f"\n✅ Clean dataset exported → '{CLEAN_DATA_PATH}'")
print(f"   Final shape : {df.shape[0]:,} rows × {df.shape[1]} columns")
print("\n" + "=" * 70)
print(" EDA complete. Next step → run 2_model_training.py")
print("=" * 70)