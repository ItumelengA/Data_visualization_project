import streamlit as st
import pandas as pd
import plotly.express as px

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
    ["Dataset Overview", "Cleaning Steps", "Visualizations", "Insights"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Group Members:\n"
    "1. Itumeleng Amantle\n"
    "2. Boago Olyn\n"
    "3. --\n"
    "4. --\n"
    "5. --\n"
    "6. --\n\n"
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
    fig = px.box(df_filtered, y="Unemployment Rate", points="all", color_discrete_sequence=["#F9A826"])
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

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center>© 2025 Urban Data Insights | Powered by Streamlit</center>",
    unsafe_allow_html=True
)
