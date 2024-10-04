import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Sample DataFrame (replace this with your actual df1)
df1 = pd.read_csv('./data/PurchasesFINAL12312016.csv')

# df1 = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app with a dropdown and a graph
app.layout = html.Div([
    html.H1("Purchase Order Counts by Date and Classification"),
    dcc.Dropdown(
        id='vendor-filter',
        options=[{'label': vendor, 'value': vendor} for vendor in df1['VendorNumber'].unique()],
        value=df1['VendorNumber'].unique(),  # Set default to select all
        multi=True,  # Enable multiple selection
        placeholder="Select Vendor(s)"
    ),
    dcc.Graph(id='line-chart')
])

# Callback to update the graph based on vendor filter
@app.callback(
    Output('line-chart', 'figure'),
    Input('vendor-filter', 'value')
)
def update_graph(selected_vendors):
    # Filter the DataFrame based on selected vendors
    if selected_vendors:  # If there are any vendors selected
        filtered_df = df1[df1['VendorNumber'].isin(selected_vendors)]
    else:
        # If no vendors are selected, show an empty plot
        filtered_df = df1.iloc[0:0]  # Empty DataFrame
    
    # Group by PODate and Classification to count
    podate_att = filtered_df.groupby(['PODate', 'Classification']).apply(lambda x: x['PODate'].count()).reset_index(name='Counts')
    
    # Create the line plot
    fig = px.line(podate_att, x='PODate', y='Counts', color='Classification', title=f'PO Counts for Selected Vendors')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
