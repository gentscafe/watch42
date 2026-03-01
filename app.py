import streamlit as st
import pandas as pd
import numpy as np
from database_engine import db_engine

# 1. CONFIGURAZIONE PAGINA (Deve essere SEMPRE il primo comando)
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS DEFINITIVO PER SIDEBAR E TILE
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
    .info-grid {
        margin: 15px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px;
    }
    .info-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    .img-box {
        height: 120px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center; font-size: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. GESTIONE STATO
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# 4. SIDEBAR COMPLETA
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
if st.sidebar.button("🗺️ Design Intelligence"): st.session_state.nav = "Design"

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">FILTRI DATABASE</div>', unsafe_allow_html=True)

# Pulizia sicura del diametro per lo slider (evita il ValueError)
# Convertiamo in stringa, togliamo 'mm' e poi in numerico
clean_dia = pd.to_numeric(db_engine.df['diameter'].astype(str).str.replace('mm', '', case=False), errors='coerce').fillna(0)
dia_min = int(clean_dia.min())
dia_max = int(clean_dia.max())

selected_brands = st.sidebar.multiselect("Seleziona Brand", sorted(db_engine.df['brand'].unique()))
dia_range = st.sidebar.slider("Diametro (mm)", dia_min, dia_max, (dia_min, dia_max))

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">DATASETS</div>', unsafe_allow_html=True)
if st.sidebar.button("🗄️ Watch DB"): st.session_state.nav = "DB"

# Recupero dati filtrati
df_to_show = db_engine.filter_data({
    'brand': selected_brands,
    'diameter': dia_range
})

# 5. LOGICA VISTE
if st.session_state.nav == "My Watches":
    st.header(f"My Watches ({len(df_to_show)} orologi)")
    
    # Pannello di Modifica
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = db_engine.df.loc[idx]
        with st.container(border=True):
            st.subheader(f"📝 Modifica: {item['model_name']}")
            st.text_input("Modello", item['model_name'])
            if st.button("Salva Modifiche"):
                st.session_state.edit_id = None
                st.rerun()

    # Griglia dinamica
    display_items = df_to_show.head(12)
    cols = st.columns(3)
    
    for i, (idx, row) in enumerate(display_items.iterrows()):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"""
                <div class="img-box">⌚</div>
                <div style="font-weight:700; font-size:17px; margin-top:15px; color:#111827;">{row['model_name']}</div>
                <div style="color:#6B7280; font-size:12px; margin-bottom:10px;">Ref: {row['reference']}</div>
                <div class="info-grid">
                    <div class="info-row"><span class="info-label">Brand</span><span class="info-value">{row['brand']}</span></div>
                    <div class="info-row"><span class="info-label">Material</span><span class="info-value">{row['case_material']}</span></div>
                    <div class="info-row"><span class="info-label">Diameter</span><span class="info-value">{row['diameter']}</span></div>
                    <div class="info-row"><span class="info-label">Style</span><span class="info-value">{row['watch_style']}</span></div>
                </div>
                """, unsafe_allow_html=True)
                
                b1, b2 = st.columns(2)
                if b1.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                    st.session_state.edit_id = idx
                    st.rerun()
                b2.button("Set Target", key=f"tr_{idx}", use_container_width=True)

elif st.session_state.nav == "DB":
    st.header("Watch Database Explorer")
    st.dataframe(df_to_show, use_container_width=True, hide_index=True)

else:
    st.title(st.session_state.nav)
    st.info("Utilizza i filtri nella sidebar per aggiornare le analisi.")
