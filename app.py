import streamlit as st
import pandas as pd
import plotly.express as px
from database_engine import db_engine, USER_BRAND_NAME

st.set_page_config(page_title="watch42", layout="wide")

if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

# --- SIDEBAR ---
st.sidebar.title(f"Admin: {USER_BRAND_NAME}")
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
        st.header(f"Modifica: {watch['reference']}")
        if st.button("← Torna alla lista"):
            st.session_state.edit_ref = None
            st.rerun()
        
        new_name = st.text_input("Modello", value=watch['model_name'])
        new_price = st.number_input("Prezzo (€)", value=int(watch['price_estimate']))
            
        if st.button("Salva"):
            db_engine.update_watch_data(st.session_state.edit_ref, {"model_name": new_name, "price_estimate": new_price})
            st.success("Salvato!")
            st.session_state.edit_ref = None
            st.rerun()
    else:
        st.header(f"Portfolio: {USER_BRAND_NAME}")
        my_df = db_engine.get_my_watches()
        cols = st.columns(3)
        for i, (idx, row) in enumerate(my_df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.write(f"### {row['model_name']}")
                    st.write(f"Ref: {row['reference']} | {row['material']}")
                    st.write(f"**Prezzo: €{row['price_estimate']:,}**")
                    if st.button("Modifica", key=f"ed_{row['reference']}", use_container_width=True):
                        st.session_state.edit_ref = row['reference']
                        st.rerun()

# --- VISTA: PRICING INTELLIGENCE ---
elif st.session_state.nav == "Pricing":
    st.header("📊 Pricing Intelligence Matrix")
    
    # Selettori orizzontali
    c1, c2 = st.columns(2)
    y_map = {
        "mov_reserve": "Riserva di Carica (h)", 
        "case_thickness": "Spessore (mm)", 
        "power_score": "Power Score"
    }
    y_choice = c1.selectbox("Seleziona parametro tecnico (Asse Y)", options=list(y_map.keys()), format_func=lambda x: y_map[x])
    
    my_df = db_engine.get_my_watches()
    target_ref = c2.selectbox("Seleziona il tuo orologio Target", options=my_df['reference'].tolist())

    # Preparazione Dati
    df_plot = db_engine.df.copy()
    
    # Debug rapido (Puoi rimuovere questa riga dopo il test)
    # st.write(f"Record totali: {len(df_plot)} | Valori asse Y medi: {df_plot[y_choice].mean()}")

    df_plot['Status'] = 'Competitor'
    df_plot.loc[df_plot['brand'] == USER_BRAND_NAME, 'Status'] = 'Il Tuo Brand'
    df_plot.loc[df_plot['reference'] == target_ref, 'Status'] = 'TARGET'

    # Creazione Grafico
    fig = px.scatter(
        df_plot,
        x="price_estimate",
        y=y_choice,
        color="Status",
        hover_name="brand",
        hover_data=["model_name", "reference"],
        color_discrete_map={'Competitor': '#D1D5DB', 'Il Tuo Brand': '#2E5BFF', 'TARGET': '#EF4444'},
        labels={"price_estimate": "Prezzo (€)", y_choice: y_map[y_choice]},
        height=600,
        template="plotly_white"
    )
    
    fig.update_traces(marker=dict(size=12, opacity=0.7))
    fig.update_traces(marker=dict(size=25, symbol="star", opacity=1), selector=dict(name='TARGET'))
    
    st.plotly_chart(fig, use_container_width=True)
