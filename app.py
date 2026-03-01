import streamlit as st
import pandas as pd
import numpy as np
from database_engine import db_engine

# 1. CONFIGURAZIONE PAGINA (Deve essere la prima riga assoluta)
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. PULIZIA DATI (Risolve il TypeError dello slider e il ValueError)
# Trasformiamo diameter in numero puro (es: "40mm" -> 40)
db_engine.df['diameter_clean'] = pd.to_numeric(
    db_engine.df['diameter'].astype(str).str.extract(r'(\d+)')[0], 
    errors='coerce'
).fillna(40).astype(int)

# 3. CSS PROFESSIONALE (Sidebar e Tile UI)
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
    </style>
""", unsafe_allow_html=True)

# 4. STATO DELLA NAVIGAZIONE
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# 5. SIDEBAR RIPRISTINATA (Senza filtri, con tutte le voci)
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
if st.sidebar.button("🗺️ Design Intelligence"): st.session_state.nav = "Design"
if st.sidebar.button("📈 Market Intelligence"): st.session_state.nav = "Market"

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">DATASETS</div>', unsafe_allow_html=True)
if st.sidebar.button("🗄️ Watch DB Explorer"): st.session_state.nav = "DB"

# 6. LOGICA DELLE VISTE
nav = st.session_state.nav

if nav == "My Watches":
    st.header(f"My Watches (5000 orologi)")
    
    # Pannello di Modifica
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = db_engine.df.loc[idx]
        with st.container(border=True):
            st.subheader(f"📝 Modifica: {item['model_name']}")
            st.text_input("Nome Modello", item['model_name'])
            if st.button("Salva"):
                st.session_state.edit_id = None
                st.rerun()

    # Griglia a 3 colonne
    display_df = db_engine.df.head(12)
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
                    <div class="info-row"><span class="info-label">Style</span><span class="info-value">{row['watch_style']}</span></div>
                </div>
                """, unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                if b1.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                    st.session_state.edit_id = idx
                    st.rerun()
                b2.button("Set Target", key=f"tr_{idx}", use_container_width=True)

elif nav == "Pricing":
    st.header("Pricing Intelligence")
    st.scatter_chart(db_engine.df.head(100), x="diameter_clean", y="brand")

elif nav == "Design":
    st.header("Design Intelligence")
    st.info("Visualizzazione degli schemi di design basata sui 5000 record.")
    st.bar_chart(db_engine.df['watch_style'].value_counts())

elif nav == "Market":
    st.header("Market Intelligence")
    st.info("Trend di mercato e analisi competitiva.")
    st.line_chart(np.random.randn(20, 2)) # Placeholder per dati di trend

elif nav == "DB":
    st.header("Watch Database Explorer")
    st.dataframe(db_engine.df, use_container_width=True, hide_index=True)
