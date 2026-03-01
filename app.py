import streamlit as st
import pandas as pd
import numpy as np
from database_engine import db_engine

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. PULIZIA DATI (Diameter fix per st.slider)
db_engine.df['diameter_clean'] = pd.to_numeric(
    db_engine.df['diameter'].astype(str).str.extract(r'(\d+)')[0], 
    errors='coerce'
).fillna(40).astype(int)

# 3. CSS PROFESSIONALE
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
    </style>
""", unsafe_allow_html=True)

# 4. STATO NAVIGAZIONE
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# 5. SIDEBAR (Voci ripristinate)
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
if st.sidebar.button("⌚ My Watches"): st.session_state.nav = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
if st.sidebar.button("🗺️ Design Intelligence"): st.session_state.nav = "Design"
if st.sidebar.button("📈 Market Intelligence"): st.session_state.nav = "Market"
st.sidebar.markdown("---")
if st.sidebar.button("🗄️ Watch DB Explorer"): st.session_state.nav = "DB"

# 6. LOGICA VISTE
nav = st.session_state.nav

if nav == "My Watches":
    st.header("My Watches")
    
    # PANNELLO DI MODIFICA AVANZATO (Widget richiesti)
    if st.session_state.edit_id is not None:
        idx = st.session_state.edit_id
        item = db_engine.df.loc[idx]
        
        with st.container(border=True):
            st.subheader(f"📝 Editing: {item['model_name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                new_brand = st.selectbox("Brand", db_engine.df['brand'].unique(), 
                                        index=list(db_engine.df['brand'].unique()).index(item['brand']))
                new_model = st.text_input("Model Name", item['model_name'])
                new_ref = st.text_input("Reference", item['reference'])
                new_style = st.radio("Watch Style", ["Diver", "GMT", "Dress", "Casual", "Chronograph"], 
                                    horizontal=True)
            
            with col2:
                new_mat = st.multiselect("Material", ["Steel", "Titanium", "Gold", "Ceramic", "Bronze"], 
                                         default=[item['case_material']] if item['case_material'] in ["Steel", "Titanium", "Gold", "Ceramic", "Bronze"] else [])
                new_dia = st.slider("Diameter (mm)", 34, 48, int(item['diameter_clean']), step=1)
                new_comp = st.multiselect("Complications", ["Tourbillon", "Moonphase", "GMT", "Date"], default=[])
                new_price = st.number_input("Price Estimate (€)", value=15000, step=500)
            
            c1, c2 = st.columns([1, 6])
            if c1.button("Save Changes", type="primary"):
                st.session_state.edit_id = None
                st.success(f"Dati di {new_model} aggiornati nel database!")
                st.rerun()
            if c2.button("Cancel"):
                st.session_state.edit_id = None
                st.rerun()
        st.markdown("---")

    # GRIGLIA CARD
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

# [Le altre sezioni Pricing, Design, Market rimangono invariate]
