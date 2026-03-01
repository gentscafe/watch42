import streamlit as st
import pandas as pd
import numpy as np
from database_engine import get_watch_dataset #

# 1. CONFIGURAZIONE PAGINA E CARICAMENTO DATI
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# Caricamento del dataset globale dal nuovo motore
df_global = get_watch_dataset() 

# 2. INJECT CSS (Manteniamo la UI professionale)
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] {
        background-color: #FBFBFE !important;
        border-right: 1px solid #E5E7EB !important;
    }
    .sidebar-header {
        font-size: 11px; font-weight: 700; color: #9CA3AF;
        letter-spacing: 1.5px; text-transform: uppercase;
        padding: 30px 25px 15px 25px;
    }
    .watch-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6; margin-bottom: 10px;
    }
    .card-image-placeholder {
        height: 140px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center;
        font-size: 45px; margin-bottom: 15px;
    }
    .watch-details {
        margin: 15px 0; padding: 12px;
        background-color: #F9FAFB; border-radius: 10px;
    }
    .detail-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; }
    .detail-label { color: #6B7280; font-weight: 500; }
    .detail-value { color: #111827; font-weight: 600; }
    
    /* Allineamento pulsanti sidebar */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; border: none !important;
        background-color: transparent !important; text-align: left !important;
        padding: 12px 25px !important; display: flex !important;
        align-items: center !important; justify-content: flex-start !important; gap: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CONFIGURAZIONE NAVIGAZIONE (SIDEBAR)
with st.sidebar:
    st.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)
    page = st.radio("Seleziona vista:", ["Watch42 Home (UI)", "Watch DB"], label_visibility="collapsed") #

# 4. LOGICA DI VISUALIZZAZIONE (ROUTING)

if page == "Watch42 Home (UI)": #
    st.title("Watch42 Discovery") #
    
    # Sottosezioni della UI Designer
    menu = st.sidebar.selectbox("Intelligence Mode", ["My Watches", "Pricing", "Design", "Market"])
    
    if menu == "My Watches":
        # Usiamo i primi 6 record del nuovo DB per popolare le card grafiche
        display_df = df_global.head(6) 
        cols = st.columns(3)
        
        for i, (idx, row) in enumerate(display_df.iterrows()):
            with cols[i % 3]:
                card_html = f"""
                <div class="watch-card">
                    <div class="card-image-placeholder">⌚</div>
                    <div style="font-size: 17px; font-weight: 700; color: #111827;">{row.get('Model', 'N/A')}</div>
                    <div style="color: #6B7280; font-size: 12px; margin-bottom: 10px;">Ref: {row.get('Reference', 'N/A')}</div>
                    <div class="watch-details">
                        <div class="detail-row"><span class="detail-label">Brand</span><span class="detail-value">{row.get('Brand', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">Material</span><span class="detail-value">{row.get('Material', 'N/A')}</span></div>
                        <div class="detail-row"><span class="detail-label">Diameter</span><span class="detail-value">{row.get('Diameter', 'N/A')}</span></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                        <div style="font-size: 20px; font-weight: 700; color: #2E5BFF;">€ {row.get('Price', '0')}</div>
                        <div style="font-size: 12px; color: #059669; font-weight: 600;">● Up to date</div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                st.button("Set as Target", key=f"target_{idx}", use_container_width=True)

    # (Qui andrebbero le logiche Pricing, Design e Market Intelligence simili a prima)

elif page == "Watch DB": #
    # AREA DATABASE: Schermata tecnica dedicata
    st.title("⌚ Watch Database Explorer") #
    st.write(f"Record totali: {len(df_global)}") #
    
    # Barra di ricerca rapida per il database tecnico
    search_query = st.text_input("Filtra database (Brand o Modello):", "")
    
    if search_query:
        filtered_df = df_global[df_global.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
    else:
        filtered_df = df_global

    # Tabella interattiva nativa per gestire grandi volumi
    st.dataframe(
        filtered_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Price": st.column_config.NumberColumn(format="€ %d")
        }
    ) #
