import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
st.set_page_config(page_title="Teen Mental Health Analysis:", page_icon="🧠", layout="wide")
st.title("🧠 Teen Mental Health Analysis:")
st.markdown( """Understanding how lifestyle affects teen mental health.

            
This project analysis:


📱 Socail Median Usage 


😴 Sleep Patterns 


📚 Academic Performance 


🤾‍♂️ Physical Activity 


🧠 Mental Health Risk""")


col1,col2,col3,col4=st.columns(4)

col1.metric("Students:","1200")

col2.metric("Avg Sleep:","6.45 hrs")

col3.metric("Avg Social Media:","4.5 hrs")

col4.metric("High Risk:","29.5%")



#1. loading dataset:



import pandas as pd
df=pd.read_csv("teen_mental_health.csv")

st.subheader("Dataset Preview:")
st.dataframe(df.head())

# 2. basic dataset information:
st.subheader("Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())

# 3. creating sidebar:

st.sidebar.title("🧠 Dashboard Filters")

gender = st.sidebar.multiselect("Select Gender",options=df["gender"].unique(),default=df["gender"].unique())

filtered_df = df[df["gender"].isin(gender)]


# 4. creating kpi card:


st.title("🧠 Teen Mental Health Dashboard")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        filtered_df.shape[0]
    )

with col2:
    st.metric(
        "Average Age",
        round(filtered_df["age"].mean(),1)
    )

with col3:
    st.metric(
        "Average Social Media Hours",
        round(filtered_df["daily_social_media_hours"].mean(),1)
    )

with col4:
    st.metric(
        "Average Mental Health Risk",
        round(filtered_df["mental_health_risk_score"].mean(),1)
    )


# 5. first interactive chart:


    gender_count = (
    filtered_df["gender"]
    .value_counts()
    .reset_index()
)

gender_count.columns = ["Gender","Count"]

