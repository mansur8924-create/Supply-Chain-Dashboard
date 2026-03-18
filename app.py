import streamlit as st
import pandas as pd
import plotly.express as px

# --- Setup ---
st.set_page_config(page_title="Warehouse Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #121418; color: #E0E4E8; font-family: 'Segoe UI', sans-serif; }
    
    div[data-testid="metric-container"] {
        background-color: #1A1D24; 
        border: 1px solid #2A2E37;
        padding: 24px 20px; 
        border-radius: 8px;
    }
    div[data-testid="stMetricValue"] { color: #4DA8DA; font-size: 2.4rem; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #8A929A; font-size: 1rem; }
    
    .strategy-card {
        background-color: #1A1D24;
        padding: 24px;
        border-radius: 8px;
        border-top: 4px solid;
        height: 100%;
    }
    .strategy-card h4 { margin-top: 0; color: #E0E4E8; }
    .tag { font-weight: 700; font-size: 0.8rem; padding: 2px 6px; border-radius: 4px; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('Electronic_Sales.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['City'] = df['City'].str.strip()
    return df

df = load_data()

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Filters")
    city_filter = st.multiselect("Pick a city to check:", options=sorted(df['City'].unique()), default=df['City'].unique())

filtered_df = df[df['City'].isin(city_filter)]

# --- Header ---
st.title("📦 Warehouse & Shipping Overview")
st.markdown("<p style='color: #8A929A;'>Checking in on how fast we're moving stock and where the bottlenecks are.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Stats ---
if not filtered_df.empty:
    total_units = filtered_df['Quantity Ordered'].sum()
    fastest_mover = filtered_df.groupby('Product')['Quantity Ordered'].sum().idxmax()
    peak_month = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}[filtered_df.groupby('Month')['Quantity Ordered'].sum().idxmax()]
    avg_size = filtered_df['Quantity Ordered'].mean()
else:
    total_units, fastest_mover, peak_month, avg_size = 0, "N/A", "N/A", 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Boxes Shipped", f"{total_units:,.0f}")
k2.metric("Most Popular Item", fastest_mover)
k3.metric("Our Busiest Month", peak_month)
k4.metric("Average Order Size", f"{avg_size:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# --- Charts ---
r1_c1, r1_c2 = st.columns([2, 1])

with r1_c1:
    st.markdown("#### How many boxes are we shipping each month?")
    monthly_trend = filtered_df.groupby('Month')['Quantity Ordered'].sum().reset_index()
    monthly_trend['Month Name'] = monthly_trend['Month'].map({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'})
    fig = px.line(monthly_trend, x='Month Name', y='Quantity Ordered', template="plotly_dark", markers=True, color_discrete_sequence=['#4DA8DA'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), height=300)
    st.plotly_chart(fig, width='stretch')

with r1_c2:
    st.markdown("#### Our Top 5 Best Sellers")
    top_5 = filtered_df.groupby('Product')['Quantity Ordered'].sum().nlargest(5).reset_index()
    fig2 = px.bar(top_5, y='Product', x='Quantity Ordered', orientation='h', template="plotly_dark", color_discrete_sequence=['#E67E22'])
    fig2.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), height=300)
    st.plotly_chart(fig2, width='stretch')

r2_c1, r2_c2 = st.columns(2)

with r2_c1:
    st.markdown("#### When do orders actually come in?")
    hr_vol = filtered_df.groupby('Hour')['Quantity Ordered'].sum().reset_index()
    fig3 = px.area(hr_vol, x='Hour', y='Quantity Ordered', template="plotly_dark", color_discrete_sequence=['#9B59B6'])
    fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), height=300)
    st.plotly_chart(fig3, width='stretch')

with r2_c2:
    st.markdown("#### Where are we sending the most stock?")
    city_vol = filtered_df.groupby('City')['Quantity Ordered'].sum().reset_index()
    fig4 = px.treemap(city_vol, path=[px.Constant("All Markets"), 'City'], values='Quantity Ordered', color='Quantity Ordered', color_continuous_scale='Blues', template="plotly_dark")
    fig4.update_layout(margin=dict(t=10, l=0, r=0, b=0), height=300)
    st.plotly_chart(fig4, width='stretch')

# --- Human Recommendations ---
st.markdown("---")
st.subheader("📝 My Thoughts & Recommendations")
s1, s2, s3 = st.columns(3)

with s1:
    st.markdown("""<div class="strategy-card" style="border-top-color: #4DA8DA;">
        <h4>The Holiday Rush</h4>
        <p><span class="tag" style="background-color: #4DA8DA22; color: #4DA8DA;">WHAT I SEE</span> Shipping goes crazy in Nov and Dec.</p>
        <p><span class="tag" style="background-color: #E74C3C22; color: #E74C3C;">WHY IT MATTERS</span> If we don't prep, our staff will burn out and orders will be late.</p>
        <p><b>ACTION:</b> Let's get our seasonal hires trained by mid-October so they're ready to go.</p>
    </div>""", unsafe_allow_html=True)

with s2:
    st.markdown("""<div class="strategy-card" style="border-top-color: #E67E22;">
        <h4>Keep Batteries in Stock</h4>
        <p><span class="tag" style="background-color: #E67E2222; color: #E67E22;">WHAT I SEE</span> Batteries and cables are our #1 sellers by volume.</p>
        <p><span class="tag" style="background-color: #E74C3C22; color: #E74C3C;">WHY IT MATTERS</span> People add these to big orders. If we're out, they might go to a competitor.</p>
        <p><b>ACTION:</b> Set an auto-reorder for AAA batteries the moment we dip below 3 weeks of stock.</p>
    </div>""", unsafe_allow_html=True)

with s3:
    st.markdown("""<div class="strategy-card" style="border-top-color: #9B59B6;">
        <h4>Shift Timing</h4>
        <p><span class="tag" style="background-color: #9B59B622; color: #9B59B6;">WHAT I SEE</span> Orders spike at lunch (12pm) and right after work (7pm).</p>
        <p><span class="tag" style="background-color: #E74C3C22; color: #E74C3C;">WHY IT MATTERS</span> That's when we get the biggest backlog.</p>
        <p><b>ACTION:</b> Let's stagger lunch breaks so we have the most people on the floor during those two windows.</p>
    </div>""", unsafe_allow_html=True)
