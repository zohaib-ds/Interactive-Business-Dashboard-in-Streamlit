import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit page layout
st.set_page_config(page_title="Global Superstore Sales Dashboard", layout="wide")

st.title("📊 Global Superstore Interactive Performance Dashboard")
st.markdown("Developed for DevelopersHub Corporation Advanced Data Science Internship")

# 1. Load the Superstore Dataset from a reliable public URL
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/amankharwal/Website-data/master/SampleSuperstore.csv"
    data = pd.read_csv(url)
    return data

try:
    df = load_data()
except Exception as e:
    st.error("Failed to fetch data from the remote server. Please check your internet connection.")
    st.stop()

# 2. Create Interactivity Sidebar Filters (Region, Category, Sub-Category)
st.sidebar.header("Filter Options")

selected_region = st.sidebar.multiselect(
    "Select Region:", options=df["Region"].unique(), default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category:", options=df["Category"].unique(), default=df["Category"].unique()
)

# Dynamically filter sub-categories based on selected categories
available_subcats = df[df["Category"].isin(selected_category)]["Sub-Category"].unique()
selected_subcat = st.sidebar.multiselect(
    "Select Sub-Category:", options=available_subcats, default=available_subcats
)

# Apply filters to the main dataframe
filtered_df = df[
    (df["Region"].isin(selected_region)) & 
    (df["Category"].isin(selected_category)) & 
    (df["Sub-Category"].isin(selected_subcat))
]

# 3. Calculate and Display Key Performance Indicators (KPIs)
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
with kpi_col1:
    st.metric(label="💰 Total Sales", value=f"${total_sales:,.2f}")
with kpi_col2:
    st.metric(label="📈 Total Profit", value=f"${total_profit:,.2f}")
with kpi_col3:
    st.metric(label="📊 Profit Margin", value=f"{profit_margin:.2f}%")

st.markdown("---")

# 4. Generate Performance Visualization Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Sales and Profit Performance by Category")
    category_perf = filtered_df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    fig_cat = px.bar(
        category_perf, x="Category", y=["Sales", "Profit"], 
        barmode="group", title="Sales vs Profit across Main Categories"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with chart_col2:
    st.subheader("Top 5 Customers by Sales Volume")
    top_customers = filtered_df.groupby("Customer Name")["Sales"].sum().reset_index()
    top_customers = top_customers.sort_values(by="Sales", ascending=False).head(5)
    fig_cust = px.bar(
        top_customers, x="Sales", y="Customer Name", 
        orientation="h", title="Top 5 High-Value Consumers",
        color="Sales", color_continuous_scale="Viridis"
    )
    fig_cust.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_cust, use_container_width=True)

# 5. Display raw underlying data summary
st.subheader("Filtered Data Summary")
st.dataframe(filtered_df.head(100), use_container_width=True)