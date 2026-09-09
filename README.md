# 🏃‍♂️ Garmin Telemetry & Performance Analytics Pipeline

## 📌 Executive Summary
This portfolio project implements an end-to-end data analytics pipeline leveraging **DuckDB**, **Plotly**, and **Streamlit** to visualize multi-year Garmin training telemetry (2019–2026). The system transforms unorganized activity records into structured analytical views, highlighting macro volume progression, cardiovascular intensity distributions, and Acute-to-Chronic Workload Ratio (ACWR) fatigue trends.

---

## 💡 Key Analytical Takeaways

* **Multi-Discipline Periodization:** Annual duration analysis demonstrates a clear progression from single-sport training to balanced multi-sport volume across Running, Cycling, Swimming, and Strength.
* **Aerobic Efficiency Control:** Heart rate distribution box plots confirm that high-volume disciplines maintain an optimal Zone 2 cardiovascular profile, preserving high-intensity efforts for target workouts.
* **Data-Driven Load Governance:** 2025+ ACWR telemetry tracking isolates 7-day acute fatigue spikes relative to 28-day chronic fitness baselines, preventing overtraining injuries.

## 📌 Business & Analytical Problem
As training volume scales across multiple disciplines (Running, Cycling, Swimming), monitoring workload progression is critical to optimizing performance while mitigating overtraining and injury risks. 

This project establishes an automated pipeline to:
1. Standardize and aggregate raw, unstructured Garmin telemetry into clean, SQL-queryable formats.
2. Calculate the **Acute-to-Chronic Workload Ratio (ACWR)** (7-day fatigue vs. 28-day fitness rolling averages).
3. Visualize performance and training load trends across multi-year training blocks.

---

## 🏗️ Architecture & Technical Stack

* **Data Processing & ETL:** Python (`pandas`, `numpy`)
* **Analytical Engine:** `duckdb` (SQL Window Functions & Aggregations)
* **Visualizations:** `plotly` (Interactive dual-axis time-series)
* **Storage:** In-memory DuckDB database + localized CSVs

---

## 🧠 Data Governance & Engineering Decision Log

| Feature / Metric | Issue / Edge Case Identified | Engineering / Analytics Decision | Technical Rationale |
| :--- | :--- | :--- | :--- |
| **Activity Categorization** | 17 granular Garmin activity types (`indoor_cycling`, `road_biking`, `lap_swimming`) created excessive reporting noise. | Mapped raw API keys into 6 standardized `activity_group` categories in Pandas. | Aggregates volume into clear discipline buckets (`Cycling`, `Running`, `Swimming`, `Strength & Cardio`, `Walking`, `Other`) for executive reporting. |
| **ACWR Time Window** | Raw data spans 2019–Present, but numerical `training_load` was only captured starting in 2025. | Applied dynamic SQL filtering (`WHERE training_load > 0`) in DuckDB views to isolate the continuous tracking period (2025–Present). | ACWR requires continuous 28-day chronic rolling windows. Plotting multi-year zero-load gaps distorts moving averages and dilutes fatigue insights. |
| **Database Engine Selection** | System disk constraints prevented installing heavy local database servers. | Embedded **DuckDB** and **SQLite** directly inside the Python execution context. | Zero disk footprint, fast execution for local analytical workloads, and seamless integration with Pandas DataFrames. |

---

## 📊 Key Analytics & Insights

### 1. High-Level Discipline Performance
* **Total Volumes:** Summarized workouts, mileage, total hours, and average heart-rate response by `activity_group`.
* **Discipline Aggregations:** Managed through persistent SQL views inside DuckDB (`v_discipline_summary`).

### 2. Workload Progression (ACWR)
* **7-Day Acute Load (Fatigue):** Captures short-term physiological stress.
* **28-Day Chronic Load (Fitness):** Captures historical baseline fitness.
* **Sweet Spot Monitoring:** Tracks ratio against the safe target zone (`0.8 – 1.3`).

---

## 🚀 How to Run This Project Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/garmin-analytics-pipeline.git](https://github.com/your-username/garmin-analytics-pipeline.git)
   cd garmin-analytics-pipeline
   
Install dependencies:

Bash
pip install pandas duckdb plotly
Execute notebook:
Launch jupyter lab or jupyter notebook and run all cells to execute the DuckDB pipeline and generate Plotly charts.

| **Multi-Year Volume Aggregation** | Multi-year historical data (2019–2024) lacks `training_load` telemetry for ACWR calculations. | Created a secondary DuckDB view (`v_yearly_volume`) isolating volume metrics (`total_miles`, `total_hours`, `avg_heart_rate`) across all years. | Preserves the full multi-year history for macro-level volume reporting without compromising the mathematical rigor of the 2025+ ACWR workload model. |

| **Multi-Year Visualization Choice** | Combining discrete activities across 6+ years can result in visual clutter or unreadable line charts. | Implemented a stacked annual bar chart segmented by `activity_group` using Plotly. | Clear, high-level visualization of macro training volume shifts across years without visual overcrowding. |

