# Moffitt_Payment_Python_PowerBI
Python (Pandas, Numpy, Script), PowerBI (Interactive Dashboard, Power Querry)

# I. Summary and objective
This project is an end-to-end financial analytics case focus on understanding research demand pattern, product, and financial insight of Moffitt Cancer Center hospital. The goal is to design an analytical pipeline and interactive dashboard so stakeholders can monitor research trends, identify which product or therapuetic area is Moffitt's domain of specialty.

# II. Business question
Using experience at BioTuring, employed ELT (Extract, Load, Transform) pipeline and data transformation principals to create reusable script for any future data from Open Payment relate to Moffitt Cancer Center. Result in a clean, visual ready dataset.

Create multipages interactive dashborad answering questions about cashflow, specialty, manufacture and product preferences

# III. Data and metrics
## 1. Dimensional reduction
To managed the overwhelmingly large number of columns (200+) in the raw dataset, I developed a “Categorical sorter” function (large_df_to_smaller_groups). This turn the huge data into more manageable groups base on their contents:
    • Static data: identify columns with only one unique value as they are often not helpful for analysis.
    • Entities: group base on commonly seen term in hospital setting (Recipient, Principal investigators (PI), Payments, Products, and Manufacture info)
## 2. Target data correction, exploratory graphs
Created some default graphs using pandas plot function to get an idea of the data and the nessesry columns. 
Targeted only the relavent columnst when correcting any typos and missing values to save time coding.
## 3. Standardization:
Apply upper case, title case. sentence case, data type casting (date time format, number format, character format) for more exploratory visual in Python.
# IV. Dashborad in PowerBI
Create multipages interactive dashborad answering questions about cashflow, specialty, manufacture and product preferences, PI contributions.

# First look
![Figure 1](https://github.com/BuuLinhTran/Moffitt_Payment_Python_PowerBI/blob/main/Fig_1.png)

# End of report.
