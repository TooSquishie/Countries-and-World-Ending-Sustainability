import geopandas as gpd
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid Tkinter issues
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

def get_status(row, week):
    if pd.isna(row['week_eliminated']):
        return 'Not in dataset'
    elif row['week_eliminated'] > week:
        return 'Alive'
    else:
        return 'Eliminated'

# === Load world map ===
world = gpd.read_file("D:\\VSCODEPYTHON\\DataMining\\ASSn2\\shapefiles\\ne_110m_admin_0_countries.shp")

# === Load prediction CSV (with pred_2020, pred_2021, pred_2022) ===
emissions = pd.read_csv("D:\\VSCODEPYTHON\\DataMining\\ASSn2\\Data\\future_emission_predictions.csv")

# Manual fixes for known country name mismatches
name_fixes = {
    "United States": "United States of America",
    "Czech Republic": "Czechia",
    "Democratic Republic of the Congo": "Dem. Rep. Congo",
    "Republic of Congo": "Congo",
    "South Korea": "Korea, South",
    "North Korea": "Korea, North",
    "Ivory Coast": "Côte d'Ivoire",
    "Russia": "Russia",
    "Syria": "Syrian Arab Republic",
    "Eswatini": "Swaziland",
    # Add more if needed...
}

emissions['country'] = emissions['country'].replace(name_fixes)

# === Track elimination order by year ===
eliminated = []

# Year-wise elimination
for year in ['pred_2020', 'pred_2021', 'pred_2022']:
    top_52 = emissions[~emissions['country'].isin(eliminated)].sort_values(by=year, ascending=False).head(52)
    eliminated.extend(top_52['country'].tolist())
    
# Assign week eliminated
elimination_df = pd.DataFrame({'country': eliminated})
elimination_df['week_eliminated'] = range(1, len(eliminated) + 1)

# === Merge with GeoDataFrame ===
world = world.merge(elimination_df, how='left', left_on='NAME', right_on='country')

# === Create output folder ===
os.makedirs("map_frames", exist_ok=True)

legend_elements = [
        Patch(facecolor='#006400', label='Alive'),
        Patch(facecolor='#FF0000', label='Eliminated'),
        Patch(facecolor='black', label='Not in dataset'),
    ]

# === Generate 156 maps ===
for week in range(1, len(eliminated) + 1):
    world['status'] = world.apply(lambda row: get_status(row, week), axis=1)

    status_colors = {'Alive': '#006400', 'Eliminated': '#FF0000', 'Not in dataset': 'black'}

    fig, ax = plt.subplots(figsize=(15, 8))
    world.plot(color=world['status'].map(status_colors), edgecolor='white', ax=ax)

    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_title(f"Week {week}: {eliminated[week-1]} eliminated", fontsize=16)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f"map_frames/week_{week:03d}.png")
    plt.close()
    
print("\nFinal 10 Countries Eliminated (Lowest 3-Year Emissions):")
print(elimination_df.tail(10).sort_values(by='week_eliminated'))