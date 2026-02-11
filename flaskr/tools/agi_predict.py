import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from datetime import datetime, timedelta

# Data Points (Date, Score, Model)
data = [
    {"date": "2025-01-24", "score": 8.12, "model": "o1 Pro"},
    {"date": "2025-02-03", "score": 26.6, "model": "Deep Research"},
    {"date": "2025-11-19", "score": 45.8, "model": "Gemini 3 Pro"},
    {"date": "2025-12-10", "score": 48.1, "model": "Zoom AI"},
    {"date": "2026-01-25", "score": 52.15, "model": "Sup AI"},
]

df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"])
start_date = df["date"].min()
df["days"] = (df["date"] - start_date).dt.days


# Define Logistic Function with L=100 fixed
def logistic_fixed_L(x, k, x0):
    return 100 / (1 + np.exp(-k * (x - x0)))


# Fit the curve
popt, _ = curve_fit(
    logistic_fixed_L, df["days"], df["score"], p0=[0.005, 300], maxfev=5000
)

# Generate Prediction Line
future_days = np.arange(0, 1500, 10)  # ~4 years
predicted_scores = logistic_fixed_L(future_days, *popt)
predicted_dates = [start_date + timedelta(days=int(d)) for d in future_days]

# Find dates for 90% (Human Expert) and 99% (Near Perfect)
try:
    idx_90 = np.where(predicted_scores >= 90)[0][0]
    date_90 = predicted_dates[idx_90]
except IndexError:
    date_90 = None

try:
    idx_99 = np.where(predicted_scores >= 99)[0][0]
    date_99 = predicted_dates[idx_99]
except IndexError:
    date_99 = None

# Plotting
plt.figure(figsize=(12, 7))

# Plot historical data
plt.scatter(df["date"], df["score"], color="blue", zorder=5, label="SOTA Models")

# Annotate models
for i, row in df.iterrows():
    plt.annotate(
        f"{row['model']}\n({row['score']}%)",
        (row["date"], row["score"]),
        xytext=(10, -10),
        textcoords="offset points",
        fontsize=9,
    )

# Plot prediction curve
plt.plot(
    predicted_dates, predicted_scores, "r--", label="Logistic Prediction", alpha=0.7
)

# Add reference lines
plt.axhline(y=90, color="green", linestyle=":", label="Human Expert Level (90%)")
plt.axhline(
    y=100, color="black", linestyle="-", linewidth=1, label="Perfect Score (100%)"
)

# Mark prediction dates
if date_90:
    plt.scatter([date_90], [90], color="green", zorder=5)
    plt.annotate(
        f"Hit 90%\n{date_90.strftime('%b %Y')}",
        (date_90, 90),
        xytext=(-60, 20),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->"),
    )

if date_99:
    plt.scatter([date_99], [99], color="purple", zorder=5)
    plt.annotate(
        f"Hit 99% (~100%)\n{date_99.strftime('%b %Y')}",
        (date_99, 99),
        xytext=(-80, -30),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->"),
    )

plt.title("Humanity's Last Exam (HLE) - Path to 100% (AGI)")
plt.xlabel("Year")
plt.ylabel("Score (%)")
plt.ylim(0, 105)
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# plt.savefig("hle_agi_prediction.png")
