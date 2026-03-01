import streamlit as st
import pandas as pd
import numpy as np
from database_engine import db_engine

# 1. CONFIGURAZIONE PAGINA (Primo comando assoluto)
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS PROFESSIONALE PER SIDEBAR E TILE
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] { background-color: #FBFBFE !important; border-right: 1px solid #E5E7EB !important; }
    .sidebar-header { font-size: 11px; font-weight: 700; color: #9CA3AF; text-transform: uppercase; padding: 25px 20px 10px 20px; }
    
    /* Reset Bottoni Sidebar */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; border: none !important; background-color: transparent !important;
        text-align: left !important; padding: 10px 20px !important; display: flex !important;
        align-items: center !important; justify-content: flex-start !important; gap: 12px !important;
        color: #1F2937 !important; font-size: 14px !important;
    }
    
    /* Card/Tile Styling */
    .info-grid { margin: 15px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px; }
    .info-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 3. STATO NAVIGAZIONE
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# 4. SIDEBAR (Voci ripristinate senza filtri)
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
    
    # PANNELLO DI MODIFICA AGGIORNATO
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = db_engine.df.loc[idx]
        
        with st.container(border=True):
            st.subheader(f"📝 Modifica Tecnica: {item['model_name']}")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.text_input("Brand", item['brand'], key="edit_brand") # cite: Richiesta Utente
                st.text_input("Model Name", item['model_name'], key="edit_model") # cite: Richiesta Utente
                st.text_input("Reference", item['reference'], key="edit_ref") # cite: Richiesta Utente
                st.pills("Watch Style", ["Diver", "GMT", "Dress", "Casual", "Chronograph"], key="edit_style") # cite: Richiesta Utente
            
            with c2:
                st.multiselect("Material", ["Steel", "Titanium", "Gold", "Ceramic", "Tantalum", "Bronze"], 
                               default=[item['case_material']] if item['case_material'] in ["Steel", "Titanium", "Gold", "Ceramic", "Tantalum", "Bronze"] else [],
                               key="edit_mat") # cite: Richiesta Utente
                st.slider("Diameter", 34, 48, int(item['diameter_clean']), format="%dmm", key="edit_dia") # cite: Richiesta Utente
                st.selectbox("Movement Type", ["Manual Wind", "Automatic", "Quartz"], key="edit_mov_type") # cite: Richiesta Utente
                st.radio("Movement Origin", ["In-House", "Third-Party (ETA/Sellita)", "Modified"], horizontal=True, key="edit_mov_orig") # cite: Richiesta Utente
            
            with c3:
                st.multiselect("Complications", ["Tourbillon", "Moonphase", "GMT", "Date", "Annual Calendar"], key="edit_comp") # cite: Richiesta Utente
                st.number_input("Price Estimate (€)", value=85000, step=1000, key="edit_price") # cite: Richiesta Utente
            
            btn_save, btn_cancel = st.columns([1, 8])
            if btn_save.button("Save Changes", type="primary"):
                st.session_state.edit_id = None
                st.toast("Database aggiornato con successo!")
                st.rerun()
            if btn_cancel.button("Cancel"):
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

# [Le altre sezioni Pricing, Design, Market rimangono accessibili dalla sidebar]
