import duckdb
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Injection
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Endurance Telemetry | Portfolio Analytics",
    layout="wide",
)

# Custom CSS for modern visual hierarchy and card styling
st.markdown(
    """
    <style>
    /* Global Page Styling */
    .main {
        background-color: #FAFAFA;
    }
    
    /* Header Scaffolding */
    h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #1A1D20;
    }
    
    /* Custom Callout Cards */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #6C757D;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
        margin-top: 4px;
    }
    
    /* Executive Takeaway Box */
    .takeaway-card {
        background-color: #F8F9FA;
        border-left: 4px solid #00A8B5;
        border-radius: 4px;
        padding: 14px 18px;
        margin-bottom: 20px;
        font-size: 0.95rem;
        color: #2B2D42;
    }
    .takeaway-title {
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.8px;
        color: #00A8B5;
        margin-bottom: 4px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. Color Palette & Plotly Theme Definitions
# -----------------------------------------------------------------------------
COLOR_RUN = "#00A8B5"  # Garmin Teal
COLOR_BIKE = "#FF5722"  # Endurance Orange
COLOR_SWIM = "#2196F3"  # Deep Blue
COLOR_STRENGTH = "#7E57C2"  # Purple Accent
COLOR_FATIGUE = "#E53935"  # Soft Red
COLOR_FITNESS = "#1E88E5"  # Deep Royal Blue

DISCIPLINE_COLORS = {
    "Running": COLOR_RUN,
    "Cycling": COLOR_BIKE,
    "Swimming": COLOR_SWIM,
    "Strength & Cardio": COLOR_STRENGTH,
    "Walking": "#9E9E9E",
    "Other": "#B0BEC5",
}


def apply_custom_layout(fig, title="", height=420):
    """Applies clean data visualization standards to Plotly figures."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=15, color="#2B2D42"),
            x=0.01,
        ),
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=50, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title="",
        ),
        xaxis=dict(showgrid=False, linecolor="#E0E0E0"),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", linecolor="#E0E0E0"),
        hoverlabel=dict(
            bgcolor="#FFFFFF", font_size=12, font_family="Helvetica"
        ),
    )
    return fig


# -----------------------------------------------------------------------------
# 3. Cached Database Connection & SQL Views
# -----------------------------------------------------------------------------
@st.cache_resource
def get_duckdb_connection():
    con = duckdb.connect()

    con.execute("""
    CREATE OR REPLACE VIEW v_yearly_volume AS
    SELECT 
        CAST(EXTRACT(YEAR FROM CAST(start_time AS DATE)) AS INT) as training_year,
        activity_group,
        COUNT(*) as total_activities,
        ROUND(SUM(distance_miles), 1) as total_miles,
        ROUND(SUM(duration_minutes) / 60, 0) as total_hours,
        ROUND(AVG(average_hr), 0) as avg_heart_rate
    FROM 'cleaned_garmin_activities.csv'
    GROUP BY 1, 2
    ORDER BY training_year ASC, total_hours DESC;
    """)

    con.execute("""
    CREATE OR REPLACE VIEW v_acwr_telemetry AS
    SELECT 
        CAST(start_time AS DATE) as activity_date,
        activity_group,
        average_hr,
        max_hr,
        training_load,
        AVG(training_load) OVER(ORDER BY CAST(start_time AS DATE) ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as acute_load,
        AVG(training_load) OVER(ORDER BY CAST(start_time AS DATE) ROWS BETWEEN 27 PRECEDING AND CURRENT ROW) as chronic_load
    FROM 'cleaned_garmin_activities.csv'
    WHERE training_load IS NOT NULL AND training_load > 0
    ORDER BY activity_date ASC;
    """)

    return con


con = get_duckdb_connection()

# -----------------------------------------------------------------------------
# 4. Dashboard Title & Intro Scaffolding
# -----------------------------------------------------------------------------
st.title("Endurance Performance Engine")
st.markdown(
    """
*Multi-year Garmin training telemetry analysis (2019–2026) evaluating volume periodization, cardiovascular stress distribution, and Ironman/70.3 build workload ratios.*
"""
)

st.divider()

