import streamlit as st
import pandas as pd
import numpy as np
from database_engine import db_engine  # Motore dati con caching e filtri tipizzati

# 1. CONFIGURAZIONE PAGINA (Deve essere il PRIMO comando assoluto)
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS DEFINITIVO (Sidebar a sinistra e Card/Tile compatte)
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] {
        background-color: #FBFBFE !important;
        border-right: 1px solid #E5E7EB !important;
    }
    
    /* Intestazioni Sidebar */
    .sidebar-header {
        font-size: 11px; font-weight: 700; color: #9CA3AF;
        text-transform: uppercase; padding: 25px 20px 10px 20px;
        letter-spacing: 1px;
    }

    /* Reset Bottoni Sidebar (Allineamento a sinistra forzato) */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; border: none !important;
        background-color: transparent !important; text-align: left !important;
        padding: 10px 20px !important; display: flex !important;
        align-items: center !important; justify-content: flex-start !important; gap: 12px !important;
        color: #1F2937 !important; font-size: 14px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #F3F4F6 !important; color: #2E5BFF !important;
    }

    /* Design Tile/Card */
    .info-grid {
        margin: 15px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px;
    }
    .info-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    
    .img-placeholder {
        height: 120px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center; font-size: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. GESTIONE STATO SESSIONE
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# 4. SIDEBAR CON NAVIGAZIONE E FILTRI TECNICI
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">FILTRI DATABASE</div>', unsafe_allow_html=True)

# Filtri dinamici che usano il motore db_engine
all_brands = sorted(db_engine.df['brand'].unique())
selected_brands = st.sidebar.multiselect("Seleziona Brand", all_brands)

# Slider numerico (grazie ai dati tipizzati int)
dia_min = int(db_engine.df['diameter'].min())
dia_max = int(db_engine.df['diameter'].max())
dia_range = st.sidebar.slider("Range Diametro (mm)", dia_min, dia_max, (38, 42))

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">DATASETS</div>', unsafe_allow_html=True)
if st.sidebar.button("🗄️ Watch DB Explorer"): st.session_state.nav = "DB"

# Recupero dati filtrati dal motore
df_to_show = db_engine.filter_data({
    'brand': selected_brands,
    'diameter': dia_range
})

# 5. LOGICA DELLE VISTE
if st.session_state.nav == "My Watches":
    st.header(f"My Watches ({len(df_to_show)} orologi)")
    
    # Pannello di Modifica (Compare solo se un ID è selezionato)
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = db_engine.df.loc[idx]
        with st.container(border=True):
            st.subheader(f"📝 Modifica: {item['model_name']}")
            new_name = st.text_input("Nome Modello", item['model_name'])
            if st.button("Salva"):
                st.session_state.edit_id = None
                st.success("Modifica simulata salvata!")
                st.rerun()
        st.markdown("---")

    # Griglia a 3 colonne
    display_items = df_to_show.head(12)
    cols = st.columns(3)
    
    for i, (idx, row) in enumerate(display_items.iterrows()):
        with cols[i % 3]:
            # Container con bordo per raggruppare visivamente card e bottoni
            with st.container(border=True):
                st.markdown(f"""
                <div class="img-placeholder">⌚</div>
                <div style="font-weight:700; font-size:17px; margin-top:15px; color:#111827;">{row['model_name']}</div>
                <div style="color:#6B7280; font-size:12px; margin-bottom:10px;">Ref: {row['reference']}</div>
                <div class="info-grid">
                    <div class="info-row"><span class="info-label">Brand</span><span class="info-value">{row['brand']}</span></div>
                    <div class="info-row"><span class="info-label">Material</span><span class="info-value">{row['case_material']}</span></div>
                    <div class="info-row"><span class="info-label">Diameter</span><span class="info-value">{row['diameter']}mm</span></div>
                    <div class="info-row"><span class="info-label">Style</span><span class="info-value">{row['watch_style']}</span></div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <div style="color:#2E5BFF; font-size:20px; font-weight:700;">Valore Stimato</div>
                    <div style="color:#059669; font-size:11px; font-weight:600;">● Online</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Pulsanti interni alla tile
                btn_col1, btn_col2 = st.columns(2)
                if btn_col1.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                    st.session_state.edit_id = idx
                    st.rerun()
                if btn_col2.button("Set Target", key=f"tr_{idx}", use_container_width=True):
                    st.toast(f"Target impostato: {row['model_name']}")

elif st.session_state.nav == "DB":
    st.header("Watch Database Explorer")
    st.dataframe(df_to_show, use_container_width=True, hide_index=True)

else:
    st.title(st.session_state.nav)
    st.info("Utilizza i filtri nella sidebar per aggiornare le analisi.")
