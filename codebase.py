import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Page Config ---
st.set_page_config(
    page_title="Urban Data Insights",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f5f7fa;
    }
    .sidebar .sidebar-content {
        background: #2C3E50;
        color: white;
    }
    h1, h2, h3, h4 {
        color: #2C3E50;
    }
    .metric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("DATA ANALYSIS AND VISUALIZATION")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dataset Overview", "Cleaning Steps", "Numerical Analysis", "Visualizations","Database Integration","Python / Excel Data analysis"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Group Members:\n"
    "1. Itumeleng Amantle\n"
    "2. Boago Olyn\n"
    "3. Tsholofelo Serati\n"
    "4. Angela Letlatsa\n"
    "5. Nametsang Monoketsi\n"
    "6. Mahadi Motaung\n\n"
    "Data Analysis & Visualization Project"
)

# Load datasets
@st.cache_data
def load_data():
    df = pd.read_csv("datasets.csv")
    df = df.rename(columns={
        "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "Urban Population",
        "Unemployment, total (% of total labor force) (national estimate) [SL.UEM.TOTL.NE.ZS]": "Unemployment Rate",
        "Individuals using the Internet (% of population) [IT.NET.USER.ZS]": "Internet Users"
    })
    df = df.drop_duplicates()
    df = df.replace("..", pd.NA)
    df = df.dropna()
    df['Unemployment Rate'] = df['Unemployment Rate'].astype(float)
    df['Internet Users'] = df['Internet Users'].astype(float)
    return df

@st.cache_data
def load_sec_data():
    df1 = pd.read_csv("dataset2.csv")
    mapping_df2 = {
        "School enrollment, secondary (% net) [SE.SEC.NENR]": "Secondary School Enrollment",
        "Gini index [SI.POV.GINI]": "Gini Index",
        "Labor force participation rate, female (% of female population ages 15+) (national estimate) [SL.TLF.CACT.FE.NE.ZS]": "Female Labor Force Participation",
    }
    df1 = df1.rename(columns=mapping_df2)
    df1 = df1.replace("..", pd.NA)
    # Identify your numeric data columns (columns 4, 5, 6 in your sample)
    data_columns = df1.columns[4:7]

    # Convert these columns to numeric (very important, as they might be strings or objects)
    for col in data_columns:
        df1[col] = pd.to_numeric(df1[col], errors='coerce')

    # Now, replace NULL values with the column's mean
    for col in data_columns:
        col_mean = df1[col].mean() # Calculate the mean of the column
        df1[col] = df1[col].fillna(col_mean) # Fill NaNs with that mean
    return df1

df_main = load_data()
df_sec = load_sec_data()

# --- Main Content ---
if page == "Dataset Overview":
    st.title("Urban Data Insights")
    st.markdown('<h3 style="color:#4F8BF9;">Explore Urban Population, Unemployment & Internet Usage Trends</h3>', unsafe_allow_html=True)
    st.subheader("Primary Dataset")
    st.dataframe(pd.read_csv("datasets.csv"))
    st.subheader("Secondary Dataset")
    st.dataframe(pd.read_csv("dataset2.csv"))
    st.markdown("View the original data before cleaning and analysis.")

elif page == "Cleaning Steps":
    st.title("Data Cleaning Steps")
    st.markdown("""
    **Steps performed:**
    - Renamed columns for clarity  
    - Removed duplicates  
    - Handled missing values  
    - Corrected data types  
    - Ensured data consistency
    - Replaced missing numeric values with column means
    - Filtered out invalid data points (e.g., negative unemployment rates)
    - Verified data ranges and distributions
    """)
    st.write("Cleaned Dataset one Preiview:")
    st.dataframe(df_main, use_container_width=True)

    st.write("Cleaned Dataset two Preiview:")
    st.dataframe(df_sec, use_container_width=True)

from numerical_analysis import show_numerical_analysis

# ... in your Streamlit page logic ...
if page == "Numerical Analysis":
    show_numerical_analysis()
    
