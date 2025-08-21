# app.py
import streamlit as st
import pandas as pd
import numpy as np

# Title
st.title("Project Heading")


# Data Preparations

# 1. Load the dataset
st.write("Dataset")
df = pd.read_csv("datasets.csv")
st.write(df)

st.header("Cleaning the dataset")
st.markdown("""
**Data Cleaning:**
- **Renaming columns**  
- **Removing duplicates**  
- **Handling missing values**  
- **Correcting data types**  
""")
#Renaming columns names
df = df.rename(columns={"Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "Urban Population",
               "Unemployment, total (% of total labor force) (national estimate) [SL.UEM.TOTL.NE.ZS]": "Unemployment Rate",
               "Individuals using the Internet (% of population) [IT.NET.USER.ZS]": "Internet Users"})
#drop duplicates
df = df.drop_duplicates()

#drop null values
df = df.replace("..", pd.NA)
df = df.dropna()

# Correct data types
df['Unemployment Rate'] = df['Unemployment Rate'].astype(float)
df['Internet Users'] = df['Internet Users'].astype(float)

st.write(df)

#Insights
st.subheader("Descriptive statistics and insights")
st.markdown(""" 
- **Urban Population**: The dataset shows the percentage of the population living in urban areas.""")

st.subheader("Numerical Analysis")