# -----------------------------------------------------------------------------
# 5. Sidebar Controls
# -----------------------------------------------------------------------------
st.sidebar.markdown("### Telemetry Controls")
df_groups = con.execute(
    "SELECT DISTINCT activity_group FROM v_yearly_volume"
).df()
all_groups = df_groups["activity_group"].tolist()

# Set core defaults or retain full selection options
default_groups = [g for g in ["Running", "Cycling", "Swimming"] if g in all_groups]

selected_groups = st.sidebar.multiselect(
    "Disciplines", options=all_groups, default=default_groups
)

groups_tuple = tuple(selected_groups) if selected_groups else ("NONE",)

# This must be defined here so Tabs 1, 2, 3 can access it globally!
df_yearly_filtered = con.execute(f"""
    SELECT * FROM v_yearly_volume 
    WHERE activity_group IN {groups_tuple}
    ORDER BY training_year ASC
""").df()

# -----------------------------------------------------------------------------
# 6. Navigation Tabs
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Macro Volume",
    "Cardiovascular Stress",
    "Load & ACWR",
    "Triathlon Build (2025–2026)",
])

# =============================================================================
# TAB 1: Macro Volume Trends
# =============================================================================
with tab1:
    st.markdown(
        """
        <div class="takeaway-card">
            <div class="takeaway-title">Executive Takeaway & Guidance</div>
            <b>Multi-Year Discipline Shift:</b> Training progression shows a transition from running-dominant years toward a multi-sport endurance structure (Cycling, Running, Swimming). Notice how total annual volume scales up significantly as triathlon periodization begins in 2024–2025.
        </div>
    """,
        unsafe_allow_html=True,
    )

    if not df_yearly_filtered.empty:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Cumulative Duration</div>
                    <div class="metric-value">{int(df_yearly_filtered['total_hours'].sum()):,} hrs</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Total Distance Covered</div>
                    <div class="metric-value">{df_yearly_filtered['total_miles'].sum():,.1f} mi</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Completed Workouts</div>
                    <div class="metric-value">{df_yearly_filtered['total_activities'].sum():,} sessions</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        fig_hours = go.Figure()
        for group in df_yearly_filtered["activity_group"].unique():
            df_g = df_yearly_filtered[
                df_yearly_filtered["activity_group"] == group
            ]
            fig_hours.add_trace(
                go.Bar(
                    x=df_g["training_year"],
                    y=df_g["total_hours"],
                    name=group,
                    marker_color=DISCIPLINE_COLORS.get(group, "#B0BEC5"),
                    hovertemplate="<b>%{x}</b><br>"
                    + group
                    + ": %{y} hrs<extra></extra>",
                )
            )

        fig_hours.update_layout(
    barmode="stack",
    xaxis=dict(
        type="category",
        categoryorder="category ascending"  # Forces chronological order (2019, 2020, ..., 2026)
    ),
)
        apply_custom_layout(
            fig_hours, title="Annual Multi-Sport Volume Periodization (Hours)"
        )
        st.plotly_chart(fig_hours, use_container_width=True)
    else:
        st.warning("Select at least one discipline in the sidebar.")

