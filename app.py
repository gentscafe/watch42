import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configurazione Pagina
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# --- INJECT CUSTOM CSS (IL VIBE) ---
def inject_custom_css():
    st.markdown("""
        <style>
        /* Sfondo e font generale */
        .main { background-color: #F8F9FC; }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E5E7EB;
        }
        
        /* Card Style per Metric e Componenti */
        div[data-testid="metric-container"], .stPlotlyChart {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #F3F4F6;
        }
        
        /* Bottoni e Interazioni */
        .stButton>button {
            border-radius: 10px;
            background-color: #2E5BFF;
            color: white;
            border: none;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #1A44D1;
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- MOCK DATA GENERATION ---
@st.cache_data
def get_mock_data():
    brands = ["Patek Philippe", "Audemars Piguet", "Vacheron Constantin", "Rolex", "Mido"]
    df = pd.DataFrame({
        'Model': [f'Watch {i}' for i in range(20)],
        'Price': np.random.randint(2000, 50000, 20),
        'PowerScore': np.random.randint(40, 100, 20),
        'Diameter': np.random.randint(34, 48, 20),
        'Thickness': np.random.randint(6, 18, 20),
        'Brand': np.random.choice(brands, 20)
    })
    return df

data = get_mock_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("watch42")
st.sidebar.caption("v1.0 MVP - WatchBase API") [cite: 2, 5]

menu = st.sidebar.radio(
    "NAVIGATION",
    ["My Watches", "Pricing Intelligence", "Design Intelligence", "Market Intelligence"],
    index=0
) [cite: 16, 18, 19, 20]

# --- GLOBAL FILTERS (PANNELLO FILTRI) ---
with st.sidebar.expander("🔍 FILTERS", expanded=True):
    brand_filter = st.multiselect("Brand", options=data['Brand'].unique()) [cite: 26]
    material = st.selectbox("Case Material", ["Steel", "Titanium", "Gold", "Bronze"]) [cite: 30]
    diameter_range = st.slider("Diameter (mm)", 34, 48, (38, 42)) [cite: 32]
    # Spazio per futuri filtri WatchBase (Caliber, Glass, WR) [cite: 25, 28, 31, 34]

# --- MAIN VIEWS ---

if menu == "My Watches":
    st.header("My Watches")
    st.info("Select a card to set the global 'Target' watch for comparisons.") [cite: 43]
    
    # Grid Layout per Card
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid #EEE;">
                <img src="https://via.placeholder.com/150" style="width:100%; border-radius:10px;">
                <h4 style="margin-top:10px;">Model {i+1}</h4>
                <p style="color: gray; font-size: 0.8em;">Ref: 12345-ABC</p>
                <hr>
                <p><b>Price:</b> €{12000 + (i*1000)}</p>
                <p><b>Status:</b> <span style="color: green;">Up to date</span></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Set Target {i+1}", key=f"btn_{i}"):
                st.session_state.target = f"Model {i+1}" [cite: 38, 39, 40, 41, 42]

elif menu == "Pricing Intelligence":
    st.header("Pricing & Value-for-Money Matrix") [cite: 18, 45]
    
    fig = px.scatter(data, x='Price', y='PowerScore', color='Brand', 
                     title="Scatter Plot: Price vs Power Score") [cite: 46, 47, 48]
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Dots are static. Only Target watch is highlighted in real-time comparison.") [cite: 49, 50]

elif menu == "Design Intelligence":
    st.header("White Space Heatmap") [cite: 19, 51]
    
    # Generazione Heatmap fittizia basata su Diameter e Thickness
    heatmap_data = np.histogram2d(data['Diameter'], data['Thickness'], bins=[7, 6])[0]
    fig = px.imshow(heatmap_data, 
                    labels=dict(x="Thickness (mm)", y="Diameter (mm)", color="Density"),
                    x=[6, 8, 10, 12, 14, 16],
                    y=[34, 36, 38, 40, 42, 44, 46],
                    color_continuous_scale='RdYlGn_r') # Green: Opportunity, Red: Saturated [cite: 55, 56, 57]
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Market Intelligence":
    st.header("Tech Evolution Tracker") [cite: 20, 58]
    
    # Time Series Mock
    dates = pd.date_range(start='2020-01-01', periods=12, freq='M')
    power_reserve_avg = [42, 42, 45, 48, 50, 50, 60, 65, 70, 72, 72, 72]
    
    fig = px.line(x=dates, y=power_reserve_avg, title="Average Power Reserve Evolution (Industry)") [cite: 59, 60]
    st.plotly_chart(fig, use_container_width=True)
    
    # AI INSIGHTS PANEL
    st.subheader("🤖 AI Strategic Insights") [cite: 61]
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        st.warning("Standard 72h detected: Your model is 30% below industry average.") [cite: 62, 63]
    with col_ai2:
        st.success("Titanium Trend: +12% increase in Diver category (< 3,000€).") [cite: 64, 65]

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.info("Data source: WatchBase Professional API") [cite: 5]