import streamlit as st
import pandas as pd
import numpy as np
from database_engine import db_engine  # Motore con caching e filtri tipizzati

# 1. CONFIGURAZIONE PAGINA (Deve essere il PRIMO comando Streamlit)
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS DEFINITIVO (Sidebar a sinistra e Tile compatte)
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
        letter-spacing: 1px;
    }
    /* Reset Bottoni Sidebar */
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
    /* Design Tile */
    .watch-tile-box {
        background-color: white; padding: 20px; border-radius: 20px;
        border: 1px solid #F3F4F6; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .img-placeholder {
        height: 120px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center; font-size: 40px;
    }
    .info-grid {
        margin: 15px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px;
    }
    .info-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 3. GESTIONE STATO
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# 4. SIDEBAR CON FILTRI E NAVIGAZIONE
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
if st.sidebar.button("🗺️ Design Intelligence"): st.session_state.nav = "Design"

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">FILTRI DATABASE</div>', unsafe_allow_html=True)
# Filtri che usano i dati tipizzati del motore
selected_brands = st.sidebar.multiselect("Brand", db_engine.df['brand'].unique())
dia_range = st.sidebar.slider("Diametro (mm)", 34, 48, (36, 44))

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">DATASETS</div>', unsafe_allow_html=True)
if st.sidebar.button("🗄️ Watch DB"): st.session_state.nav = "DB"

# Recupero dati filtrati
df_filtered = db_engine.filter_data({
    'brand': selected_brands,
    'diameter': dia_range
})

# 5. LOGICA VISTE
if st.session_state.nav == "My Watches":
    st.header(f"My Watches ({len(df_filtered)} risultati)")
    
    # Pannello di Modifica Inline
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = db_engine.df.loc[idx]
        with st.container(border=True):
            st.subheader(f"📝 Modifica: {item['model_name']}")
            c1, c2 = st.columns(2)
            c1.text_input("Nome Modello", item['model_name'])
            c2.text_input("Referenza", item['reference'])
            if st.button("Salva Modifiche"):
                st.session_state.edit_id = None
                st.rerun()

    # Griglia di Tile
    display_df = df_filtered.head(12)
    cols = st.columns(3)
    
    for i, (idx, row) in enumerate(display_df.iterrows()):
        with cols[i % 3]:
            # Utilizziamo un container con bordo per includere i pulsanti nella tile
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
                
                # Pulsanti d'azione interni al container/tile
                b1, b2 = st.columns(2)
                if b1.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                    st.session_state.edit_id = idx
                    st.rerun()
                if b2.button("Set Target", key=f"tr_{idx}", use_container_width=True):
                    st.toast(f"Target impostato: {row['model_name']}")

elif st.session_state.nav == "DB":
    st.header("Watch Database Explorer")
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

else:
    st.title(st.session_state.nav)
    st.info("Utilizza i filtri nella sidebar per aggiornare i dati.")
