import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# === Plotting Function ===
def plot_country_prediction(country_name):
    country_data = df[df['country'] == country_name].sort_values('year')

    # Filter and prepare features
    country_data = country_data[features + [target]].dropna()

    # Train model
    X = country_data[features]
    y = country_data[target]

    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)

    # Predict full range including 2020–2022
    years = list(country_data['year']) + [2020, 2021, 2022]

    # Add future projections inside the plot_country_prediction function
    fossil_proj = project_feature(country_data, 'fossil_elec_TWh', [2020, 2021, 2022])
    renew_proj = project_feature(country_data, 'renew_elec_total_pct', [2020, 2021, 2022])
    gdp_proj = project_feature(country_data, 'gdp_per_capita', [2020, 2021, 2022])

    future_data = pd.DataFrame({
        'year': [2020, 2021, 2022],
        'fossil_elec_TWh': fossil_proj,
        'renew_elec_total_pct': renew_proj,
        'gdp_per_capita': gdp_proj
    })

    # Combine past and future for plotting
    all_years = pd.concat([X, future_data], ignore_index=True)
    all_predictions = model.predict(all_years)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(country_data['year'], y, label='Actual', marker='o')
    plt.plot(years, all_predictions, label='Predicted (incl. 2020–2022)', linestyle='--', marker='x', color='orange')

    plt.title(f'Carbon Emissions Forecast: {country_name}')
    plt.xlabel('Year')
    plt.ylabel('Emissions (metric tons)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Used to project a feature to be used for emission prediction
def project_feature(group, feature, future_years):
    model = LinearRegression()
    X_feat = group[['year']]
    y_feat = group[feature]
    
    if len(y_feat.dropna()) < 2:
        # Not enough data to fit a trend
        return [y_feat.iloc[-1]] * len(future_years)
    
    model.fit(X_feat, y_feat)
    return model.predict(pd.DataFrame({'year': future_years}))

df = pd.read_csv("D:\\VSCODEPYTHON\\DataMining\\ASSn2\\Data\\cleaned_global_sustainability.csv")

# === I believe that the data is already sorted, but just in case ===
df = df[df['year'] <= 2019].sort_values(by=['country', 'year'])

# === Select features for prediction ===
features = ['year', 'fossil_elec_TWh', 'renew_elec_total_pct', 'gdp_per_capita']
target = 'carbon_emit_m_tons'

future_preds = []

# === Forecast for each country ===
for country, group in df.groupby('country'):
    group = group[features + [target]].dropna()

    X = group[features]
    y = group[target]

    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)

    # Build future feature rows (2020–2022)
    last_vals = group.iloc[-1]
    future_years = [2020, 2021, 2022]
    fossil_proj = project_feature(group, 'fossil_elec_TWh', future_years)
    renew_proj = project_feature(group, 'renew_elec_total_pct', future_years)
    gdp_proj = project_feature(group, 'gdp_per_capita', future_years)

    future_data = pd.DataFrame({
        'year': future_years,
        'fossil_elec_TWh': fossil_proj,
        'renew_elec_total_pct': renew_proj,
        'gdp_per_capita': gdp_proj,
    })

    # Predict future emissions
    predictions = model.predict(future_data)
    total_future_emissions = predictions.sum()

    # Store result
    future_preds.append({
        'country': country,
        'pred_2020': predictions[0],
        'pred_2021': predictions[1],
        'pred_2022': predictions[2],
        'total_3yr_emissions': total_future_emissions
    })

# === Convert to DataFrame and sort by emissions ===
future_df = pd.DataFrame(future_preds).sort_values(by='total_3yr_emissions', ascending=False).reset_index(drop=True)

plot_country_prediction("India")
plot_country_prediction("United States")
plot_country_prediction("Germany")

# === Export predicted emissions ===
# future_df.to_csv("future_emission_predictions.csv", index=False)