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
    html.H1("Supermarket Sales Dashboard", style={'textAlign': 'center', 'font-family': 'Arial,sans-serif'}),
    
    # KPI Metrics
    html.Div([
        html.H3(id='total-sales', style={'textAlign': 'center'}),
        html.H3(id='total-transactions', style={'textAlign': 'center', 'font-family': 'Arial,sans-serif'}),
        html.H3(id='avg-purchase-value', style={'textAlign': 'center', 'font-family': 'Arial,sans-serif'}),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'font-family': 'Arial,sans-serif'}),
    
    # Filters
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': cat, 'value': cat} for cat in df['Product line'].unique()],
        placeholder="Select Product Category",
        multi=True,
        style={'width': '50%', 'font-family': 'Arial,sans-serif'}
    ),
    
    dcc.DatePickerRange(
        id='date-filter',
        start_date=df['Date'].min(),
        end_date=df['Date'].max(),
        display_format='YYYY-MM-DD',
        style={'margin': '10px', 'font-family': 'Arial,sans-serif'}
    ),
    
    # Graphs
    dcc.Graph(id='sales-trend'),
    dcc.Graph(id='category-sales'),
    dcc.Graph(id='geo-sales')
])

# Callbacks
@app.callback(
    [Output('sales-trend', 'figure'),
     Output('category-sales', 'figure'),
     Output('geo-sales', 'figure'),
     Output('total-sales', 'children'),
     Output('total-transactions', 'children'),
     Output('avg-purchase-value', 'children')],
    [Input('category-filter', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')]
)
def dashboard(selected_category, start_date, end_date):
    # Filter data
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    if selected_category:
        filtered_df = filtered_df[filtered_df['Product line'].isin(selected_category)]
    
    # Aggregated Data
    df_grouped_filtered = filtered_df.groupby(['Date', 'Product line', 'City'])[['Total']].sum().reset_index()

    # Time-Series Sales Trend
    sales_trend = px.line(df_grouped_filtered, x='Date', y='Total', color='Product line', title="Sales Trend Over Time")
    
    # Category Sales Breakdown
    category_sales = px.bar(filtered_df.groupby('Product line')[['Total']].sum().reset_index(), 
                             x='Product line', y='Total', title="Sales by Category", color='Product line')
    
    # Geographic Sales
    geo_sales = px.bar(filtered_df.groupby('City')[['Total']].sum().reset_index(), 
                        x='City', y='Total', title="Sales by City", color='City')

    # KPIs
    total_sales = f"Total Sales: ${filtered_df['Total'].sum():,.2f}"
    total_transactions = f"Transactions: {filtered_df.shape[0]}"
    avg_purchase = f"Avg Purchase: ${filtered_df['Total'].mean():,.2f}"

    return sales_trend, category_sales, geo_sales, total_sales, total_transactions, avg_purchase

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
