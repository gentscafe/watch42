import streamlit as st
import pandas as pd
import plotly.express as px
from database_engine import db_engine, USER_BRAND_NAME

st.set_page_config(page_title="watch42", layout="wide")

# Navigazione
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

# Sidebar
st.sidebar.title(f"CEO Panel: {USER_BRAND_NAME}")
if st.sidebar.button("⌚ My Watches", use_container_width=True):
    st.session_state.nav = "My Watches"
    st.session_state.edit_ref = None
    st.rerun()
if st.sidebar.button("📊 Pricing Intelligence", use_container_width=True):
    st.session_state.nav = "Pricing"
    st.rerun()

# --- VISTA: MY WATCHES ---
if st.session_state.nav == "My Watches":
    if st.session_state.edit_ref:
        watch = db_engine.df[db_engine.df['reference'] == st.session_state.edit_ref].iloc[0]
        st.header(f"Editing: {watch['reference']}")
        if st.button("← Back"):
            st.session_state.edit_ref = None
            st.rerun()
        # Pannello semplificato per test
        new_price = st.number_input("Prezzo (€)", value=int(watch['price_estimate']))
        if st.button("Salva"):
            db_engine.update_watch_data(st.session_state.edit_ref, {"price_estimate": new_price})
            st.success("Dato Salvato!")
            st.session_state.edit_ref = None
            st.rerun()
    else:
        st.header(f"I Tuoi Orologi ({USER_BRAND_NAME})")
        df_my = db_engine.get_my_watches()
        cols = st.columns(3)
        for i, (idx, row) in enumerate(df_my.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(row['model_name'])
                    st.write(f"Prezzo: €{row['price_estimate']:,}")
                    if st.button("Modifica", key=f"btn_{row['reference']}"):
                        st.session_state.edit_ref = row['reference']
                        st.rerun()

# --- VISTA: PRICING INTELLIGENCE ---
elif st.session_state.nav == "Pricing":
    st.header("📊 Analisi Competitiva di Mercato")
    
    # Selettori in alto
    c1, c2 = st.columns(2)
    y_map = {"mov_reserve": "Riserva di Carica", "case_thickness": "Spessore", "power_score": "Power Score"}
    y_choice = c1.selectbox("Seleziona parametro Asse Y", options=list(y_map.keys()), format_func=lambda x: y_map[x])
    
    my_df = db_engine.get_my_watches()
    target_ref = c2.selectbox("Seleziona il Tuo Target", options=my_df['reference'].tolist())

    # Generazione Grafico
    df_plot = db_engine.df.copy()
    df_plot['Status'] = 'Competitor'
    df_plot.loc[df_plot['brand'] == USER_BRAND_NAME, 'Status'] = 'I Tuoi Brand'
    df_plot.loc[df_plot['reference'] == target_ref, 'Status'] = 'TARGET'

    

    fig = px.scatter(
        df_plot,
        x="price_estimate",
        y=y_choice,
        color="Status",
        hover_name="brand",
        color_discrete_map={'Competitor': '#D1D5DB', 'I Tuoi Brand': '#2E5BFF', 'TARGET': '#EF4444'},
        labels={"price_estimate": "Prezzo (€)", y_choice: y_map[y_choice]},
        height=600,
        template="plotly_white"
    )
    
    fig.update_traces(marker=dict(size=10, opacity=0.6))
    fig.update_traces(marker=dict(size=20, symbol="star", opacity=1), selector=dict(name='TARGET'))
    
    st.plotly_chart(fig, use_container_width=True)
