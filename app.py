import streamlit as st
import pandas as pd
import numpy as np
from database_engine import get_watch_dataset

# 1. CONFIGURAZIONE LAYOUT
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# Caricamento Dati
df_global = get_watch_dataset()

# 2. CSS "HARD-CODED" (Forza l'allineamento a sinistra e lo stile delle card)
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] {
        background-color: #FBFBFE !important;
        border-right: 1px solid #E5E7EB !important;
    }
    .sidebar-header {
        font-size: 11px; font-weight: 700; color: #9CA3AF;
        text-transform: uppercase; padding: 25px 20px 10px 20px;
    }
    /* CARD DESIGN */
    .watch-tile {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #F3F4F6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .img-box {
        height: 120px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center; font-size: 40px;
    }
    .info-table {
        margin: 15px 0; padding: 10px; background-color: #F9FAFB; border-radius: 10px;
    }
    .row-info { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px; }
    
    /* SIDEBAR FIX: Forza i bottoni a sinistra */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; text-align: left !important;
        justify-content: flex-start !important; border: none !important;
        background: transparent !important; padding: 10px 20px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover { background: #F3F4F6 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. STATO DELLA NAVIGAZIONE
if 'nav' not in st.session_state:
    st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None

# 4. SIDEBAR
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
if st.sidebar.button("🗄️ Watch DB"): st.session_state.nav = "DB"

# 5. LOGICA DELLE PAGINE
if st.session_state.nav == "My Watches":
    st.header("My Watches")
    
    # Pannello di Modifica (appare solo se clicchi Modifica)
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = df_global.iloc[idx]
        with st.container(border=True):
            st.subheader(f"Modifica: {item['model_name']}")
            c1, c2 = st.columns(2)
            new_price = c1.text_input("Prezzo (€)", item['price'])
            new_mat = c2.text_input("Materiale", item['case_material'])
            if st.button("Conferma Modifiche"):
                st.session_state.edit_id = None
                st.rerun()

    # GRIGLIA 3 COLONNE
    rows = df_global.head(6)
    cols = st.columns(3)
    
    for i, (idx, row) in enumerate(rows.iterrows()):
        with cols[i % 3]:
            # Tile HTML
            st.markdown(f"""
            <div class="watch-tile">
                <div class="img-box">⌚</div>
                <div style="font-weight:700; font-size:18px; margin-top:10px;">{row['model_name']}</div>
                <div style="color:gray; font-size:12px;">Ref: {row['reference']}</div>
                <div class="info-table">
                    <div class="row-info"><span>Brand</span><b>{row['brand']}</b></div>
                    <div class="row-info"><span>Material</span><b>{row['case_material']}</b></div>
                    <div class="row-info"><span>Diameter</span><b>{row['diameter']}</b></div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="color:#2E5BFF; font-size:22px; font-weight:700;">€ {row['price']}</div>
                    <div style="color:green; font-size:12px;">● Online</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Bottoni interni (Streamlit nativi)
            b1, b2 = st.columns(2)
            if b1.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                st.session_state.edit_id = idx
                st.rerun()
            if b2.button("Target", key=f"tr_{idx}", use_container_width=True):
                st.toast(f"Target impostato su {row['model_name']}")

elif st.session_state.nav == "Pricing":
    st.header("Pricing Intelligence")
    st.scatter_chart(df_global.head(50), x="price", y="diameter", color="brand")

elif st.session_state.nav == "DB":
    st.header("Watch Database")
    st.dataframe(df_global, use_container_width=True)
