import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import base64

# """
# MINDIQ — Teen Mental Health Intelligence Dashboard
# Pure Python / native Streamlit widgets — no HTML or CSS.
# Dark theme comes entirely from .streamlit/config.toml
# Run with: streamlit run app.py
# """



# ---------------------------------------------------------
# 1. PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(
    page_title="MindIQ | Teen Mental Health Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


PLOTLY_TEMPLATE = "plotly_dark"
COLOR_SEQ = ["#FF4B4B", "#FF8C42", "#FFD23F", "#4E9F3D", "#3E92CC", "#9B5DE5"]
RISK_COLORS = {"At Risk": "#FF4B4B", "Moderate": "#FFD23F", "Healthy": "#4E9F3D"}
SLEEP_COLORS = {"Poor": "#FF4B4B", "Fair": "#FFD23F", "Good": "#4E9F3D"}

# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
 return pd.read_csv("Teen_Mental_Health.csv")

df_raw = load_data()

# ---------------------------------------------------------
# 3. SIDEBAR AND BACKGROUND IMAGE — BOTH BACKGROUND IMAGE.
# ---------------------------------------------------------


def set_backgrounds(main_svg, sidebar_svg):
    with open(main_svg, "rb") as f:
        main_b64 = base64.b64encode(f.read()).decode()
    with open(sidebar_svg, "rb") as f:
        side_b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/svg+xml;base64,{main_b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stSidebar"] {{
            background-image: url("data:image/svg+xml;base64,{side_b64}");
            background-size: cover;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)
set_backgrounds("mindiq_background.svg", "mindiq_sidebar_background.svg")

# ---------------------------------------------------------
# 3. SIDEBAR — NAVIGATION + FILTERS
# ---------------------------------------------------------

st.sidebar.title("🧠 MindIQ:")
st.sidebar.caption("Teen Wellbeing Analytics System:")
st.sidebar.divider()

page = st.sidebar.radio(
"Navigate",
  ["📊 Overview:", "🧹 Data Cleaning:", "📈 Analytics:", "👥 Demographics Explorer:",
     "📅 Age Analysis:", "💡 Insights:", "⬇️ Export:"],
)

st.sidebar.divider()
st.sidebar.subheader("Filters:")
age_range = st.sidebar.slider(
    "Age range", int(df_raw.age.min()), int(df_raw.age.max()),
    (int(df_raw.age.min()), int(df_raw.age.max()))
)
gender_sel = st.sidebar.multiselect("Gender", sorted(df_raw.gender.unique()), default=sorted(df_raw.gender.unique()))
platform_sel = st.sidebar.multiselect("Platform", sorted(df_raw.platform_usage.unique()),
                                       default=sorted(df_raw.platform_usage.unique()))
risk_sel = st.sidebar.multiselect("Wellbeing Status", sorted(df_raw.digital_wellbeing_flag.unique()),
                                   default=sorted(df_raw.digital_wellbeing_flag.unique()))

df = df_raw[
    df_raw.age.between(*age_range) &
    df_raw.gender.isin(gender_sel) &
    df_raw.platform_usage.isin(platform_sel) &
    df_raw.digital_wellbeing_flag.isin(risk_sel)
]

st.sidebar.divider()
st.sidebar.caption(f"{len(df):,} of {len(df_raw):,} records match filters")

if df.empty:
    st.warning("No records match the current filters. Try widening your selection.")
    st.stop()

