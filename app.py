import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | CEO Dashboard", layout="wide")

# 2. DATI STATICI (Senza dipendenze esterne)
MY_WATCHES = [
    {"ref": "V-01", "name": "Ocean Deep", "price": 4500, "reserve": 72, "thick": 12.5, "mat": "Steel"},
    {"ref": "V-02", "name": "Midnight GMT", "price": 8900, "reserve": 48, "thick": 11.0, "mat": "Gold"},
    {"ref": "V-03", "name": "Sky High", "price": 12500, "reserve": 80, "thick": 9.5, "mat": "Titanium"},
    {"ref": "V-04", "name": "Urban Slim", "price": 3200, "reserve": 42, "thick": 7.8, "mat": "Steel"},
    {"ref": "V-05", "name": "Chronos Gold", "price": 24000, "reserve": 60, "thick": 13.0, "mat": "Gold"},
    {"ref": "V-06", "name": "Pure White", "price": 5400, "reserve": 72, "thick": 10.5, "mat": "Steel"},
    {"ref": "V-07", "name": "Black Stealth", "price": 6700, "reserve": 48, "thick": 12.0, "mat": "Titanium"},
    {"ref": "V-08", "name": "Heritage 38", "price": 4100, "reserve": 38, "thick": 11.5, "mat": "Steel"},
    {"ref": "V-09", "name": "Luna Phase", "price": 15600, "reserve": 72, "thick": 10.2, "mat": "Gold"},
    {"ref": "V-10", "name": "Aqua Master", "price": 2800, "reserve": 42, "thick": 14.0, "mat": "Steel"},
]

# Dati per il grafico (Competitor fittizi)
MARKET_DATA = pd.DataFrame([
    {"brand": "Rolex", "price": 12000, "reserve": 70, "thick": 12.5, "type": "Competitor"},
    {"brand": "Omega", "price": 6500, "reserve": 60, "thick": 13.5, "type": "Competitor"},
    {"brand": "Patek", "price": 45000, "reserve": 45, "thick": 8.5, "type": "Competitor"},
    {"brand": "Cartier", "price": 7200, "reserve": 42, "thick": 9.2, "type": "Competitor"},
    {"brand": "Tudor", "price": 4100, "reserve": 70, "thick": 14.5, "type": "Competitor"},
    {"brand": "MY BRAND", "price": 8900, "reserve": 48, "thick": 11.0, "type": "Target"},
] + [{"brand": f"Indie {i}", "price": 2000 + (i*500), "reserve": 40 + (i%30), "thick": 9+(i%5), "type": "Market"} for i in range(50)])

# 3. SIDEBAR STATICA
st.sidebar.title("watch42")
nav = st.sidebar.radio("NAVIGAZIONE", ["⌚ My Watches", "📊 Pricing Intelligence"])

# 4. LOGICA UI
if nav == "⌚ My Watches":
    st.header("Il Tuo Portfolio")
    st.markdown("Visualizzazione dei 10 modelli principali in collezione.")
    
    cols = st.columns(3)
    for i, watch in enumerate(MY_WATCHES):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {watch['name']}")
                st.caption(f"Ref: {watch['ref']} | {watch['mat']}")
                
                # Griglia info
                c1, c2 = st.columns(2)
                c1.metric("Prezzo", f"€{watch['price']:,}")
                c2.metric("Spessore", f"{watch['thick']}mm")
                
                st.progress(watch['reserve']/100, text=f"Riserva: {watch['reserve']}h")
                st.button("Vedi Dettagli", key=f"btn_{watch['ref']}", use_container_width=True)

elif nav == "📊 Pricing Intelligence":
    st.header("Analisi Posizionamento Prezzo")
    
    # Sezione Filtri sopra il grafico
    with st.expander("🛠️ Filtri e Parametri di Analisi", expanded=True):
        f1, f2, f3 = st.columns(3)
        y_axis = f1.selectbox("Seleziona parametro Asse Y", ["reserve", "thick"], format_func=lambda x: "Riserva (h)" if x=="reserve" else "Spessore (mm)")
        price_range = f2.slider("Range Prezzo (€)", 0, 50000, (2000, 30000))
        target_watch = f3.selectbox("Highlight Modello", [w['name'] for w in MY_WATCHES])

    # Grafico Statico Popolato
    
    
    fig = px.scatter(
        MARKET_DATA, 
        x="price", 
        y=y_axis, 
        color="type",
        hover_name="brand",
        color_discrete_map={"Competitor": "#D1D5DB", "Market": "#E5E7EB", "Target": "#2E5BFF"},
        labels={"price": "Prezzo (€)", "reserve": "Riserva di Carica (h)", "thick": "Spessore Cassa (mm)"},
        height=600,
        template="plotly_white"
    )
    
    fig.update_traces(marker=dict(size=12, opacity=0.7))
    st.plotly_chart(fig, use_container_width=True)

    # Tabella Comparativa Statica
    st.subheader("Top Competitor nel Range")
    st.table(MARKET_DATA.sort_values("price").head(5))
