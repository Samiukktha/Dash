import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go

def scrape_webslinger_data():
    data = {
        'Metric': ['CPU Load', 'Memory Usage', 'Active Users', 'API Errors'],
        'Value': [0.75, 0.62, 150, 4],
        'Timestamp': pd.to_datetime('now').strftime('%Y-%m-%d %H:%M:%S')
    }
    df = pd.DataFrame(data)
    return df

# --- Step 2: Initialize the Dash App ---
app = dash.Dash(__name__)

# --- Step 3: Define the App Layout ---
app.layout = html.Div(children=[
    html.H1(children='Live Webslinger Dashboard'),

    html.Div(id='live-update-text'),
    
    # This component will hold the data table
    dash_table.DataTable(id='live-update-table'),

    # The Interval component triggers the update
    dcc.Interval(
        id='interval-component',
        interval=20 * 1000,  # in milliseconds (20 seconds)
        n_intervals=0
    )
])

# --- Step 4: Create the Callback for Live Updates ---
@app.callback(
    [Output('live-update-table', 'data'),
     Output('live-update-text', 'children')],   
    [Input('interval-component', 'n_intervals')]
)
def update_table(n):
    # Run the scraper function to get the latest data
    df = scrape_webslinger_data()
    
    # Prepare the data for the DataTable component
    table_data = df.to_dict('records')
    
    # Create a status text
    status_text = f"Last updated: {df['Timestamp'].iloc[0]}"
    
    return table_data, status_text

# --- Step 5: Run the App ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
