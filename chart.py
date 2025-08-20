# chart.py
# Author: Data Scientist
# Email: 23f2004422@ds.study.iitm.ac.in

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# -----------------------------
# 1. Generate synthetic data
# -----------------------------
np.random.seed(42)

months = pd.date_range("2023-01-01", periods=12, freq="M")
categories = ["Electronics", "Clothing", "Groceries"]

data = []
for cat in categories:
    base = np.linspace(20000, 35000, 12)  # upward seasonal trend
    noise = np.random.normal(0, 1500, 12)  # random fluctuations
    seasonality = 3000 * np.sin(np.linspace(0, 2 * np.pi, 12))  # seasonal effect
    revenue = base + seasonality + noise
    for m, r in zip(months, revenue):
        data.append([m, r, cat])

df = pd.DataFrame(data, columns=["Month", "Revenue", "Category"])

# -----------------------------
# 2. Set Seaborn style
# -----------------------------
sns.set_style("whitegrid")
sns.set_context("talk")  # presentation-friendly text sizes

# -----------------------------
# 3. Create lineplot
# -----------------------------
plt.figure(figsize=(8, 8))  # ensures 512x512 output with dpi=64

sns.lineplot(
    data=df,
    x="Month",
    y="Revenue",
    hue="Category",
    palette="tab10",
    linewidth=2.5,
    marker="o"
)

# -----------------------------
# 4. Customize chart
# -----------------------------
plt.title("Seasonal Revenue Trends (Synthetic Data)", fontsize=18, weight="bold")
plt.xlabel("Month")
plt.ylabel("Revenue (USD)")
plt.xticks(rotation=45)

# -----------------------------
# 5. Save chart
# -----------------------------
plt.tight_layout()
plt.savefig("chart.png", dpi=64, bbox_inches="tight")  # 512x512
plt.close()
