import streamlit as st
import pandas as pd
import numpy as np
from database_engine import get_watch_dataset

# 1. CONFIGURAZIONE LAYOUT
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# Caricamento Dati Reali
df_global = get_watch_dataset()

# 2. CSS "HARD-CODED" DEFINITIVO
# Risolve l'allineamento a sinistra e il rendering delle card
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
    /* TILE DESIGN */
    .watch-tile {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #F3F4F6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        min-height: 450px;
    }
    .img-box {
        height: 120px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center; font-size: 40px;
    }
    .info-table {
        margin: 15px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px;
    }
    .row-info { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .row-info span { color: #6B7280; font-weight: 500; }
    .row-info b { color: #111827; font-weight: 600; }
    
    /* SIDEBAR FIX: Forza allineamento a sinistra */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; text-align: left !important;
        justify-content: flex-start !important; border: none !important;
        background: transparent !important; padding: 10px 20px !important;
        display: flex !important; align-items: center !important; gap: 10px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover { background: #F3F4F6 !important; color: #2E5BFF !important; }
    </style>
""", unsafe_allow_html=True)

# 3. STATO DELLA SESSIONE
if 'nav' not in st.session_state:
    st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None

# 4. SIDEBAR PROFESSIONALE
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">DATASETS</div>', unsafe_allow_html=True)
if st.sidebar.button("🗄️ Watch DB"): st.session_state.nav = "DB"

# 5. LOGICA DELLE PAGINE
if st.session_state.nav == "My Watches":
    st.header("My Watches")
    
    # Pannello di Modifica Dinamico
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = df_global.loc[idx]
        with st.container(border=True):
            st.subheader(f"Modifica: {item['model_name']}")
            c1, c2, c3 = st.columns(3)
            # Nota: usiamo i nomi colonne corretti dal DB
            new_model = c1.text_input("Modello", item['model_name'])
            new_mat = c2.text_input("Materiale", item['case_material'])
            new_dia = c3.text_input("Diametro", item['diameter'])
            
            save_col, cancel_col = st.columns([1, 8])
            if save_col.button("Salva", type="primary"):
                st.session_state.edit_id = None
                st.success("Modifiche simulate salvate!")
                st.rerun()
            if cancel_col.button("Annulla"):
                st.session_state.edit_id = None
                st.rerun()

    # GRIGLIA 3 COLONNE CON DATI REALI
    # Filtriamo i dati per assicurarci che non ci siano errori di visualizzazione
    display_items = df_global.head(6)
    cols = st.columns(3)
    
    for i, (idx, row) in enumerate(display_items.iterrows()):
        with cols[i % 3]:
            # Tile HTML con i nomi colonne corretti (verificati nel DB explorer)
            # Usiamo 'diameter' e 'case_material' come visto nel tuo database
            st.markdown(f"""
            <div class="watch-tile">
                <div class="img-box">⌚</div>
                <div style="font-weight:700; font-size:18px; margin-top:15px; color:#111827;">{row['model_name']}</div>
                <div style="color:#6B7280; font-size:12px; margin-bottom:10px;">Ref: {row['reference']}</div>
                <div class="info-table">
                    <div class="row-info"><span>Brand</span><b>{row['brand']}</b></div>
                    <div class="row-info"><span>Material</span><b>{row['case_material']}</b></div>
                    <div class="row-info"><span>Diameter</span><b>{row['diameter']}</b></div>
                    <div class="row-info"><span>Style</span><b>{row['watch_style']}</b></div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <div style="color:#2E5BFF; font-size:22px; font-weight:700;">Valore Stimato</div>
                    <div style="color:#059669; font-size:12px; font-weight:600;">● Up to date</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Bottoni interni al tile (Streamlit nativi)
            b1, b2 = st.columns(2)
            if b1.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                st.session_state.edit_id = idx
                st.rerun()
            if b2.button("Set Target", key=f"tr_{idx}", use_container_width=True):
                st.toast(f"Target impostato su {row['model_name']}")

elif st.session_state.nav == "Pricing":
    st.header("Pricing Intelligence")
    st.info("Analisi basata sull'intero dataset di 5000 record.")
    # Grafico di esempio
    st.scatter_chart(df_global.head(100), x="diameter", y="watch_style", color="brand")

elif st.session_state.nav == "DB":
    st.header("Watch Database Explorer")
    st.write(f"Record totali: {len(df_global)}")
    # Tabella tecnica
    st.dataframe(df_global, use_container_width=True, hide_index=True)
