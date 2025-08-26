import pandas as pd
import plotly.express as px
import joblib
from pathlib import Path
from disasterpredictor import settings
# Load dataset and model
df = pd.read_csv("Disaster_Zones.csv")
model_path = Path(settings.BASE_DIR) / "danger_zone_model.pkl"
model = joblib.load(model_path)


# Aliases for common country names → always map to canonical
country_aliases = {
    "russia": "Russian Federation",
    "usa": "United States of America",
    "us": "United States of America",
    "america": "United States of America",
    "uk": "United Kingdom of Great Britain and Northern Ireland",
    "britain": "United Kingdom of Great Britain and Northern Ireland"
}

# Risk colors
color_map = {
    "Safe": "green",
    "Low": "yellow",
    "Moderate": "orange",
    "Danger": "red",
    "Extreme Danger": "darkred"
}

def analyze_country(country: str):
    """Analyze disaster frequency & risk levels for a country (canonical or alias)."""
    if not country:
        return None, None

    # Normalize input
    user_country = country.strip().lower()

    # Resolve alias → canonical
    if user_country in country_aliases:
        user_country = country_aliases[user_country].lower()

    # Filter data by canonical name
    country_data = df[df["Location"].str.strip().str.lower() == user_country]

    if country_data.empty:
        return None, None  # no data for this country

    # Count disasters
    summary = country_data["Disaster_Type"].value_counts().reset_index()
    summary.columns = ["Disaster_Type", "Count"]

    # Z-score normalization
    mu = summary["Count"].mean()
    sigma = summary["Count"].std(ddof=0)  # population std
    if sigma == 0:
        summary["z_score"] = 0
    else:
        summary["z_score"] = (summary["Count"] - mu) / sigma

    # Map Z-scores → Risk levels
    def map_risk(z):
        if z <= -0.5:
            return "Safe"
        elif z <= 0.5:
            return "Low"
        elif z <= 1.0:
            return "Moderate"
        elif z <= 2.0:
            return "Danger"
        else:
            return "Extreme Danger"

    summary["Risk_Level"] = summary["z_score"].apply(map_risk)

    # Pie chart
    fig = px.pie(
        summary,
        names="Disaster_Type",
        values="Count",
        color="Risk_Level",
        color_discrete_map=color_map,
        title=f"Disaster Frequency in {country} (Z-score Normalized Risk Levels)"
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="black", width=2))
    )

    return summary, fig


