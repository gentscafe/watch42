import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. INJECT ADVANCED CUSTOM CSS (SIDEBAR PROFESSIONALE)
def inject_custom_css():
    st.markdown("""
        <style>
        /* Sfondo generale Off-White */
        .main { background-color: #F8F9FC; }
        
        /* Sidebar pulita e minimale */
        [data-testid="stSidebar"] {
            background-color: #FBFBFE !important;
            border-right: 1px solid #E5E7EB !important;
        }
        
        /* Sezione Titolo (REPORTS nel riferimento) */
        .sidebar-header {
            font-size: 11px;
            font-weight: 700;
            color: #9CA3AF;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 20px 20px 10px 20px;
        }

        /* RESET BOTTONI SIDEBAR: Allineamento a sinistra e stile testo */
        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            border: none !important;
            background-color: transparent !important;
            text-align: left !important;
            padding: 12px 20px !important;
            border-radius: 0px !important;
            color: #1F2937 !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            display: flex !important;
            align-items: center !important;
            gap: 15px !important;
            transition: all 0.2s;
        }
        
        /* Effetto hover e selezione */
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #F3F4F6 !important;
            color: #2E5BFF !important;
        }

        /* CARD STYLE: Ombre morbide */
        .watch-card {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            border: 1px solid #F3F4F6;
            margin-bottom: 20px;
        }

        .card-title { font-size: 18px; font-weight: 600; color: #111827; }
        .card-price { font-size: 22px; font-weight: 700; color: #2E5BFF; margin-top: 10px; }
        .card-status { font-size: 12px; color: #059669; font-weight: 600; }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 3. MOCK DATA
@st.cache_data
def get_mock_data():
    return pd.DataFrame({
        'Model': [f'Watch {i}' for i in range(25)],
        'Price': np.random.randint(800, 50000, 25),
        'PowerScore': np.random.randint(38, 80, 25),
        'Diameter': np.random.randint(34, 48, 25),
        'Thickness': np.random.randint(6, 18, 25),
        'Brand': np.random.choice(["Mido", "Rolex", "Cartier"], 25)
    })

data = get_mock_data()

# 4. SIDEBAR NAVIGATION (Esattamente come Screenshot 14.43.19)
st.sidebar.markdown('<div class="sidebar-header">MENU</div>', unsafe_allow_html=True)

if 'menu' not in st.session_state:
    st.session_state.menu = "My Watches"

# Navigazione con icone pulite e allineamento a sinistra
if st.sidebar.button("⌚  My Watches"):
    st.session_state.menu = "My Watches"
if st.sidebar.button("📊  Pricing Intelligence"):
    st.session_state.menu = "Pricing Intelligence"
if st.sidebar.button("🗺️  Design Intelligence"):
    st.session_state.menu = "Design Intelligence"
if st.sidebar.button("📈  Market Intelligence"):
    st.session_state.menu = "Market Intelligence"

# 5. VISTE
menu = st.session_state.menu

if menu == "My Watches":
    st.header("My Watches")
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="watch-card">
                <div class="card-title">All Dial Model {i+1}</div>
                <div style="color: #6B7280; font-size: 13px;">Ref: M001.431.11.0{i}1.02</div>
                <div class="card-price">€ {1200 + (i*150)}</div>
                <div class="card-status">● Up to date</div>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Set as Target", key=f"target_{i}")

elif menu == "Pricing Intelligence":
    st.header("Pricing Intelligence")
    fig = px.scatter(data, x='Price', y='PowerScore', color='Brand')
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Design Intelligence":
    st.header("Design Intelligence")
    fig = px.density_heatmap(data, x='Diameter', y='Thickness')
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Market Intelligence":
    st.header("Market Intelligence")
    st.warning("Trend Alert: Il mercato si sta spostando verso lo standard 72h.")
    st.line_chart(np.random.randint(42, 72, 12))
