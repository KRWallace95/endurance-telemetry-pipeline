# Garmin Telemetry: Periodization & Progression Dashboard

An end-to-end telemetry analytics pipeline and interactive Streamlit application exploring multi-year triathlon training data. This project analyzes volume periodization, discipline specific gravity, session distribution, and long-term progressive overload across cycling, running, and swimming.

---

## Dashboard Overview

The application is structured into a narrative 3-chapter analytical flow:

1. **Chapter 1: Macro Volume & Cadence**
   * *Monthly Duration Stacked Bar:* Tracks macro volume progression (20–50+ hrs/month).
   * *4-Week Moving Average Cadence:* Monitors discipline frequency shifts and workout consistency.
2. **Chapter 2: Discipline Balance & Proportions**
   * *Volume Share Donut Chart:* Highlights cumulative time allocation across disciplines.
   * *100% Stacked Monthly Proportions:* Visualizes phase transitions (e.g., run-heavy base vs. bike-dominant build blocks).
3. **Chapter 3: Granular Session Profiles**
   * *Session Duration Box Plots:* Identifies session duration spread and outlier long efforts.
   * *Faceted Distance Progression:* Unit-aware scatter profiles (Miles & Yards) with LOWESS trendlines proving multi-year progressive overload.

---

## Architecture & Tech Stack

* **Data Processing & Transformations:** Python, Pandas, NumPy
* **Data Visualization:** Plotly Express (`statsmodels` for LOWESS trendlines)
* **Web Dashboard:** Streamlit
* **Environment & Package Management:** Virtualenv / Pip

---

## Quickstart & Local Setup

### 1. Clone Repository & Setup Environment
```bash
git clone [https://github.com/your-username/triathlon-telemetry-pipeline.git](https://github.com/your-username/triathlon-telemetry-pipeline.git)
cd triathlon-telemetry-pipeline

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

