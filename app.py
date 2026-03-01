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
    st.rerun()
if st.sidebar.button("📊 Pricing Intelligence", use_container_width=True):
    st.session_state.nav = "Pricing"
    st.rerun()
if st.sidebar.button("🗄️ Database Explorer", use_container_width=True):
    st.session_state.nav = "Explorer"
    st.rerun()

# --- VISTA: MY WATCHES (Invariata) ---
if st.session_state.nav == "My Watches":
    st.header(f"Portfolio: {USER_BRAND_NAME}")
    # ... logica card esistente ...

# --- VISTA: PRICING INTELLIGENCE (Grafico Corretto) ---
elif st.session_state.nav == "Pricing":
    st.header("📊 Pricing Intelligence Matrix")
    
    c1, c2 = st.columns(2)
    y_map = {"mov_reserve": "Riserva di Carica", "case_thickness": "Spessore", "power_score": "Power Score"}
    y_choice = c1.selectbox("Asse Y", options=list(y_map.keys()), format_func=lambda x: y_map[x])
    
    my_watches = db_engine.df[db_engine.df['brand'] == USER_BRAND_NAME]
    target_ref = c2.selectbox("Orologio Target", options=my_watches['reference'].tolist())

    df_plot = db_engine.df.copy()
    df_plot['Status'] = 'Competitor'
    df_plot.loc[df_plot['brand'] == USER_BRAND_NAME, 'Status'] = 'Il Tuo Brand'
    df_plot.loc[df_plot['reference'] == target_ref, 'Status'] = 'TARGET'

    # Forza Plotly a leggere i dati come numeri
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

# --- VISTA: DATABASE EXPLORER (Nuova Sezione) ---
elif st.session_state.nav == "Explorer":
    st.header("🗄️ Database Explorer & Filtri Avanzati")
    df_exp = db_engine.df.copy()
    
    # Barra dei Filtri
    st.markdown("### Filtra Mercato")
    f1, f2, f3, f4 = st.columns(4)
    
    with f1:
        brand_f = st.multiselect("Brand", options=df_exp['brand'].unique())
    with f2:
        mat_f = st.multiselect("Materiale", options=df_exp['material'].unique())
    with f3:
        price_range = st.slider("Range Prezzo (€)", 0, 80000, (0, 80000))
    with f4:
        reserve_f = st.slider("Riserva min (h)", 0, 100, 0)

    # Applicazione Filtri
    if brand_f: df_exp = df_exp[df_exp['brand'].isin(brand_f)]
    if mat_f: df_exp = df_exp[df_exp['material'].isin(mat_f)]
    df_exp = df_exp[(df_exp['price_estimate'] >= price_range[0]) & (df_exp['price_estimate'] <= price_range[1])]
    df_exp = df_exp[df_exp['mov_reserve'] >= reserve_f]

    st.write(f"Risultati trovati: {len(df_exp)}")
    st.dataframe(df_exp, use_container_width=True, hide_index=True)
    
    # Download pulsante
    st.download_button("Esporta CSV", df_exp.to_csv(index=False), "export_market.csv", "text/csv")
