import streamlit as st
import pandas as pd
import random
import os

# --- LOGICA DI GENERAZIONE DATI (FASE 3) ---
def create_mock_data():
    brands = ["Rolex", "Patek Philippe", "Audemars Piguet", "Oris", "Nomos", "FP Journe", "Omega", "Cartier", "Tudor", "IWC"] 
    # Espandiamo a 100 brand internamente per il vibe
    full_brands = brands + [f"Independent_{i}" for i in range(1, 91)]
    styles = ["Dress", "Diver", "Chronograph", "Casual", "Pilot/Field", "GMT", "Digital"]
    
    data = []
    for brand in full_brands:
        for i in range(1, 51):
            style = random.choice(styles)
            data.append({
                'watch_style': style,
                'brand': brand,
                'model_name': f"{brand} {style} Model {i}",
                'reference': f"REF-{random.randint(1000, 9999)}",
                'case_material': random.choice(["Steel", "Titanium", "Gold", "Ceramic"]),
                'diameter': f"{random.choice([38, 39, 40, 41, 42])}mm"
            })
    return pd.DataFrame(data)

# --- CARICAMENTO DATABASE ---
DB_FILE = 'watches_database.csv'

if not os.path.exists(DB_FILE):
    df = create_mock_data()
    df.to_csv(DB_FILE, index=False)
else:
    df = pd.read_csv(DB_FILE)

# --- INTERFACCIA STREAMLIT (FASE 1) ---
st.set_page_config(page_title="Watch42 Explorer", layout="wide")

st.title("⌚ Watch42: Independent Watch Explorer")
st.write(f"Database caricato con successo: **{len(df)} orologi** in memoria.")

# Sidebar per i Filtri
st.sidebar.header("Filtri di Ricerca")
selected_style = st.sidebar.multiselect("Stile", options=sorted(df['watch_style'].unique()), default=["Diver", "Dress"])
selected_brand = st.sidebar.selectbox("Cerca Brand", options=["Tutti"] + sorted(df['brand'].unique().tolist()))

# Logica di Filtraggio
filtered_df = df[df['watch_style'].isin(selected_style)]
if selected_brand != "Tutti":
    filtered_df = filtered_df[filtered_df['brand'] == selected_brand]

# Display
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
