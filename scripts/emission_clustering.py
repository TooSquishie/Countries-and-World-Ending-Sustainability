import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

cluster_labels = {
    0: "Low Emission, Low GDP, High Renewables",
    1: "Wealthy Balanced Energy Users",
    2: "Mega Emitters (US/China)",
    3: "Developing, Fossil-Reliant"
}

# Function to return the cluster description for a country
def get_country_cluster_verbose(country_name):
    match = country_agg[country_agg['country'].str.lower() == country_name.lower()]
    if not match.empty:
        cluster = match['cluster'].values[0]
        label = cluster_labels.get(cluster, "Unknown")
        print(f"🌍 {country_name} is: {label}")
    else:
        print(f"❌ Country '{country_name}' not found.")

# === Load cleaned data ===
df = pd.read_csv("D:\\VSCODEPYTHON\\DataMining\\ASSn2\\Data\\cleaned_global_sustainability.csv")

# === Average per country across years ===
country_agg = df.groupby('country').mean(numeric_only=True).reset_index()

# === Select features for clustering ===
features = [
    'renew_elec_total_pct',
    'fossil_elec_TWh',
    'nuclear_elec_TWh',
    'elec_per_GDP',
    'gdp_per_capita',
    'elec_consume_KWh_person',
    'low_carbon_elec_pct',
    'carbon_emit_m_tons'
]

X = country_agg[features]

# === Normalize features ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Run KMeans clustering ===
kmeans = KMeans(n_clusters=4, random_state=42)
country_agg['cluster'] = kmeans.fit_predict(X_scaled)

# === Reduce to 2D for visualization ===
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
country_agg['pca1'] = X_pca[:, 0]
country_agg['pca2'] = X_pca[:, 1]

# === Plot clusters ===
plt.figure(figsize=(10, 7))
sns.scatterplot(data=country_agg, x='pca1', y='pca2', hue='cluster', palette='Set2', s=100)
for i in range(len(country_agg)):
    plt.text(country_agg['pca1'][i], country_agg['pca2'][i], country_agg['country'][i], fontsize=8, alpha=0.7)
plt.title('Country Clusters Based on Sustainability & Emissions')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.tight_layout()
plt.show()

# Add cluster info to original dataset
df_with_clusters = df.merge(country_agg[['country', 'cluster']], on='country')

# Get average stats per cluster
cluster_summary = df_with_clusters.groupby('cluster')[features].mean()

print(cluster_summary)

while True:
    country_input = input("Enter a country name (or type 'exit' to quit): ")
    if country_input.lower() == 'exit':
        break
    get_country_cluster_verbose(country_input)