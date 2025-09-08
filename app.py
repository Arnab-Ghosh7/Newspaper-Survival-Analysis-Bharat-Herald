import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# Helper: Clean column names
# ------------------------
def clean_columns(df):
    df.columns = (
        df.columns.str.strip()       # remove leading/trailing spaces
        .str.lower()                 # lowercase
        .str.replace(" ", "_")       # replace spaces with underscores
        .str.replace(r"[^\w_]", "", regex=True)  # remove special chars
    )
    return df

# ------------------------
# Load Datasets
# ------------------------
@st.cache_data
def load_data():
    df_ad = pd.read_csv("Datasets/fact_ad_revenue.csv")
    df_city = pd.read_csv("Datasets/fact_city_readiness.csv")
    df_digital = pd.read_csv("Datasets/fact_digital_pilot.csv")
    df_print = pd.read_excel("Datasets/fact_print_sales.xlsx")

    # Clean all columns
    df_ad = clean_columns(df_ad)
    df_city = clean_columns(df_city)
    df_digital = clean_columns(df_digital)
    df_print = clean_columns(df_print)

    # Convert numerics where possible
    for df in [df_ad, df_city, df_digital, df_print]:
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="ignore")

    return df_ad, df_city, df_digital, df_print


df_ad, df_city, df_digital, df_print = load_data()

# ------------------------
# Sidebar Navigation
# ------------------------
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Print Sales Analysis",
    "Ad Revenue Analysis",
    "City Readiness",
    "Digital Pilot Study",
    "Recommendations"
])

# ------------------------
# Debug Helper
# ------------------------
def show_debug_info(df, name):
    with st.expander(f"🔍 Debug Info: {name}"):
        st.write("**Columns:**", df.columns.tolist())
        st.dataframe(df.head())

# ------------------------
# Pages
# ------------------------
if page == "Home":
    st.title("📰 Newspaper Survival Analysis - Bharat Herald")
    st.markdown("""
    Welcome to the **interactive dashboard**.  
    Use the sidebar to navigate through different analysis sections.
    """)

elif page == "Print Sales Analysis":
    st.header("📖 Print Newspaper Circulation")

    # Debug info
    show_debug_info(df_print, "Print Sales Data")

    # Line chart: Net circulation
    if "month" in df_print.columns and "net_circulation" in df_print.columns:
        fig = px.line(df_print, x="month", y="net_circulation",
                      title="Net Circulation Over Months")
        st.plotly_chart(fig, use_container_width=True)

    # Bar chart: Copies sold vs returned
    if {"month", "copies_sold", "copies_returned"}.issubset(df_print.columns):
        df_melt = df_print.melt(id_vars="month",
                                value_vars=["copies_sold", "copies_returned"],
                                var_name="type", value_name="count")
        fig2 = px.bar(df_melt, x="month", y="count", color="type",
                      barmode="group", title="Copies Sold vs Copies Returned")
        st.plotly_chart(fig2, use_container_width=True)

elif page == "Ad Revenue Analysis":
    st.header("📢 Advertisement Revenue")

    # Debug info
    show_debug_info(df_ad, "Ad Revenue Data")

    if {"category", "revenue", "city"}.issubset(df_ad.columns):
        fig = px.bar(df_ad, x="category", y="revenue", color="city",
                     title="Ad Revenue by Category and City")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.pie(df_ad, names="category", values="revenue",
                      title="Revenue Share by Category")
        st.plotly_chart(fig2, use_container_width=True)

elif page == "City Readiness":
    st.header("🏙️ City Readiness for Digital Adoption")

    # Debug info
    show_debug_info(df_city, "City Readiness Data")

    if {"city", "readinessscore"}.issubset(df_city.columns):
        fig = px.bar(df_city, x="city", y="readinessscore", color="city",
                     title="City Readiness Index")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Digital Pilot Study":
    st.header("🚀 Digital Pilot Study Outcomes")

    # Debug info
    show_debug_info(df_digital, "Digital Pilot Data")

    if {"city", "engagement", "users"}.issubset(df_digital.columns):
        fig = px.scatter(df_digital, x="city", y="engagement", size="users",
                         color="city", title="Digital Pilot Study Results")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Recommendations":
    st.header("📌 Strategic Recommendations")
    st.markdown("""
    - Invest in **digital-first cities** with high readiness.  
    - Diversify **ad revenue streams** across categories.  
    - Use **pilot results** to expand into new cities.  
    - Maintain **print strongholds** while scaling digital.  
    """)

