import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS DEFINITIVO (Fix Sidebar e Card)
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] {
        background-color: #FBFBFE !important;
        border-right: 1px solid #E5E7EB !important;
    }
    .sidebar-header {
        font-size: 11px; font-weight: 700; color: #9CA3AF;
        letter-spacing: 1.5px; text-transform: uppercase;
        padding: 30px 25px 15px 25px;
    }
    .watch-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6; margin-bottom: 10px;
    }
    .card-image-placeholder {
        height: 140px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center;
        font-size: 45px; margin-bottom: 15px;
    }
    .watch-details {
        margin: 15px 0; padding: 12px;
        background-color: #F9FAFB; border-radius: 10px;
    }
    .detail-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; }
    .detail-label { color: #6B7280; font-weight: 500; }
    .detail-value { color: #111827; font-weight: 600; }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; border: none !important;
        background-color: transparent !important; text-align: left !important;
        padding: 12px 25px !important; display: flex !important;
        align-items: center !important; justify-content: flex-start !important; gap: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. GESTIONE DATI IN SESSION STATE
if 'watch_data' not in st.session_state:
    st.session_state.watch_data = [
        {"Model": "All Dial Model 1", "Ref": "M001.431.11.001.02", "Price": "1.200", "Mat": "Steel", "Dia": "42mm", "Mov": "Manual"},
        {"Model": "All Dial Model 2", "Ref": "M001.431.11.011.02", "Price": "1.350", "Mat": "Titanium", "Dia": "38mm", "Mov": "Manual"},
        {"Model": "All Dial Model 3", "Ref": "M001.431.11.021.02", "Price": "1.500", "Mat": "Titanium", "Dia": "38mm", "Mov": "Manual"},
        {"Model": "All Dial Model 4", "Ref": "M001.431.11.031.02", "Price": "1.650", "Mat": "Steel", "Dia": "40mm", "Mov": "Manual"},
        {"Model": "All Dial Model 5", "Ref": "M001.431.11.041.02", "Price": "1.800", "Mat": "Gold", "Dia": "42mm", "Mov": "Automatic"},
        {"Model": "All Dial Model 6", "Ref": "M001.431.11.051.02", "Price": "1.950", "Mat": "Steel", "Dia": "38mm", "Mov": "Automatic"}
    ]

if 'editing_index' not in st.session_state:
    st.session_state.editing_index = None

# 4. SIDEBAR
st.sidebar.markdown('<div class="sidebar-header">MENU</div>', unsafe_allow_html=True)
if 'menu' not in st.session_state: st.session_state.menu = "My Watches"

if st.sidebar.button("⌚ My Watches"): st.session_state.menu = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.menu = "Pricing Intelligence"
if st.sidebar.button("🗺️ Design Intelligence"): st.session_state.menu = "Design Intelligence"
if st.sidebar.button("📈 Market Intelligence"): st.session_state.menu = "Market Intelligence"

menu = st.session_state.menu

# 5. LOGICA DELLE VISTE
if menu == "My Watches":
    st.header("My Watches")
    
    # SEZIONE DI MODIFICA (Sostituisce il Pop-up se un indice è selezionato)
    if st.session_state.editing_index is not None:
        idx = st.session_state.editing_index
        watch = st.session_state.watch_data[idx]
        
        with st.expander(f"📝 Editing: {watch['Model']}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                new_model = st.text_input("Model Name", watch["Model"])
                new_ref = st.text_input("Reference", watch["Ref"])
                new_price = st.text_input("Price (€)", watch["Price"])
            with col2:
                new_mat = st.selectbox("Material", ["Steel", "Titanium", "Gold", "Bronze"], index=0)
                new_dia = st.text_input("Diameter", watch["Dia"])
                new_mov = st.selectbox("Movement", ["Manual", "Automatic", "Quartz"], index=0)
            
            c1, c2 = st.columns(2)
            if c1.button("Save Changes", type="primary"):
                st.session_state.watch_data[idx] = {
                    "Model": new_model, "Ref": new_ref, "Price": new_price,
                    "Mat": new_mat, "Dia": new_dia, "Mov": new_mov
                }
                st.session_state.editing_index = None
                st.rerun()
            if c2.button("Cancel"):
                st.session_state.editing_index = None
                st.rerun()
        st.markdown("---")

    # GRIGLIA OROLOGI
    cols = st.columns(3)
    for i, w in enumerate(st.session_state.watch_data):
        with cols[i % 3]:
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
            
            btn_col1, btn_col2 = st.columns(2)
            if btn_col1.button(f"Edit Details", key=f"edit_btn_{i}"):
                st.session_state.editing_index = i
                st.rerun()
            btn_col2.button("Set as Target", key=f"target_btn_{i}")

else:
    st.info(f"Sezione {menu} in fase di sviluppo.")
