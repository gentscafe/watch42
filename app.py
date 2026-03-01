import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from database_engine import get_watch_dataset # Importa la logica del DB

# 1. CONFIGURAZIONE PAGINA E CARICAMENTO DATI
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")
df_global = get_watch_dataset() # Carica i 5000 record

# 2. INJECT ADVANCED CSS (Ripristino Sidebar originale e Card)
def inject_custom_css():
    st.markdown("""
        <style>
        .main { background-color: #F8F9FC; }
        [data-testid="stSidebar"] {
            background-color: #FBFBFE !important;
            border-right: 1px solid #E5E7EB !important;
        }
        
        /* Intestazione MENU in maiuscolo */
        .sidebar-header {
            font-size: 11px;
            font-weight: 700;
            color: #9CA3AF;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 30px 25px 15px 25px;
        }

        /* Navigazione: Allineamento a sinistra e icone */
        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            border: none !important;
            background-color: transparent !important;
            text-align: left !important;
            padding: 12px 25px !important;
            border-radius: 0px !important;
            color: #1F2937 !important;
            font-size: 15px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 15px !important;
            transition: all 0.2s ease;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #F3F4F6 !important;
            color: #2E5BFF !important;
        }

        /* Stile Card My Watches */
        .watch-card {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            border: 1px solid #F3F4F6;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 3. LOGICA DI NAVIGAZIONE (SIDEBAR RIPRISTINATA)
st.sidebar.markdown('<div class="sidebar-header">MENU</div>', unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Watch42 Home (UI)"

# Pulsanti di navigazione con icone
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
if st.sidebar.button("🗄️ Watch DB"): # Nuova sezione richiesta
    st.session_state.page = "Watch DB"

page = st.session_state.page

# 4. ROUTING DELLE PAGINE
if page == "Watch42 Home (UI)":
    st.header("My Watches")
    # Visualizziamo i primi 6 record con le card grafiche
    display_df = df_global.head(6)
    cols = st.columns(3)
    for i, (idx, row) in enumerate(display_df.iterrows()):
        with cols[i % 3]:
            card_html = f"""
            <div class="watch-card">
                <div style="height: 140px; background-color: #F3F4F6; border-radius: 15px; display: flex; justify-content: center; align-items: center; font-size: 45px; margin-bottom: 15px;">⌚</div>
                <div style="font-size: 17px; font-weight: 700;">{row.get('model_name', 'N/A')}</div>
                <div style="color: #6B7280; font-size: 12px; margin-bottom: 10px;">Ref: {row.get('reference', 'N/A')}</div>
                <div style="font-size: 20px; font-weight: 700; color: #2E5BFF;">€ {row.get('price', '0')}</div>
                <div style="font-size: 12px; color: #059669; font-weight: 600; margin-top: 5px;">● Up to date</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            st.button("Set as Target", key=f"target_{idx}")

elif page == "Watch DB":
    st.title("⌚ Watch Database Explorer")
    st.write(f"Record totali disponibili: {len(df_global)}") #
    
    # Tabella tecnica interattiva
    st.dataframe(df_global, use_container_width=True, hide_index=True)

elif page == "Pricing Intelligence":
    st.header("Pricing Intelligence")
    fig = px.scatter(df_global.head(100), x='price', y='diameter', color='brand')
    st.plotly_chart(fig, use_container_width=True)

# Altre pagine (Design/Market) seguono lo stesso pattern
