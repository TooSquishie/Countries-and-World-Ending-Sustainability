import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

globe_sustain = pd.read_csv("C:\\Users\\defen\\OneDrive\\Documents\\PythonStuff\\DataMiningClass\\Assn2\\Data\\global-data-on-sustainable-energy_renamed.csv")

print(globe_sustain.info())
print(globe_sustain.head())
print(globe_sustain['pop_density_square_km'].isnull().sum())

# Set the target variable
target = globe_sustain['carbon_emit_m_tons']

# Set the feature variables
features = globe_sustain.drop('carbon_emit_m_tons', axis=1)

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

testdf = globe_sustain.drop(columns=['country'],axis=1, inplace=False).copy() 

print(testdf.info())

# Assuming df is your DataFrame and 'target' is your target variable
correlation_matrix = testdf.corr(method='pearson') # or 'spearman'

# Print correlations with the target variable
print(correlation_matrix['carbon_emit_m_tons'].sort_values(ascending=False))

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()
