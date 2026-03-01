import streamlit as st
import pandas as pd
import os

# Proviamo a importare plotly, se fallisce mostriamo un errore chiaro
try:
    import plotly.express as px
except ImportError:
    st.error("ERRORE: La libreria 'plotly' non è installata. Assicurati di aver caricato il file 'requirements.txt' su GitHub.")
    st.stop()

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="watch42 Dashboard", layout="wide")
USER_BRAND_NAME = "MY BRAND"

# --- CARICAMENTO DATI ---
@st.cache_data
def load_data():
    file_path = 'db-watches.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Pulizia forzata per il grafico
        for col in ['price_estimate', 'mov_reserve', 'case_thickness', 'power_score']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
        return df
    else:
        # Dati di emergenza se il file non viene trovato
        return pd.DataFrame([
            {"brand": USER_BRAND_NAME, "model_name": "Demo 1", "reference": "REF-001", "price_estimate": 5000, "mov_reserve": 72, "case_thickness": 12},
            {"brand": "Rolex", "model_name": "Sub", "reference": "REF-RLX", "price_estimate": 12000, "mov_reserve": 70, "case_thickness": 13}
        ])

df = load_data()

# --- NAVIGAZIONE ---
nav = st.sidebar.radio("MENU", ["⌚ My Watches", "📊 Pricing Intelligence", "🗄️ Database Explorer"])

# --- SEZIONE: MY WATCHES ---
if nav == "⌚ My Watches":
    st.header(f"Portfolio: {USER_BRAND_NAME}")
    my_df = df[df['brand'] == USER_BRAND_NAME]
    
    if my_df.empty:
        st.warning(f"Nessun orologio trovato per il brand '{USER_BRAND_NAME}' nel file CSV.")
    else:
        cols = st.columns(3)
        for i, (idx, row) in enumerate(my_df.head(12).iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(row['model_name'])
                    st.write(f"Ref: {row['reference']}")
                    st.metric("Prezzo", f"€{row['price_estimate']:,}")
                    st.write(f"⚙️ Riserva: {row['mov_reserve']}h | 📏 Spessore: {row['case_thickness']}mm")

# --- SEZIONE: PRICING INTELLIGENCE ---
elif nav == "Pricing Intelligence":
    st.header("📊 Matrice di Posizionamento Prezzo")
    
    if df.empty:
        st.error("Database vuoto.")
    else:
        c1, c2 = st.columns(2)
        y_options = {"mov_reserve": "Riserva di Carica", "case_thickness": "Spessore", "power_score": "Power Score"}
        y_choice = c1.selectbox("Parametro Asse Y", options=list(y_options.keys()), format_func=lambda x: y_options[x])
        
        # Filtriamo per evidenziare il brand
        df['Status'] = df['brand'].apply(lambda x: 'Il Mio Brand' if x == USER_BRAND_NAME else 'Competitor')

        fig = px.scatter(
            df, x="price_estimate", y=y_choice, color="Status",
            hover_name="brand", hover_data=["model_name", "reference"],
            color_discrete_map={'Il Mio Brand': '#2E5BFF', 'Competitor': '#D1D5DB'},
            labels={"price_estimate": "Prezzo (€)", y_choice: y_options[y_choice]},
            height=600, template="plotly_white"
        )
        fig.update_traces(marker=dict(size=12, opacity=0.7))
        st.plotly_chart(fig, use_container_width=True)

# --- SEZIONE: EXPLORER ---
elif nav == "Database Explorer":
    st.header("🗄️ Market Explorer")
    st.dataframe(df, use_container_width=True)
