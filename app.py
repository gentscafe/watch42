import streamlit as st
import pandas as pd
import plotly.express as px
from database_engine import db_engine, USER_BRAND_NAME

st.set_page_config(page_title="watch42 | CEO Dashboard", layout="wide")

if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

# SIDEBAR
st.sidebar.title(f"Admin: {USER_BRAND_NAME}")
if st.sidebar.button("⌚ My Watches", use_container_width=True):
    st.session_state.nav = "My Watches"
    st.session_state.edit_ref = None
    st.rerun()
if st.sidebar.button("📊 Pricing Intelligence", use_container_width=True):
    st.session_state.nav = "Pricing"
    st.rerun()
if st.sidebar.button("🗄️ Database Explorer", use_container_width=True):
    st.session_state.nav = "Explorer"
    st.rerun()

# --- VISTA: MY WATCHES ---
if st.session_state.nav == "My Watches":
    my_df = db_engine.df[db_engine.df['brand'] == USER_BRAND_NAME]
    
    if st.session_state.edit_ref:
        watch = my_df[my_df['reference'] == st.session_state.edit_ref].iloc[0]
        st.header(f"Modifica: {watch['model_name']}")
        if st.button("← Torna alla lista"):
            st.session_state.edit_ref = None
            st.rerun()
        
        new_price = st.number_input("Prezzo (€)", value=float(watch['price_estimate']))
        if st.button("Salva Modifiche"):
            db_engine.update_watch_data(st.session_state.edit_ref, {"price_estimate": new_price})
            st.success("Salvato!")
            st.session_state.edit_ref = None
            st.rerun()
    else:
        st.header(f"I Tuoi Orologi")
        cols = st.columns(3)
        for i, (idx, row) in enumerate(my_df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(row['model_name'])
                    st.write(f"Ref: {row['reference']} | €{row['price_estimate']:,}")
                    if st.button("Modifica", key=f"btn_{row['reference']}", use_container_width=True):
                        st.session_state.edit_ref = row['reference']
                        st.rerun()

# --- VISTA: PRICING INTELLIGENCE ---
elif st.session_state.nav == "Pricing":
    st.header("📊 Analisi Competitiva")
    
    c1, c2 = st.columns(2)
    y_map = {"mov_reserve": "Riserva di Carica", "case_thickness": "Spessore", "power_score": "Power Score"}
    y_choice = c1.selectbox("Confronta Prezzo vs:", options=list(y_map.keys()), format_func=lambda x: y_map[x])
    
    my_refs = db_engine.df[db_engine.df['brand'] == USER_BRAND_NAME]['reference'].tolist()
    target_ref = c2.selectbox("Seleziona il Tuo Target", options=my_refs)

    df_plot = db_engine.df.copy()
    df_plot['Status'] = 'Competitor'
    df_plot.loc[df_plot['brand'] == USER_BRAND_NAME, 'Status'] = 'Il Tuo Brand'
    df_plot.loc[df_plot['reference'] == target_ref, 'Status'] = 'TARGET'

    # Immagine di riferimento per il posizionamento di prezzo
    

    fig = px.scatter(
        df_plot, x="price_estimate", y=y_choice, color="Status",
        hover_name="brand", hover_data=["model_name", "reference"],
        color_discrete_map={'Competitor': '#D1D5DB', 'Il Tuo Brand': '#2E5BFF', 'TARGET': '#EF4444'},
        labels={"price_estimate": "Prezzo (€)", y_choice: y_map[y_choice]},
        height=600, template="plotly_white"
    )
    fig.update_traces(marker=dict(size=12, opacity=0.7))
    fig.update_traces(marker=dict(size=25, symbol="star", opacity=1), selector=dict(name='TARGET'))
    st.plotly_chart(fig, use_container_width=True)

# --- VISTA: DATABASE EXPLORER ---
elif st.session_state.nav == "Explorer":
    st.header("🗄️ Database Explorer")
    st.dataframe(db_engine.df, use_container_width=True, hide_index=True)
