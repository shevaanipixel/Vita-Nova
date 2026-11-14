"""
Vita Nova - small demo of the personal-baseline health check idea.
IMPORTANT: all data here is SIMULATED (made up by us). No real astronaut or patient data is used.

Idea: learn what is "normal" for ONE astronaut in the first week, then flag days
that drift away from that personal baseline in a bad direction.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(7)
DAYS = 21

# ---- 1. make simulated daily data -------------------------------------------
day = np.arange(1, DAYS + 1)
rest_hr  = np.random.normal(62, 1.3, DAYS)    # resting heart rate (bpm)
sleep_h  = np.random.normal(7.2, 0.35, DAYS)  # sleep (hours)
mood     = np.random.normal(7.6, 0.45, DAYS)  # daily self check-in mood (1-10)
exercise = np.random.normal(120, 8, DAYS)     # exercise minutes

# we deliberately add a "stress period" on days 12-17 so we can test the detector
for i, d in enumerate(range(12, 18)):
    strength = min(1.0, (i + 1) / 3)          # builds up over 3 days
    rest_hr[d - 1]  += 7.5 * strength
    sleep_h[d - 1]  -= 1.7 * strength
    mood[d - 1]     -= 2.3 * strength
    exercise[d - 1] -= 35 * strength

df = pd.DataFrame({"day": day, "rest_hr": rest_hr, "sleep_h": sleep_h,
                   "mood": mood, "exercise": exercise})

# ---- 2. personal baseline from the first 7 days ------------------------------
base = df.iloc[:7]
bad_direction = {"rest_hr": +1, "sleep_h": -1, "mood": -1, "exercise": -1}  # +1 = higher is worse
for col, sign in bad_direction.items():
    z = (df[col] - base[col].mean()) / base[col].std()
    df["z_" + col] = z * sign          # positive number = moving in the bad direction

# ---- 3. simple risk score and status -----------------------------------------
zcols = ["z_" + c for c in bad_direction]
df["risk"] = df[zcols].clip(lower=0).mean(axis=1)
def status(r):
    if r >= 3.0: return "ALERT"
    if r >= 1.8: return "WATCH"
    return "OK"
df["status"] = df["risk"].apply(status)

print(df[["day", "rest_hr", "sleep_h", "mood", "exercise", "risk", "status"]].round(2).to_string(index=False))
df.round(3).to_csv("simulated_results.csv", index=False)

# ---- 4. chart -----------------------------------------------------------------
NAVY, TEAL, AMBER, RED, GREY = "#0B1530", "#14A89A", "#F5A623", "#D64545", "#8A93A6"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(2, 2, figsize=(11, 5.2), dpi=200)
panels = [(ax[0, 0], "rest_hr", "Resting heart rate (bpm)"),
          (ax[0, 1], "sleep_h", "Sleep (hours)"),
          (ax[1, 0], "mood", "Mood check-in (1-10)")]
for a, col, title in panels:
    a.plot(df.day, df[col], color=NAVY, lw=2, marker="o", ms=3.5)
    a.axhspan(base[col].mean() - base[col].std(), base[col].mean() + base[col].std(), color=TEAL, alpha=0.15)
    a.axvspan(12, 17, color=AMBER, alpha=0.15)
    a.set_title(title, fontsize=10.5, loc="left", color=NAVY, fontweight="bold")
    a.tick_params(labelsize=8)
a = ax[1, 1]
colors = [RED if s == "ALERT" else AMBER if s == "WATCH" else TEAL for s in df.status]
a.bar(df.day, df.risk, color=colors)
a.axhline(1.8, color=AMBER, ls="--", lw=1); a.axhline(3.0, color=RED, ls="--", lw=1)
a.set_title("Vita Nova risk score (OK / WATCH / ALERT)", fontsize=10.5, loc="left", color=NAVY, fontweight="bold")
a.tick_params(labelsize=8)
for x in ax[1]: x.set_xlabel("Mission day", fontsize=8.5)
fig.text(0.01, 0.005, "Simulated data. Green band = personal baseline (first 7 days). Orange area = simulated stress period.",
         fontsize=7.5, color=GREY)
plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig("demo_chart.png")
print("saved chart")
