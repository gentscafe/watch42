import streamlit as st
import pandas as pd
import os

# Forza il caricamento di Plotly solo se necessario per evitare crash all'avvio
def get_plotly():
    import plotly.express as px
    return px

# CONFIGURAZIONE
st.set_page_config(page_title="watch42 Dashboard", layout="wide")
USER_BRAND_NAME = "MY BRAND"

# TITOLO SEMPRE VISIBILE
st.title("watch42 | Market Intelligence")

# CARICAMENTO DATI
@st.cache_data
def load_data():
    file_path = 'db-watches.csv'
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            # Pulizia minima colonne numeriche
            cols = ['price_estimate', 'mov_reserve', 'case_thickness']
            for c in cols:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
            return df
        except Exception as e:
            st.error(f"Errore nella lettura del file CSV: {e}")
            return pd.DataFrame()
    else:
        st.error(f"ATTENZIONE: File 'db-watches.csv' non trovato nella cartella principale.")
        return pd.DataFrame()

df = load_data()

# SIDEBAR NAVIGAZIONE
nav = st.sidebar.radio("MENU", ["⌚ My Watches", "📊 Pricing Matrix", "🗄️ Database Explorer"])

# 1. SEZIONE MY WATCHES
if nav == "⌚ My Watches":
    if not df.empty:
        my_df = df[df['brand'] == USER_BRAND_NAME]
        st.header(f"Portfolio: {USER_BRAND_NAME}")
        
        if my_df.empty:
            st.warning(f"Nessun dato trovato per il brand '{USER_BRAND_NAME}'.")
        else:
            cols = st.columns(3)
            for i, (idx, row) in enumerate(my_df.head(12).iterrows()):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.subheader(row['model_name'])
                        st.write(f"Ref: {row['reference']}")
                        st.metric("Prezzo", f"€{int(row['price_estimate']):,}")

# 2. SEZIONE PRICING MATRIX
elif nav == "📊 Pricing Matrix":
    st.header("Analisi Posizionamento")
    if not df.empty:
        try:
            px = get_plotly()
            y_choice = st.selectbox("Seleziona parametro Y", ["mov_reserve", "case_thickness"])
            
            # Evidenzia il brand
            df['Status'] = df['brand'].apply(lambda x: 'Il Mio Brand' if x == USER_BRAND_NAME else 'Competitor')
            
            fig = px.scatter(
                df, x="price_estimate", y=y_choice, color="Status",
                hover_name="brand",
                color_discrete_map={'Il Mio Brand': '#2E5BFF', 'Competitor': '#D1D5DB'},
                height=600, template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Errore nel caricamento del grafico: {e}")

# 3. SEZIONE EXPLORER
elif nav == "🗄️ Database Explorer":
    st.header("Esplora l'intero mercato")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
