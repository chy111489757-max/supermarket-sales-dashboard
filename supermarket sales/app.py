import streamlit as st
import pandas as pd
import base64
import os
import plotly.express as px  

# 设置Basic configuration of a webpage
st.set_page_config(page_title="Supermarket Operations Dashboard", layout="wide")


# ==========================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_image_path = 'R-C.jpg'

try:
    if os.path.exists(background_image_path):
        img_base64 = get_base64_of_bin_file(background_image_path)
        custom_css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&display=swap');
        
        * {{
            font-family: 'Nunito', 'Microsoft YaHei', sans-serif !important;
        }}

        /* 2. Global Background Overlay */
        .stApp {{
            background-image: linear-gradient(rgba(240, 242, 246, 0.85), rgba(240, 242, 246, 0.85)), url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2C3E50 !important;
            font-weight: 700 !important;
        }}
        
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: rgba(255, 255, 255, 0.55) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08) !important;
            padding: 1.5rem !important;
        }}
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
except Exception as e:
    st.warning("Background image failed to load. Please check if the file name and path are correct.")



# ==========================================
st.title("Independent retail store operation monitoring dashboard")
st.write("Based on historical turnover data, this tool provides multi-dimensional interactive screening to assist store managers in making scientific operational decisions")

@st.cache_data
def load_data():
    df = pd.read_csv('database.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
    return df

df = load_data()



# ==========================================
st.sidebar.header("🎯 Multidimensional interaction filter panel")
st.sidebar.write("Please adjust the parameters below; the data on the right will be updated in real time.")

# Interactive Feature 1: Product Category Selection (Added "All Categories" option)
product_lines = ["All categories"] + list(df['Product line'].unique())
selected_category = st.sidebar.selectbox("1. Select the product category you are interested in：", product_lines)

# Interaction Function 2: Switch Core Observation Indicators
metric_dict = {
    "Total daily sales (units)": "Quantity", 
    "Daily revenue ($)": "Total", 
    "Daily Gross Profit ($)": "gross income"
}
selected_metric_name = st.sidebar.radio("2. Switch charts to observe indicators：", list(metric_dict.keys()))
selected_metric_col = metric_dict[selected_metric_name]

# Interactive Feature 3: Customer Group Filtering
customer_types = ["All customers", "Member", "Normal"]
selected_customer = st.sidebar.selectbox("3. Filter specific customer groups：", customer_types)

st.sidebar.markdown("---")
st.sidebar.success("💡 Tip: You can use these options interchangeably, for example, to observe the 'gross profit' trend of 'Members Only' under the 'Food & Beverage' category.")


# ==========================================
st.subheader("I. Overview of Revenue and Profit for Core Product Categories")
category_summary = df.groupby('Product line').agg(
    Total_Revenue=('Total', 'sum'),
    Total_Gross_Income=('gross income', 'sum')
).reset_index()

category_summary['Total_Revenue'] = category_summary['Total_Revenue'].round(2)
category_summary['Total_Gross_Income'] = category_summary['Total_Gross_Income'].round(2)
st.dataframe(category_summary, use_container_width=True)


# ==========================================
with st.container(border=True):
    st.subheader(f"II. Dynamic Trend Analysis：{selected_category} - {selected_metric_name}")
    
    # The data is filtered layer by layer based on three conditions in the sidebar.
    filtered_df = df.copy()
    
    if selected_category != "All categories":
        filtered_df = filtered_df[filtered_df['Product line'] == selected_category]
        
    if selected_customer == "Member":
        filtered_df = filtered_df[filtered_df['Customer type'] == 'Member']
    elif selected_customer == "Normal":
        filtered_df = filtered_df[filtered_df['Customer type'] == 'Normal']

    # Selected metrics by day
    daily_trend = filtered_df.groupby('Date')[selected_metric_col].sum().reset_index()
    
    # Create advanced line charts using Plotly: enable spline smoothing and a beautiful bottom fill area (tozeroy).
    if not daily_trend.empty:
        fig = px.line(
            daily_trend, 
            x='Date', 
            y=selected_metric_col, 
            markers=True, 
            line_shape='spline'
        )
        
        fig.update_traces(line_color="#2C3E50", fill="tozeroy", fillcolor="rgba(44, 62, 80, 0.15)")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="",
            yaxis_title=selected_metric_name,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("There is currently no data for this filter combination.")


# ==========================================
st.subheader("III. Customer Type and Average Transaction Value Analysis")
st.write("Assess the actual stimulating effect of the current membership program on increasing the average order value.")

customer_summary = df.groupby('Customer type')['Total'].mean().reset_index()
customer_summary.set_index('Customer type', inplace=True)

member_spend = customer_summary.loc['Member', 'Total']
normal_spend = customer_summary.loc['Normal', 'Total']
difference = member_spend - normal_spend

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="🌟 Average order value per member customer", 
        value=f"${member_spend:.2f}", 
        delta=f"Higher than ordinary customers ${difference:.2f}"
    )

with col2:
    st.metric(
        label="👤 Average order value per ordinary customers", 
        value=f"${normal_spend:.2f}"
    )



# ==========================================
st.subheader("IV. Data-Driven Operational Recommendations")

with st.container(border=True):
    st.markdown("#### 💡 1. Deeply activate member value")
    st.info("Data shows that the average order value difference between current members and regular customers is less than $10. It is recommended to *restructure the membership benefits system,* for example, by introducing *tiered discounts* or *double points for high-value orders* to provide tangible incentives and increase members' average purchase volume per transaction.")
    
    st.markdown("#### 📦 2. Optimize long tail and disadvantageous categories")
    st.warning("Currently, the health and beauty category has the lowest revenue and gross profit. For slow-moving categories, it is recommended to **bundle sales** with top-profit categories (such as food and beverages), or to set up a dedicated discount area at the checkout to accelerate inventory turnover.")
    
    st.markdown("#### 📈 3. Trade 'quantity' for absolute profit")
    st.success("The gross profit margin for all product categories in the store remains consistently around 4.76%. Under a uniform fixed markup strategy, the only way to increase total profit is to **increase total sales volume**. It is recommended to thoroughly explore peak customer traffic periods and conduct limited-time promotions on core traffic-driving categories to boost overall store sales.")