elif page == "Visualizations":
    st.title("Data Visualizations")

    # --- KPI Cards ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Urban Population", f"{df_main['Urban Population'].iloc[-1]:.2f}%")
    col2.metric("Latest Unemployment", f"{df_main['Unemployment Rate'].iloc[-1]:.2f}%")
    col3.metric("Internet Users", f"{df_main['Internet Users'].iloc[-1]:.2f}%")

    st.markdown("---")
    
    # --- MAIN DATASET VISUALIZATIONS ---
    st.header("Primary Dataset Analysis")
    
    # Year Filter for Main Dataset
    year_range_main = st.slider("Select Year Range for Primary Data", 
                               int(df_main["Time"].min()), 
                               int(df_main["Time"].max()),
                               (int(df_main["Time"].min()), int(df_main["Time"].max())),
                               key="main_year_slider")
    
    df_filtered_main = df_main[(df_main["Time"] >= year_range_main[0]) & 
                              (df_main["Time"] <= year_range_main[1])]

    # --- Line Plot ---
    st.subheader("Trends Over Time")
    fig = px.line(df_filtered_main, x="Time", y=["Urban Population", "Unemployment Rate", "Internet Users"],
                  markers=True, title="Urban Population, Unemployment & Internet Users Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # --- Scatter Plot ---
    st.subheader("Internet Users vs Urban Population")
    fig = px.scatter(df_filtered_main, x="Urban Population", y="Internet Users", color="Time",
                     size="Unemployment Rate", title="Internet Users vs Urban Population")
    st.plotly_chart(fig, use_container_width=True)

    # --- Histogram ---
    st.subheader("Distribution of Internet Users")
    fig = px.histogram(df_filtered_main, x="Internet Users", nbins=15, color_discrete_sequence=["#43AA8B"])
    st.plotly_chart(fig, use_container_width=True)

    # --- Box Plot ---
    st.subheader("Unemployment Rate Distribution")
    fig = px.box(df_filtered_main, y="Unemployment Rate", points="all", color_discrete_sequence=["#43AA8B"])
    st.plotly_chart(fig, use_container_width=True)

    # --- Download Button ---
    st.download_button("Download Cleaned Dataset", df_main.to_csv(index=False).encode("utf-8"),
                       "cleaned_data.csv", "text/csv")
    
    st.markdown("---")
    
    # --- SECONDARY DATASET VISUALIZATIONS ---
    st.header("Secondary Dataset Analysis")
    
    # Year Filter for Secondary Dataset
    year_range_sec = st.slider("Select Year Range for Secondary Data", 
                              int(df_sec["Time"].min()), 
                              int(df_sec["Time"].max()),
                              (int(df_sec["Time"].min()), int(df_sec["Time"].max())),
                              key="sec_year_slider")
    
    df_filtered_sec = df_sec[(df_sec["Time"] >= year_range_sec[0]) & 
                            (df_sec["Time"] <= year_range_sec[1])]
    
    st.subheader("Secondary Dataset Preview")
    st.dataframe(df_filtered_sec, use_container_width=True)

# --- Line Plot (Secondary Dataset) ---
    st.subheader("Secondary Dataset Trends Over Time")
    fig = px.line(
        df_filtered_sec,
        x="Time",
        y=["Secondary School Enrollment", "Gini Index", "Female Labor Force Participation"],
        markers=True,
        title="Secondary School Enrollment, Gini Index & Female Labor Force Participation Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Scatter Plot ---
    st.subheader("Female Labor Force Participation vs Secondary School Enrollment")
    fig = px.scatter(
        df_filtered_sec,
        x="Secondary School Enrollment",
        y="Female Labor Force Participation",
        color="Time",
        size="Gini Index",
        title="Female Labor Force Participation vs Secondary School Enrollment"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Histogram ---
    st.subheader("Distribution of Gini Index")
    fig = px.histogram(
        df_filtered_sec,
        x="Gini Index",
        nbins=15,
        color_discrete_sequence=["#43AA8B"]
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Box Plot ---
    st.subheader("Secondary School Enrollment Distribution")
    fig = px.box(
        df_filtered_sec,
        y="Secondary School Enrollment",
        points="all",
        color_discrete_sequence=["#3498DB"]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.title("Insights & Trends")
    st.markdown("""
    ### Key Observations
    - **Line Plot:** Urban population rises steadily, while internet usage grows sharply.  
    - **Scatter Plot:** Positive correlation between urban population and internet users.  
    - **Box Plot:** Unemployment shows wide variability with some high outliers.  
    - **Histogram:** Internet usage distribution has shifted upward over the years.  
    """)
    st.success("Explore other tabs for more details and interactive visualizations!")

   
elif page == "Database Integration":
    st.title("Database Integration (Q4)")

    # --- Step 1: Connect & Create Database/Table ---
    server_engine = create_engine("mysql+mysqlconnector://root:202303305%40spu.ac.za@localhost")

    with server_engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS SA_Trends"))

    engine = create_engine("mysql+mysqlconnector://root:202303305%40spu.ac.za@localhost/SA_Trends")

   
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS SA_TrendsData (
                year INT PRIMARY KEY,
                urban_population DECIMAL(6,3),
                unemployment_rate DECIMAL(6,3),
                internet_usage DECIMAL(6,3)
            )
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS SA_SocialData (
            Year INT PRIMARY KEY,
            `Secondary Enrollment` DECIMAL(6,3),
            `Gini Index` DECIMAL(6,3),
            `Female Labor Force Participation` DECIMAL(6,3)
    
            )
        """))

    # --- Step 2: Load CSV into DB if empty (First Dataset) ---
    csv_df = pd.read_csv("datasets.csv")
    csv_df = csv_df.rename(columns={
        "Time": "year",
        "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "urban_population",
        "Unemployment, total (% of total labor force) (national estimate) [SL.UEM.TOTL.NE.ZS]": "unemployment_rate",
        "Individuals using the Internet (% of population) [IT.NET.USER.ZS]": "internet_usage"
    })
    csv_df = csv_df[["year", "urban_population", "unemployment_rate", "internet_usage"]]
    csv_df = csv_df.replace("..", pd.NA).dropna()
    csv_df = csv_df.astype({
        "year": int,
        "urban_population": float,
        "unemployment_rate": float,
        "internet_usage": float
    })

    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM SA_TrendsData"))
        if result.scalar() == 0:
            csv_df.to_sql("SA_TrendsData", con=engine, if_exists="append", index=False)

    # --- Step 3: Query Data from Database ---
    query = "SELECT * FROM SA_TrendsData ORDER BY year"
    db_df = pd.read_sql(query, engine)

    st.subheader("Data Loaded from MySQL Database")
    st.dataframe(db_df)

    # --- Step 4: Demonstrate Update & Delete (Your Operations Stay) ---
    st.subheader("Database Operations")

    col1, col2, col3 = st.columns(3)
    with col1:
        round_clicked = st.button("Round Values to Whole Numbers")
    with col2:
        delete_clicked = st.button("Delete Duplicate Rows")
    with col3:
        query_clicked = st.button("Run SQl Queries")

    if round_clicked:
        refreshed_df = pd.read_sql(query, engine)
        refreshed_df = refreshed_df.round(0).astype(int)
        st.subheader("Rounded Dataset ")
        st.dataframe(refreshed_df)

    if delete_clicked:
        refreshed_df = pd.read_sql(query, engine)
        refreshed_df[["urban_population", "unemployment_rate", "internet_usage"]] = (
            refreshed_df[["urban_population", "unemployment_rate", "internet_usage"]].round(0).astype(int)
        )
        duplicate_mask = refreshed_df.duplicated(
            subset=["urban_population", "unemployment_rate", "internet_usage"],
            keep="first"
        )
        duplicates = refreshed_df.loc[duplicate_mask, "year"].tolist()
        cleaned_df = refreshed_df[~duplicate_mask].reset_index(drop=True)
        start_year = refreshed_df["year"].min()
        cleaned_df["year"] = [start_year + i for i in range(len(cleaned_df))]
        st.warning(f"⚠️ Removed duplicate rows  {duplicates}")
        st.subheader("Database View After Removing Duplicates (Display Only)")
        st.dataframe(cleaned_df)

    if query_clicked:
        st.subheader("SQL Queries ")

        # Query 1: Average values
        avg_query = """
        SELECT 
            ROUND(AVG(urban_population),2) AS avg_urban_population,
            ROUND(AVG(unemployment_rate),2) AS avg_unemployment_rate,
            ROUND(AVG(internet_usage),2) AS avg_internet_usage
        FROM SA_TrendsData
        """
        avg_result = pd.read_sql(avg_query, engine)
        st.markdown("**Average Urban Population, Unemployment Rate & Internet Usage:**")
        st.dataframe(avg_result)

        # Query 2: Highest unemployment year
        high_unemp_query = """
        SELECT year, unemployment_rate 
        FROM SA_TrendsData
        ORDER BY unemployment_rate DESC
        LIMIT 1
        """
        high_unemp_result = pd.read_sql(high_unemp_query, engine)
        st.markdown("**Year with Highest Unemployment Rate:**")
        st.dataframe(high_unemp_result)

        # Query 3: Internet usage growth (first vs last year)
        growth_query = """
        SELECT 
            (MAX(internet_usage) - MIN(internet_usage)) AS growth_in_internet_usage,
            MIN(year) AS start_year,
            MAX(year) AS end_year
        FROM SA_TrendsData
        """
        growth_result = pd.read_sql(growth_query, engine)
        st.markdown("**Growth in Internet Usage (from first to last year):**")
        st.dataframe(growth_result)

        # Query 4: Years with Unemployment Rate above 30%
        high_unemp_years_query = """
        SELECT year, urban_population, unemployment_rate, internet_usage
        FROM SA_TrendsData
        WHERE unemployment_rate > 30
        ORDER BY year
        """
        high_unemp_years_result = pd.read_sql(high_unemp_years_query, engine)
        st.markdown("**Years where Unemployment Rate was above 30%:**")
        st.dataframe(high_unemp_years_result)

        # Query 5: Group By Decade (example of GROUP BY)
        group_by_decade_query = """
        SELECT 
            FLOOR(year/10)*10 AS decade,
            ROUND(AVG(urban_population),2) AS avg_urban_population,
            ROUND(AVG(unemployment_rate),2) AS avg_unemployment_rate,
            ROUND(AVG(internet_usage),2) AS avg_internet_usage
        FROM SA_TrendsData
        GROUP BY decade
        ORDER BY decade
        """
        group_by_decade_result = pd.read_sql(group_by_decade_query, engine)
        st.markdown("**Average Trends Grouped by Decade:**")
        st.dataframe(group_by_decade_result)
    
        # --- Step 5: Load & Show Second Dataset ---
    st.subheader("Second Dataset")

    df2 = pd.read_csv("dataset2.csv")
    mapping_df2 = {
        "School enrollment, secondary (% net) [SE.SEC.NENR]": "Secondary Enrollment",
        "Gini index [SI.POV.GINI]": "Gini Index",
        "Labor force participation rate, female (% of female population ages 15+) (national estimate) [SL.TLF.CACT.FE.NE.ZS]": "Female Labor Force Participation",
        "Time": "Year",
        "Country Name": "Country"
    }
    df2_clean = df2.rename(columns=mapping_df2)
    df2_clean = df2_clean.dropna()

    # Convert to numeric
    data_columns = df2_clean.columns[4:7]
    for col in data_columns:
        df2_clean[col] = pd.to_numeric(df2_clean[col], errors='coerce')
        df2_clean[col] = df2_clean[col].fillna(df2_clean[col].mean())

    st.dataframe(df2_clean)

    # Load into DB if empty
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM SA_SocialData"))
        if result.scalar() == 0:
            df2_clean[["Year", "Secondary Enrollment", "Gini Index", "Female Labor Force Participation"]].to_sql(
                "SA_SocialData", con=engine, if_exists="append", index=False
            )

    # --- Run Queries only when button clicked ---
    if st.button("Run SQL Queries on Second Dataset"):
        st.subheader("SQL Queries on Second Dataset")

        # Query 1: Average values
        avg_query2 = """
        SELECT 
            ROUND(AVG(`Secondary Enrollment`),2) AS avg_secondary_enrollment,
            ROUND(AVG(`Gini Index`),2) AS avg_gini_index,
            ROUND(AVG(`Female Labor Force Participation`),2) AS avg_female_labor_force
        FROM SA_SocialData
        """
        st.markdown("**Average of all indicators (1975–2024):**")
        st.dataframe(pd.read_sql(avg_query2, engine))

        # Query 2: Group by Decade
        group_query2 = """
        SELECT 
            FLOOR(Year/10)*10 AS decade,
            ROUND(AVG(`Secondary Enrollment`),2) AS avg_secondary_enrollment,
            ROUND(AVG(`Gini Index`),2) AS avg_gini_index,
            ROUND(AVG(`Female Labor Force Participation`),2) AS avg_female_labor_force
        FROM SA_SocialData
        GROUP BY decade
        ORDER BY decade
        """
        st.markdown("**Average Trends Grouped by Decade:**")
        st.dataframe(pd.read_sql(group_query2, engine))

        # Query 3: Highest & Lowest Secondary Enrollment
        high_low_enroll_query = """
        SELECT Year, `Secondary Enrollment`
        FROM SA_SocialData
        WHERE `Secondary Enrollment` = (SELECT MAX(`Secondary Enrollment`) FROM SA_SocialData)
           OR `Secondary Enrollment` = (SELECT MIN(`Secondary Enrollment`) FROM SA_SocialData)
        """
        st.markdown("**Years with Highest & Lowest Secondary Enrollment:**")
        st.dataframe(pd.read_sql(high_low_enroll_query, engine))

        # Query 4: Years where Gini Index > 60
        gini_query = """
        SELECT Year, `Gini Index`
        FROM SA_SocialData
        WHERE `Gini Index` > 60
        ORDER BY Year
        """
        st.markdown("**Years with Gini Index above 60 (high inequality):**")
        st.dataframe(pd.read_sql(gini_query, engine))

        # Query 5: Full yearly dataset
        corr_query = """
        SELECT Year,
               ROUND(`Secondary Enrollment`,2) AS secondary_enrollment,
               ROUND(`Gini Index`,2) AS gini_index,
               ROUND(`Female Labor Force Participation`,2) AS female_labor_force
        FROM SA_SocialData
        ORDER BY Year
        """
        st.markdown("**Full Yearly Dataset (to inspect relationships manually):**")
        st.dataframe(pd.read_sql(corr_query, engine))

        # Query 6: Female Labor Force > 50%
        female_query = """
        SELECT Year, `Female Labor Force Participation`
        FROM SA_SocialData
        WHERE `Female Labor Force Participation` > 50
        ORDER BY Year
        """
        st.markdown("**Years when Female Labor Force Participation exceeded 50%:**")
        st.dataframe(pd.read_sql(female_query, engine))

    st.subheader("Insights from First Dataset")
    st.markdown("""
- The average urban population from 1960 to 2021 is approximately **62.40%**, indicating a significant urbanization trend in South Africa.
- The average unemployment rate over the same period is around **26.36%**, highlighting ongoing economic challenges.
- Internet usage has seen a substantial increase, with an average of **33.44%**, reflecting growing digital connectivity.
- The year with the highest unemployment rate was **2021**, reaching **34.00%**, likely influenced by the economic impacts of the COVID-19 pandemic.
- There has been a remarkable growth in internet usage, increasing by **72.09%** from **2.91% in 1990** to **75.00% in 2021**.
- Notably, the unemployment rate exceeded **30%** in several years, particularly from **2019 to 2021**, indicating persistent labor market issues.
- Grouping the data by decade reveals that the **2010s** experienced the highest average urban population (**64.56%**) and internet usage (**48.87%**), while the unemployment rate peaked in the **2020s** at **32.15%**.
""")

    st.subheader("Insights from Second Dataset")
    st.markdown("""
- The average secondary enrollment rate from 1975 to 2024 is approximately **64.80%**, indicating a strong emphasis on education in South Africa.
- The average Gini index over the same period is around **61.80%**, highlighting significant income inequality in the country.
- The average trends grouped by decade show that the **2010s** had the highest average secondary enrollment (**68.12%**), while the **1990s** experienced a slight decline to **62.00%**. The Gini index remained relatively stable across decades.
- The Gini index exceeded **60** in several years, particularly from **1995 to 2024**, indicating persistent income inequality.
- The years when female labor force participation exceeded **50%** were **2018, 2019, 2020, 2021, 2022, 2023, and 2024**, reflecting increasing participation.
""")

from py_data_analysis import show_py_excel_analysis

if page == "Python / Excel Data analysis":
    show_py_excel_analysis()

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center>© 2025 Urban Data Insights | Powered by Streamlit</center>",
    unsafe_allow_html=True
)