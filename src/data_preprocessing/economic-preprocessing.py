from typing import Dict
import pandas as pd
import os


# preprocess income of tax payers data
df_income = pd.read_excel(
    "../data/economic-data/income-of-tax-payers.xlsx",
    sheet_name="Total Income",
    header=1,
).dropna(subset=["Code"])

rows = []

for year in range(1999, 2022):
    if year == 2008:  # data is missing for 2008
        continue

    offset = 2 if year < 2008 else -1
    column_index = (year - 1999) * 3 + offset

    for _, row in df_income.iterrows():
        rows.append(
            {
                "Year": year,
                "Area": row["Area"].replace("-", " "),
                "number_of_respondents_income": row.iloc[column_index],
                "mean": row.iloc[column_index + 1],
                "median": row.iloc[column_index + 2],
            }
        )

df_reshaped = pd.DataFrame(rows)

df_reshaped[df_reshaped["Year"] > 2000].tail(10)

os.makedirs("../data/economic-data/indexed/", exist_ok=True)

output_file_path = "../data/economic-data/indexed/income-of-tax-payers.csv"
df_reshaped.to_csv(output_file_path, index=False)


# preprocess economic activity by gender

path = "../data/economic-data/economic-activity-by-gender.xlsx"
df_activity = pd.read_excel(path, sheet_name=None)

df_activity["Females"].iloc[
    43, 1
] = "South East"  # they misspelled "South East" as "South West" in Females data

rows = []

for year in range(2005, 2024):
    df_males = df_activity["Males"].iloc[2:].dropna(subset=["Area"])
    df_females = df_activity["Females"].iloc[2:].dropna(subset=["Area"])

    for i in range(df_males.shape[0]):
        row_males = df_males.iloc[i]
        row_females = df_females.iloc[i]

        assert row_males["Area"] == row_females["Area"]

        year_index = year - 2005

        row_index = year_index + 3 * year_index + 2

        rows.append(
            {
                "Year": year,
                "Area": row_males["Area"],
                "economically_active_male": row_males.iloc[row_index],
                "economically_active_female": row_females.iloc[row_index],
                "working_age_male": row_males.iloc[row_index + 1],
                "working_age_female": row_females.iloc[row_index + 1],
                "confindence_male": row_males.iloc[row_index + 3],
                "confidence_female": row_females.iloc[row_index + 3],
            }
        )

df = pd.DataFrame(rows)

os.makedirs("../data/economic-data/indexed/", exist_ok=True)

output_file_path = "../data/economic-data/indexed/economic-activity-by-gender.csv"
df.to_csv(output_file_path, index=False)


# preprocess economic inactivity data

df_economic_inactivity = pd.read_csv("../data/economic-data/economic-inactivity.csv")

cols = ["Economically Inactive", "Working age", "percent", "confidence"]

restructured_data = pd.DataFrame(columns=["Year", "Borough"] + cols)

for year_range in range(2004, 2024):
    year_columns = [f"{col}; Jan {year_range}-Dec {year_range}" for col in cols]
    temp_df = df_economic_inactivity[["Area"] + year_columns].copy()

    temp_df.columns = ["Borough"] + cols
    temp_df["Year"] = year_range
    temp_df = temp_df[["Year", "Borough"] + cols]

    restructured_data = pd.concat([restructured_data, temp_df], ignore_index=True)

restructured_data = restructured_data.rename(columns={"Borough": "Area"})

os.makedirs("../data/economic-data/indexed/", exist_ok=True)

output_file_path = "../data/economic-data/indexed/economic-inactivity-index.csv"
restructured_data.to_csv(output_file_path, index=False)


# preprocess employment industry data
df_employment_industry = pd.read_excel(
    "../data/economic-data/employment-rate-by-industry.xlsx", sheet_name=None
)


cols = ["economically_inactive", "working_age_percent", "confidence"]
cleaned_dfs = []

