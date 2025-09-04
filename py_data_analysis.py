import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def show_py_excel_analysis():
    st.title("Project Heading")

    # Data Preparations
    st.write("Dataset")
    df1 = pd.read_csv("datasets.csv")
    df2 = pd.read_csv("dataset2.csv")
    st.write(df1)
    st.write(df2)

    st.header("Cleaning the dataset")
    st.markdown("""
    **Data Cleaning:**
    - **Renaming columns**  
    - **Removing duplicates**  
    - **Handling missing values**  
    - **Correcting data types**  
    """)

    # Renaming columns names
    df1 = df1.rename(columns={
        "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "Urban Population",
        "Unemployment, total (% of total labor force) (national estimate) [SL.UEM.TOTL.NE.ZS]": "Unemployment Rate",
        "Individuals using the Internet (% of population) [IT.NET.USER.ZS]": "Internet Users"
    })

    df2 = df2.rename(columns={
        "School enrollment, secondary (% net) [SE.SEC.NENR]": "School Enrollment (Secondary, % net)",
        "Gini index [SI.POV.GINI]": "Gini Index",
        "Labor force participation rate, female (% of female population ages 15+) (national estimate) [SL.TLF.CACT.FE.NE.ZS]": "Female Labor Force Participation"
    })

    st.write("Cleaned df")
    st.write(df1.head())
    st.write("Cleaned df2")
    st.write(df2.head())

    # Drop duplicates
    df1 = df1.drop_duplicates()
    df2 = df2.drop_duplicates()

    # Drop null values
    df1 = df1.replace("..", pd.NA)
    df1 = df1.dropna()
    df2 = df2.replace("..", pd.NA)
    df2 = df2.dropna()

    # Correct data types
    df1['Unemployment Rate'] = df1['Unemployment Rate'].astype(float)
    df1['Internet Users'] = df1['Internet Users'].astype(float)
    df1['Urban Population'] = df1['Urban Population'].astype(float)
    df2['School Enrollment (Secondary, % net)'] = df2['School Enrollment (Secondary, % net)'].astype(float)
    df2['Gini Index'] = df2['Gini Index'].astype(float)

    st.write(df1)
    st.write(df2)

    # Insights
    st.subheader("Descriptive statistics and insights")
    st.markdown(""" 
    - **Urban Population**: The dataset shows the percentage of the population living in urban areas.""")
    st.subheader("Numerical Analysis")

    # Clean and transform Dataset 1
    fn = "datasets.csv"
    if not os.path.exists(fn):
        st.error(f"File not found: {fn} — place datasets.csv in the app folder")
        st.stop()
    df1 = pd.read_csv(fn)
    st.subheader(" Dataset 1")
    st.write("Initial shape:", df1.shape)
    st.dataframe(df1.head())

    mapping = {
        "Urban population (% of total population) [SP.URB.TOTL.IN.ZS]": "Urban Population",
        "Unemployment, total (% of total labor force) (national estimate) [SL.UEM.TOTL.NE.ZS]": "Unemployment Rate",
        "Individuals using the Internet (% of population) [IT.NET.USER.ZS]": "Internet Users",
        "Time": "Year",
        "Country Name": "Country",
        "Country": "Country",
        "CountryName": "Country",
    }
    rename_map = {c: mapping[c] for c in df1.columns if c in mapping}
    df1 = df1.rename(columns=rename_map)
    st.write("✅ After renaming columns:")
    st.write(list(df1.columns))

    # Rename columns for dataset 2 df2 
    fn2 = "dataset2.csv"   
    if not os.path.exists(fn2):
        st.error(f"File not found: {fn2} — place dataset1.csv in the app folder")
        st.stop()
    df2 = pd.read_csv(fn2)
    st.subheader("Dataset 2")
    st.write("Initial shape:", df2.shape)
    st.dataframe(df2.head())

    mapping2 = {
        "School enrollment, secondary (% net) [SE.SEC.NENR]": "School Enrollment (Secondary, % net)",
        "Gini index [SI.POV.GINI]": "Gini Index",
        "Labor force participation rate, female (% of female population ages 15+) (national estimate) [SL.TLF.CACT.FE.NE.ZS]": "Female Labor Force Participation",
        "Time": "Year",
        "Country Name": "Country",
        "Country": "Country",
        "CountryName": "Country",
    }
    rename_map2 = {c: mapping2[c] for c in df2.columns if c in mapping2}
    df2 = df2.rename(columns=rename_map2)
    st.write("✅ After renaming columns in df2:")
    st.write(list(df2.columns))

    # --- Clean Dataset 1 and transform---
    st.subheader("Clean and transform Dataset 1")
    df1 = df1.drop_duplicates()
    df1 = df1.replace({"..": pd.NA, "": pd.NA})
    if 'Year' in df1.columns:
        df1['Year'] = pd.to_numeric(df1['Year'], errors='coerce').astype('Int64')
    numeric_cols = []
    for col in ['Unemployment Rate', 'Internet Users', 'Urban Population']:
        if col in df1.columns:
            df1[col] = pd.to_numeric(df1[col], errors='coerce')
            numeric_cols.append(col)
    st.write("Numeric columns cleaned:", numeric_cols)
    st.write("Missing counts:")
    st.write(df1[numeric_cols].isna().sum())
    cols_core = [c for c in ['Unemployment Rate', 'Internet Users'] if c in df1.columns]
    df1 = df1.dropna(subset=cols_core, how='all')
    for col in numeric_cols:
        if df1[col].isna().any():
            median_val = df1[col].median(skipna=True)
            df1[col] = df1[col].fillna(median_val)
    st.success("Dataset 1 cleaned successfully!")
    clean = df1.copy()
    for col in numeric_cols:
        clean[col] = clean[col].round(3)
    st.subheader("📊 Descriptive Stats dataset 1 ")
    st.dataframe(clean[numeric_cols].describe().T)

    # --- Clean Dataset 2 and transform ---
    st.subheader("Clean and transform Dataset 2")
    df2 = df2.drop_duplicates()
    df2 = df2.replace({"..": pd.NA, "": pd.NA})
    if 'Year' in df2.columns:
        df2['Year'] = pd.to_numeric(df2['Year'], errors='coerce').astype('Int64')
    numeric_cols2 = [
        col for col in df2.columns 
        if col not in ['Year', 'Country', 'Country Code', 'Time Code']
    ]
    for col in numeric_cols2:
        df2[col] = pd.to_numeric(df2[col], errors='coerce')
    st.write("Numeric columns cleaned (dataset 2):", numeric_cols2)
    st.write("Missing counts (dataset 2):")
    st.write(df2[numeric_cols2].isna().sum())
    df2 = df2.dropna(subset=numeric_cols2, how='all')
    for col in numeric_cols2:
        if df2[col].isna().any():
            median_val = df2[col].median(skipna=True)
            df2[col] = df2[col].fillna(median_val)
    st.success("Dataset 2 cleaned successfully!")
    clean2 = df2.copy()
    for col in numeric_cols2:
        clean2[col] = clean2[col].round(3)
    if numeric_cols2:
        st.subheader("📊 Descriptive Stats dataset 2")
        st.dataframe(clean2[numeric_cols2].describe().T)
    else:
        st.warning("No numeric columns found in Dataset 2 after cleaning.")

    # Excel Export, conditional formatting
    st.subheader("💾 Excel Export, conditional formatting")
    dataset_choice = st.selectbox(
        "Select which dataset to download:",
        ["Dataset 1", "Dataset 2"]
    )
    if dataset_choice == "Dataset 1":
        data_to_export = clean
        file_prefix = "dataset1"
    else:
        data_to_export = clean2
        file_prefix = "dataset2"
    csv = data_to_export.to_csv(index=False).encode("utf-8")
    st.download_button(
        f"Download {dataset_choice} as CSV",
        data=csv,
        file_name=f"{file_prefix}_cleaned.csv",
        mime="text/csv"
    )
    excel_out = f"{file_prefix}_cleaned_conditional.xlsx"
    with pd.ExcelWriter(excel_out, engine='xlsxwriter') as writer:
        data_to_export.to_excel(writer, sheet_name='cleaned', index=False)
        workbook = writer.book
        worksheet = writer.sheets['cleaned']
        nrows = len(data_to_export)
        def col_idx_to_excel(col_idx):
            letters = ''
            while col_idx >= 0:
                letters = chr(col_idx % 26 + 65) + letters
                col_idx = col_idx // 26 - 1
            return letters
        # Conditional formatting
        if 'Unemployment Rate' in data_to_export.columns:
            col_unemp = data_to_export.columns.get_loc('Unemployment Rate')
            col_letter = col_idx_to_excel(col_unemp)
            cell_range = f'{col_letter}2:{col_letter}{nrows+1}'
            q75 = data_to_export['Unemployment Rate'].quantile(0.75)
            fmt_red = workbook.add_format({'bg_color': '#FFC7CE'})
            worksheet.conditional_format(cell_range, {'type':'cell','criteria':'>','value':q75,'format':fmt_red})
            worksheet.conditional_format(cell_range, {'type':'data_bar'})
        if 'Internet Users' in data_to_export.columns:
            col_inet = data_to_export.columns.get_loc('Internet Users')
            col_letter = col_idx_to_excel(col_inet)
            cell_range = f'{col_letter}2:{col_letter}{nrows+1}'
            q75 = data_to_export['Internet Users'].quantile(0.75)
            fmt_green = workbook.add_format({'bg_color': '#C6EFCE'})
            worksheet.conditional_format(cell_range, {'type':'cell','criteria':'>','value':q75,'format':fmt_green})
            worksheet.conditional_format(cell_range, {'type':'3_color_scale'})
        if 'Urban Population' in data_to_export.columns:
            col_urb = data_to_export.columns.get_loc('Urban Population')
            col_letter = col_idx_to_excel(col_urb)
            cell_range = f'{col_letter}2:{col_letter}{nrows+1}'
            worksheet.conditional_format(cell_range, {'type':'3_color_scale'})
        if 'School Enrollment (Secondary, % net)' in data_to_export.columns:
            col_school = data_to_export.columns.get_loc('School Enrollment (Secondary, % net)')
            col_letter = col_idx_to_excel(col_school)
            cell_range = f'{col_letter}2:{col_letter}{nrows+1}'
            worksheet.conditional_format(cell_range, {'type':'3_color_scale'})
        if 'Gini Index' in data_to_export.columns:
            col_gini = data_to_export.columns.get_loc('Gini Index')
            col_letter = col_idx_to_excel(col_gini)
            cell_range = f'{col_letter}2:{col_letter}{nrows+1}'
            worksheet.conditional_format(cell_range, {'type':'3_color_scale'})
        if 'Female Labor Force Participation' in data_to_export.columns:
            col_female = data_to_export.columns.get_loc('Female Labor Force Participation')
            col_letter = col_idx_to_excel(col_female)
            cell_range = f'{col_letter}2:{col_letter}{nrows+1}'
            worksheet.conditional_format(cell_range, {'type':'data_bar'})
    st.info(f"Excel with conditional formatting written locally as {excel_out}")

    # Charts and summarise findings
    # -------- Dataset 1 Charts --------
    if not clean.empty:
        st.subheader("📈 Trends in Dataset 1")
        numeric_cols1 = ['Urban Population', 'Unemployment Rate', 'Internet Users']
        if 'Year' in clean.columns:
            fig, ax = plt.subplots(figsize=(10,5))
            for col in numeric_cols1:
                clean.groupby('Year')[col].mean().plot(ax=ax, label=col)
            ax.set_title("Average Trends over Years ")
            ax.set_xlabel("Year")
            ax.set_ylabel("Value")
            ax.legend()
            st.pyplot(fig)
        if 'Internet Users' in clean.columns and 'Urban Population' in clean.columns:
            fig, ax = plt.subplots()
            ax.scatter(clean['Urban Population'], clean['Internet Users'], alpha=0.5)
            ax.set_title("Internet Users vs Urban Population")
            ax.set_xlabel("Urban Population (%)")
            ax.set_ylabel("Internet Users (%)")
            st.pyplot(fig)
        st.markdown("""
        **Findings (Dataset 1):**
        - Urban population generally increases over time.
        - Internet users show strong growth, especially in later years.
        - Higher urbanization tends to correlate with more Internet users.
        """)

    # -------- Dataset 2 Charts --------
    if not clean2.empty:
        st.subheader("📈 Trends in Dataset 2")
        numeric_cols2 = ['School Enrollment (Secondary, % net)', 'Gini Index', 'Female Labor Force Participation']
        if 'Year' in clean2.columns:
            fig, ax = plt.subplots(figsize=(10,5))
            for col in numeric_cols2:
                if col in clean2.columns:
                    clean2.groupby('Year')[col].mean().plot(ax=ax, label=col)
            ax.set_title("Average Trends over Years ")
            ax.set_xlabel("Year")
            ax.set_ylabel("Value")
            ax.legend()
            st.pyplot(fig)
        if 'Gini Index' in clean2.columns and 'School Enrollment (Secondary, % net)' in clean2.columns:
            fig, ax = plt.subplots()
            ax.scatter(clean2['Gini Index'], clean2['School Enrollment (Secondary, % net)'], alpha=0.5)
            ax.set_title("Gini Index vs School Enrollment")
            ax.set_xlabel("Gini Index (Inequality)")
            ax.set_ylabel("School Enrollment (% net)")
            st.pyplot(fig)
        if 'Female Labor Force Participation' in clean2.columns and 'School Enrollment (Secondary, % net)' in clean2.columns:
            fig, ax = plt.subplots()
            ax.scatter(clean2['Female Labor Force Participation'], clean2['School Enrollment (Secondary, % net)'], alpha=0.5, color='green')
            ax.set_title("Female Labor Force Participation vs School Enrollment")
            ax.set_xlabel("Female Labor Force Participation (%)")
            ax.set_ylabel("School Enrollment (% net)")
            st.pyplot(fig)
        st.markdown("""
        **Findings (Dataset 2):**
        - School enrollment rates generally improve over time.
        - Female labor force participation fluctuates but shows some growth.
        - Higher inequality (Gini Index) may correlate with lower school enrollment.
        - Countries (or years) with higher female labor force participation tend to have better school enrollment outcomes.
        """)