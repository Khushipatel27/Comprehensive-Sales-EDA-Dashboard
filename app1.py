import os
os.environ["STREAMLIT_DATAFRAME_USE_LEGACY_SERIALIZER"] = "1"


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from prophet import Prophet
from prophet.plot import plot_plotly
import warnings
warnings.filterwarnings('ignore')

# Custom CSS for consistent table styling
st.markdown("""
<style>
    .stDataFrame > div {
        background-color: #2d3748 !important;
        border-radius: 8px !important;
    }
    
    .stDataFrame table {
        background-color: #2d3748 !important;
        color: #e2e8f0 !important;
        border-collapse: collapse !important;
    }
    
    .stDataFrame th {
        background-color: #1a202c !important;
        color: #e2e8f0 !important;
        font-weight: bold !important;
        border: 1px solid #4a5568 !important;
        padding: 8px 12px !important;
    }
    
    .stDataFrame td {
        background-color: #2d3748 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4a5568 !important;
        padding: 8px 12px !important;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #3a4556 !important;
    }
    
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: #2d3748 !important;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #4a5568 !important;
    }
    
    /* Additional styling for better visibility */
    .scrollable-table {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #4a5568;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load and Prepare Data
# -----------------------------
@st.cache_data
def load_and_prepare_data():
    try:
        df = pd.read_csv("Dataset_Superstore.csv", encoding="latin1")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Ship Date'] = pd.to_datetime(df['Ship Date'])
        df['Year'] = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.month
        df['Quarter'] = df['Order Date'].dt.quarter
        df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_and_prepare_data()

if df is None:
    st.stop()

# -----------------------------
# Sidebar Configuration
# -----------------------------
st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Analysis type selection
analysis_type = st.sidebar.selectbox(
    "Select Analysis Type",
    ["📋 Database Overview", "📊 Yearly Analysis", "🔮 Forecasting", "📈 Advanced Analytics"]
)

# Forecasting parameters
st.sidebar.markdown("### Forecasting Parameters")
forecast_periods = st.sidebar.slider("Forecast Periods (months)", 6, 36, 12)
confidence_interval = st.sidebar.slider("Confidence Interval", 0.8, 0.95, 0.95)

# Filter options
st.sidebar.markdown("### Filters")
selected_years = st.sidebar.multiselect(
    "Select Years", 
    options=sorted(df['Year'].unique()), 
    default=sorted(df['Year'].unique())
)

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Apply filters
filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Category'].isin(selected_categories)) &
    (df['Region'].isin(selected_regions))
]

# -----------------------------
# Main Dashboard Title
# -----------------------------
st.title("📊 Comprehensive Sales Forecasting Dashboard")
st.markdown(f"**Data Period:** {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}")
st.markdown("---")

# -----------------------------
# Database Overview
# -----------------------------
if analysis_type == "📋 Database Overview":
    st.header("📋 Database Overview & Analysis")
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Records", f"{len(filtered_df):,}")
    with col2:
        st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
    with col3:
        st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
    with col4:
        st.metric("Avg Profit Margin", f"{filtered_df['Profit Margin'].mean():.2f}%")
    with col5:
        st.metric("Unique Customers", f"{filtered_df['Customer Name'].nunique():,}")
    
    st.markdown("---")
    
    # Database Structure
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Dataset Information")
        info_df = pd.DataFrame({
            'Column': df.columns,
            'Data Type': [str(dtype) for dtype in df.dtypes],
            'Non-Null Count': [df[col].notna().sum() for col in df.columns],
            'Null Count': [df[col].isna().sum() for col in df.columns]
        })
        
        st.dataframe(
            info_df, 
            height=400,
            use_container_width=True
        )

    with col2:
        st.subheader("📈 Data Distribution")
        st.write("**Sample Data:**")
        
        st.dataframe(
            filtered_df.head(10), 
            height=400,
            use_container_width=True
        )

    # Statistical summary
    st.subheader("📊 Statistical Summary")
    st.dataframe(
        filtered_df[['Sales', 'Profit', 'Discount', 'Quantity']].describe(),   
        use_container_width=True,
        height=400
    )

    
    # Visualizations
    st.subheader("📊 Data Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales distribution
        fig = px.histogram(filtered_df, x='Sales', nbins=50, title='Sales Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
        # Category breakdown
        category_stats = filtered_df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count'
        }).round(2)
        fig = px.pie(values=category_stats['Sales'], names=category_stats.index, 
                     title='Sales by Category')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit distribution
        fig = px.histogram(filtered_df, x='Profit', nbins=50, title='Profit Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
        # Regional performance
        region_stats = filtered_df.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count'
        }).round(2)
        fig = px.bar(x=region_stats.index, y=region_stats['Sales'], 
                     title='Sales by Region')
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Yearly Analysis
# -----------------------------
elif analysis_type == "📊 Yearly Analysis":
    st.header("📊 Comprehensive Yearly Analysis")
    
    # Yearly trends
    yearly_stats = filtered_df.groupby('Year').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count',
        'Customer Name': 'nunique',
        'Quantity': 'sum'
    }).round(2)
    yearly_stats['Profit Margin'] = (yearly_stats['Profit'] / yearly_stats['Sales']) * 100
    yearly_stats['Avg Order Value'] = yearly_stats['Sales'] / yearly_stats['Order ID']
    
    st.subheader("📈 Year-over-Year Performance")
    st.dataframe(yearly_stats, use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales trend
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly_stats.index, y=yearly_stats['Sales'],
                                mode='lines+markers', name='Sales', line=dict(width=3)))
        fig.update_layout(title='Yearly Sales Trend', xaxis_title='Year', yaxis_title='Sales ($)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Orders count
        fig = px.bar(x=yearly_stats.index, y=yearly_stats['Order ID'], 
                     title='Number of Orders by Year')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit trend
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly_stats.index, y=yearly_stats['Profit'],
                                mode='lines+markers', name='Profit', line=dict(width=3, color='green')))
        fig.update_layout(title='Yearly Profit Trend', xaxis_title='Year', yaxis_title='Profit ($)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Profit margin
        fig = px.line(x=yearly_stats.index, y=yearly_stats['Profit Margin'], 
                      title='Profit Margin Trend (%)', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Monthly analysis for each year
    st.subheader("📅 Monthly Analysis by Year")
    
    monthly_yearly = filtered_df.groupby(['Year', 'Month']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Monthly Sales by Year', 'Monthly Profit by Year'))
    
    for year in sorted(filtered_df['Year'].unique()):
        year_data = monthly_yearly[monthly_yearly['Year'] == year]
        fig.add_trace(go.Scatter(x=year_data['Month'], y=year_data['Sales'],
                                mode='lines+markers', name=f'Sales {year}'), row=1, col=1)
        fig.add_trace(go.Scatter(x=year_data['Month'], y=year_data['Profit'],
                                mode='lines+markers', name=f'Profit {year}'), row=2, col=1)
    
    fig.update_layout(height=600, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Forecasting Section
# -----------------------------
elif analysis_type == "🔮 Forecasting":
    st.header("🔮 Sales & Profit Forecasting")
    st.caption(f"Forecasting {forecast_periods} months ahead with {int(confidence_interval*100)}% confidence interval")

    
    # Prepare data for Prophet
    @st.cache_data
    def prepare_forecast_data(df, metric='Sales'):
        monthly_data = df.groupby(pd.Grouper(key='Order Date', freq='M'))[metric].sum().reset_index()
        prophet_df = monthly_data.rename(columns={'Order Date': 'ds', metric: 'y'})
        return prophet_df
    
    # Overall forecasting
    st.subheader("📈 Overall Sales Forecast")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales forecast
        sales_data = prepare_forecast_data(filtered_df, 'Sales')
        
        model_sales = Prophet(interval_width=confidence_interval)
        model_sales.fit(sales_data)
        
        future_sales = model_sales.make_future_dataframe(periods=forecast_periods, freq='M')
        forecast_sales = model_sales.predict(future_sales)
        
        fig_sales = plot_plotly(model_sales, forecast_sales)
        fig_sales.update_layout(title="Sales Forecast")
        st.plotly_chart(fig_sales, use_container_width=True)
    
    with col2:
        # Profit forecast
        profit_data = prepare_forecast_data(filtered_df, 'Profit')
        
        model_profit = Prophet(interval_width=confidence_interval)
        model_profit.fit(profit_data)
        
        future_profit = model_profit.make_future_dataframe(periods=forecast_periods, freq='M')
        forecast_profit = model_profit.predict(future_profit)
        
        fig_profit = plot_plotly(model_profit, forecast_profit)
        fig_profit.update_layout(title="Profit Forecast")
        st.plotly_chart(fig_profit, use_container_width=True)
    
    # Forecast results table
    st.subheader("📊 Forecast Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Sales Forecast:**")
        sales_forecast_df = forecast_sales[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_periods)
        sales_forecast_df.columns = ['Date', 'Predicted Sales', 'Lower Bound', 'Upper Bound']
        sales_forecast_df['Predicted Sales'] = sales_forecast_df['Predicted Sales'].round(2)
        st.dataframe(sales_forecast_df, use_container_width=True)
    
    with col2:
        st.write("**Profit Forecast:**")
        profit_forecast_df = forecast_profit[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_periods)
        profit_forecast_df.columns = ['Date', 'Predicted Profit', 'Lower Bound', 'Upper Bound']
        profit_forecast_df['Predicted Profit'] = profit_forecast_df['Predicted Profit'].round(2)
        st.dataframe(profit_forecast_df, use_container_width=True)
    
    # Category-wise forecasting
    st.subheader("📂 Category-wise Forecasting")
    
    selected_category_forecast = st.selectbox("Select Category for Detailed Forecast", 
                                            filtered_df['Category'].unique())
    
    category_data = filtered_df[filtered_df['Category'] == selected_category_forecast]
    category_sales_data = prepare_forecast_data(category_data, 'Sales')
    
    model_cat = Prophet(interval_width=confidence_interval)
    model_cat.fit(category_sales_data)
    
    future_cat = model_cat.make_future_dataframe(periods=forecast_periods, freq='M')
    forecast_cat = model_cat.predict(future_cat)
    
    fig_cat = plot_plotly(model_cat, forecast_cat)
    fig_cat.update_layout(title=f"Sales Forecast for {selected_category_forecast}")
    st.plotly_chart(fig_cat, use_container_width=True)
    
    # Components analysis
    st.subheader("🔍 Forecast Components Analysis")
    fig_comp = model_sales.plot_components(forecast_sales)
    st.pyplot(fig_comp)

# -----------------------------
# Advanced Analytics
# -----------------------------
elif analysis_type == "📈 Advanced Analytics":
    st.header("📈 Advanced Analytics & Insights")
    
    # Customer analysis
    st.subheader("👥 Customer Analysis")
    
    customer_stats = filtered_df.groupby('Customer Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count'
    }).round(2)
    customer_stats['Avg Order Value'] = customer_stats['Sales'] / customer_stats['Order ID']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top customers by sales
        top_customers_sales = customer_stats.nlargest(10, 'Sales')
        fig = px.bar(x=top_customers_sales['Sales'], y=top_customers_sales.index,
                     orientation='h', title='Top 10 Customers by Sales')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Customer value distribution
        fig = px.histogram(customer_stats, x='Sales', nbins=50, 
                          title='Customer Sales Value Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    # Product analysis
    st.subheader("📦 Product Performance Analysis")
    
    product_stats = filtered_df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).round(2)
    product_stats['Profit Margin'] = (product_stats['Profit'] / product_stats['Sales']) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top products by sales
        top_products = product_stats.nlargest(10, 'Sales')
        fig = px.bar(x=top_products.index, y=top_products['Sales'],
                     title='Top 10 Sub-Categories by Sales')
        plt.xticks(rotation=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit margin analysis
        fig = px.scatter(product_stats, x='Sales', y='Profit Margin', 
                        size='Quantity', hover_name=product_stats.index,
                        title='Sales vs Profit Margin by Sub-Category')
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation analysis
    st.subheader("📊 Correlation Analysis")
    
    correlation_cols = ['Sales', 'Profit', 'Discount', 'Quantity']
    correlation_matrix = filtered_df[correlation_cols].corr()
    
    fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto",
                    title='Correlation Matrix of Key Metrics')
    st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal analysis
    st.subheader("🗓️ Seasonal Analysis")
    
    seasonal_data = filtered_df.groupby(['Month', 'Quarter']).agg({
        'Sales': 'mean',
        'Profit': 'mean'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(seasonal_data, x='Month', y='Sales', 
                     title='Average Monthly Sales Pattern')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        quarterly_data = filtered_df.groupby('Quarter').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        })
        fig = px.bar(x=quarterly_data.index, y=quarterly_data['Sales'],
                     title='Quarterly Sales Performance')
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("### 📋 Dashboard Summary")
st.info(f"""
**Current Analysis**: {analysis_type}  
**Data Range**: {filtered_df['Order Date'].min().strftime('%Y-%m-%d')} to {filtered_df['Order Date'].max().strftime('%Y-%m-%d')}  
**Records Analyzed**: {len(filtered_df):,}  
**Total Sales**: ${filtered_df['Sales'].sum():,.2f}  
Total Profit: ${filtered_df['Profit'].sum():,.2f}
""")