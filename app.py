import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. INJECT CSS (Ottimizzato per evitare errori di visualizzazione)
def inject_custom_css():
    st.markdown("""
        <style>
        .main { background-color: #F8F9FC; }
        [data-testid="stSidebar"] {
            background-color: #FBFBFE !important;
            border-right: 1px solid #E5E7EB !important;
        }
        
        /* Allineamento Sidebar */
        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            border: none !important;
            background-color: transparent !important;
            text-align: left !important;
            padding: 12px 25px !important;
            color: #1F2937 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 15px !important;
        }

        /* CARD STYLE: Rendering grafico */
        .watch-card {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            border: 1px solid #F3F4F6;
            margin-bottom: 20px;
        }

        .card-image-placeholder {
            height: 140px;
            background-color: #F3F4F6;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 45px;
            margin-bottom: 15px;
        }

        .watch-details {
            margin: 15px 0;
            padding: 10px 0;
            border-top: 1px solid #F3F4F6;
            border-bottom: 1px solid #F3F4F6;
        }

        .detail-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-size: 13px;
        }

        .detail-label { color: #6B7280; font-weight: 500; }
        .detail-value { color: #111827; font-weight: 600; text-align: right; }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 3. MOCK DATA (Generazione riga per riga)
@st.cache_data
def get_clean_data():
    return pd.DataFrame({
        'Model': [f'All Dial Model {i+1}' for i in range(6)],
        'Reference': [f'M001.431.11.0{i}1.02' for i in range(6)],
        'Price': [1200, 1350, 1500, 1650, 1800, 1950],
        'Material': ["Steel", "Titanium", "Titanium", "Steel", "Gold", "Steel"],
        'Diameter': ["42mm", "38mm", "38mm", "40mm", "42mm", "38mm"],
        'Movement': ["Manual", "Manual", "Manual", "Manual", "Automatic", "Automatic"]
    })

df = get_clean_data()

# 4. SIDEBAR
st.sidebar.title("watch42")
if 'menu' not in st.session_state: st.session_state.menu = "My Watches"

if st.sidebar.button("⌚ My Watches"): st.session_state.menu = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.menu = "Pricing Intelligence"
if st.sidebar.button("🗺️ Design Intelligence"): st.session_state.menu = "Design Intelligence"
if st.sidebar.button("📈 Market Intelligence"): st.session_state.menu = "Market Intelligence"

# 5. VISTA "MY WATCHES"
if st.session_state.menu == "My Watches":
    st.header("My Watches")
    
    cols = st.columns(3)
    for i in range(len(df)):
        with cols[i % 3]:
            # Estrazione valori singoli per evitare errori di testo
            row = df.iloc[i]
            
            # Rendering della Card
            st.markdown(f"""
            <div class="watch-card">
                <div class="card-image-placeholder">⌚</div>
                <div style="font-size: 17px; font-weight: 700; color: #111827;">{row['Model']}</div>
                <div style="color: #6B7280; font-size: 12px; margin-bottom: 10px;">Ref: {row['Reference']}</div>
                
                <div class="watch-details">
                    <div class="detail-row">
                        <span class="detail-label">Material</span>
                        <span class="detail-value">{row['Material']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Diameter</span>
                        <span class="detail-value">{row['Diameter']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Movement</span>
                        <span class="detail-value">{row['Movement']}</span>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div style="font-size: 20px; font-weight: 700; color: #2E5BFF;">€ {row['Price']}</div>
                    <div style="font-size: 12px; color: #059669; font-weight: 600;">● Up to date</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Bottone azione Streamlit separato dall'HTML
            st.button("Set as Target", key=f"target_{i}")
