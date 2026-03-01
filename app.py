import streamlit as st
import pandas as pd
import plotly.express as px
from database_engine import db_engine, USER_BRAND_NAME

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS PROFESSIONALE
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] { background-color: #FBFBFE !important; border-right: 1px solid #E5E7EB !important; }
    .sidebar-header { font-size: 11px; font-weight: 700; color: #9CA3AF; text-transform: uppercase; padding: 25px 20px 10px 20px; }
    .info-grid { margin: 10px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px; border: 1px solid #F3F4F6; }
    .info-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    .control-panel { background-color: #FFFFFF; padding: 20px; border-radius: 15px; border: 1px solid #E5E7EB; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. GESTIONE STATO
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

# 4. SIDEBAR PERMANENTE
st.sidebar.markdown(f'<div style="padding: 20px; color: #2E5BFF; font-weight: 800; font-size: 24px;">{USER_BRAND_NAME}</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)

if st.sidebar.button("⌚ My Watches", use_container_width=True):
    st.session_state.nav = "My Watches"
    st.session_state.edit_ref = None
    st.rerun()

if st.sidebar.button("📊 Pricing Intelligence", use_container_width=True):
    st.session_state.nav = "Pricing"
    st.session_state.edit_ref = None
    st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🗄️ Watch DB Explorer", use_container_width=True):
    st.session_state.nav = "DB"
    st.rerun()

# --- LOGICA VISTA: MY WATCHES ---
if st.session_state.nav == "My Watches":
    # (Logica identica alla precedente per le card e la modifica)
    st.header(f"Portfolio: {USER_BRAND_NAME}")
    my_df = db_engine.get_my_watches()
    
    if st.session_state.edit_ref:
        # Codice pannello modifica (Estetica/Meccanica/Mercato)
        watch = db_engine.df[db_engine.df['reference'] == st.session_state.edit_ref].iloc[0]
        if st.button("← Torna alla lista"):
            st.session_state.edit_ref = None
            st.rerun()
        st.write(f"Editing {watch['reference']}...")
        # ... (Pannello Tab esistente) ...
    else:
        cols = st.columns(3)
        for i, (idx, row) in enumerate(my_df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{row['model_name']}**<br><small>{row['reference']}</small>", unsafe_allow_html=True)
                    if st.button("Modifica", key=f"ed_{row['reference']}", use_container_width=True):
                        st.session_state.edit_ref = row['reference']
                        st.rerun()

# --- LOGICA VISTA: PRICING INTELLIGENCE ---
elif st.session_state.nav == "Pricing":
    st.header("📊 Pricing Intelligence Matrix")
    
    # Pannello di Controllo Sopra al Grafico
    with st.container():
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        
        # Mapping preciso con le colonne del database_engine
        y_options = {
            "mov_reserve": "Riserva di Carica (h)", 
            "case_thickness": "Spessore Cassa (mm)", 
            "mov_freq": "Frequenza (vph)",
            "power_score": "Power Score (Indice Tec.)"
        }
        
        y_choice = c1.selectbox("Seleziona parametro tecnico (Asse Y)", 
                                options=list(y_options.keys()), 
                                format_func=lambda x: y_options[x])
        
        my_watches = db_engine.get_my_watches()
        target_ref = c2.selectbox("Seleziona il tuo orologio di riferimento (Target)", 
                                  options=my_watches['reference'].tolist())
        st.markdown('</div>', unsafe_allow_html=True)

    # Preparazione dati
    plot_df = db_engine.df.copy()
    
    # Pulizia nomi per hover
    plot_df['Status'] = 'Competitor'
    plot_df.loc[plot_df['brand'] == USER_BRAND_NAME, 'Status'] = 'I Tuoi Prodotti'
    plot_df.loc[plot_df['reference'] == target_ref, 'Status'] = 'TARGET SELEZIONATO'

    # Creazione Scatter Plot
    fig = px.scatter(
        plot_df, 
        x="price_estimate", 
        y=y_choice, 
        color="Status",
        hover_name="brand", 
        hover_data={"model_name": True, "price_estimate": ":.2f", "reference": True, "Status": False},
        color_discrete_map={
            'Competitor': '#E5E7EB', 
            'I Tuoi Prodotti': '#2E5BFF', 
            'TARGET SELEZIONATO': '#FF4B4B'
        },
        labels={
            "price_estimate": "Prezzo (€)", 
            y_choice: y_options[y_choice]
        },
        height=650, 
        template="plotly_white"
    )

    # Stile dei punti
    fig.update_traces(marker=dict(size=12, opacity=0.6, line=dict(width=1, color='White')))
    
    # Evidenzia il Target con una stella grande
    fig.update_traces(
        marker=dict(size=25, symbol="star", opacity=1), 
        selector=dict(name='TARGET SELEZIONATO')
    )

    # Layout grafico
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

# --- LOGICA VISTA: DB EXPLORER ---
elif st.session_state.nav == "DB":
    st.header("🗄️ Watch Database Explorer")
    st.dataframe(db_engine.df, use_container_width=True)
