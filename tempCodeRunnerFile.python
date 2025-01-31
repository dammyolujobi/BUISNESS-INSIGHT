import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
file_path = "supermarket_sales - Sheet1.csv"
df = pd.read_csv(file_path)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')


# Aggregate total sales per date and category
df_grouped = df.groupby(['Date', 'Product line', 'City'])[['Total']].sum().reset_index()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Supermarket Sales Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Supermarket Sales Dashboard", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': cat, 'value': cat} for cat in df['Product line'].unique()],
        placeholder="Select Product Category",
        multi=True,
        style={'width': '50%'}
    ),
    
    dcc.DatePickerRange(
        id='date-filter',
        start_date=df['Date'].min(),
        end_date=df['Date'].max(),
        display_format='YYYY-MM-DD',
        style={'margin': '10px'}
    ),
    
    dcc.Graph(id='sales-trend'),
    dcc.Graph(id='category-sales'),
    dcc.Graph(id='geo-sales')
])

# Callbacks
@app.callback(
    [Output('sales-trend', 'figure'),
     Output('category-sales', 'figure'),
     Output('geo-sales', 'figure')],
    [Input('category-filter', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def update_dashboard(selected_category, start_date, end_date):
    filtered_df = df_grouped[(df_grouped['Date'] >= start_date) & (df_grouped['Date'] <= end_date)]
    if selected_category:
        filtered_df = filtered_df[filtered_df['Product line'].isin(selected_category)]
    
    # Time-Series Sales Trend
    sales_trend = px.line(filtered_df, x='Date', y='Total', color='Product line', title="Sales Trend Over Time")
    
    # Category Sales Breakdown
    category_sales = px.bar(filtered_df.groupby('Product line')[['Total']].sum().reset_index(), 
                             x='Product line', y='Total', title="Sales by Category", color='Product line')
    
    # Geographic Sales
    geo_sales = px.bar(filtered_df.groupby('City')[['Total']].sum().reset_index(), 
                        x='City', y='Total', title="Sales by City", color='City')
    
    return sales_trend, category_sales, geo_sales

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
