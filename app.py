import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Academic Improvement Journey Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin: 1rem 0;
    }
    .ethics-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv('academic_journey_dataset.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.title("📚 Academic Journey Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    [
        "📖 Story Overview",
        "📊 Data Visualizations",
        "🎯 Decision-Making",
        "⚖️ Ethics & Responsibility",
        "🔍 Data Explorer"
    ]
)

st.sidebar.markdown("---")

# Sidebar filters (used in Data Explorer and Visualizations)
st.sidebar.markdown("### Filters")
selected_semester = st.sidebar.multiselect(
    "Select Semester(s)",
    options=df['Semester'].unique(),
    default=df['Semester'].unique()
)

exam_status_filter = st.sidebar.multiselect(
    "Exam Status",
    options=df['Exam_Status'].unique(),
    default=df['Exam_Status'].unique()
)

stress_range = st.sidebar.slider(
    "Stress Level Range",
    min_value=int(df['Stress_Level'].min()),
    max_value=int(df['Stress_Level'].max()),
    value=(int(df['Stress_Level'].min()), int(df['Stress_Level'].max()))
)

# Apply filters
filtered_df = df[
    (df['Semester'].isin(selected_semester)) &
    (df['Exam_Status'].isin(exam_status_filter)) &
    (df['Stress_Level'] >= stress_range[0]) &
    (df['Stress_Level'] <= stress_range[1])
]

st.sidebar.markdown("---")
st.sidebar.info(
    "This dashboard analyzes academic performance patterns across two semesters "
    "with 5 courses, an internship, and civic engagement commitments."
)

# ============================================================================
# PAGE 1: STORY OVERVIEW
# ============================================================================
if page == "📖 Story Overview":
    st.title("📖 My Academic Improvement Journey")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ## The Challenge

        This semester, I took on significantly more responsibilities than ever before:
        - **5 courses** (compared to 3 last semester)
        - **Internship** at a tech company working on a fraud detection analysis dashboard
        - **Civic engagement project** — SDS Bridge Program

        This created unprecedented time pressure and stress, but also an opportunity to understand
        my academic patterns and optimize my performance.
        """)

    with col2:
        st.metric("Courses This Semester", "5", "+2 from last semester")
        st.metric("GPA Improvement", "3.57", "+0.26 from 3.31")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### Why This Matters
        - Identify what actually improves my grades
        - Optimize time management
        - Maintain health while performing well
        - Make data-driven decisions about future commitments
        """)

    with col2:
        st.markdown("""
        ### The Data
        I tracked:
        - Study hours per day
        - Sleep hours per day
        - Stress levels (1–5 scale)
        - Productivity (1–5 scale)
        - Assignment scores & exam results

        **Period:** September 2025 – May 2026
        **Observations:** 25 data points
        """)

    with col3:
        st.markdown("""
        ### Key Questions
        1. What habits improves my academic performance?
        2. What is the trade-off between stress and productivity?
        3. How does sleep affect my exam performance?
        4. Can I replicate finals-level focus earlier?
        5. Is this workload sustainable long-term?
        """)

    st.markdown("---")
    st.markdown("## Semester Comparison")

    comparison_df = pd.DataFrame({
        'Metric': ['Number of Courses', 'GPA', 'Average Stress (1–5)', 'Average Sleep (hours)', 'Average Study Hours'],
        'Fall 2025': [3, 3.31, '2–3', '8+', 6],
        'Spring 2026': [5, 3.57, '3–5', 7, 8],
        'Change': ['+2', '+0.26', '+1–2', '−1', '+2']
    })
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    st.markdown("""
    ### Initial Observations

    Despite taking 5 courses instead of 3, my GPA actually improved. However, this came at a cost:
    - Stress levels increased significantly
    - Sleep hours decreased by about 1 hour per night
    - Study hours increased by 2 hours per day

    This raises important questions about sustainability and whether this pattern can continue.
    """)