| **Dependency Resolution (`llvmlite`)** | Environment error missing `libllvmlite.dylib` binary required for telemetry visualization packages. | Force-reinstalled `llvmlite` and `numba` binaries via environment package manager (`conda-forge`). | Ensures environment stability and reproducible execution across different local Python environments. |

| **Visualization Rendering Engine** | Conda environment error (`libllvmlite.dylib`) caused by broken optional C++ backends in `plotly.express`. | Migrated volume aggregation visual to native `plotly.graph_objects` (`go.Bar`). | Decouples visual reporting from heavy C++ dependencies (`llvmlite`/`numba`), ensuring lightweight execution across standard Python runtime environments. |

| **X-Axis Categorical Ordering** | Discrete grouping traces in `plotly.graph_objects` rendered chronological years out of sequence. | Cast `training_year` to explicit integer types in DuckDB and configured `categoryorder="category ascending"` on the Plotly layout. | Guarantees strictly chronological multi-year rendering across discrete categorical bar traces. |

| **Non-Spatial Activity Aggregation** | Strength & Cardio activities record zero spatial distance (`distance_miles = 0`), rendering them invisible on mileage-based bar charts. | Built dual aggregation metrics in DuckDB (`v_yearly_volume`) and switched macro volume visual to Time (`total_hours`). | Ensures non-distance-based workouts (weightlifting, cardio) are accurately captured in multi-discipline volume reporting. |

| **Visual Numeric Precision** | Floating-point duration values created visual clutter on stacked bar text labels. | Applied integer casting (`astype(int)`) and SQL `ROUND(..., 0)` to duration aggregations. | Optimizes chart readability and scannability for executive dashboard consumption. |

| **Tooltip Formatting (`hovertemplate`)** | Unified Plotly hover tooltips duplicated numbers by displaying both bar `text` labels and raw `y` values. | Defined custom `hovertemplate="%{y} hrs<extra></extra>"` on `go.Bar` traces. | Eliminates redundant text in interactive tooltips, ensuring clean user experience on dashboard hover. |

| **Interactive Dashboard Framework** | Static notebook visuals limit user ability to filter by discipline or isolate specific load periods. | Built a multi-tab Streamlit dashboard (`app.py`) powered by cached DuckDB connections (`@st.cache_resource`). | Provides responsive, interactive querying (discipline multi-selects, dynamic KPI metrics, and tabbed analytical views) for executive review. |

| **Headless Server Deployment** | First-time Streamlit initialization halts process execution while waiting for interactive email prompt input. | Added `--server.headless true` flag to server execution commands. | Bypasses interactive prompts to enable automated, non-blocking background server deployment. |

| **Visual Library Synchronization** | Executing `app.py` under the global system interpreter triggered a missing `plotly` dependency (`ModuleNotFoundError`). | Installed `plotly` alongside runtime dependencies via `pip`. | Secures complete environment parity so dashboard rendering engines function seamlessly outside of Jupyter. |

| **Storytelling & Telemetry Visuals** | Raw chart metrics lacked analytical context and narrative flow for portfolio review. | Integrated narrative callouts, 3-tab storytelling hierarchy, and a Heart Rate vs. Duration intensity scatter plot (`px.scatter`). | Transforms standard telemetry dashboard into an analytical story covering volume trends, cardiovascular stress, and ACWR fatigue balance. |

| **Notebook Engine Compatibility** | `plotly.express` imports failed in Jupyter due to environment-level `llvmlite` dynamic library link errors. | Standardized all interactive visual testing to `plotly.graph_objects` (`go.Scatter`). | Ensures seamless visual rendering across both Jupyter notebook sessions and Streamlit app deployments without extra C++ binary dependencies. |

| **Visual Encoding & Scaling** | Aggregated bubble chart scaling (`sizeref`) created distorted visuals due to high total volume variance. | Refactored telemetry visual to a Box Plot (`go.Box`) showing heart rate distributions (mean, median, interquartile ranges). | Provides clear cardiovascular stress profiling per discipline while preventing visual distortion. |

| **Ironman Telemetry Focus** | General volume trends lacked specificity around targeted long-distance triathlon prep. | Isolated 2025–2026 records in DuckDB (`v_ironman_build`) and aggregated weekly swim/bike/run build metrics. | Highlights peak training weeks, race build cycles, and discipline periodization for triathlon performance analysis. |

| **Ironman & 70.3 Analytics Expansion** | Basic weekly totals did not isolate race-specific preparation metrics such as brick sessions or peak session distance ramps. | Created `v_ironman_build` view, integrated a Peak Long Session Ramp visual (`go.Scatter`), and built a SQL query to isolate same-day multi-sport brick workouts. | Delivers sports science metrics tailored to long-course triathlon prep, highlighting peak endurance ramping and race-day specificity. |

| **SQL Syntax Compatibility** | Backtick syntax (`` `...` ``) in DuckDB column aliasing threw a `ParserException`. | Replaced backticks with ANSI SQL-compliant double quotes (`"..."`) for column names containing spaces. | Ensures robust query parsing across DuckDB engines. |