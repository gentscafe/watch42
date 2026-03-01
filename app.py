import streamlit as st
import pandas as pd
from database_engine import db_engine, USER_BRAND_NAME

st.set_page_config(page_title="watch42", layout="wide")

# CSS (Manteniamo l'info-grid per le tile)
st.markdown("""
    <style>
    .info-grid { margin: 10px 0; padding: 10px; background-color: #F9FAFB; border-radius: 8px; }
    .info-row { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# Gestione Session State
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

# SIDEBAR
st.sidebar.title(f"Dashboard: {USER_BRAND_NAME}")
if st.sidebar.button("⌚ My Watches"): 
    st.session_state.nav = "My Watches"
    st.session_state.edit_ref = None
    st.rerun()
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"

# PAGINA MY WATCHES
if st.session_state.nav == "My Watches":
    if st.session_state.edit_ref is not None:
        # --- PANNELLO MODIFICA ATTIVO ---
        watch = db_engine.df[db_engine.df['reference'] == st.session_state.edit_ref].iloc[0]
        st.header(f"Modifica Tecnica: {watch['reference']}")
        if st.button("← Torna alla lista"):
            st.session_state.edit_ref = None
            st.rerun()

        tab_ext, tab_mov, tab_perf = st.tabs(["Estetica", "Meccanica", "Prestazioni"])
        with tab_ext:
            c1, c2 = st.columns(2)
            c1.text_input("Model Name", value=watch['model_name'])
            c2.selectbox("Material", ["Steel", "Gold", "Titanium", "Platinum"], index=0)
        with tab_mov:
            m1, m2 = st.columns(2)
            m1.text_input("Calibro", value=watch['mov_ref'])
            m2.number_input("Jewels", value=int(watch['mov_jewels']))
        with tab_perf:
            p1, p2 = st.columns(2)
            p1.number_input("Price (€)", value=int(watch['price_estimate']))
            p2.number_input("Power Reserve (h)", value=int(watch['mov_reserve']))
            
        if st.button("Salva Modifiche", type="primary"):
            st.success("Dati aggiornati (Simulazione)")
            
    else:
        # --- GRIGLIA CARD ---
        st.header(f"Portfolio: {USER_BRAND_NAME}")
        df = db_engine.get_my_watches()
        cols = st.columns(3)
        for i, (idx, row) in enumerate(df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    # Ripristino Immagine Placeholder e Info
                    st.markdown(f"""
                    <div style="height:100px; background-color:#F3F4F6; border-radius:12px; display:flex; justify-content:center; align-items:center; font-size:30px;">⌚</div>
                    <div style="font-weight:700; margin-top:10px;">{row['model_name']}</div>
                    <div style="color:#6B7280; font-size:11px;">Ref: {row['reference']}</div>
                    
                    <div class="info-grid">
                        <div class="info-row"><span class="info-label">Materiale</span><span class="info-value">{row['material']}</span></div>
                        <div class="info-row"><span class="info-label">Diametro</span><span class="info-value">{row['diameter']}mm</span></div>
                        <div class="info-row"><span class="info-label">Spessore</span><span class="info-value">{row['case_thickness']}mm</span></div>
                        <div class="info-row"><span class="info-label">Prezzo</span><span class="info-value">€{row['price_estimate']:,}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Modifica", key=f"btn_{row['reference']}", use_container_width=True):
                        st.session_state.edit_ref = row['reference']
                        st.rerun()
