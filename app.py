import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration & Styling ---
st.set_page_config(page_title="Supply Chain Operations", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Executive Night Mode */
    .main { background-color: #121418; color: #E0E4E8; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Elevated Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #1A1D24; 
        border: 1px solid #2A2E37;
        padding: 24px 20px; 
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetricValue"] { color: #4DA8DA; font-size: 2.4rem; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #8A929A; font-size: 1.05rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Clean Dataframes */
    .stDataFrame { border: 1px solid #2A2E37; border-radius: 6px; overflow: hidden; }
    
    /* Custom Strategy Cards */
    .strategy-card {
        background-color: #1A1D24;
        padding: 24px;
        border-radius: 6px;
        border-top: 4px solid;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        height: 100%;
    }
    .strategy-card h4 { margin-top: 0; font-size: 1.1rem; font-weight: 600; margin-bottom: 12px; }
    .strategy-card p, .strategy-card li { color: #BAC1C8; font-size: 0.95rem; line-height: 1.5; }
    .tag { font-weight: 700; font-size: 0.85rem; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    df = pd.read_csv('Electronic_Sales.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['City'] = df['City'].str.strip()
    return df

df = load_data()

# --- Global Sidebar Controls ---
with st.sidebar:
    st.title("⚙️ Operations Filter")
    st.markdown("---")
    city_filter = st.multiselect(
        "Regional Market Allocation",
        options=sorted(df['City'].unique()),
        default=df['City'].unique()
    )
    st.markdown("---")

filtered_df = df[df['City'].isin(city_filter)]

# --- Header & Executive KPIs ---
st.title("📦 Supply Chain & Fulfillment Operations")
st.markdown("<span style='color: #8A929A; font-size: 1.1rem;'>Executive overview of outbound inventory velocity, regional distribution, and operational bottlenecks.</span>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if not filtered_df.empty:
    total_units = filtered_df['Quantity Ordered'].sum()
    fastest_mover = filtered_df.groupby('Product')['Quantity Ordered'].sum().idxmax()
    peak_month_name = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}[filtered_df.groupby('Month')['Quantity Ordered'].sum().idxmax()]
    avg_order_size = filtered_df['Quantity Ordered'].mean()
else:
    total_units, fastest_mover, peak_month_name, avg_order_size = 0, "N/A", "N/A", 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Units Shipped", f"{total_units:,.0f}")
kpi2.metric("Highest Velocity SKU", fastest_mover)
kpi3.metric("Peak Load Month", peak_month_name)
kpi4.metric("Avg Units Per Order", f"{avg_order_size:,.2f}")

st.markdown("<br><br>", unsafe_allow_html=True) 

# --- Row 1 Visualizations ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("<h4 style='color: #E0E4E8; font-weight: 500;'>Inventory Velocity (YTD)</h4>", unsafe_allow_html=True)
    monthly_trend = filtered_df.groupby('Month')['Quantity Ordered'].sum().reset_index()
    month_map = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    monthly_trend['Month Name'] = monthly_trend['Month'].map(month_map)
    
    fig_line = px.line(monthly_trend, x='Month Name', y='Quantity Ordered', template="plotly_dark", markers=True, color_discrete_sequence=['#4DA8DA'])
    fig_line.update_traces(hovertemplate='<b>%{x}</b><br>Units Shipped: %{y:,.0f}<extra></extra>')
    fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title=None, yaxis_title=None, hovermode="x unified", margin=dict(l=0, r=0, t=10, b=0), height=320)
    fig_line.update_xaxes(showgrid=False)
    fig_line.update_yaxes(showgrid=True, gridcolor='#2A2E37', zeroline=False)
    st.plotly_chart(fig_line, width='stretch')

with c2:
    st.markdown("<h4 style='color: #E0E4E8; font-weight: 500;'>Top SKU Movers</h4>", unsafe_allow_html=True)
    top_products = filtered_df.groupby('Product')['Quantity Ordered'].sum().nlargest(5).reset_index()
    
    fig_bar = px.bar(top_products, y='Product', x='Quantity Ordered', orientation='h', template="plotly_dark", color_discrete_sequence=['#E67E22'])
    fig_bar.update_traces(hovertemplate='<b>%{y}</b><br>Volume: %{x:,.0f}<extra></extra>')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title=None, yaxis_title=None, margin=dict(l=0, r=0, t=10, b=0), height=320)
    fig_bar.update_xaxes(showgrid=True, gridcolor='#2A2E37', zeroline=False)
    st.plotly_chart(fig_bar, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

# --- Row 2 Visualizations ---
c3, c4 = st.columns([1, 1])

with c3:
    st.markdown("<h4 style='color: #E0E4E8; font-weight: 500;'>Fulfillment Load by Hour</h4>", unsafe_allow_html=True)
    hourly_vol = filtered_df.groupby('Hour')['Quantity Ordered'].sum().reset_index()
    
    fig_hour = px.area(hourly_vol, x='Hour', y='Quantity Ordered', template="plotly_dark", color_discrete_sequence=['#9B59B6'])
    fig_hour.update_traces(hovertemplate='<b>Time: %{x}:00</b><br>Units Processed: %{y:,.0f}<extra></extra>')
    fig_hour.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(tickmode='linear', tick0=0, dtick=2), yaxis_title=None, xaxis_title="Hour of Day (24H)", margin=dict(l=0, r=0, t=10, b=0), height=320)
    fig_hour.update_xaxes(showgrid=False)
    fig_hour.update_yaxes(showgrid=True, gridcolor='#2A2E37', zeroline=False)
    st.plotly_chart(fig_hour, width='stretch')

with c4:
    st.markdown("<h4 style='color: #E0E4E8; font-weight: 500;'>Regional Distribution</h4>", unsafe_allow_html=True)
    city_vol = filtered_df.groupby('City')['Quantity Ordered'].sum().reset_index()
    
    fig_tree = px.treemap(city_vol, path=[px.Constant("US Markets"), 'City'], values='Quantity Ordered', color='Quantity Ordered', color_continuous_scale='Blues', template="plotly_dark")
    fig_tree.update_traces(hovertemplate='<b>%{label}</b><br>Units: %{value:,.0f}<extra></extra>')
    fig_tree.update_layout(margin=dict(t=10, l=0, r=0, b=0), paper_bgcolor='rgba(0,0,0,0)', height=320)
    st.plotly_chart(fig_tree, width='stretch')

# --- Executive Briefing & Strategy ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #E0E4E8; font-weight: 600; border-bottom: 1px solid #2A2E37; padding-bottom: 10px;'>📑 Executive Briefing & Strategic Imperatives</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col_strat1, col_strat2, col_strat3 = st.columns(3)

with col_strat1:
    st.markdown("""
    <div class="strategy-card" style="border-top-color: #4DA8DA;">
        <h4 style="color: #4DA8DA;">Surge Capacity Planning</h4>
        <p><span class="tag" style="background-color: rgba(77, 168, 218, 0.15); color: #4DA8DA;">Observation</span> Q4 volume (Nov-Dec) accounts for a disproportionate percentage of total annual outbound freight.</p>
        <p><span class="tag" style="background-color: rgba(231, 76, 60, 0.15); color: #E74C3C;">Risk</span> Floor staff burnout and 3PL carrier rejection during peak weeks.</p>
        <p><span class="tag" style="background-color: rgba(46, 204, 113, 0.15); color: #2ECC71;">Action</span> Finalize seasonal warehouse labor contracts by Oct 15th and pre-book LTL (Less-Than-Truckload) freight capacity with carriers.</p>
    </div>
    """, unsafe_allow_html=True)

with col_strat2:
    st.markdown("""
    <div class="strategy-card" style="border-top-color: #E67E22;">
        <h4 style="color: #E67E22;">SKU Velocity & Replenishment</h4>
        <p><span class="tag" style="background-color: rgba(230, 126, 34, 0.15); color: #E67E22;">Observation</span> Low-margin staples (AAA/AA Batteries, Cables) exhibit the highest physical inventory turnover.</p>
        <p><span class="tag" style="background-color: rgba(231, 76, 60, 0.15); color: #E74C3C;">Risk</span> Stockouts of these components directly block high-margin add-on cart conversions.</p>
        <p><span class="tag" style="background-color: rgba(46, 204, 113, 0.15); color: #2ECC71;">Action</span> Implement automated, strict ERP re-ordering protocols when physical battery stock dips below a 21-day trailing sales average.</p>
    </div>
    """, unsafe_allow_html=True)

with col_strat3:
    st.markdown("""
    <div class="strategy-card" style="border-top-color: #9B59B6;">
        <h4 style="color: #9B59B6;">Intra-Day Shift Optimization</h4>
        <p><span class="tag" style="background-color: rgba(155, 89, 182, 0.15); color: #9B59B6;">Observation</span> Order ingestion spikes predictably in a bi-modal pattern (11:00 AM - 1:00 PM and 6:00 PM - 8:00 PM).</p>
        <p><span class="tag" style="background-color: rgba(231, 76, 60, 0.15); color: #E74C3C;">Risk</span> Processing bottlenecks leading to missed same-day shipping cutoffs.</p>
        <p><span class="tag" style="background-color: rgba(46, 204, 113, 0.15); color: #2ECC71;">Action</span> Stagger warehouse picker shift-starts to overlap maximum headcount exactly during the 12:00 PM and 7:00 PM ingestion spikes.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Raw Data Table ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📁 View Filtered Production Data Segment (Top 100 Rows)"):
    st.dataframe(filtered_df[['Order ID', 'Product', 'Quantity Ordered', 'Price Each', 'City', 'Order Date']].head(100), use_container_width=True)
    
