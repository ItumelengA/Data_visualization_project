import streamlit as st
import pandas as pd
import numpy as np

def show_numerical_analysis():
    st.title("Project Report: Data Preparation & Numerical Analysis")

    # Dataset 1
    st.header("1. Load and Clean Dataset 1")
    df1 = pd.read_csv("datasets.csv")
    mapping_df1 = {
        "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "Urban Population",
        "Unemployment, total (% of total labor force) (national estimate) [SL.UEM.TOTL.NE.ZS]": "Unemployment Rate",
        "Individuals using the Internet (% of population) [IT.NET.USER.ZS]": "Internet Users",
        "Time": "Year",
        "Country Name": "Country"
    }
    df1 = df1.rename(columns=mapping_df1)
    for col in ["Urban Population", "Unemployment Rate", "Internet Users"]:
        df1[col] = pd.to_numeric(df1[col], errors="coerce")
    df1 = df1.dropna(subset=["Urban Population", "Unemployment Rate", "Internet Users"])
    st.subheader("Cleaned Dataset 1")
    st.write(df1.head())

    # Dataset 2
    st.header("2. Load and Clean Dataset 2")
    df2 = pd.read_csv("dataset2.csv")
    mapping_df2 = {
        "School enrollment, secondary (% net) [SE.SEC.NENR]": "Secondary Enrollment",
        "Gini index [SI.POV.GINI]": "Gini Index",
        "Labor force participation rate, female (% of female population ages 15+) (national estimate) [SL.TLF.CACT.FE.NE.ZS]": "Female Labor Force Participation",
        "Time": "Year",
        "Country Name": "Country"
    }
    df2 = df2.rename(columns=mapping_df2)
    for col in ["Secondary Enrollment", "Gini Index", "Female Labor Force Participation"]:
        df2[col] = pd.to_numeric(df2[col], errors="coerce")
    df2 = df2.dropna(subset=["Secondary Enrollment", "Gini Index", "Female Labor Force Participation"])
    st.subheader("Cleaned Dataset 2")
    st.write(df2.head())

    # Numerical Analysis
    st.header("3. Numerical Analysis with NumPy")

    # Dataset 1
    st.subheader("Dataset 1 Analysis (Urban, Jobs, Internet)")
    urban = df1["Urban Population"].to_numpy()
    unemployment = df1["Unemployment Rate"].to_numpy()
    internet = df1["Internet Users"].to_numpy()
    st.write("Urban Population → Mean:", np.mean(urban), "Std:", np.std(urban))
    st.write("Unemployment Rate → Mean:", np.mean(unemployment), "Std:", np.std(unemployment))
    st.write("Internet Users → Mean:", np.mean(internet), "Std:", np.std(internet))
    corr1 = np.corrcoef([urban, unemployment, internet])
    st.write("Correlation Matrix (Dataset 1):")
    st.write(corr1)
    urban_reshaped = urban.reshape(-1, 1)
    st.write("Urban Population reshaped (first 5 rows):", urban_reshaped[:5])

    # Dataset 2
    st.subheader("Dataset 2 Analysis (Education, Inequality, Female Work)")
    secondary = df2["Secondary Enrollment"].to_numpy()
    gini = df2["Gini Index"].to_numpy()
    female_lfp = df2["Female Labor Force Participation"].to_numpy()
    st.write("Secondary Enrollment → Mean:", np.mean(secondary), "Std:", np.std(secondary))
    st.write("Gini Index → Mean:", np.mean(gini), "Std:", np.std(gini))
    st.write("Female LFP → Mean:", np.mean(female_lfp), "Std:", np.std(female_lfp))
    corr2 = np.corrcoef([secondary, gini, female_lfp])
    st.write("Correlation Matrix (Dataset 2):")
    st.write(corr2)
    secondary_reshaped = secondary.reshape(-1, 1)
    st.write("Secondary Enrollment reshaped (first 5 rows):", secondary_reshaped[:5])

    # Insights
    st.header("4. Insights & Findings")
    st.markdown("""
    ### Dataset 1 (Urban, Jobs, Internet)
    - Urban Population & Internet Users: More city living → more internet use.  
    - Unemployment: Small positive link with internet use (maybe job search or staying connected).  
    - Overall: Internet is driven by urban growth, not jobs.

    ### Dataset 2 (Education, Inequality, Female Work)
    - Weak Links: Education, inequality, and women’s work don’t strongly affect each other.  
    - Education: Schooling isn’t directly tied to inequality.  
    - Female Work: Participation depends more on culture or policies, not inequality or schooling.

    Comparison
    - Dataset 1 (Technology): Internet growth follows city growth.  
    - Dataset 2 (Society): Social progress (schooling, equality, working women) follows its own slower path.  
                
    - Technology adoption is faster and tied to cities, while social change is slower and influenced by culture and policies.
    """)