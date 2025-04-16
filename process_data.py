import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

globe_sustain = pd.read_csv("C:\\Users\\defen\\OneDrive\\Documents\\PythonStuff\\DataMiningClass\\Assn2\\Data\\global-data-on-sustainable-energy.csv")

print(globe_sustain.info())
print(globe_sustain.head())
print(globe_sustain['Density\n(P/Km2)'])
# Set the target variable
target = globe_sustain['Value_co2_emissions_kt_by_country']

# Set the feature variables
features = globe_sustain.drop('Value_co2_emissions_kt_by_country', axis=1)

# For handling null values
# https://www.youtube.com/watch?v=9ARreeMweNM

null_counts = globe_sustain.isnull().sum()

null_counts.plot(kind='bar')
plt.title('Number of Null Values per Column')
plt.xlabel('Column Name')
plt.ylabel('Number of Nulls')
#plt.xticks(rotation=20)  # Rotates x-axis labels by 45 degrees
plt.tight_layout()  # Optional: Adjusts layout to prevent label cut-off
plt.show()

# Assuming df is your DataFrame and 'target' is your target variable
correlation_matrix = globe_sustain.corr(method='pearson') # or 'spearman'

# Print correlations with the target variable
print(correlation_matrix['Value_co2_emissions_kt_by_country'].sort_values(ascending=False))

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()