column_mapping = {
    "Unnamed: 1": "Area",
    "Unnamed: 3": "total_working_population",
    "A:agriculture and fishing": "agriculture_and_fishing",
    "Unnamed: 5": "agriculture_and_fishing_confidence",
    "B,D,E:energy and water": "energy_and_water",
    "Unnamed: 9": "energy_and_water_confidence",
    "C:manufacturing": "manufacturing",
    "Unnamed: 13": "manufacturing_confidence",
    "F:construction": "construction",
    "Unnamed: 17": "construction_confidence",
    "G,I:distribution, hotels and restaurants": "distribution_hotels_and_restaurants",
    "Unnamed: 21": "distribution_hotels_and_restaurants_confidence",
    "H,J:transport and communications": "transport_and_communications",
    "Unnamed: 25": "transport_and_communications_confidence",
    "K-N:banking, finance and insurance": "banking_finance_and_insurance",
    "Unnamed: 29": "banking_finance_and_insurance_confidence",
    "O-Q:public admin. education and health": "public_admin_education_and_health",
    "Unnamed: 33": "public_admin_education_and_health_confidence",
    "R-U:other services": "other_services",
    "Unnamed: 37": "other_services_confidence",
    "G-U:total services": "total_services",
    "Unnamed: 41": "total_services_confidence",
}

selected_columns = ["Year"] + list(column_mapping.values())


for year, df in df_employment_industry.items():
    if year.isdigit() == False:
        continue

    df = df.rename(columns=column_mapping)
    df["Year"] = year
    df = df[selected_columns]
    df = df.rename(columns=column_mapping)
    cleaned_dfs.append(df)


merged_cleaned_df = pd.concat(cleaned_dfs, ignore_index=True)
merged_cleaned_df.dropna(subset=["Area"], inplace=True)
merged_cleaned_df.sort_values(by=["Area", "Year"], inplace=True)
merged_cleaned_df = merged_cleaned_df.iloc[20:]

merged_cleaned_df.head(10)

os.makedirs("../data/economic-data/indexed/", exist_ok=True)

output_file_path = "../data/economic-data/indexed/employment-rate-by-industry.csv"
merged_cleaned_df.to_csv(output_file_path, index=False)


# preprocess gender employment data
path = "../data/economic-data/employment-status-by-genderxls.xlsx"
eployment_df = pd.read_excel(path, sheet_name=None)

cleaned_dfs = []

for year, df in eployment_df.items():
    if year == "Metadata":
        continue

    df.columns = df.columns.str.strip()

    column_mapping = {
        "% in employment who are employees - working age": "total_employed",
        "Unnamed: 5": "total_employed_confidence",
        "% in employment who are self employed - working age": "total_self_employed",
        "Unnamed: 9": "total_self_employed_confidence",
        "% in employment working full-time - working age": "total_full_time",
        "Unnamed: 13": "total_full_time_confidence",
        "% in employment working part-time - working age": "total_part_time",
        "Unnamed: 17": "total_part_time_confidence",
        "% of males in employment rate working full-time - working age": "males_full_time",
        "Unnamed: 21": "males_full_time_confidence",
        "% of males in employment rate working part-time - working age": "males_part_time",
        "Unnamed: 25": "males_part_time_confidence",
        "% of females in employment rate working full-time - working age": "females_full_time",
        "Unnamed: 29": "females_full_time_confidence",
        "% of females in employment rate working part-time - working age": "females_part_time",
        "Unnamed: 33": "females_part_time_confidence",
    }

    df = df.rename(columns=column_mapping)
    df["Year"] = year
    selected_columns = ["Year", "Area"] + list(column_mapping.values())
    df = df[selected_columns]

    cleaned_dfs.append(df)


merged_cleaned_df = pd.concat(cleaned_dfs, ignore_index=True)
merged_cleaned_df.dropna(subset=["Area"], inplace=True)
merged_cleaned_df.sort_values(by=["Area", "Year"], inplace=True)

merged_cleaned_df.head(20)

os.makedirs("../data/economic-data/indexed/", exist_ok=True)

output_file_path = "../data/economic-data/indexed/employment-status-by-gender.csv"
merged_cleaned_df.to_csv(output_file_path, index=False)


# preprocess economic inactivity by gender and reason

path = "../data/economic-data/economic-inactivity-by-gender-reason.xlsx"
excel_economic_activity_gender = pd.ExcelFile(path)

males_data = pd.read_excel(path, sheet_name="Males")
females_data = pd.read_excel(path, sheet_name="Females")

males_data.head(), females_data.head()

males_data_corrected = pd.read_excel(path, sheet_name="Males", header=2)
females_data_corrected = pd.read_excel(path, sheet_name="Females", header=2)

males_data_corrected.columns.values[:2] = ["Code", "Area"]
females_data_corrected.columns.values[:2] = ["Code", "Area"]

males_data_corrected.head(), females_data_corrected.head()


males_data_corrected = pd.read_excel(path, sheet_name="Males", header=2)
females_data_corrected = pd.read_excel(path, sheet_name="Females", header=2)

males_data_corrected.columns.values[:2] = ["Code", "Area"]
females_data_corrected.columns.values[:2] = ["Code", "Area"]

