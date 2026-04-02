# %% [markdown]
# # ABSTRACT AND INTRODUCTION

# %% [markdown]
# Here, I use Python 3.10 and visualizing software PowerBI to create a overview of financial relationship between medical manufactors and hospital - specifically Moffit Cancer Center. The data is open source gather from OpenPaymentData.cms.gov
# 
# Open payments is a public platform containing metadata showcasing the financial relationship between heathcare provides and its steak holders - medical companies, patients, goverment. I have always curious about the fundings acquisition and expense - where it cocme from, how it's used, what role each steak holders play in the financial envadors. Hence, i am using the data from a pretigious teaching hospital - Moffitt Cancer Center - to explore its payment in 2024.

# %% [markdown]
# # GOALS AND OBJECTIVES

# %% [markdown]
# 1. Total annual investment
# 2. Properties of Nature of payment
# 3. Top 10 company made research payment to Moffitt
# 2. Top and least funded product type
# 3. Top and least funded specialty 
# 4. Seasonal trend in spending
# 

# %% [markdown]
# # RAW DATA

# %%
import pandas as pd
import numpy as np
import os

# %%
research_pay = pd.read_csv("RAW_Research_payment.csv")
research_pay

# %% [markdown]
# # DATA CLEAN UP

# %% [markdown]
# ## Strip and remove empty columns

# %%
def strip_n_drop_raw_data(df):
    # Drop columns contain all NaN. Now there are only 89 cols from the original 252 cols. A significant decreased!
    print(f"Shape before: {df.shape}")
    df = df.dropna(axis="columns", how="all")

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.lower()
            df[col] = df[col].str.strip(".!? \n\t")

    print(f"Shape after: {df.shape}")
    return df

research_pay_clean = strip_n_drop_raw_data(research_pay)
research_pay_clean

# %% [markdown]
# ## Extract infomation of Hospital (recipients), Publications, Principal investigators, Donors

# %% [markdown]
# ### Group the columns into small chunk for managable cleanup in bulk

# %%
# For easy managment reduce the numuber of columns slowly
# Use the code below to gate out infomation about Moffit, as there should only be 1 hospital, 2 adress associate with Moffitt from quick web search
def large_df_to_smaller_groups(big_df):
    # Moffit info extraction
    groups = {
        "one_value":[], 
        "recipient":[], 
        "pi":[], 
        "payment":[],
        "product":[], 
        "other_manufacture":[], 
    }

    for col in big_df.columns:
        n_of_unique_to_find = 1
        if big_df[col].nunique(dropna = False) == n_of_unique_to_find: # dropna=Flase i want column that fill with 1 value only not NA
            groups["one_value"].append(col)

        elif "Recipient" in col or "Hospital" in col or "Change_Type" in col:
            groups["recipient"].append(col)

        elif "Investigator" in col:
            groups["pi"].append(col)

        elif "Payment" in col or "payment" in col:
            groups["payment"].append(col)

        elif "Drug" in col or "Product" in col:
            groups["product"].append(col)

        else:
            groups["other_manufacture"].append(col)
            
    return groups

# %%
group_dict = large_df_to_smaller_groups(research_pay_clean)

total_col = 0

for k, v in group_dict.items():
    print(f"{k}: {len(v)}")
    total_col += len(v)
print("-"*20)
print(f"Total columns: {total_col}; Is it the same as original df: {total_col == research_pay_clean.shape[1]}")

# %% [markdown]
# ## 6 smaller groups

# %%
def apply_specific_fix(df):
    print(f"Update adress and add missing values")

    address_col = "Recipient_Primary_Business_Street_Address_Line1"
    drug_col = "Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1"
    ndc_col = "Associated_Drug_or_Biological_NDC_1"

    if address_col in df.columns:
        df[address_col] = df[address_col].replace(
            "12902 magnolia dr", 
            "12902 magnolia drive"
        )
    else: 
        print(f"--Warning: Column '{address_col}' does not exist. Skipping address fix.")

    if drug_col in df.columns and ndc_col in df.columns:
        mask = df[drug_col] == "imdelltra (amg757)"
        df.loc[mask, ndc_col] = "55513"
    else:
        missing = [c for c in [drug_col, ndc_col] if c not in df.columns]
        print(f"--Warning: Column(s) {missing} not found. Skipping NDC mapping.")
    
    print(f"Update adress and add missing values -- DONE")
    return df

def final_clean_func(df):
    # RECIPIENT INFO CLEAN
    print(f"Update cases and format in recipient info")
    col_w_value_to_capitalize = ["Recipient_State", "Change_Type"]
    col_w_value_to_title = group_dict["recipient"] + group_dict["one_value"]

    for col in col_w_value_to_title:
        if col not in df.columns:
            continue

        if df[col].dtype == "object":
            if col in col_w_value_to_capitalize:
                df[col] = df[col].str.upper()
            else:
                df[col] = df[col].str.title()
        else:
            print(f"--Skipped {col}, It is a {df[col].dtype}, not object.")
    print(f"Update cases and format in recipient info-- DONE")

    # PI INFO CLEAN
    print(f"Update cases and format in PI info")
    for col in group_dict["pi"]:
        if df[col].dtype == "object":
            if "State" in col:
                df[col] = df[col].str.upper()
            else:
                df[col] = df[col].str.title()
    print(f"Update cases and format in PI info-- DONE")

    # DATE FORMATTING CLEAN
    print(f"Update date type and formatting in payment info")
    df['Date_of_Payment'] = pd.to_datetime(
        df['Date_of_Payment'], 
        format="%m/%d/%Y"
    )

    # PAYMENT INFO CLEAN
    for col in group_dict["payment"]:
        if df[col].dtype == "object":
            if "State" in col:
                df[col] = df[col].str.upper()
            elif "Form_of_Payment_or_Transfer_of_Value" in col:
                df[col] = df[col].str.capitalize()
            else:
                df[col] = df[col].str.title()
    print(f"Update date type and formatting in payment info-- DONE")

    # PRODUCT INFO CLEAN
    print(f"Update formatting in product info")
    for col in group_dict["product"]:
        if df[col].dtype == "object":
            df[col] = df[col].str.title()

            col_to_upper = ["ClinicalTrials_Gov_Identifier"]
    print(f"Update formatting in product info-- DONE")

    # OTHER INFO CLEAN
    print(f"Update formatting in othe and manufacture info")
    for col in group_dict["other_manufacture"]:
        if df[col].dtype == "object":
            if col in col_to_upper:
                df[col] = df[col].str.upper()
            else:
                df[col] = df[col].str.title()
    print(f"Update formatting in other and manufacture info-- DONE")

    return df

# %%
research_pay_clean = (
    research_pay_clean
    .pipe(apply_specific_fix)
    .pipe(final_clean_func)
)
research_pay_clean

# %% [markdown]
# # EXPORT CLEAN DATA

# %%
os.getcwd()

# %%
output_folder_name = "clean_data_final"
output_dir = os.path.join(os.getcwd(), output_folder_name)
os.makedirs(output_dir, exist_ok=True)

print(f"Checking output directory: {output_dir}")

final_file_path = os.path.join(output_dir, "clean_moffitt_research_payment.csv")
research_pay_clean.to_csv(final_file_path, sep = ",")
print(f"Exported to [{final_file_path}]")

# %% [markdown]
# # END


