# Project Overview
- Data cleaning and preprocessing
- Numerical analysis with NumPy
- Interactive visualizations with Plotly and Matplotlib
- Database integration with MySQL
- Excel export with conditional formatting
- Comprehensive statistical analysis
## Execution instructions 
## Step : Step 1: Clone the Repository
- git clone {your-repository-url}
- cd {project-directory}
## Step 2: Create Virtual Environment (Recommended)
- python -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate
## Step 3: Install Required Packages
- pip install streamlit pandas numpy plotly matplotlib sqlalchemy mysql-connector-python openpyxl xlsxwriter
## Step 4: Database Setup
1. Ensure MySQL server is running
2. Create a database user with appropriate privileges or use root
3. Update the database connection string in codebase.py if needed:
   engine = create_engine("mysql+mysqlconnector://root:your_password@localhost/SA_Trends")
## Step 5: Prepare Data Files
Place the following CSV files in the project root directory:
- datasets.csv - Primary dataset with urban population, unemployment, and internet usage data
- dataset2.csv - Secondary dataset with education, inequality, and female labor data
## Step 6: Run the Application
streamlit run codebase.py
##  Environment configuration 
1. Python 3.8+
2. Git
   ## Core libraries
   - Streamlit - Web application framework
   - Pandas - Data manipulation and analysis
   - NumPy - Numerical computing
   - Plotly Express - Interactive visualizations
   - Matplotlib - Static visualizations
   - SQLAlchemy - Database ORM and connectivity
   - mysql-connector-python - MySQL database driver
   - openpyxl - Excel file operations (for xlsxwriter dependency)
   ## Database
   MySQL - Relational database management system
## PC Details
1. Device name: DESKTOP-9VKBSRE
2. Processor: AMD Ryzen 5 5625U with Radeon Graphics          (2.30 GHz)
3. Installed RAM: 8,00 GB (7,31 GB usable
4. System type: 64-bit operating system, x64-based processor
5. Disk storage: 237

## Indicators used:
1) Individual internet Access (% population)
link: https://data360.worldbank.org/en/indicator/WB_WDI_IT_NET_USER_ZS

2) Unemployment, total (% of total labor force) (national estimate)
link: https://data360.worldbank.org/en/indicator/WB_WDI_SL_UEM_TOTL_NE_ZS

3) Urban population (% of total population)
link: https://data360.worldbank.org/en/indicator/WB_WDI_SP_URB_TOTL_IN_ZS

4) School enrollment, secondary (% net)
  link: https://data360.worldbank.org/en/indicator/WB_WDI_SE_SEC_NENR

5) Gini Index
link: https://data360.worldbank.org/en/indicator/WB_WDI_SI_POV_GINI

6) Labor force participation rate, female (% of female population ages 15+) (national estimate)
link: https://data360.worldbank.org/en/indicator/WB_WDI_SL_TLF_CACT_FE_NE_ZS

