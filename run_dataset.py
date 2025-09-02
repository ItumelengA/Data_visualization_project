import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import numpy as np

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

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dataset Overview", "Numerical Analysis", "Cleaning Steps", "Visualizations", "Database Integration", "Insights"]
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


# --- Load Data ---
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

df = load_data()

# --- Main Content ---
if page == "Dataset Overview":
    st.title("🌆 Urban Data Insights")
    st.markdown('<h3 style="color:#4F8BF9;">Explore Urban Population, Unemployment & Internet Usage Trends</h3>', unsafe_allow_html=True)
    st.subheader("Raw Dataset")
    st.dataframe(pd.read_csv("datasets.csv"))
    st.markdown("View the original data before cleaning and analysis.")

elif page == "Cleaning Steps":
    st.title("🧹 Data Cleaning Steps")
    st.markdown("""
    **Steps performed:**
    - Renamed columns for clarity  
    - Removed duplicates  
    - Handled missing values  
    - Corrected data types  
    """)
    st.write("Cleaned Dataset Preview:")
    st.dataframe(df, use_container_width=True)

elif page == "Visualizations":
    st.title("📑 Data Visualizations")

    # --- KPI Cards ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Urban Population", f"{df['Urban Population'].iloc[-1]:.2f}%")
    col2.metric("Latest Unemployment", f"{df['Unemployment Rate'].iloc[-1]:.2f}%")
    col3.metric("Internet Users", f"{df['Internet Users'].iloc[-1]:.2f}%")

    st.markdown("---")

    # --- Year Filter ---
    year_range = st.slider("Select Year Range", int(df["Time"].min()), int(df["Time"].max()),
                           (int(df["Time"].min()), int(df["Time"].max())))
    df_filtered = df[(df["Time"] >= year_range[0]) & (df["Time"] <= year_range[1])]

    # --- Line Plot ---
    st.subheader("Trends Over Time")
    fig = px.line(df_filtered, x="Time", y=["Urban Population", "Unemployment Rate", "Internet Users"],
                  markers=True, title="Urban Population, Unemployment & Internet Users Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # --- Scatter Plot ---
    st.subheader("Internet Users vs Urban Population")
    fig = px.scatter(df_filtered, x="Urban Population", y="Internet Users", color="Time",
                     size="Unemployment Rate", title="Internet Users vs Urban Population")
    st.plotly_chart(fig, use_container_width=True)

    # --- Histogram ---
    st.subheader("Distribution of Internet Users")
    fig = px.histogram(df_filtered, x="Internet Users", nbins=15, color_discrete_sequence=["#43AA8B"])
    st.plotly_chart(fig, use_container_width=True)

    # --- Box Plot ---
    st.subheader("Unemployment Rate Distribution")
    fig = px.box(df_filtered, y="Unemployment Rate", points="all", color_discrete_sequence=["#43AA8B"])
    st.plotly_chart(fig, use_container_width=True)

    # --- Download Button ---
    st.download_button("📥 Download Cleaned Dataset", df.to_csv(index=False).encode("utf-8"),
                       "cleaned_data.csv", "text/csv")

elif page == "Insights":
    st.title("🔎 Insights & Trends")
    st.markdown("""
    ### Key Observations
    - **Line Plot:** Urban population rises steadily, while internet usage grows sharply.  
    - **Scatter Plot:** Positive correlation between urban population and internet users.  
    - **Box Plot:** Unemployment shows wide variability with some high outliers.  
    - **Histogram:** Internet usage distribution has shifted upward over the years.  
    """)
    st.success("Explore other tabs for more details and interactive visualizations!")
elif page == "Database Integration":
    st.title("🗄️ Database Integration (Q4)")

    # --- Step 1: Connect & Create Database/Table ---
    # ...existing code...
    server_engine = create_engine("mysql+mysqlconnector://root:202303305%40spu.ac.za@localhost")

    with server_engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS SA_Trends"))

    engine = create_engine("mysql+mysqlconnector://root:202303305%40spu.ac.za@localhost/SA_Trends")
# ...existing code...

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS SA_TrendsData (
        year INT PRIMARY KEY,
        urban_population DECIMAL(6,3),
        unemployment_rate DECIMAL(6,3),
        internet_usage DECIMAL(6,3)
    )
    """
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))

    # --- Step 2: Load CSV into DB if empty ---
    csv_df = pd.read_csv("datasets.csv")
    csv_df = csv_df.rename(columns={
        "Time": "year",
        "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "urban_population",
        "Unemployment, total (% of total labor force) (national estimate) [SL.UEM.TOTL.NE.ZS]": "unemployment_rate",
        "Individuals using the Internet (% of population) [IT.NET.USER.ZS]": "internet_usage"
    })
    csv_df = csv_df[["year", "urban_population", "unemployment_rate", "internet_usage"]]
    csv_df = csv_df.replace("..", pd.NA).dropna()
    csv_df["year"] = csv_df["year"].astype(int)
    csv_df["urban_population"] = csv_df["urban_population"].astype(float)
    csv_df["unemployment_rate"] = csv_df["unemployment_rate"].astype(float)
    csv_df["internet_usage"] = csv_df["internet_usage"].astype(float)

    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM SA_TrendsData"))
        if result.scalar() == 0:
            csv_df.to_sql("SA_TrendsData", con=engine, if_exists="append", index=False)

    # --- Step 3: Query Data from Database ---
    query = "SELECT * FROM SA_TrendsData ORDER BY year"
    db_df = pd.read_sql(query, engine)

    st.subheader("📊 Data Loaded from MySQL Database")
    st.dataframe(db_df)

    # --- Step 4: Demonstrate Update & Delete ---
    st.subheader("⚙️ Database Operations")

    if st.button("Round & Remove Duplicates"):
        # Reload table
        refreshed_df = pd.read_sql(query, engine)

        # Round to whole numbers
        refreshed_df = refreshed_df.round(0).astype(int)

        # Remove duplicates & missing rows
        refreshed_df = refreshed_df.drop_duplicates().dropna()

        # Ensure continuous years 1998 → 2024
        all_years = pd.DataFrame({"year": range(1998, 2025)})
        refreshed_df = all_years.merge(refreshed_df, on="year", how="left")

        # Fill gaps with previous year values
        refreshed_df = refreshed_df.ffill()

        # Reset index
        refreshed_df = refreshed_df.reset_index(drop=True)

        st.subheader("✅ Cleaned & Continuous Dataset")
        st.dataframe(refreshed_df)

    elif page == "Numerical Analysis":
        st.title("🗄️ Numerical Analysis")

        # 1. LOAD RAW DATASET

st.header("1.Data")
df = pd.read_csv("datasets.csv")  
st.dataframe(df)


st.header("2. Clean the Data")


# Rename columns
df = df.rename(columns={
    "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "Urban Population",
    "Unemployment, total (% of total labor force) (national estimate) [SL.UEM.TOTL.NE.ZS]": "Unemployment Rate",
    "Individuals using the Internet (% of population) [IT.NET.USER.ZS]": "Internet Users"
})

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df = df.replace(["..", "...", "N/A", "n/a", "", " "], pd.NA)
df = df.dropna(how='all')
df = df.dropna(subset=['Urban Population', 'Unemployment Rate', 'Internet Users'], how='all')

# Convert to numbers
df['Urban Population'] = pd.to_numeric(df['Urban Population'], errors='coerce')
df['Unemployment Rate'] = pd.to_numeric(df['Unemployment Rate'],   errors='coerce')
df['Internet Users'] = pd.to_numeric(df['Internet Users'], errors='coerce')

# Keep only rows with no missing values
df_clean = df.dropna(subset=['Urban Population', 'Unemployment Rate', 'Internet Users'])

st.subheader("Cleaned Data")
st.dataframe(df_clean)


if df_clean.empty:
    st.error("No complete data rows available for analysis")
    st.stop()

# Descriptive stats
st.subheader("Quick Stats")
desc_stats = df_clean[['Urban Population', 'Unemployment Rate', 'Internet Users']].describe()
st.dataframe(desc_stats.style.format("{:.2f}"))

# 3. NUMPY CALCULATIONS

st.header("3. Calculations with NumPy")

# Convert to NumPy arrays
urban = df_clean["Urban Population"].to_numpy()
unemployment = df_clean["Unemployment Rate"].to_numpy()
internet = df_clean["Internet Users"].to_numpy()

# Averages and spread
st.subheader("Averages and Spread")
urban_mean, urban_std = np.mean(urban), np.std(urban)
unemp_mean, unemp_std = np.mean(unemployment), np.std(unemployment)
internet_mean, internet_std = np.mean(internet), np.std(internet)

st.write(f"Urban Population → Average: {urban_mean:.2f}, Spread: {urban_std:.2f}")
st.write(f"Unemployment Rate → Average: {unemp_mean:.2f}, Spread: {unemp_std:.2f}")
st.write(f"Internet Users → Average: {internet_mean:.2f}, Spread: {internet_std:.2f}")

# Relationship between columns
st.subheader("Relationship Between Numbers")
corr_matrix = np.corrcoef([urban, unemployment, internet])
st.write(corr_matrix)
st.markdown("""
- Close to 1→ There's a strong positive link  
- Close to -1 → There's a strong negative link  
- Close to 0 → There's no real link  
""")


# 4. RESHAPING 

st.header("4. Reshaping and Extra Math")


urban_reshaped = urban.reshape(-1, 1)
st.write("Original shape:", urban.shape)
st.write("New shape:", urban_reshaped.shape)
st.write("Urban Population reshaped as a column:")
st.write(urban_reshaped)

# Join columns side by side
stacked = np.column_stack((urban, unemployment, internet))
st.subheader("All Columns Joined Together")
st.write(stacked)

# Normalize unemployment rate
st.subheader("Unemployment Rate (normalized)")
unemployment_normalized = (unemployment - unemp_mean) / unemp_std
st.write(unemployment_normalized)

# Compare Urban Population and Internet Users
st.subheader("Urban Population minus Internet Users")
difference = urban - internet
st.write(difference)

# 5.INSIGHTS

st.header("5. What We Found")
st.markdown(f"""
- Urban Population: Around {urban_mean:.2f}% on average (changes about ±{urban_std:.2f})  
- Unemployment Rate: Around {unemp_mean:.2f}% on average  
- Internet Users: Around {internet_mean:.2f}% and growing fast  

How they link (correlation): 
""")

# Putting correlation results into a dataframe for clarity
corr_df = pd.DataFrame(
    corr_matrix, 
    index=["Urban Population", "Unemployment Rate", "Internet Users"], 
    columns=["Urban Population", "Unemployment Rate", "Internet Users"]
)
st.dataframe(corr_df.style.format("{:.2f}"))

# Interpret correlations
urban_internet_corr = corr_df.loc["Urban Population", "Internet Users"]
urban_unemp_corr = corr_df.loc["Urban Population", "Unemployment Rate"]
internet_unemp_corr = corr_df.loc["Internet Users", "Unemployment Rate"]

st.markdown("Key Insights:")

if urban_internet_corr > 0.5:
    st.markdown("When more people live in cities, more people also use the internet.")
elif urban_internet_corr < -0.5:
    st.markdown("In places with more city living, fewer people use the internet — this is unusual and worth checking.")
else:
    st.markdown("City living and internet use don’t really move together.")

if abs(urban_unemp_corr) < 0.3:
    st.markdown("Jobs (unemployment) don’t really change with city living.")
else:
    st.markdown("Jobs (unemployment) show some link with city living.")

if abs(internet_unemp_corr) < 0.3:
    st.markdown("Jobs (unemployment) don’t really change with internet use.")
else:
    st.markdown("Jobs (unemployment) have some link with internet use.")


# --- Footer ---
st.markdown("---")
st.markdown(
    "<center>© 2025 Urban Data Insights | Powered by Streamlit</center>",
    unsafe_allow_html=True
)