fig = px.bar(
    gender_count,
    x="Gender",
    y="Count",
    color="Gender",
    text="Count",
    title="Gender Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 6. two charts in row:


col1, col2 = st.columns(2)
with col1:

    gender_count = (
        filtered_df["gender"]
        .value_counts()
        .reset_index()
    )

    gender_count.columns = ["Gender","Count"]

    fig1 = px.bar(
        gender_count,
        x="Gender",
        y="Count",
        color="Gender",
        text="Count",
        title="Gender Distribution"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


with col2:

    fig2 = px.histogram(
        filtered_df,
        x="daily_social_media_hours",
        nbins=10,
        title="Daily Social Media Hours"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )# st.sidebar.title("🔍 ")

gender=st.sidebar.selectbox("Select gender:",["All"]+list(df["gender"].unique()))

age=st.sidebar.selectbox("Select age:",["All"]+sorted(df["age"].unique().tolist()))

sleep=st.sidebar.selectbox("sleep quality:",["All"]+list(df["sleep_quality"].unique()))
filtered_df=df.copy()

if gender!="All":
   filtered_df=filtered_df[filtered_df["gender"]==gender]

if age!="All":
   filtered_df=filtered_df[filtered_df["age"]==age]

if sleep!="All":
    filtered_df=filtered_df[filtered_df["sleep_quality"]==sleep]

    st.subheader("Filtered Dataset:")
#     st.dataframe(filtered_df)
with st.sidebar:
   opt=option_menu("Main Menu", ["Home","Dataset","Processing","Visualization","About"],icons=["house","table","gear","bar-chart","person"],menu_icon="cast",default_index=0)
   if opt=="Home":
    st.title("🏠 Home")
    gender=st.sidebar.selectbox("Select gender:",["All"]+list(df["gender"].unique()))

    age=st.sidebar.selectbox("Select age:",["All"]+sorted(df["age"].unique().tolist()))

   sleep=st.sidebar.selectbox("sleep quality:",["All"]+list(df["sleep_quality"].unique()))
   filtered_df=df.copy()

   if gender!="All":
    filtered_df=filtered_df[filtered_df["gender"]==gender]

   if age!="All":
    filtered_df=filtered_df[filtered_df["age"]==age]

   if sleep!="All":
    filtered_df=filtered_df[filtered_df["sleep_quality"]==sleep]

    st.subheader("Filtered Dataset:")
    st.dataframe(filtered_df)
    
   elif opt=="📈 Dataset":
    st.title("Dataset")
    t1,t2,t3=st.tabs(["Data","Columns","Summary"])

    with t1:
        st.dataframe(df)
        st.head()

    with t2:
        st.write(df.columns)

    with t3:
        st.write(df.describe())

   elif opt=="🔃 Processing":
    st.title("Processing")
    t1,t2=st.tabs(["Before-Processing","After-Processing"])

    with t1:
        st.write(df.isna().sum())

    with t2:
      #   df.drop(columns=["gender","age","daily_social_media_hours","sleep_hours","platform_usage","sleep_hours","screen_time_before_sleep","academic_performance","physical_activity","social_interaction_level","stress_level","anxiety_level","addiction_level","mental_health_risk_score","sleep_quality","digital_wellbeing_flag"],inplace=True)
      #   df.dropna(inplace=True)
      #   df.reset_index(drop=True,inplace=True)
        st.write(df.isna().sum())
#    elif opt=="Visualization":
#     st.title("Visualization")
#    #  df.drop(columns=["gender","age","daily_social_media_hours","sleep_hours","platform_usage","screen_time_before_sleep","academic_performance","physical_activity","social_interaction_level","stress_level","anxiety_level","addiction_level","mental_health_risk_score","sleep_quality","digital_wellbeing_flag"],inplace=True)
#    #  df.dropna(inplace=True)
#    #  df.reset_index(drop=True,inplace=True)
# t1,t2,t3=st.tabs(["Streamlit","Plotly","Seaborn"])

#     with t1:
#         #Bar
#       #   st.bar_chart(df,x="sleep_hours",y="daily_social_media_hours")
#         st.bar_chart(df,x="sleep_hours",y="daily_social_media_hours",color="red",x_label="SLEEP HOURS",y_label="SOCIAL MEDIA HOURS")

#         # #LINE
#         st.line_chart(df,x="academic_performance",y="mental_health_risk_score")

#         # #Area
#         st.area_chart(df,x="gender",y="sleep_hours")
#         # #Scatter
#         st.scatter_chart(df,x="screen_time_before_sleep",y="stress_level")
#         # st.scatter_chart(df,x="TotalDeaths",y="TotalCases",color="Country/Region",x_label="CONTINENT",y_label="TOTAL CASES",size="TotalRecovered")

#    with t2:
#         #bar
#         # fig1=px.bar(df,x="Continent",y="TotalCases")
#         # st.plotly_chart(fig1)

#         # fig12=px.bar(df,x="Continent",y="TotalCases",color="Country/Region",title="Total case by continent",hover_data=["Population","TotalRecovered"])
#         # st.plotly_chart(fig12)

#         # #line
#         fig2=px.line(df,x="screen_time_before_sleep",y="stress_level")
#         st.plotly_chart(fig2)

#         # fig21=px.line(df,x="TotalDeaths",y="TotalCases",title="Total case by continent",hover_data=["Population","TotalRecovered"],line_dash="Continent")
#         # st.plotly_chart(fig21)
#         # fig22=px.line(df,x="TotalDeaths",y="TotalCases",color="Continent",title="Total case by continent",hover_data=["Population","TotalRecovered"])
#         # st.plotly_chart(fig22)
#         # fig23=px.line(df,x="TotalDeaths",y="TotalCases",color="Continent",title="Total case by continent",hover_data=["Population","TotalRecovered"],log_x=True,log_y=True)
#         # st.plotly_chart(fig23)

#         #area
#         # fig3=px.area(df,x="Population",y="TotalCases")
#         # st.plotly_chart(fig3)

#         # fig31=px.area(df,x="Population",y="TotalCases",title="Total case by continent",hover_data=["Population","TotalRecovered"],color="Continent")
#         # st.plotly_chart(fig31)

#         # #scatter
#         fig4=px.scatter(df,x="screen_time_before_sleep",y="stress_level")
#         st.plotly_chart(fig4)

#         # fig41=px.scatter(df,x="TotalDeaths",y="TotalCases",title="Total case by continent",hover_data=["Population","TotalRecovered"],color="Continent")
#         # st.plotly_chart(fig41)

#         # fig42=px.scatter(df,x="TotalDeaths",y="TotalCases",color="Continent",title="Total case by continent",hover_data=["Population","TotalRecovered"],size="TotalRecovered",size_max=50)
#         # st.plotly_chart(fig42)

#         # fig43=px.scatter(df,x="TotalDeaths",y="TotalCases",color="Continent",title="Total case by continent",hover_data=["Population","TotalRecovered"],size="TotalRecovered",size_max=50,log_x=True,log_y=True)
#         # st.plotly_chart(fig43)

#         #3-d
#         # fig5=px.scatter_3d(df,x="TotalDeaths",y="TotalCases",z="TotalRecovered",color="Continent",log_x=True,log_y=True,log_z=True,title="Total case by continent",size="TotalRecovered",size_max=50)
#         # st.plotly_chart(fig5)

#         #pie
#       #   fig6=px.pie(df,name="Continent",values="TotalCases",title="Total case by continent")
#       #   st.plotly_chart(fig6)

#         # fig61=px.pie(df,names="Continent",values="TotalCases",title="Total case by continent",hole=0.5)
#         # st.plotly_chart(fig61)

#         #Sunburst
#       #   fig7=px.sunburst(df,path=["Continent","Country/Region","Population"],values="TotalCases",title="Total case by continent")
#       #   st.plotly_chart(fig7)
#    with t3:
#         import matplotlib.pyplot as plt
#         import seaborn as sns

#         #bar
#         fig1=sns.barplot(x="screen_time_before_sleep",y="stress_level",data=df)
#         st.pyplot(fig1)

#         # #line
#         # fig2=sns.lineplot(x="TotalDeaths",y="TotalCases",data=df)
#         # st.pyplot(fig2)

#         # #area
#         # fig3=sns.areaplot(x="Population",y="TotalCases",data=df)
#         # st.pyplot(fig3)

#         # #scatter
#         # fig4=sns.scatterplot(x="TotalDeaths",y="TotalCases",data=df)
#         # st.pyplot(fig4)


    

    
#    elif opt=="About":
#     st.title("About")
#     st.write("This is about page")
