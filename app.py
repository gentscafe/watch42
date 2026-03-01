import streamlit as st
import pandas as pd
import numpy as np
from database_engine import get_watch_dataset

# 1. CONFIGURAZIONE PAGINA E DATI
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# Caricamento database (5000 record)
df_global = get_watch_dataset()

# 2. CSS AVANZATO (Allineamento Sidebar e Bottoni nel Tile)
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
        padding: 30px 25px 10px 25px;
    }
    
    /* Design del Tile/Card */
    .watch-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6; margin-bottom: 20px;
    }
    .card-image-placeholder {
        height: 120px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center;
        font-size: 40px; margin-bottom: 15px;
    }
    .watch-details-box {
        margin: 12px 0; padding: 10px;
        background-color: #F9FAFB; border-radius: 10px;
    }
    .detail-row { display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 12px; }
    .detail-label { color: #6B7280; font-weight: 500; }
    .detail-value { color: #111827; font-weight: 600; }

    /* Forzatura allineamento Sidebar a sinistra */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; border: none !important;
        background-color: transparent !important; text-align: left !important;
        padding: 10px 25px !important; display: flex !important;
        align-items: center !important; justify-content: flex-start !important; gap: 12px !important;
        color: #1F2937 !important;
    }
    
    /* Hover e Active Sidebar */
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #F3F4F6 !important;
        color: #2E5BFF !important;
    }

    /* Stile pulsanti interni al tile */
    .stButton > button {
        border-radius: 8px !important;
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. GESTIONE STATO MODIFICA
if 'editing_id' not in st.session_state:
    st.session_state.editing_id = None
if 'page' not in st.session_state:
    st.session_state.page = "My Watches"

# Pannello di modifica inline (per evitare errori di versione st.dialog)
def show_edit_panel(row_data, idx):
    with st.container(border=True):
        st.subheader(f"📝 Modifica: {row_data['model_name']}")
        col1, col2, col3 = st.columns(3)
        new_model = col1.text_input("Modello", row_data['model_name'], key=f"ed_m_{idx}")
        new_price = col2.text_input("Prezzo (€)", str(row_data['price']), key=f"ed_p_{idx}")
        new_mat = col3.text_input("Materiale", row_data['case_material'], key=f"ed_mat_{idx}")
        
        c1, c2 = st.columns([1, 5])
        if c1.button("Salva", key=f"save_{idx}", type="primary"):
            st.toast("Modifiche salvate con successo!")
            st.session_state.editing_id = None
            st.rerun()
        if c2.button("Annulla", key=f"cancel_{idx}"):
            st.session_state.editing_id = None
            st.rerun()

# 4. SIDEBAR NAVIGATION
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)

if st.sidebar.button("⌚ My Watches"):
    st.session_state.page = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"):
    st.session_state.page = "Pricing Intelligence"
if st.sidebar.button("🗄️ Watch DB"):
    st.session_state.page = "Watch DB"

# 5. LOGICA VISTE
if st.session_state.page == "My Watches":
    st.header("My Watches")
    
    # Se un orologio è in fase di modifica, mostra il pannello in alto
    if st.session_state.editing_id is not None:
        target_row = df_global.iloc[st.session_state.editing_id]
        show_edit_panel(target_row, st.session_state.editing_id)

    # Visualizzazione primi record dal DB
    display_df = df_global.head(6)
    cols = st.columns(3)
    
    for i, (idx, row) in enumerate(display_df.iterrows()):
        with cols[i % 3]:
            # Contenitore Tile fisico per raggruppare HTML e Bottoni
            with st.container(border=False):
                # Parte Superiore: Card Grafica (HTML)
                html_card = f"""
                <div class="watch-card">
                    <div class="card-image-placeholder">⌚</div>
                    <div style="font-size: 16px; font-weight: 700; color: #111827;">{row['model_name']}</div>
                    <div style="color: #6B7280; font-size: 11px; margin-bottom: 8px;">Ref: {row['reference']}</div>
                    <div class="watch-details-box">
                        <div class="detail-row"><span class="detail-label">Brand</span><span class="detail-value">{row['brand']}</span></div>
                        <div class="detail-row"><span class="detail-label">Material</span><span class="detail-value">{row['case_material']}</span></div>
                        <div class="detail-row"><span class="detail-label">Diameter</span><span class="detail-value">{row['diameter']}</span></div>
                        <div class="detail-row"><span class="detail-label">Style</span><span class="detail-value">{row['watch_style']}</span></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-size: 18px; font-weight: 700; color: #2E5BFF;">€ {row['price']}</div>
                        <div style="font-size: 11px; color: #059669; font-weight: 600;">● Up to date</div>
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)
                
                # Parte Inferiore: Bottoni nativi (dentro il tile)
                btn_col1, btn_col2 = st.columns(2)
                if btn_col1.button("Modifica", key=f"edit_btn_{idx}", use_container_width=True):
                    st.session_state.editing_id = idx
                    st.rerun()
                if btn_col2.button("Set Target", key=f"target_{idx}", use_container_width=True):
                    st.success(f"Target impostato: {row['model_name']}")

elif st.session_state.page == "Pricing Intelligence":
    st.header("Pricing Intelligence")
    st.info("Analisi dei dati basata sui 5000 record del database.")
    # Esempio di grafico dinamico col DB
    fig = px.scatter(df_global.head(100), x='price', y='diameter', color='brand', title="Posizionamento Prezzo/Diametro")
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == "Watch DB":
    st.title("⌚ Watch Database Explorer")
    st.write(f"Record totali disponibili: {len(df_global)}")
    st.dataframe(df_global, use_container_width=True, hide_index=True)
