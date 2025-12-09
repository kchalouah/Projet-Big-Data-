import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import time

# Page Config
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

# Database Connection
@st.cache_resource
def get_connection():
    # Connecting to MySQL from within Docker network (use service name 'mysql')
    # Or localhost if running locally. We will assume internal docker network 'mysql:3306'
    # But for Streamlit container, it should be 'mysql'.
    return create_engine('mysql+pymysql://root:root@mysql:3306/retail_db')

def load_data():
    engine = get_connection()
    try:
        query = "SELECT * FROM sales"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

# Title
st.title("📊 Retail Big Data Analytics")
st.markdown("Real-time insights from our Big Data Pipeline.")

# Auto-refresh
if st.button("Refresh Data"):
    st.cache_data.clear()

df = load_data()

if not df.empty:
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${df['SALES'].sum():,.2f}")
    col2.metric("Total Orders", len(df))
    col3.metric("Unique Customers", df['CUSTOMERNAME'].nunique())

    st.divider()

    # Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Sales by Product Line")
        sales_by_product = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
        fig_product = px.bar(sales_by_product, x='PRODUCTLINE', y='SALES', color='PRODUCTLINE')
        st.plotly_chart(fig_product, use_container_width=True)

    with c2:
        st.subheader("Order Status Distribution")
        status_counts = df['STATUS'].value_counts().reset_index()
        status_counts.columns = ['STATUS', 'COUNT']
        fig_status = px.pie(status_counts, values='COUNT', names='STATUS', hole=0.4)
        st.plotly_chart(fig_status, use_container_width=True)

    st.subheader("Recent Transactions")
    st.dataframe(df.tail(10))

else:
    st.info("Waiting for data ingestion...")
