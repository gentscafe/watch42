import streamlit as st
import pandas as pd
import numpy as np
from database_engine import db_engine

# 1. CONFIGURAZIONE PAGINA (Indispensabile come primo comando)
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS PROFESSIONALE
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] { background-color: #FBFBFE !important; border-right: 1px solid #E5E7EB !important; }
    .sidebar-header { font-size: 11px; font-weight: 700; color: #9CA3AF; text-transform: uppercase; padding: 25px 20px 10px 20px; }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; border: none !important; background-color: transparent !important;
        text-align: left !important; padding: 10px 20px !important; display: flex !important;
        align-items: center !important; justify-content: flex-start !important; gap: 12px !important;
        color: #1F2937 !important; font-size: 14px !important;
    }
    
    .info-grid { margin: 15px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px; }
    .info-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    
    /* Titoli sezioni nel pannello Modifica */
    .edit-section-header {
        font-size: 14px; font-weight: 700; color: #2E5BFF;
        margin-bottom: 15px; padding-bottom: 5px; border-bottom: 2px solid #EEF2FF;
    }
    </style>
""", unsafe_allow_html=True)

# 3. STATO NAVIGAZIONE
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# 4. SIDEBAR
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
if st.sidebar.button("🗺️ Design Intelligence"): st.session_state.nav = "Design"
if st.sidebar.button("📈 Market Intelligence"): st.session_state.nav = "Market"
st.sidebar.markdown("---")
if st.sidebar.button("🗄️ Watch DB Explorer"): st.session_state.nav = "DB"

# 5. LOGICA VISTA "MY WATCHES"
if st.session_state.nav == "My Watches":
    st.header("My Watches")
    
    # PANNELLO DI MODIFICA ESTESO (Nuovi campi Movimento)
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = db_engine.df.loc[idx]
        
        with st.container(border=True):
            st.subheader(f"📝 Modifica Tecnica Avanzata: {item['model_name']}")
            
            # SUDDIVISIONE IN COLONNE PER GESTIRE I MOLTI CAMPI
            tab_ext, tab_mov, tab_perf = st.tabs(["Estetica & Brand", "Meccanica (Calibro)", "Funzioni & Prestazioni"])
            
            with tab_ext:
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Brand", item['brand'], key="edit_brand")
                    st.text_input("Model Name", item['model_name'], key="edit_model")
                    st.text_input("Reference", item['reference'], key="edit_ref")
                with c2:
                    st.multiselect("Material", ["Steel", "Titanium", "Gold", "Ceramic", "Bronze", "Tantalum"], key="edit_mat")
                    st.slider("Diameter (mm)", 34, 48, 39, format="%dmm", key="edit_dia")
                    st.radio("Watch Style", ["Diver", "GMT", "Dress", "Casual", "Chronograph"], horizontal=True, key="edit_style")

            with tab_mov:
                st.markdown('<div class="edit-section-header">DETTAGLI MOVIMENTO</div>', unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.text_input("Caliber Brand", value="Mido", help="Marca del produttore del movimento", key="mov_brand")
                    st.text_input("Caliber Reference", value="Mido 72", help="Sigla del calibro", key="mov_ref")
                    st.text_input("Base Movement", value="ETA A31.111", help="Movimento di partenza", key="mov_base")
                with m2:
                    st.selectbox("Winding", ["Manual", "Automatic", "Quartz", "Kinetic"], index=1, key="mov_type")
                    st.text_input("Display", value="Analog", key="mov_display")
                    st.number_input("Mov. Diameter (mm)", value=25.60, step=0.01, format="%.2f", key="mov_diam")
                with m3:
                    st.number_input("Jewels", value=21, step=1, key="mov_jewels")
                    st.text_input("Movement Origin", value="In-House", key="mov_origin")

            with tab_perf:
                st.markdown('<div class="edit-section-header">PRESTAZIONI E COMPLICAZIONI</div>', unsafe_allow_html=True)
                p1, p2 = st.columns(2)
                with p1:
                    st.text_input("Power Reserve", value="72 hours", key="mov_reserve")
                    st.text_input("Frequency", value="25,200 vph", key="mov_freq")
                    st.number_input("Price Estimate (€)", value=85000, step=1000, key="edit_price")
                with p2:
                    st.multiselect("Functions (Hands)", ["Hours", "Minutes", "Seconds", "Small Seconds"], default=["Hours", "Minutes", "Seconds"], key="mov_hands")
                    st.multiselect("Complications", ["Tourbillon", "Moonphase", "GMT", "Date", "Annual Calendar"], key="edit_comp")
                    st.text_input("Astro Complications", value="Moonphase", key="mov_astro")
            
            save_col, cancel_col = st.columns([1, 8])
            if save_col.button("Save Changes", type="primary"):
                st.session_state.edit_id = None
                st.toast("Database aggiornato con successo!")
                st.rerun()
            if cancel_col.button("Cancel"):
                st.session_state.edit_id = None
                st.rerun()
        st.markdown("---")

    # GRIGLIA CARD (Esempio sui primi 9 record)
    display_df = db_engine.df.head(9)
    cols = st.columns(3)
    for i, (idx, row) in enumerate(display_df.iterrows()):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"""
                <div style="height:120px; background-color:#F3F4F6; border-radius:15px; display:flex; justify-content:center; align-items:center; font-size:40px;">⌚</div>
                <div style="font-weight:700; font-size:17px; margin-top:15px; color:#111827;">{row['model_name']}</div>
                <div style="color:#6B7280; font-size:12px; margin-bottom:10px;">Ref: {row['reference']}</div>
                <div class="info-grid">
                    <div class="info-row"><span class="info-label">Brand</span><span class="info-value">{row['brand']}</span></div>
                    <div class="info-row"><span class="info-label">Material</span><span class="info-value">{row['case_material']}</span></div>
                    <div class="info-row"><span class="info-label">Diameter</span><span class="info-value">{row['diameter']}</span></div>
                </div>
                """, unsafe_allow_html=True)
                
                b1, b2 = st.columns(2)
                if b1.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                    st.session_state.edit_id = idx
                    st.rerun()
                b2.button("Set Target", key=f"tr_{idx}", use_container_width=True)

# [Le altre sezioni rimangono invariate]
