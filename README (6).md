# Vita Nova

NASA Space Apps Challenge 2026 | Challenge: Create Health Monitoring Software for Astronauts on Space Missions

**Team Vita Nova:** Shevaani AP, Supraja G, Nivetha P, Tejeswini D

## What is Vita Nova?

Vita Nova is a software concept that helps an astronaut notice health changes early on long space missions. Each day it takes four simple signals: resting heart rate, sleep hours, exercise time and a short mood check-in. It learns what is normal for that astronaut in the first 7 days and then flags changes that move in a worrying direction. It shows a simple OK / WATCH / ALERT status (WATCH above 1.8, ALERT above 3.0) with a short reason. Vita Nova supports decisions, it does not diagnose.

## What is in this repository

| File | What it is |
|---|---|
| `Vita_Nova_Demo_7_Slides.pdf` | 7-slide project demonstration |
| `Vita_Nova_NASA_Space_Apps_2026.pdf` | Full 10-slide presentation |
| `Vita_Nova_Abstract_and_Description.pdf` | Abstract, objective, feasibility, what is done, future implementation |
| `vita_nova_demo.py` | Python demo on simulated data |

## About the demo

`vita_nova_demo.py` simulates 21 mission days for one astronaut. Days 12 to 17 are made stressful on purpose (higher heart rate, less sleep, lower mood, less exercise). The system raises an ALERT on day 13 and returns to OK on day 18.

**The data is simulated. This is a proof of concept, not a medical tool, and it has not been tested on real people.**

To run it:

```
pip install numpy pandas matplotlib
python vita_nova_demo.py
```

It prints a table and saves `demo_chart.png` and `simulated_results.csv`.
