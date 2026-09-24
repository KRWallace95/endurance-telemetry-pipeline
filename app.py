import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import streamlit as st


# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Triathlon Telemetry Dashboard",
    page_icon="🚴",
    layout="wide"
)

st.title("🚴 Garmin Telemetry: Periodization & Progression")
st.markdown("""
*An interactive exploration of multi-year triathlon training data, focusing on volume periodization, discipline balance, and session intensity progression.*
""")

# ---------------------------------------------------------
# Data Loading & Preprocessing
# ---------------------------------------------------------
@st.cache_data
def load_data():
  # Resolves the directory where app.py lives
  BASE_DIR = Path(__file__).resolve().parent
  file_path = BASE_DIR / 'df_clean.csv'

  df = pd.read_csv(file_path)
  df['date'] = pd.to_datetime(df['date'])
  return df

try:
    df_clean = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}. Please ensure `data/df_clean.csv` exists.")
    st.stop()

# Filter core disciplines
triathlon_df = df_clean[df_clean['discipline'] != 'other'].copy()

# Unit conversions
def calculate_custom_distance(row):
    meters = row.get('distance', 0)
    if pd.isna(meters) or meters <= 0:
        return 0.0
    if row['discipline'] == 'swimming':
        return meters * 1.09361  # Meters to Yards
    else:
        return meters * 0.000621371  # Meters to Miles

triathlon_df['distance_custom'] = triathlon_df.apply(calculate_custom_distance, axis=1)
unit_map = {'cycling': 'Miles', 'running': 'Miles', 'swimming': 'Yards'}
triathlon_df['unit_label'] = triathlon_df['discipline'].map(unit_map)

# Color Scheme
color_map = {
    'cycling': '#2b5c8f',
    'running': '#2ca02c',
    'swimming': '#17becf'
}

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("Filter Controls")

min_date = triathlon_df['date'].min().date()
max_date = triathlon_df['date'].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

selected_disciplines = st.sidebar.multiselect(
    "Disciplines",
    options=['cycling', 'running', 'swimming'],
    default=['cycling', 'running', 'swimming']
)

# Apply Filters
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = triathlon_df[
        (triathlon_df['date'].dt.date >= start_date) &
        (triathlon_df['date'].dt.date <= end_date) &
        (triathlon_df['discipline'].isin(selected_disciplines))
    ]
else:
    filtered_df = triathlon_df[triathlon_df['discipline'].isin(selected_disciplines)]

# ---------------------------------------------------------
# Chapter 1: Macro Volume & Cadence
# ---------------------------------------------------------
st.header("Chapter 1: Macro Volume & Cadence")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Monthly Duration Volume")
    monthly_vol = filtered_df.groupby(['year_month', 'discipline'])['duration_hours'].sum().reset_index()
    fig_1a = px.bar(
        monthly_vol,
        x='year_month',
        y='duration_hours',
        color='discipline',
        color_discrete_map=color_map,
        labels={'year_month': 'Month', 'duration_hours': 'Duration (Hours)', 'discipline': 'Discipline'},
        barmode='stack'
    )
    fig_1a.update_layout(template='plotly_white', xaxis_tickangle=-45)
    st.plotly_chart(fig_1a, use_container_width=True)

with col2:
    st.subheader("Weekly Cadence (4-Wk Moving Average)")
    # Group weekly and spline smooth
    weekly_cadence = (
        filtered_df.groupby([pd.Grouper(key='date', freq='W-MON'), 'discipline'])
        .size()
        .unstack(fill_value=0)
        .rolling(window=4, min_periods=1)
        .mean()
        .reset_index()
        .melt(id_vars='date', var_name='discipline', value_name='avg_sessions')
    )
    fig_1b = px.line(
        weekly_cadence,
        x='date',
        y='avg_sessions',
        color='discipline',
        color_discrete_map=color_map,
        line_shape='spline',
        labels={'date': 'Date', 'avg_sessions': 'Avg Sessions/Wk', 'discipline': 'Discipline'}
    )
    fig_1b.update_layout(template='plotly_white')
    st.plotly_chart(fig_1b, use_container_width=True)

st.info("""
**Chapter 1 Key Takeaways & Periodization Observations:**
* **Macro Progression:** Monthly volume shows distinct annual progression, escalating from initial ~20-hour baselines in 2024 to peak build blocks exceeding 40–50 hours per month in mid-2025 and 2026.
* **Frequency Adaptation:** The 4-week moving average demonstrates an early reliance on running frequency (~4 sessions/week in 2024). As triathlon preparation matured, cycling frequency spiked (peaking near 5 sessions/week in 2025) while swimming stabilized into a consistent 1–2 session/week rhythm.
""")

    
st.divider()

# ---------------------------------------------------------
# Chapter 2: Discipline Balance
# ---------------------------------------------------------
st.header("Chapter 2: Discipline Balance & Proportions")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("Total Volume Share")
    total_share = filtered_df.groupby('discipline')['duration_hours'].sum().reset_index()
    fig_2a = px.pie(
        total_share,
        values='duration_hours',
        names='discipline',
        color='discipline',
        color_discrete_map=color_map,
        hole=0.45
    )
    fig_2a.update_traces(textinfo='percent+label')
    fig_2a.update_layout(template='plotly_white', showlegend=False)
    st.plotly_chart(fig_2a, use_container_width=True)