males_data_corrected.columns = ["Code", "Area"] + [
    f"{metric}_{year}"
    for year in range(2004, 2024)
    for metric in ["Economically Inactive", "Working age", "percent", "confidence"]
]
females_data_corrected.columns = ["Code", "Area"] + [
    f"{metric}_{year}"
    for year in range(2004, 2024)
    for metric in ["Economically Inactive", "Working age", "percent", "confidence"]
]

males_melted = males_data_corrected.melt(
    id_vars=["Code", "Area"], var_name="Metric_Year", value_name="Value"
)
females_melted = females_data_corrected.melt(
    id_vars=["Code", "Area"], var_name="Metric_Year", value_name="Value"
)

males_melted["Year"] = males_melted["Metric_Year"].str.extract(r"(\d{4})")[0]
males_melted["Metric"] = (
    males_melted["Metric_Year"].str.extract(r"([a-zA-Z\s]+)")[0].str.strip()
)

females_melted["Year"] = females_melted["Metric_Year"].str.extract(r"(\d{4})")[0]
females_melted["Metric"] = (
    females_melted["Metric_Year"].str.extract(r"([a-zA-Z\s]+)")[0].str.strip()
)

metrics = ["Economically Inactive", "Working age", "percent", "confidence"]
males_filtered = males_melted[males_melted["Metric"].isin(metrics)]
females_filtered = females_melted[females_melted["Metric"].isin(metrics)]

males_pivot = males_filtered.pivot_table(
    index=["Area", "Year"], columns="Metric", values="Value", aggfunc="first"
).reset_index()
females_pivot = females_filtered.pivot_table(
    index=["Area", "Year"], columns="Metric", values="Value", aggfunc="first"
).reset_index()

males_pivot.columns = ["Area", "Year"] + [
    f"{col}_male" for col in males_pivot.columns if col not in ["Area", "Year"]
]
females_pivot.columns = ["Area", "Year"] + [
    f"{col}_female" for col in females_pivot.columns if col not in ["Area", "Year"]
]

combined_pivot = pd.merge(males_pivot, females_pivot, on=["Area", "Year"], how="outer")

combined_pivot = combined_pivot.sort_values(by=["Area", "Year"])


combined_pivot.head()


os.makedirs("../data/economic-data/indexed/", exist_ok=True)

output_file_path = (
    "../data/economic-data/indexed/economic-inactivity-by-gender-reason.csv"
)
combined_pivot.to_csv(output_file_path, index=False)

# preprocess jobs and density dataset

df_job_density = pd.read_csv("../data/economic-data/jobs-and-job-density.csv")

df_job_density = df_job_density.drop(0)

df_melted = df_job_density.melt(
    id_vars=["Code", "Area"], var_name="Year", value_name="job_density"
)

df_melted = df_melted.drop(columns=["Code"])

df_melted["job_density"] = df_melted["job_density"].str.replace(",", "")
df_melted["job_density"] = pd.to_numeric(df_melted["job_density"], errors="coerce")
df_melted = df_melted.dropna(subset=["Area"])
df_melted["job_density"] = df_melted["job_density"].fillna(0).astype(int)

os.makedirs("../data/economic-data/indexed/", exist_ok=True)

output_file_path = "../data/economic-data/indexed/jobs-and-job-density.csv"
df_melted.to_csv(output_file_path, index=False)

datasets: Dict[str, pd.DataFrame] = {}

for file in os.listdir("../data/economic-data/indexed"):
    if file.endswith(".csv"):
        datasets[file] = pd.read_csv(f"../data/economic-data/indexed/{file}")

sets = [set(df['Area']) for df in datasets.values()]

union_set = set.union(*sets) # all unique boroughs/areas
intersection_set = set.intersection(*sets) # exist in all datasets

non_common_areas = union_set - intersection_set

for file in datasets:
    datasets[file] = datasets[file].reset_index(drop=True).set_index(['Area', 'Year'])

joined_df = pd.concat(datasets.values(), axis=1, join='inner')

joined_df.reset_index(inplace=True)

excluded_areas = [
    "City of London",
    "North East",
    "North West",
    "Yorkshire and The Humber",
    "East Midlands",
    "West Midlands",
    "London",
    "South East",
    "South West",
    "England",
    "Wales",
    "Scotland",
    "Northern Ireland",
    "United Kingdom",
]

joined_df = joined_df[~joined_df["Area"].isin(excluded_areas)]

joined_df.to_csv("../data/economic-data/indexed/joined-economic.csv")
