import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

globe_sustain = pd.read_csv("C:\\Users\\Derek\\Documents\\code_python\\Datamining\\ASSn2\\global-data-on-sustainable-energy_renamed.csv")

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

globe_sustain['pop_density_square_km'] = globe_sustain['pop_density_square_km'].str.replace(',', '')
globe_sustain['pop_density_square_km'] = pd.to_numeric(globe_sustain['pop_density_square_km'], errors='coerce')


null_counts.plot(kind='bar')
plt.title('Number of Null Values per Column')
plt.xlabel('Column Name')
plt.ylabel('Number of Nulls')
plt.tight_layout()  # Optional: Adjusts layout to prevent label cut-off
plt.show()

testdf = globe_sustain.drop(columns=['country'],axis=1, inplace=False).copy() 
# Dropping nulls before final filling
clean_df = testdf.dropna()
correlation_matrix = clean_df.corr()

print(clean_df.info())

# Assuming df is your DataFrame and 'target' is your target variable
correlation_matrix = clean_df.corr(method='pearson') # or 'spearman'

# Print correlations with the target variable
print(correlation_matrix['carbon_emit_m_tons'].sort_values(ascending=False))

plt.figure(figsize=(12,10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.tight_layout() 
plt.show()