with col_b:
    st.subheader("Monthly Volume Proportion (100% Stacked)")
    monthly_share = filtered_df.groupby(['year_month', 'discipline'])['duration_hours'].sum().reset_index()
    monthly_share['monthly_total'] = monthly_share.groupby('year_month')['duration_hours'].transform('sum')
    monthly_share['percentage'] = (monthly_share['duration_hours'] / monthly_share['monthly_total']) * 100

    fig_2b = px.bar(
        monthly_share,
        x='year_month',
        y='percentage',
        color='discipline',
        color_discrete_map=color_map,
        labels={'year_month': 'Month', 'percentage': 'Share (%)', 'discipline': 'Discipline'},
        barmode='stack'
    )
    fig_2b.update_layout(template='plotly_white', xaxis_tickangle=-45, yaxis=dict(range=[0, 100], ticksuffix='%'))
    st.plotly_chart(fig_2b, use_container_width=True)

st.info("""
**Chapter 2 Key Takeaways & Volume Allocation:**
* **Aerobic Allocation:** Overall training hours align directly with standard triathlon race duration profiles, with **cycling accounting for 55%** of total volume, **running at 37%**, and **swimming comprising 8.1%**.
* **Phase Shifts:** Monthly 100% stacked views illustrate operational shifts across phases—early 2024 featured heavy run-dominant blocks (>70% duration share), whereas peak race prep in 2025–2026 transitioned to a steady 50–70% cycling volume allocation.
""")    
    
st.divider()

# ---------------------------------------------------------
# Chapter 3: Granular Profiles & Outlier Analysis
# ---------------------------------------------------------
st.header("Chapter 3: Granular Session Profiles")

st.subheader("Session Duration Box Plot")
fig_3a = px.box(
    filtered_df,
    x='discipline',
    y='duration_hours',
    color='discipline',
    color_discrete_map=color_map,
    points='outliers',
    labels={'discipline': 'Discipline', 'duration_hours': 'Duration (Hours)'}
)
fig_3a.update_layout(template='plotly_white', showlegend=False)
st.plotly_chart(fig_3a, use_container_width=True)

st.subheader("Session Distance Progression Over Time")
# Filter noise for progression visual
scatter_df = filtered_df[filtered_df['distance_custom'] > 0.2].copy()

fig_3c = px.scatter(
    scatter_df,
    x='date',
    y='distance_custom',
    color='discipline',
    color_discrete_map=color_map,
    facet_row='discipline',
    category_orders={'discipline': ['cycling', 'running', 'swimming']},
    custom_data=['unit_label'],
    trendline='lowess',
    trendline_options=dict(frac=0.3),
    labels={'date': 'Date', 'distance_custom': 'Distance', 'discipline': 'Discipline'}
)

fig_3c.update_traces(
    selector=dict(type='scatter', mode='markers'),
    marker=dict(size=7, opacity=0.5, line=dict(width=0.5, color='white')),
    hovertemplate='<b>Date:</b> %{x|%b %d, %Y}<br><b>Distance:</b> %{y:,.1f} %{customdata[0]}<extra></extra>'
)
fig_3c.update_traces(
    selector=dict(type='scatter', mode='lines'),
    line=dict(width=3, dash='solid')
)
fig_3c.update_layout(template='plotly_white', height=650, showlegend=False, hovermode='closest')
fig_3c.update_yaxes(matches=None, showticklabels=True)

facet_titles = {'cycling': 'Cycling (Miles)', 'running': 'Running (Miles)', 'swimming': 'Swimming (Yards)'}
fig_3c.for_each_annotation(lambda a: a.update(text=facet_titles.get(a.text.split("=")[-1], a.text)))

st.plotly_chart(fig_3c, use_container_width=True)

st.info("""
**Chapter 3 Key Takeaways & Progressive Overload:**
* **Duration Spread (Box Plot):** Cycling displays the highest variance and upper-whisker extension (median ~1.5 hours, with long endurance rides stretching to 4–7 hours). Running maintains a tight, predictable band (median ~0.75 hours with long runs up to 3 hours), while swimming is strictly bounded between 0.5 to 1.25 hours.
* **Progressive Overload (Distance Progression):** LOWESS trendlines confirm continuous long-term physical adaptation across all disciplines:
  * **Running:** Smooth upward baseline progression from ~3-mile averages in 2024 to 6+ mile averages in 2026, with peak long runs reaching 15–20 miles.
  * **Cycling:** Shifted baseline from ~15-mile efforts up to consistent 25–30 mile workouts, featuring several century-distance efforts (~100 miles) in late 2025.
  * **Swimming:** Session volume increased from ~1,200-yard sets to peak workouts surpassing 3,000–4,000 yards in 2026.
""")