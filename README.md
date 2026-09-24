# Garmin Telemetry: Periodization & Progression Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://triathlon-telemetry-pipeline.streamlit.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/your-username/triathlon-telemetry-pipeline)

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
```

### 2. Install Dependencies
```Bash
pip install -r requirements.txt
```

### 3. Ingestion Notebook & Credentials Setup (.env)
The interactive Streamlit dashboard runs out-of-the-box using pre-cleaned telemetry (df_clean.csv).

However, if you wish to run 01_data_ingestion_and_cleaning.ipynb to fetch and process your own raw Garmin Connect data, set up your credentials as follows:

Create your .env file from the example template:

```Bash
cp .env.example .env
```

Open .env and enter your Garmin Connect credentials:
```
Plaintext
GARMIN_EMAIL="your_email@example.com"
GARMIN_PASSWORD="your_password"
Install python-dotenv:
Ensure python-dotenv is installed (included in requirements.txt). The notebook automatically loads these variables via load_dotenv().
```

### 4. Run Streamlit Application
```Bash
streamlit run app.py
```

The application will open automatically in your browser at http://localhost:8501.

### Repository Structure
```Plaintext
├── app.py              # Main Streamlit interactive dashboard
├── df_clean.csv        # Standardized Garmin activity telemetry dataset
├── CHANGELOG.md        # Detailed engineering and visual design iteration logs
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable template for notebook ETL
└── README.md           # Project documentation
```