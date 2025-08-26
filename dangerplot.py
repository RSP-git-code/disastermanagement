# Importing req libraries
import pandas as pd
import joblib
import json
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path
from disasterpredictor import settings

def generate_map():
    # ---- all your existing code (unchanged) ----
    df = pd.read_csv("Disaster_Zones.csv")
    model_path = Path(settings.BASE_DIR) / "danger_zone_model.pkl"
    model = joblib.load(model_path)

    name_mapping = {
        "USA": "United States of America",
        "UK": "United Kingdom",
        "Russia": "Russian Federation",
        "Vietnam": "Viet Nam",
        "South Korea": "Republic of Korea",
        "North Korea": "Democratic People's Republic of Korea",
        "Syria": "Syrian Arab Republic",
        "Iran": "Iran (Islamic Republic of)",
        "Czech Republic": "Czechia",
        "Bolivia": "Bolivia (Plurinational State of)",
        "Venezuela": "Venezuela (Bolivarian Republic of)",
        "Tanzania": "United Republic of Tanzania",
        "Congo": "Republic of the Congo",
        "DRC": "Democratic Republic of the Congo"
    }
    df["Location"] = df["Location"].replace(name_mapping)

    df["Predicted_Category"] = model.predict(
        df[['Disaster_Type','Location','Magnitude','Fatalities','Economic_Loss($)','Danger_Score']]
    )

    prediction_map = (
        df.groupby(["Location","Disaster_Type"])["Predicted_Category"]
          .apply(lambda x: x.mode()[0])
          .reset_index()
    )

    with open("custom.geo_small.json", "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    all_countries = [f["properties"]["admin"] for f in geojson_data["features"]]

    cat_to_code = {
        "Safe": 0,
        "Low": 1,
        "Moderate": 2,
        "Danger": 3,
        "Extreme Danger": 4,
        "No Data": 5
    }

    step_colorscale = [
        [0.0, "green"], [0.16, "green"],
        [0.17, "yellow"], [0.32, "yellow"],
        [0.33, "orange"], [0.48, "orange"],
        [0.49, "red"], [0.64, "red"],
        [0.65, "darkred"], [0.80, "darkred"],
        [0.81, "lightgrey"], [1.0, "lightgrey"]
    ]

    disasters = sorted(prediction_map["Disaster_Type"].unique())
    fig = go.Figure()

    for i, d in enumerate(disasters):
        sub = prediction_map[prediction_map["Disaster_Type"] == d]
        full_map = pd.DataFrame({"Location": all_countries}).merge(sub, on="Location", how="left")
        full_map["Predicted_Category"] = full_map["Predicted_Category"].fillna("No Data")
        full_map["z_code"] = (
            full_map["Predicted_Category"]
            .map(cat_to_code)
            .fillna(cat_to_code["No Data"])
            .astype(int)
        )

        fig.add_choropleth(
            geojson=geojson_data,
            featureidkey="properties.admin",
            locations=full_map["Location"],
            z=full_map["z_code"],
            zmin=0, zmax=5,
            colorscale=step_colorscale,
            showscale=False,
            visible=(i == 0),
            name=d,
            hovertext=full_map["Location"] + " — " + full_map["Predicted_Category"],
            hovertemplate="%{hovertext}<extra></extra>"
        )

    category_colors = {
        "Safe": "green",
        "Low": "yellow",
        "Moderate": "orange",
        "Danger": "red",
        "Extreme Danger": "darkred",
        "No Data": "lightgrey"
    }

    for category, color in category_colors.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker=dict(size=15, color=color),
            name=category,
            showlegend=True
        ))

    fig.update_layout(
         title={
             "text": f"Predicted Disaster Risk Zones — {disasters[0]}",
             "x": 0.3,  
             "xanchor": "center" },
        updatemenus=[dict(
            buttons=[
                dict(
                    label=d,
                    method="update",
                    args=[{"visible": [j == i for j in range(len(disasters))] + [True]*len(category_colors)},
                          {"title": f"Predicted Disaster Risk Zones — {d}"}]
                )
                for i, d in enumerate(disasters)
            ],
            direction="down",
            showactive=True,
            x=0.02, y=1.08,
            font=dict(size=14, family="Georgia", color="black")
        )],
        margin={"r":0,"t":40,"l":0,"b":0},  # remove white borders
        height=800,
        legend=dict(
        font=dict(size=14, family="Verdana", color="black"),
        title="Categories")
    )

    fig.update_geos(fitbounds="locations", visible=False)

    #  instead of fig.show()
    import plotly.io as pio
    return pio.to_html(fig, full_html=False, config={"responsive": True})




