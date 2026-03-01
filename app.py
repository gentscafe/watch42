import streamlit as st
import pandas as pd
from database_engine import db_engine, USER_BRAND_NAME

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# (Mantieni qui il tuo blocco CSS originale)

# 3. STATO NAVIGAZIONE
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# 4. SIDEBAR
st.sidebar.markdown(f'<div style="padding: 20px; color: #2E5BFF; font-weight: 800; font-size: 24px;">{USER_BRAND_NAME}</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
st.sidebar.markdown("---")
if st.sidebar.button("🗄️ Watch DB Explorer"): st.session_state.nav = "DB"

# 5. LOGICA VISTA "MY WATCHES"
if st.session_state.nav == "My Watches":
    st.header(f"Portfolio: {USER_BRAND_NAME}")
    
    my_watches_df = db_engine.get_my_watches()
    
    if my_watches_df.empty:
        st.info("Generazione database in corso... Ricarica la pagina tra un istante.")
    else:
        cols = st.columns(3)
        for i, (idx, row) in enumerate(my_watches_df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"""
                    <div style="height:120px; background-color:#F3F4F6; border-radius:15px; display:flex; justify-content:center; align-items:center; font-size:40px;">⌚</div>
                    <div style="font-weight:700; font-size:17px; margin-top:15px; color:#111827;">{row['model_name']}</div>
                    <div style="color:#6B7280; font-size:12px; margin-bottom:10px;">Ref: {row['reference']}</div>
                    <div class="info-grid">
                        <div class="info-row"><span class="info-label">Material</span><span class="info-value">{row['material']}</span></div>
                        <div class="info-row"><span class="info-label">Price</span><span class="info-value">€{row['price_estimate']:,}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                        st.session_state.edit_id = idx
                        st.rerun()