# ============================================================================
# PAGE 2: DATA VISUALIZATIONS
# ============================================================================
elif page == "📊 Data Visualizations":
    st.title("📊 Data Visualizations & Key Insights")

    # Key metrics bar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Study Hours", f"{filtered_df['Study_Hours'].mean():.1f} hrs", "per day")
    with col2:
        st.metric("Avg Sleep Hours", f"{filtered_df['Sleep_Hours'].mean():.1f} hrs", "per day")
    with col3:
        st.metric("Avg Stress Level", f"{filtered_df['Stress_Level'].mean():.1f}/5", "self-rated")
    with col4:
        st.metric("Avg Productivity", f"{filtered_df['Productivity_Level'].mean():.1f}/5", "self-rated")

    st.markdown("---")

    # Chart 1: Study vs Sleep
    st.subheader("1️⃣ Study Hours vs Sleep Hours Over Time")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=filtered_df['Date'], y=filtered_df['Study_Hours'],
        mode='lines+markers', name='Study Hours',
        line=dict(color='#1f77b4', width=3), marker=dict(size=8)
    ))
    fig1.add_trace(go.Scatter(
        x=filtered_df['Date'], y=filtered_df['Sleep_Hours'],
        mode='lines+markers', name='Sleep Hours',
        line=dict(color='#ff7f0e', width=3), marker=dict(size=8)
    ))
    fig1.update_layout(
        title="Study vs Sleep Hours — The Trade-off Pattern",
        xaxis_title="Date", yaxis_title="Hours",
        hovermode='x unified', height=400, template='plotly_white'
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
    **Key Finding:** There is a clear inverse relationship between study hours and sleep hours.
    As study hours increase (especially during midterms and finals), sleep hours decrease.
    """)

    st.markdown("---")

    # Chart 2: Stress vs Productivity
    st.subheader("2️⃣ Stress Level vs Productivity Level")
    fig2 = px.scatter(
        filtered_df, x='Stress_Level', y='Productivity_Level',
        color='Exam_Status', size='Study_Hours',
        hover_data=['Date', 'Sleep_Hours'],
        title="Stress vs Productivity — The Paradox",
        labels={'Stress_Level': 'Stress Level (1–5)', 'Productivity_Level': 'Productivity (1–5)'},
        color_discrete_map={'Normal': '#2ca02c', 'Midterm': '#ff7f0e', 'Finals': '#d62728'},
        height=400
    )
    fig2.update_layout(template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
    **Key Finding:** Counterintuitively, maximum stress (5/5) correlates with maximum productivity (5/5).
    Deadline pressure appears to create conditions that enhance focus — though outcome bias may play a role.
    """)

    st.markdown("---")

    # Chart 3: Exam Performance Trajectory
    st.subheader("3️⃣ Exam Performance Trajectory")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=['Week 1–3\n(Beginning)', 'Week 8–10\n(Midterm)', 'Week 14–16\n(Finals)'],
        y=[85, 72.5, 92.5],
        mode='lines+markers',
        name='Average Score',
        line=dict(color='#1f77b4', width=4),
        marker=dict(size=12, color=['#2ca02c', '#d62728', '#2ca02c'])
    ))
    fig3.update_layout(
        title="Exam Performance Trajectory — The Midterm Dip",
        xaxis_title="Semester Phase", yaxis_title="Average Score",
        yaxis=dict(range=[60, 100]), height=400,
        template='plotly_white', showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    **Key Finding:** There is a consistent 20–25 point drop during midterms compared to both
    the start of semester and finals. This pattern repeats across semesters, suggesting a
    systematic issue with midterm preparation strategy.
    """)

    st.markdown("---")

    # Chart 4: Weekday vs Weekend
    st.subheader("4️⃣ Study Hours: Weekday vs Weekend")
    fig4 = go.Figure()
    fig4.add_trace(go.Box(
        y=filtered_df[filtered_df['Is_Weekend'] == False]['Study_Hours'],
        name='Weekday', marker_color='#1f77b4'
    ))
    fig4.add_trace(go.Box(
        y=filtered_df[filtered_df['Is_Weekend'] == True]['Study_Hours'],
        name='Weekend', marker_color='#ff7f0e'
    ))
    fig4.update_layout(
        title="Study Hours Distribution: Weekday vs Weekend",
        yaxis_title="Study Hours", height=400, template='plotly_white'
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
    **Key Finding:** Study hours are high on weekdays (7–9 hrs) but drop dramatically on weekends (2 hrs).
    However, during finals weeks, weekend hours increase to 8–10 hrs — showing this behaviour is discretionary.
    """)

    st.markdown("---")
    st.markdown("## 🔍 Key Insights Summary")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Insight 1: Sleep–Study Trade-off
        - Study hours increase from 6 to 10–12 during finals
        - Sleep decreases from 8+ to 5–7 hours
        - **Risk:** Chronic sleep deprivation may harm long-term health

        ### Insight 2: Productivity Paradox
        - Maximum stress correlates with maximum productivity
        - Deadline pressure enhances focus
        - **Caveat:** Outcome bias may inflate self-rated productivity
        """)
    with col2:
        st.markdown("""
        ### Insight 3: Midterm Vulnerability
        - Consistent 20–25 point gap between midterm and finals scores
        - Midterm prep strategy is less effective
        - Opportunity: earlier preparation

        ### Insight 4: Discretionary Behaviour
        - Weekend social media dominates normal weeks (6+ hours)
        - Drops to minimal during finals (redirected to study)
        - Shows behaviour can be changed with motivation
        """)

# ============================================================================
# PAGE 3: DECISION-MAKING
# ============================================================================
elif page == "🎯 Decision-Making":
    st.title("🎯 Decision-Making Section")

    st.markdown("""
    ## Based on My Data, What Should I Do Differently?

    The data reveals clear patterns that can inform future academic strategies.
    Each recommendation comes with trade-offs and limitations.
    """)

    st.markdown("---")
    st.markdown("## 5 Evidence-Based Recommendations")

    recommendations = [
        {
            "title": "1. Protect Sleep During Exam Periods",
            "action": "Maintain 7–8 hours minimum, reduce study hours if needed",
            "rationale": "Research shows 7–8 hours is optimal for memory retention and exam performance.",
            "data_support": "Sleep deprivation during finals (5–7 hrs) correlates with increased stress.",
            "trade_off": "May reduce study time, but improves retention and cognitive function."
        },
        {
            "title": "2. Start Midterm Prep 2 Weeks Earlier",
            "action": "Begin studying 2 weeks in advance instead of 1 week",
            "rationale": "Consistent 20–25 point gap between midterm (70–75) and finals (90–95) scores.",
            "data_support": "Pattern repeats across both semesters, indicating a systematic issue.",
            "trade_off": "Requires more sustained effort earlier, but improves midterm performance."
        },
        {
            "title": "3. Redirect Weekend Social Media Time",
            "action": "Limit to 1–2 hours, especially in weeks 5–7 (pre-midterm)",
            "rationale": "Currently only 2 hrs study on weekends; redirecting 2–3 hrs could improve preparation.",
            "data_support": "Behaviour is discretionary — drops to minimal during finals.",
            "trade_off": "Reduces leisure time, but provides 10–15 extra study hours per month."
        },
        {
            "title": "4. Front-Load Internship Work",
            "action": "Concentrate internship during weeks 1–7 (low-stress periods)",
            "rationale": "Reduces concurrent demands during midterms and finals.",
            "data_support": "Stress peaks during exam periods; front-loading reduces overlap.",
            "trade_off": "More intense early semester, but provides breathing room during exams."
        },
        {
            "title": "5. Replicate Finals Focus Earlier",
            "action": "Create artificial deadlines and structured study environments",
            "rationale": "Peak productivity occurs during finals; replicating these conditions could improve earlier performance.",
            "data_support": "Productivity jumps to 5/5 during finals despite similar or higher stress.",
            "trade_off": "Requires discipline to maintain artificial pressure, but improves consistency."
        }
    ]

    for rec in recommendations:
        with st.expander(f"**{rec['title']}**"):
            st.markdown(f"**Action:** {rec['action']}")
            st.markdown(f"**Rationale:** {rec['rationale']}")
            st.markdown(f"**Data Support:** {rec['data_support']}")
            st.markdown(f"**Trade-off:** {rec['trade_off']}")

    st.markdown("---")
    st.markdown("""
    ## Implementation Strategy

    **Phase 1 — Immediate (Next Semester)**
    - Protect sleep: commit to 7–8 hours minimum during exam periods
    - Start midterm prep 2 weeks earlier
    - Monitor effectiveness through continued tracking

    **Phase 2 — Medium-term (Following Year)**
    - Redirect weekend social media time gradually
    - Front-load internship work
    - Establish artificial deadlines for consistency

    **Phase 3 — Long-term**
    - Develop sustainable study habits
    - Balance academic performance with health
    - Adjust based on outcomes and well-being
    """)

    st.markdown("---")
    st.markdown("""
    ## ⚠️ Important Caveats

    These recommendations are based on:
    - Only 25 observations over 2 semesters
    - Self-reported data subject to bias
    - One person's experience (may not generalise)
    - Correlation, not necessarily causation

    Before implementing: test gradually, monitor outcomes objectively, and prioritise health over grades.
    """)

# ============================================================================
# PAGE 4: ETHICS & RESPONSIBILITY
# ============================================================================
elif page == "⚖️ Ethics & Responsibility":
    st.title("⚖️ Ethics & Responsibility")

    with st.expander("🔒 Privacy Statement", expanded=True):
        st.markdown("""
        **What Data is Included?**
        - Study hours, sleep hours, stress levels, productivity ratings, exam scores, course load

        **What is Anonymised?**
        - Internship company name (referred to as "tech company — fraud detection")
        - Civic engagement project details (referred to as "SDS Bridge Program")
        - Specific course codes and instructors
        - Personal identifiers (email, ID numbers, etc.)

        **Data Source:**
        All data is self-reported and synthetic, created for educational purposes. No third-party data is included.
        """)

    st.markdown("---")

    with st.expander("⚠️ Bias & Limitation Disclosure", expanded=True):
        bias_df = pd.DataFrame({
            'Bias / Limitation': [
                'Memory Bias', 'Subjective Measurement', 'Small Sample Size',
                'Confounding Variables', 'Outcome Bias', 'Survivorship Bias', 'Selection Bias'
            ],
            'Description': [
                'All data collected retrospectively. Stress and productivity levels particularly subject to recall bias.',
                'Stress and productivity are self-rated 1–5 scales without objective tools.',
                'Only 25 observations across 2 semesters. Too small for statistical significance.',
                'Course difficulty, instructor quality, and external life events not controlled for.',
                'Productivity self-rating may be inflated during finals due to better results, not actual productivity.',
                'Only tracking successful academic outcomes. Failures or dropped courses not included.',
                'Data only from semesters where I took 3–5 courses. May not represent other course loads.'
            ],
            'Impact': ['High', 'High', 'Medium', 'High', 'Medium', 'Medium', 'Low']
        })
        st.dataframe(bias_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    with st.expander("📊 Visualization Justification"):
        viz_df = pd.DataFrame({
            'Visualization': [
                'Study vs Sleep Hours', 'Stress vs Productivity',
                'Exam Performance Trajectory', 'Weekday vs Weekend Study'
            ],
            'Why Chosen': [
                'Line chart shows time-series trend clearly; reveals inverse relationship',
                'Scatter plot with colour/size encoding shows multivariate relationships',
                'Line chart emphasises the midterm dip pattern across semester',
                'Box plot compares distributions and shows outliers clearly'
            ],
            'Risk of Misinterpretation': [
                'May appear causal when both variables actually respond to exam pressure',
                'Correlation between stress and productivity might suggest stress improves performance',
                'Midterm dip might be attributed to lack of preparation rather than course difficulty',
                'Weekend pattern might be seen as laziness, but is actually discretionary behaviour'
            ],
            'Mitigation': [
                'Include explanation of confounding variable (exam period)',
                'Include caveat about outcome bias and alternative explanations',
                'Discuss multiple possible causes (preparation strategy, difficulty, motivation)',
                'Show that behaviour changes during finals, proving it is discretionary'
            ]
        })
        st.dataframe(viz_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    with st.expander("🔗 Correlation ≠ Causation"):
        st.markdown("""
        This dashboard shows correlations observed in my data. Important reminders:

        - **Correlation:** Two variables move together (e.g., stress and productivity both increase during finals)
        - **Causation:** One variable causes changes in another (e.g., stress causes productivity)

        In this data, high stress and high productivity are correlated during finals — but both may be caused
        by a third factor: **exam deadlines**. Stress doesn't cause productivity; deadlines cause both.

        This is why recommendations should be tested carefully before full implementation.
        """)

    st.markdown("---")

    with st.expander("🎯 Responsible Decision-Making"):
        st.markdown("""
        **✅ DO:**
        - Use patterns to inform decisions, not dictate them
        - Test recommendations gradually and monitor outcomes
        - Combine with other sources of information
        - Prioritise health and well-being over grades

        **❌ DON'T:**
        - Assume these patterns apply to everyone
        - Implement all recommendations simultaneously
        - Ignore warning signs of burnout or health issues
        - Treat correlations as definitive proof of causation
        - Sacrifice mental or physical health for academic performance
        """)

# ============================================================================
# PAGE 5: DATA EXPLORER
# ============================================================================
elif page == "🔍 Data Explorer":
    st.title("🔍 Interactive Data Explorer")

    st.markdown("""
    Explore the raw data and create custom visualizations.
    Use the sidebar filters to focus on specific time periods, semesters, or stress levels.
    """)

    st.markdown("---")
    st.markdown(f"## Filtered Data ({len(filtered_df)} records)")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("## Summary Statistics")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Study Hours", f"{filtered_df['Study_Hours'].mean():.1f}")
    with col2:
        st.metric("Avg Sleep Hours", f"{filtered_df['Sleep_Hours'].mean():.1f}")
    with col3:
        st.metric("Avg Stress Level", f"{filtered_df['Stress_Level'].mean():.1f}")
    with col4:
        st.metric("Avg Productivity", f"{filtered_df['Productivity_Level'].mean():.1f}")

    st.markdown("---")
    st.markdown("## Custom Visualization")

    numeric_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X-Axis:", options=numeric_cols, index=0)
    with col2:
        y_axis = st.selectbox("Y-Axis:", options=numeric_cols, index=1)

    if x_axis != y_axis:
        fig = px.scatter(
            filtered_df, x=x_axis, y=y_axis,
            color='Exam_Status',
            size='Study_Hours' if 'Study_Hours' in filtered_df.columns else None,
            hover_data=['Date'],
            title=f"{y_axis} vs {x_axis}",
            color_discrete_map={'Normal': '#2ca02c', 'Midterm': '#ff7f0e', 'Finals': '#d62728'}
        )
        fig.update_layout(height=500, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("## Download Filtered Data")
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="academic_journey_filtered.csv",
        mime="text/csv"
    )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Academic Improvement Journey Dashboard</strong></p>
    <p>Data Collection Period: September 2025 – May 2026 &nbsp;|&nbsp; 25 observations</p>
    <p style='font-size: 12px; color: #999;'>
        Data201: Data Communication and Ethics &nbsp;|&nbsp; Parami University
    </p>
</div>
""", unsafe_allow_html=True)
