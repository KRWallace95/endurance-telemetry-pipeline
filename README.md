# Garmin Telemetry: Periodization & Progression Dashboard

An end-to-end telemetry analytics pipeline and interactive Streamlit application exploring multi-year triathlon training data. This project analyzes volume periodization, discipline specific gravity, session distribution, and long-term progressive overload across cycling, running, and swimming[cite: 1].

---

## Dashboard Overview

The application is structured into a narrative 3-chapter analytical flow[cite: 1]:

1. **Chapter 1: Macro Volume & Cadence**[cite: 1]
   * *Monthly Duration Stacked Bar:* Tracks macro volume progression (20–50+ hrs/month)[cite: 1].
   * *4-Week Moving Average Cadence:* Monitors discipline frequency shifts and workout consistency[cite: 1].
2. **Chapter 2: Discipline Balance & Proportions**[cite: 1]
   * *Volume Share Donut Chart:* Highlights cumulative time allocation across disciplines[cite: 1].
   * *100% Stacked Monthly Proportions:* Visualizes phase transitions (e.g., run-heavy base vs. bike-dominant build blocks)[cite: 1].
3. **Chapter 3: Granular Session Profiles**[cite: 1]
   * *Session Duration Box Plots:* Identifies session duration spread and outlier long efforts[cite: 1].
   * *Faceted Distance Progression:* Unit-aware scatter profiles (Miles & Yards) with LOWESS trendlines proving multi-year progressive overload[cite: 1].

---

## Architecture & Tech Stack

* **Data Processing & Transformations:** Python, Pandas, NumPy[cite: 1]
* **Data Visualization:** Plotly Express (`statsmodels` for LOWESS trendlines)[cite: 1]
* **Web Dashboard:** Streamlit[cite: 1]
* **Environment & Package Management:** Virtualenv / Pip[cite: 1]

---

## Quickstart & Local Setup

### 1. Clone Repository & Setup Environment
```bash
git clone [https://github.com/your-username/triathlon-telemetry-pipeline.git](https://github.com/your-username/triathlon-telemetry-pipeline.git)
cd triathlon-telemetry-pipeline

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

