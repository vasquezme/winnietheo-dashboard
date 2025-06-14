import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import dash
from dash import dash_table, dcc, html


# Load the CSV file
file_path1 = r"data\WinnieCustomersHUBLOC.csv"  # Update with the correct path
file_path2 = r"data\WinnieHotelLocations.csv"

df_customers = pd.read_csv(file_path1)
df_hubs = pd.read_csv(file_path2)

# Display the first few rows
print(df_customers.head())
print(df_hubs.head())

fig_map = None
if ({"LAT", "LONG"}.issubset(df_customers.columns) and not df_customers.empty and
    {"lat", "long"}.issubset(df_hubs.columns) and not df_hubs.empty):

    # IMPORTANT CHANGE: Create a separate DataFrame for customer map data to avoid modifying original df_customers
    df_customers_for_map = df_customers[['LAT', 'LONG']].copy()
    df_customers_for_map['Type'] = 'Customer'

    # Create a separate DataFrame for hub map data
    df_hubs_for_map = df_hubs[['lat', 'long']].copy()
    df_hubs_for_map.columns = ['LAT', 'LONG'] # Rename for consistency
    df_hubs_for_map['Type'] = 'Hub'

    # Concatenate for the map
    df_combined = pd.concat([df_customers_for_map, df_hubs_for_map], ignore_index=True)

    fig_map = px.scatter_map(df_combined, lat="LAT", lon="LONG", color="Type", size=[20]*len(df_combined), size_max=10,
                             title="Customer and Hub Locations Map",
                             map_style="open-street-map",
                             zoom=10) # Adjust zoom level
    
    fig_map.update_layout(margin={"r":0,"t":50,"l":0,"b":0}) # Adjust map margins
else:
    fig_map = None

# Initialize Dash app
app = dash.Dash(__name__)

server = app.server

# Example visualization (modify based on your CSV structure)
# use fig.show() to display the figure in a browser

total_records = df_customers.shape[0]
total_visits = df_customers['VISITS'].sum() if 'VISITS' in df_customers.columns else 0
residence_percentage = df_customers['RESIDENCE'].value_counts(normalize=True).get("Owner", 0) * 100 if "RESIDENCE" in df_customers.columns else 0
unique_hub_names = df_customers['HubName'].nunique() if 'HubName' in df_customers.columns else 0
average_distance = df_customers['HubDist'].mean() if 'HubDist' in df_customers.columns else 0
if "SEGMENTATION" in df_customers.columns:
    hub_counts_by_segment = df_customers.groupby("SEGMENTATION").size().reset_index(name="Count").sort_values(by="Count", ascending=False)
else:
    hub_counts_by_segment = pd.DataFrame(columns=["SEGMENTATION", "Count"])
if "EDUCATION" in df_customers.columns:
    education_counts = df_customers.groupby("EDUCATION").size().reset_index(name="Count").sort_values(by="Count", ascending=False)
else:
    education_counts = pd.DataFrame(columns=["EDUCATION", "Count"])


fig1 = px.histogram(df_customers, x="HubName", y="VISITS", title="Total Visits by Location")
fig2 = px.pie(df_customers, names="GENDER", title="Gender Distribution of Customers")
fig3 = px.pie(df_customers, names="EDUCATION", title="Education Level Distribution of Customers")
fig4 = px.histogram(df_customers, x="VISITS", y="SEGMENTATION", color="GENDER", title="Visits by Segmentation")

fig5 = go.Figure(data=[go.Table(
    header=dict(values=['SEGMENTATION', 'HUB_COUNTS'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[hub_counts_by_segment['SEGMENTATION'], hub_counts_by_segment['Count']],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

fig5.update_layout(title="Location Segmentation Profile", width=500, height=300)

fig6 = go.Figure(data=[go.Table(
    header=dict(values=['EDUCATION', 'VISITS_COUNT'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[education_counts['EDUCATION'], education_counts['Count']],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

fig6.update_layout(title="Visitors by Education", width=500, height=300)

app.layout = html.Div([
    html.H1("WinnieTheo's Hotel and Resto Dashboard", 
       style={"font-size": "48px", "font-weight": "bold", "text-align": "center"}),

    # Scorecard Section (Side by Side)
    html.Div([
            html.Div([
                html.H3("Total Records in Table"),
                html.P(f"{total_records}", style={"font-size": "48px", "font-weight": "bold"})
            ], style={"width": "10%", "text-align": "center", "border": "2px solid black", "padding": "10px", "margin": "10px", "background-color": "#f9f9f9"}),

            html.Div([
                html.H3("Total Visits"),
                html.P(f"{total_visits}", style={"font-size": "48px", "font-weight": "bold"})
            ], style={"width": "10%", "text-align": "center", "border": "2px solid black", "padding": "10px", "margin": "10px", "background-color": "#f9f9f9"}),

            html.Div([
                html.H3("Dwelling Owners"),
                html.P(f"{residence_percentage:.1f}%", style={"font-size": "48px", "font-weight": "bold"}) 
            ], style={"width": "10%", "text-align": "center", "border": "2px solid black", "padding": "10px", "margin": "10px", "background-color": "#f9f9f9"}),

            html.Div([
                html.H3("Unique Store Visits"),
                html.P(f"{unique_hub_names}", style={"font-size": "48px", "font-weight": "bold"})
            ], style={"width": "10%", "text-align": "center", "border": "2px solid black", "padding": "10px", "margin": "10px", "background-color": "#f9f9f9"}),

            html.Div([
                html.H3("Average Distance to Store"),
                html.P(f"{average_distance:.1f}km", style={"font-size": "48px", "font-weight": "bold"})
            ], style={"width": "10%", "text-align": "center", "border": "2px solid black", "padding": "10px", "margin": "10px", "background-color": "#f9f9f9"}),
        ], style={"display": "flex", "justify-content": "space-around"}),

    # Graphs section
    html.Div([
        dcc.Graph(figure=fig1) if fig1 else html.P("No location data available."),
        dcc.Graph(figure=fig2) if fig2 else html.P("No gender data available."),
        dcc.Graph(figure=fig3) if fig3 else html.P("No education data available."),
        dcc.Graph(figure=fig4) if fig4 else html.P("No segmentation data available."),
        dcc.Graph(figure=fig5) if fig5 else html.P("No segmentation data available."),
        dcc.Graph(figure=fig6) if fig6 else html.P("No education data available."),
        dcc.Graph(figure=fig_map, style={"height": "700px", "width": "80%"}) if fig_map else html.P("No latitude/longitude data available.")
    ], style={"display": "flex", "flex-wrap": "wrap", "justify-content": "space-around"})

])

if __name__ == "__main__":
    app.run(debug=True)