# =============================================================================
# TAB 2: Cardiovascular Intensity & Triathlon Evolution
# =============================================================================
with tab2:
    # 1. Fetch filtered heart rate data strictly for Running, Cycling, Swimming
    df_hr_dist = con.execute("""
        SELECT 
            activity_group,
            average_hr,
            max_hr,
            ROUND(duration_minutes / 60, 1) as duration_hours
        FROM 'cleaned_garmin_activities.csv'
        WHERE average_hr IS NOT NULL AND average_hr > 60 AND average_hr < 220
          AND activity_group IN ('Running', 'Cycling', 'Swimming')
    """).df()

    if not df_hr_dist.empty:
        hr_means = df_hr_dist.groupby('activity_group')['average_hr'].mean().round(0).to_dict()
        run_hr = int(hr_means.get('Running', 169))
        bike_hr = int(hr_means.get('Cycling', 153))

        st.markdown(f"""
            <div class="takeaway-card">
                <div class="takeaway-title">Executive Takeaway & Guidance</div>
                <b>Aerobic Specificity & Triathlon Shift:</b> As triathlon training volume scales up, tracking multi-year heart rate evolution reveals aerobic efficiency gains—noting how sustained aerobic baseline targets stabilize (~{run_hr} BPM avg for running, ~{bike_hr} BPM avg for cycling) across multi-sport blocks.
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2.2, 1])

        with col1:
            fig_hr = go.Figure()
            for group in ["Swimming", "Cycling", "Running"]:
                df_g = df_hr_dist[df_hr_dist["activity_group"] == group]
                if not df_g.empty:
                    fig_hr.add_trace(
                        go.Box(
                            y=df_g["average_hr"],
                            name=group,
                            marker_color=DISCIPLINE_COLORS.get(group, "#B0BEC5"),
                            boxmean=True,
                            hovertemplate="<b>%{x}</b><br>Avg HR: %{y} BPM<extra></extra>",
                        )
                    )

            fig_hr.update_layout(
                yaxis=dict(title="Heart Rate (BPM)", range=[80, 200]),
                showlegend=False,
            )
            apply_custom_layout(
                fig_hr, title="Heart Rate Distribution & Zone 2 Profile (BPM)"
            )
            st.plotly_chart(fig_hr, use_container_width=True)

        with col2:
            st.markdown("##### Cardiovascular Summary")
            df_hr_summary = con.execute("""
                SELECT 
                    activity_group as "Discipline",
                    ROUND(AVG(average_hr), 0) as "Avg HR",
                    ROUND(MAX(max_hr), 0) as "Peak HR",
                    COUNT(*) as "Workouts"
                FROM 'cleaned_garmin_activities.csv'
                WHERE average_hr IS NOT NULL AND average_hr > 60
                  AND activity_group IN ('Running', 'Cycling', 'Swimming')
                GROUP BY activity_group
                ORDER BY "Avg HR" DESC
            """).df()

            st.dataframe(
                df_hr_summary, hide_index=True, use_container_width=True
            )

        st.divider()

        st.markdown("##### Multi-Year Average Heart Rate Evolution by Sport")
        st.caption("Tracks how operating heart rates changed year-over-year as training evolved into structured multi-sport blocks.")

        df_yearly_hr = con.execute("""
            SELECT 
                CAST(EXTRACT(YEAR FROM CAST(start_time AS DATE)) AS INT) as training_year,
                activity_group,
                ROUND(AVG(average_hr), 1) as mean_hr
            FROM 'cleaned_garmin_activities.csv'
            WHERE average_hr IS NOT NULL AND average_hr > 60
              AND activity_group IN ('Running', 'Cycling', 'Swimming')
            GROUP BY 1, 2
            ORDER BY training_year ASC
        """).df()

        if not df_yearly_hr.empty:
            fig_yearly_hr = go.Figure()
            for group in ["Swimming", "Cycling", "Running"]:
                df_g = df_yearly_hr[df_yearly_hr["activity_group"] == group]
                if not df_g.empty:
                    fig_yearly_hr.add_trace(
                        go.Scatter(
                            x=df_g["training_year"],
                            y=df_g["mean_hr"],
                            mode="lines+markers",
                            name=group,
                            line=dict(color=DISCIPLINE_COLORS.get(group, "#B0BEC5"), width=2.2),
                            marker=dict(size=6),
                            hovertemplate="<b>%{x}</b><br>" + group + " Avg HR: %{y} BPM<extra></extra>"
                        )
                    )

            fig_yearly_hr.update_layout(
                xaxis=dict(type="category", categoryorder="category ascending"),
                yaxis=dict(title="Average Heart Rate (BPM)"),
            )
            apply_custom_layout(fig_yearly_hr, title="Year-Over-Year Discipline Heart Rate Trends", height=380)
            st.plotly_chart(fig_yearly_hr, use_container_width=True)
    else:
        st.warning("No heart rate data available for core triathlon disciplines.")

# =============================================================================
# TAB 3: ACWR Load & Fatigue Metrics
# =============================================================================
with tab3:
    # 1. Calculate dynamic ACWR telemetry statistics
    df_acwr_stats = con.execute("""
        SELECT 
            ROUND(AVG(acute_load / NULLIF(chronic_load, 0)), 2) as avg_acwr,
            ROUND(MAX(acute_load / NULLIF(chronic_load, 0)), 2) as peak_acwr
        FROM v_acwr_telemetry
        WHERE chronic_load > 0
    """).df()

    mean_acwr = df_acwr_stats['avg_acwr'].iloc[0] if not df_acwr_stats.empty else 1.0
    max_acwr = df_acwr_stats['peak_acwr'].iloc[0] if not df_acwr_stats.empty else 1.8

    # 2. Render advanced sports science takeaway card
    st.markdown(f"""
        <div class="takeaway-card">
            <div class="takeaway-title">Executive Takeaway & Guidance</div>
            <b>Gabbett ACWR Model Evaluation:</b> The optimal workload "sweet spot" sits between <b>0.8 and 1.3</b>. Your telemetry indicates an average ratio of <b>{mean_acwr}</b> with peak spikes hitting <b>{max_acwr}</b>. Periods where the 7-day load significantly outpaces the 28-day baseline highlight high-risk overreaching phases that require structured recovery blocks to prevent overuse injuries.
        </div>
    """, unsafe_allow_html=True)

    df_acwr = con.execute("SELECT * FROM v_acwr_telemetry").df()

    if not df_acwr.empty:
        fig_acwr = go.Figure()
        fig_acwr.add_trace(
            go.Scatter(
                x=df_acwr["activity_date"],
                y=df_acwr["acute_load"],
                mode="lines",
                name="7-Day Fatigue (Acute)",
                line=dict(color=COLOR_FATIGUE, width=1.8),
            )
        )
        fig_acwr.add_trace(
            go.Scatter(
                x=df_acwr["activity_date"],
                y=df_acwr["chronic_load"],
                mode="lines",
                name="28-Day Fitness (Chronic)",
                line=dict(color=COLOR_FITNESS, width=2.2),
            )
        )

        fig_acwr.update_layout(
            hovermode="x unified",
            yaxis=dict(title="Training Load Units"),
        )
        apply_custom_layout(
            fig_acwr, title="Acute-to-Chronic Workload Ratio (ACWR Telemetry)"
        )
        st.plotly_chart(fig_acwr, use_container_width=True)
    else:
        st.warning("No workload telemetry available.")

# =============================================================================
# TAB 4: Ironman & 70.3 Build Analytics
# =============================================================================
with tab4:
    st.markdown(
        """
        <div class="takeaway-card">
            <div class="takeaway-title">Executive Takeaway & Guidance</div>
            <b>Race Preparation Progression (2025–2026):</b> This build view evaluates how you stack multi-sport volume (Hours) and ramp up peak single-session distance (Miles) as your race approaches. Watch for the 3-week volume build pattern followed by recovery drop-offs, and pay close attention to the <b>Brick Workouts</b> table at the bottom—proving your body's ability to run efficiently off the bike.
        </div>
    """,
        unsafe_allow_html=True,
    )

    df_weekly = con.execute("""
        SELECT 
            DATE_TRUNC('week', CAST(start_time AS DATE)) as week_start,
            activity_group,
            ROUND(SUM(duration_minutes) / 60, 1) as weekly_hours,
            ROUND(MAX(distance_miles), 1) as max_single_session_miles
        FROM 'cleaned_garmin_activities.csv'
        WHERE CAST(EXTRACT(YEAR FROM CAST(start_time AS DATE)) AS INT) IN (2025, 2026)
          AND activity_group IN ('Running', 'Cycling', 'Swimming')
        GROUP BY 1, 2
        ORDER BY week_start ASC
    """).df()

    if not df_weekly.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig_weekly = go.Figure()
            for group in ["Swimming", "Cycling", "Running"]:
                df_g = df_weekly[df_weekly["activity_group"] == group]
                fig_weekly.add_trace(
                    go.Bar(
                        x=df_g["week_start"],
                        y=df_g["weekly_hours"],
                        name=group,
                        marker_color=DISCIPLINE_COLORS.get(group, "#B0BEC5"),
                        hovertemplate="%{x|%b %d, %Y}<br>"
                        + group
                        + ": %{y} hrs<extra></extra>",
                    )
                )

            # Fixed layout with clean legend and top margin to prevent overlap
            fig_weekly.update_layout(
                barmode="stack",
                xaxis=dict(type="date", title="Training Week (Start Date)"),
                yaxis=dict(title="Volume (Hours)"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.05,
                    xanchor="right",
                    x=1,
                    bgcolor="rgba(0,0,0,0)",
                ),
                margin=dict(t=80),
            )
            apply_custom_layout(
                fig_weekly,
                title="Weekly Build Volume Stack (2025–2026)",
                height=400,
            )
            st.plotly_chart(fig_weekly, use_container_width=True)

        with col2:
            fig_ramp = go.Figure()
            for group in ["Cycling", "Running"]:
                df_g = df_weekly[df_weekly["activity_group"] == group]
                fig_ramp.add_trace(
                    go.Scatter(
                        x=df_g["week_start"],
                        y=df_g["max_single_session_miles"],
                        mode="lines+markers",
                        name=f"Peak {group}",
                        line=dict(
                            color=DISCIPLINE_COLORS.get(group), width=2
                        ),
                        marker=dict(size=5),
                        hovertemplate="%{x|%b %d, %Y}<br>Longest "
                        + group
                        + ": %{y} mi<extra></extra>",
                    )
                )

            fig_ramp.update_layout(
                xaxis=dict(type="date", title="Training Week (Start Date)"),
                yaxis=dict(title="Distance (Miles)"),
            )
            apply_custom_layout(
                fig_ramp, title="Peak Long Session Ramp (Miles)", height=400
            )
            st.plotly_chart(fig_ramp, use_container_width=True)

        st.divider()

        st.markdown(
            "##### Progressive Brick Workout Capacity (2025–2026)"
        )
        st.caption(
            "Tracking long-ride volume leading directly into run sessions to measure neuromuscular transition adaptation."
        )

        df_bricks = con.execute("""
            WITH ranked_sessions AS (
                SELECT 
                    CAST(start_time AS DATE) as activity_date,
                    activity_group,
                    duration_minutes,
                    distance_miles,
                    average_hr,
                    ROW_NUMBER() OVER(PARTITION BY CAST(start_time AS DATE), activity_group ORDER BY start_time ASC) as rn
                FROM 'cleaned_garmin_activities.csv'
                WHERE CAST(EXTRACT(YEAR FROM CAST(start_time AS DATE)) AS INT) IN (2025, 2026)
                  AND activity_group IN ('Running', 'Cycling')
            ),
            brick_pairs AS (
                SELECT 
                    b.activity_date,
                    b.distance_miles as bike_miles,
                    b.duration_minutes / 60.0 as bike_hours,
                    b.average_hr as bike_hr,
                    r.distance_miles as run_miles,
                    r.duration_minutes / 60.0 as run_hours,
                    r.average_hr as run_hr
                FROM ranked_sessions b
                JOIN ranked_sessions r ON b.activity_date = r.activity_date
                WHERE b.activity_group = 'Cycling' 
                  AND r.activity_group = 'Running'
                  AND b.rn = 1 AND r.rn = 1
            )
            SELECT 
                activity_date as "Date",
                ROUND(bike_miles, 1) as "Bike Distance (mi)",
                ROUND(bike_hours, 1) as "Bike Duration (hrs)",
                ROUND(run_miles, 1) as "Run Distance (mi)",
                ROUND(run_hours, 1) as "Run Duration (hrs)",
                ROUND(bike_hr, 0) as "Bike Avg HR",
                ROUND(run_hr, 0) as "Run Avg HR"
            FROM brick_pairs
            ORDER BY activity_date DESC;
        """).df()

        if not df_bricks.empty:
            st.dataframe(
                df_bricks, hide_index=True, use_container_width=True
            )
        else:
            st.info(
                "No sequenced Bike-to-Run brick sessions logged for 2025–2026."
            )
    else:
        st.warning("No 2025–2026 data available.")