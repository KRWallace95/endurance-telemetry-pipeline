# Changelog & Design Iterations

All notable changes and technical design decisions for the Triathlon Telemetry Dashboard.

## [v1.2.0] - Visual Refinements & Granular Progression - 2026-09-23

### Added
- **Visual 3C (Discipline Distance Profiles):** Integrated unit-aware custom distance calculations (Miles for Cycling/Running, Yards for Swimming).
- **LOWESS Trendlines:** Added locally weighted scatterplot smoothing (`trendline='lowess'`) to highlight progressive overload trajectories while dampening short-session noise.
- **Narrative Callouts:** Integrated executive takeaway callout boxes (`st.info`) beneath each chapter in `app.py`.

### Fixed
- **Trace-Label Drift:** Fixed Plotly custom data binding issue by passing `custom_data=['unit_label']` directly within `px.scatter()` parameters to prevent "Yards" labels from appearing on cycling traces.
- **Environment Dependencies:** Added `statsmodels` to project requirements for LOWESS calculation support.

---

## [v1.1.0] - Data Pipeline & Streamlit Porting - 2026-09-22

### Added
- **Path-Agnostic Data Loader:** Standardized `load_data()` using Python's `Path(__file__)` to ensure robust CSV resolution regardless of execution context.
- **Chapter 2 Proportional Stacked Charts:** Computed percentage volume shares directly via Pandas transformation (`transform('sum')`) to maintain compatibility across Plotly versions.

### Fixed
- **Missing Temporal Weeks:** Handled zero-activity weeks in cadence calculations by unstacking frequency matrices with `fill_value=0`.

---

## [v1.0.0] - Initial EDA & Macro Framing - 2026-09-21

### Added
- **Garmin Connect ETL Pipeline:** Standardized raw exported telemetry into `df_clean.csv`.
- **Chapter 1 Macro Volume:** Implemented stacked monthly duration bars and 4-week moving average cadence line charts.
- **Chapter 2 Discipline Share:** Generated overall volume donut charts.