# ===========================================================
# PAGE: OVERVIEW
# ===========================================================
if page == "📊 Overview:":
    st.title(" 🧠 MENTAL HEALTH INTELLIGENCE:")
    st.caption("ADVANCED ANALYTICS & WELLBEING RISK DETECTION SYSTEM.")


    st.markdown( """Understanding how lifestyle affects teen mental health.

            
This project analysis:


📱 Socail Median Usage 


😴 Sleep Patterns 


📚 Academic Performance 


🤾‍♂️ Physical Activity 


🧠 Mental Health Risk and etc.""")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Records", f"{len(df):,}")
    c2.metric("Platforms", df.platform_usage.nunique())
    c3.metric("Avg. Risk Score", f"{df.mental_health_risk_score.mean():.1f}")
    c4.metric("% At Risk", f"{(df.digital_wellbeing_flag=='At Risk').mean()*100:.1f}%")
    c5.metric("Columns", df.shape[1])

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Platforms by Usage")
        counts = df.platform_usage.value_counts().reset_index()
        counts.columns = ["platform", "count"]
        fig = px.bar(counts, x="count", y="platform", orientation="h",
                     template=PLOTLY_TEMPLATE, color="platform", color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Risk Score by Age")
        by_age = df.groupby("age")["mental_health_risk_score"].mean().reset_index()
        fig = px.bar(by_age, x="age", y="mental_health_risk_score", template=PLOTLY_TEMPLATE,
                     color="mental_health_risk_score", color_continuous_scale=["#FF8C42", "#FF4B4B"])
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

# ===========================================================
# PAGE: DATA CLEANING
# ===========================================================
elif page == "🧹 Data Cleaning:":
    st.title("Data Cleaning")

    c1, c2, c3 = st.columns(3)
    c1.metric("Original Rows", f"{len(df_raw):,}")
    c2.metric("Missing Values", int(df_raw.isna().sum().sum()))
    c3.metric("Duplicate Rows", int(df_raw.duplicated().sum()))

    st.divider()
    st.subheader("Cleaning Pipeline")
    st.markdown("""
    - Strip whitespace from column names
    - Remove exact duplicate rows
    - Standardize categorical text (gender, platform, sleep_quality)
    - Fill numeric NaN with column median
    - Fill categorical NaN with column mode
    - Clip out-of-range values (e.g. negative hours)
    """)

    if st.button("▶ Run Cleaning Summary", type="primary"):
        st.subheader("Cleaning Report")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Rows After Clean", f"{len(df_raw.drop_duplicates()):,}")
        r2.metric("Rows Removed", int(df_raw.duplicated().sum()))
        r3.metric("Numeric Columns", df_raw.select_dtypes("number").shape[1])
        r4.metric("Categorical Columns", df_raw.select_dtypes("object").shape[1])
        st.success("Cleaning summary generated.")

# ===========================================================
# PAGE: ANALYTICS
# ===========================================================
elif page == "📈 Analytics:":
    st.title("Mental Health Analytics")
    st.caption(f"Analyzing {len(df):,} records after filters")

    t1, t2, t3, t4 = st.tabs(["By Platform", "By Wellbeing Status", "Sleep vs Stress", "Correlation"])

    with t1:
        fig = px.box(df, x="platform_usage", y="mental_health_risk_score", color="platform_usage",
                     template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        counts = df.digital_wellbeing_flag.value_counts().reset_index()
        counts.columns = ["status", "count"]
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(counts, names="status", values="count", hole=0.55,
                         color="status", color_discrete_map=RISK_COLORS, template=PLOTLY_TEMPLATE)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(counts, x="status", y="count", color="status",
                         color_discrete_map=RISK_COLORS, template=PLOTLY_TEMPLATE)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with t3:
        fig = px.box(df, x="sleep_quality", y="stress_level", color="sleep_quality",
                     category_orders={"sleep_quality": ["Poor", "Fair", "Good"]},
                     color_discrete_map=SLEEP_COLORS, template=PLOTLY_TEMPLATE)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with t4:
        numeric_cols = ["daily_social_media_hours", "sleep_hours", "screen_time_before_sleep",
                         "academic_performance", "physical_activity", "stress_level",
                         "anxiety_level", "addiction_level", "mental_health_risk_score"]
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=".2f", template=PLOTLY_TEMPLATE,
                         color_continuous_scale=["#FF8C42", "#1A1A24", "#FF4B4B"], zmin=-1, zmax=1)
        st.plotly_chart(fig, use_container_width=True)

# ===========================================================
# PAGE: DEMOGRAPHICS EXPLORER
# ===========================================================
elif page == "👥 Demographics Explorer:":
    st.title("Demographics Explorer")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Risk Score by Gender")
        fig = px.violin(df, x="gender", y="mental_health_risk_score", color="gender", box=True,
                         template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Social Interaction vs Risk")
        fig = px.box(df, x="social_interaction_level", y="mental_health_risk_score",
                     color="social_interaction_level",
                     category_orders={"social_interaction_level": ["low", "medium", "high"]},
                     template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Highest-Risk Profiles")
    top_risk = df.nlargest(10, "mental_health_risk_score")[
        ["age", "gender", "platform_usage", "daily_social_media_hours",
         "sleep_hours", "mental_health_risk_score", "digital_wellbeing_flag"]
    ]
    st.dataframe(top_risk, use_container_width=True)

# ===========================================================
# PAGE: AGE ANALYSIS
# ===========================================================
elif page == "📅 Age Analysis:":
    st.title("Age-Based Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Social Media Hours by Age")
        by_age = df.groupby("age")["daily_social_media_hours"].mean().reset_index()
        fig = px.bar(by_age, x="age", y="daily_social_media_hours", template=PLOTLY_TEMPLATE,
                     color_discrete_sequence=["#FF4B4B"])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Sleep Hours by Age")
        by_age2 = df.groupby("age")["sleep_hours"].mean().reset_index()
        fig = px.bar(by_age2, x="age", y="sleep_hours", template=PLOTLY_TEMPLATE,
                     color_discrete_sequence=["#FF8C42"])
        st.plotly_chart(fig, use_container_width=True)

# ===========================================================
# PAGE: INSIGHTS
# ===========================================================
elif page == "💡 Insights:":
    st.title("Analytical Insights")

    if st.button("⚡ Generate Insights", type="primary"):
        top_platform = df.platform_usage.value_counts().idxmax()
        worst_age = df.groupby("age")["mental_health_risk_score"].mean().idxmax()
        at_risk_pct = (df.digital_wellbeing_flag == "At Risk").mean() * 100
        corr_val = df["daily_social_media_hours"].corr(df["sleep_hours"])
        direction = "negatively" if corr_val < 0 else "positively"
        poor_sleep_stress = df[df.sleep_quality == "Poor"]["stress_level"].mean()
        good_sleep_stress = df[df.sleep_quality == "Good"]["stress_level"].mean()
        dep_rate = df.depression_label.mean() * 100

        st.subheader("Key Findings")
        st.info(f"📱 **{top_platform}** is the most-used platform — "
                f"{(df.platform_usage==top_platform).mean()*100:.1f}% of respondents.")
        st.warning(f"⚠️ Age **{worst_age}** shows the highest average risk score in this filtered set.")
        st.error(f"🚨 **{at_risk_pct:.1f}%** of respondents are flagged 'At Risk' for digital wellbeing.")
        st.info(f"😴 Daily social media use is {direction} correlated with sleep hours (r = {corr_val:.2f}).")
        st.warning(f"💤 Poor sleepers report avg. stress of **{poor_sleep_stress:.1f}**, "
                   f"vs **{good_sleep_stress:.1f}** for good sleepers.")
        st.error(f"🧠 **{dep_rate:.1f}%** of respondents carry a positive depression label.")
    else:
        st.info("Click **Generate Insights** to compute key findings from the current filtered data.")

# ===========================================================
# PAGE: EXPORT
# ===========================================================
elif page == "⬇️ Export:":
    st.title("Export Data")
    st.write(f"Exporting **{len(df):,}** of **{len(df_raw):,}** total records based on active filters.")
    table_height= min(35 * len(df) + 38, 800)
    st.dataframe(df, use_container_width=True, height=table_height)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered CSV", data=csv,
                        file_name="teen_mental_health_filtered.csv", mime="text/csv")

# st.sidebar.divider()
# st.sidebar.caption("MindIQ · Built with Streamlit & Plotly")


