import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS AVANZATO (Correzione definitiva per card e sidebar)
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] {
        background-color: #FBFBFE !important;
        border-right: 1px solid #E5E7EB !important;
    }
    
    /* Stile per le card */
    .watch-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6;
        margin-bottom: 20px;
        font-family: 'Inter', sans-serif;
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
    .detail-value { color: #111827; font-weight: 600; }
    
    /* Sidebar Allineamento Sinistra */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        border: none !important;
        background-color: transparent !important;
        text-align: left !important;
        padding: 12px 25px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. DATI PULITI (Estraiamo i valori correttamente)
@st.cache_data
def get_clean_data():
    return [
        {"Model": "All Dial Model 1", "Ref": "M001.431.11.001.02", "Price": 1200, "Mat": "Steel", "Dia": "42mm", "Mov": "Manual"},
        {"Model": "All Dial Model 2", "Ref": "M001.431.11.011.02", "Price": 1350, "Mat": "Titanium", "Dia": "38mm", "Mov": "Manual"},
        {"Model": "All Dial Model 3", "Ref": "M001.431.11.021.02", "Price": 1500, "Mat": "Titanium", "Dia": "38mm", "Mov": "Manual"},
        {"Model": "All Dial Model 4", "Ref": "M001.431.11.031.02", "Price": 1650, "Mat": "Steel", "Dia": "40mm", "Mov": "Manual"},
        {"Model": "All Dial Model 5", "Ref": "M001.431.11.041.02", "Price": 1800, "Mat": "Gold", "Dia": "42mm", "Mov": "Automatic"},
        {"Model": "All Dial Model 6", "Ref": "M001.431.11.051.02", "Price": 1950, "Mat": "Steel", "Dia": "38mm", "Mov": "Automatic"}
    ]

watches = get_clean_data()

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
    for i, w in enumerate(watches):
        with cols[i % 3]:
            # Utilizziamo una f-string pulita per l'HTML
            card_html = f"""
            <div class="watch-card">
                <div class="card-image-placeholder">⌚</div>
                <div style="font-size: 17px; font-weight: 700; color: #111827;">{w['Model']}</div>
                <div style="color: #6B7280; font-size: 12px; margin-bottom: 10px;">Ref: {w['Ref']}</div>
                
                <div class="watch-details">
                    <div class="detail-row"><span class="detail-label">Material</span><span class="detail-value">{w['Mat']}</span></div>
                    <div class="detail-row"><span class="detail-label">Diameter</span><span class="detail-value">{w['Dia']}</span></div>
                    <div class="detail-row"><span class="detail-label">Movement</span><span class="detail-value">{w['Mov']}</span></div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div style="font-size: 20px; font-weight: 700; color: #2E5BFF;">€ {w['Price']}</div>
                    <div style="font-size: 12px; color: #059669; font-weight: 600;">● Up to date</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            st.button("Set as Target", key=f"target_{i}")
