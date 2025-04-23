import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === Load Dataset ===
globe_sustain = pd.read_csv("PATH TO CSV")

print(globe_sustain.info())
print(globe_sustain.head())

# === Clean Population Density Column (convert from string with commas) ===
globe_sustain['pop_density_square_km'] = (
    globe_sustain['pop_density_square_km']
    .str.replace(',', '', regex=False)
    .astype(float)
)

# === Drop Sparse Columns ===
cols_to_drop = [ 'finance_assist', 'primary_elec_equiv_to_renew', 'renew_elec_person']
globe_sustain.drop(columns=cols_to_drop, inplace=True)
print("\nDropped columns with excessive null values:", cols_to_drop)

# === Drop Countries Missing lat/long for All Years ===
countries_to_drop = globe_sustain.groupby('country')[['lat', 'long']].apply(
    lambda df: df.isnull().all().any()
)

# Just French Guiana
globe_sustain = globe_sustain[~globe_sustain['country'].isin(countries_to_drop[countries_to_drop].index)]
print("Dropping countries with missing lat/long for all years:")
print(countries_to_drop[countries_to_drop].index.tolist())

# === Analyze Missing Values by Country ===
missing_by_country = globe_sustain.groupby('country').apply(lambda group: group.isnull().sum())
total_missing_per_country = missing_by_country.sum(axis=1).sort_values(ascending=False)
print(total_missing_per_country.head(10))

# === Drop Countries with >5 Missing Values ===
high_null_countries = total_missing_per_country[total_missing_per_country > 5].index
globe_sustain = globe_sustain[~globe_sustain['country'].isin(high_null_countries)]
print(f"\nDropped {len(high_null_countries)} countries with >5 missing values.")

# === Recalculate total missing values per country AFTER filtering ===
filtered_missing_by_country = globe_sustain.groupby('country').apply(lambda group: group.isnull().sum())
filtered_total_missing_per_country = filtered_missing_by_country.sum(axis=1)
filtered_missing_counts = filtered_total_missing_per_country.value_counts().sort_index()

# === Plot Updated Distribution ===
# plt.figure(figsize=(10, 6))
# filtered_missing_counts.plot(kind='bar')
# plt.title('Number of Countries by Total Missing Values (After Filtering)')
# plt.xlabel('Total Missing Values')
# plt.ylabel('Number of Countries')
# plt.tight_layout()
# plt.show()

# === Plot Distribution of Missing Values per Country ===
# missing_counts = total_missing_per_country.value_counts().sort_index()
# plt.figure(figsize=(10, 6))
# missing_counts.plot(kind='bar')
# plt.title('Number of Countries by Total Missing Values')
# plt.xlabel('Total Missing Values')
# plt.ylabel('Number of Countries')
# plt.tight_layout()
# plt.show()

# === Final Null Check ===
print("\nRemaining missing values per column:")
print(globe_sustain.isnull().sum())

# === Export the almost cleaned  ===
#globe_sustain.to_csv("almost_cleaned_global_sustainability.csv", index=False)

#print("Cleaned data exported to 'almost_cleaned_global_sustainability.csv'")


# Drop 2020 data
globe_sustain = globe_sustain[globe_sustain['year'] != 2020]

print("\nDropped all rows from year 2020.")

# Recalculate missing values after dropping 2020
missing_by_country = globe_sustain.groupby('country').apply(lambda group: group.isnull().sum())
total_missing_per_country = missing_by_country.sum(axis=1).sort_values(ascending=False)

print("\nTop 10 countries by total missing values after dropping 2020:")
print(total_missing_per_country.head(10))

missing_counts = total_missing_per_country.value_counts().sort_index()

# === Plot Distribution of Missing Values per Country After Removing 2020 ===
# missing_counts = total_missing_per_country.value_counts().sort_index()
# plt.figure(figsize=(10, 6))
# missing_counts.plot(kind='bar')
# plt.title('Number of Countries by Total Missing Values (After Dropping 2020)')
# plt.xlabel('Total Missing Values')
# plt.ylabel('Number of Countries')
# plt.tight_layout()
# plt.show()

# === Fill remaining nulls using column-wise mean ===
globe_sustain = globe_sustain.fillna(globe_sustain.mean(numeric_only=True))

print("\nAll remaining missing values filled with column means.")
print(globe_sustain.isnull().sum())  # Just to confirm

# === Save to file ===
# globe_sustain.to_csv("cleaned_global_sustainability.csv", index=False)
print("Exported to 'cleaned_global_sustainability.csv'")
