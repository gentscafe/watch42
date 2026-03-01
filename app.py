import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. INJECT DEFINITIVE CSS
def inject_custom_css():
    st.markdown("""
        <style>
        .main { background-color: #F8F9FC; }
        [data-testid="stSidebar"] {
            background-color: #FBFBFE !important;
            border-right: 1px solid #E5E7EB !important;
        }

        .sidebar-header {
            font-size: 11px;
            font-weight: 700;
            color: #9CA3AF;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 30px 25px 15px 25px;
        }

        [data-testid="stSidebar"] .stButton {
            display: flex;
            justify-content: flex-start !important;
            width: 100%;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            border: none !important;
            background-color: transparent !important;
            text-align: left !important;
            padding: 12px 25px !important;
            border-radius: 0px !important;
            color: #1F2937 !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 15px !important;
            transition: all 0.2s ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #F3F4F6 !important;
            color: #2E5BFF !important;
        }

        /* Stile Card area principale aggiornato */
        .watch-card {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            border: 1px solid #F3F4F6;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .card-image-placeholder {
            height: 150px;
            background-color: #F3F4F6;
            border-radius: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 50px;
            color: #9CA3AF;
        }

        .watch-details {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .detail-item {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
        }

        .detail-label {
            color: #6B7280;
            font-weight: 500;
        }

        .detail-value {
            color: #111827;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 3. MOCK DATA
@st.cache_data
def get_mock_data():
    return pd.DataFrame({
        'Model': [f'All Dial Model {i+1}' for i in range(6)],
        'Reference': [f'Ref: M001.431.11.0{i}1.02' for i in range(6)],
        'Price': [1200 + (i*150) for i in range(6)],
        'Material': np.random.choice(["Steel", "Gold", "Gold/Steel", "Titanium"], 6),
        'Diameter': np.random.choice(["38mm", "40mm", "42mm"], 6),
        'Movement': np.random.choice(["Automatic", "Quartz", "Manual"], 6),
        'TechStatus': ["● Up to date"] * 6
    })

data = get_mock_data()

# 4. SIDEBAR NAVIGATION
st.sidebar.markdown('<div class="sidebar-header">MENU</div>', unsafe_allow_html=True)

if 'menu' not in st.session_state:
    st.session_state.menu = "My Watches"

if st.sidebar.button("⌚ My Watches"):
    st.session_state.menu = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"):
    st.session_state.menu = "Pricing Intelligence"
if st.sidebar.button("🗺️ Design Intelligence"):
    st.session_state.menu = "Design Intelligence"
if st.sidebar.button("📈 Market Intelligence"):
    st.session_state.menu = "Market Intelligence"

# 5. LOGICA VISTE
menu = st.session_state.menu

if menu == "My Watches":
    st.header("My Watches")
    st.caption("Visualizzazione a griglia degli orologi del brand.")
    
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            # Card HTML personalizzata con placeholder e dettagli aggiuntivi
            st.markdown(f"""
            <div class="watch-card">
                <div class="card-image-placeholder">⌚</div>
                <div>
                    <div style="font-size: 18px; font-weight: 600;">{data['Model'][i]}</div>
                    <div style="color: #6B7280; font-size: 13px; margin-bottom: 15px;">{data['Reference']}</div>
                </div>
                
                <div class="watch-details">
                    <div class="detail-item"><span class="detail-label">Material:</span><span class="detail-value">{data['Material']}</span></div>
                    <div class="detail-item"><span class="detail-label">Diameter:</span><span class="detail-value">{data['Diameter']}</span></div>
                    <div class="detail-item"><span class="detail-label">Movement:</span><span class="detail-value">{data['Movement']}</span></div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: auto; padding-top: 15px;">
                    <div style="font-size: 22px; font-weight: 700; color: #2E5BFF;">€ {data['Price']}</div>
                    <div style="font-size: 12px; color: #059669; font-weight: 600;">{data['TechStatus']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Manteniamo il pulsante "Set as Target" sotto la card
            st.button("Set as Target", key=f"target_{i}")

elif menu == "Pricing Intelligence":
    st.header("Pricing Intelligence")
    # Generiamo mock data temporanei più ampi per il grafico
    graph_data = pd.DataFrame({
        'Price': np.random.randint(800, 50000, 25),
        'PowerScore': np.random.randint(38, 80, 25),
        'Brand': np.random.choice(["Mido", "Rolex", "Cartier"], 25)
    })
    st.plotly_chart(px.scatter(graph_data, x='Price', y='PowerScore', color='Brand'), use_container_width=True)

elif menu == "Design Intelligence":
    st.header("Design Intelligence")
    # Generiamo mock data temporanei più ampi per la heatmap
    heatmap_data = pd.DataFrame({
        'Diameter': np.random.randint(34, 48, 25),
        'Thickness': np.random.randint(6, 18, 25)
    })
    st.plotly_chart(px.density_heatmap(heatmap_data, x='Diameter', y='Thickness'), use_container_width=True)

elif menu == "Market Intelligence":
    st.header("Market Intelligence")
    st.line_chart(np.random.randint(42, 72, 12))
