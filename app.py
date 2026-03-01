import streamlit as st
import pandas as pd
import numpy as np
from database_engine import get_watch_dataset

# 1. CONFIGURAZIONE PAGINA E DATI
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# Caricamento dataset dal modulo esterno
df_global = get_watch_dataset()

# 2. CSS AVANZATO (Allineamento a sinistra e Card Design)
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] {
        background-color: #FBFBFE !important;
        border-right: 1px solid #E5E7EB !important;
    }
    
    /* Header Menu Sidebar */
    .sidebar-header {
        font-size: 11px; font-weight: 700; color: #9CA3AF;
        letter-spacing: 1.5px; text-transform: uppercase;
        padding: 30px 25px 15px 25px;
    }

    /* Reset Bottoni Sidebar: Allineamento a sinistra forzato */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; border: none !important;
        background-color: transparent !important; text-align: left !important;
        padding: 12px 25px !important; display: flex !important;
        align-items: center !important; justify-content: flex-start !important; gap: 15px !important;
        color: #1F2937 !important; font-size: 15px !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #F3F4F6 !important; color: #2E5BFF !important;
    }

    /* Stile Card Professional */
    .watch-card {
        background-color: #FFFFFF; padding: 24px; border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6; margin-bottom: 10px;
    }
    
    .card-image-placeholder {
        height: 140px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center;
        font-size: 45px; margin-bottom: 15px;
    }

    .watch-details-box {
        margin: 15px 0; padding: 12px;
        background-color: #F9FAFB; border-radius: 10px;
    }

    .detail-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; }
    .detail-label { color: #6B7280; font-weight: 500; }
    .detail-value { color: #111827; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 3. NAVIGAZIONE SIDEBAR (Stile icone a sinistra)
if 'page' not in st.session_state:
    st.session_state.page = "Watch42 Home (UI)"

st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)

if st.sidebar.button("⌚ My Watches"):
    st.session_state.page = "Watch42 Home (UI)"
if st.sidebar.button("📊 Pricing Intelligence"):
    st.session_state.page = "Pricing Intelligence"
if st.sidebar.button("🗺️ Design Intelligence"):
    st.session_state.page = "Design Intelligence"
if st.sidebar.button("📈 Market Intelligence"):
    st.session_state.page = "Market Intelligence"

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-header">DATASETS</div>', unsafe_allow_html=True)
if st.sidebar.button("🗄️ Watch DB"):
    st.session_state.page = "Watch DB"

current_page = st.session_state.page

# 4. ROUTING LOGIC
if current_page == "Watch42 Home (UI)":
    st.header("My Watches")
    # Prendiamo i primi 6 record per la visualizzazione grafica
    display_df = df_global.head(6)
    
    cols = st.columns(3)
    for i, (idx, row) in enumerate(display_df.iterrows()):
        with cols[i % 3]:
            # Rendering HTML Card
            card_html = f"""
            <div class="watch-card">
                <div class="card-image-placeholder">⌚</div>
                <div style="font-size: 18px; font-weight: 700; color: #111827;">{row.get('model_name', 'Watch Model')}</div>
                <div style="color: #6B7280; font-size: 12px; margin-bottom: 10px;">Ref: {row.get('reference', 'N/A')}</div>
                
                <div class="watch-details-box">
                    <div class="detail-row"><span class="detail-label">Material</span><span class="detail-value">{row.get('case_material', 'N/A')}</span></div>
                    <div class="detail-row"><span class="detail-label">Diameter</span><span class="detail-value">{row.get('diameter', 'N/A')}</span></div>
                    <div class="detail-row"><span class="detail-label">Movement</span><span class="detail-value">{row.get('watch_style', 'N/A')}</span></div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div style="font-size: 22px; font-weight: 700; color: #2E5BFF;">€ {row.get('price', '0')}</div>
                    <div style="font-size: 12px; color: #059669; font-weight: 600;">● Up to date</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            st.button("Set as Target", key=f"target_{idx}")

elif current_page == "Watch DB":
    st.title("⌚ Watch Database Explorer")
    st.write(f"Record totali: {len(df_global)}")
    st.dataframe(df_global, use_container_width=True, hide_index=True)

else:
    st.title(current_page)
    st.info("Sezione in fase di caricamento dati...")
