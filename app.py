import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA (Vibe Clean-Tech)
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. INJECT CUSTOM CSS (Replica il look & feel dell'immagine di riferimento)
def inject_custom_css():
    st.markdown("""
        <style>
        .main { background-color: #F8F9FC; }
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E5E7EB;
        }
        div[data-testid="metric-container"], .stPlotlyChart {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #F3F4F6;
        }
        .stButton>button {
            border-radius: 10px;
            background-color: #2E5BFF;
            color: white;
            border: none;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 3. MOCK DATA (In attesa di WatchBase Professional API)
@st.cache_data
def get_watchbase_mock_data():
    brands = ["Mido", "Patek Philippe", "Audemars Piguet", "Rolex", "Cartier"]
    df = pd.DataFrame({
        'Model': [f'Watch {i}' for i in range(25)],
        'Price': np.random.randint(800, 50000, 25),
        'PowerScore': np.random.randint(38, 80, 25),
        'Diameter': np.random.randint(34, 48, 25),
        'Thickness': np.random.randint(6, 18, 25),
        'Brand': np.random.choice(brands, 25),
        'Movement': np.random.choice(["Automatic", "Manual", "Quartz"], 25)
    })
    return df

data = get_watchbase_mock_data()

# 4. SIDEBAR NAVIGATION (Architettura Sidebar Sinistra)
st.sidebar.title("watch42")
st.sidebar.caption("v1.0 MVP - WatchBase API")

menu = st.sidebar.radio(
    "MENU",
    ["My Watches", "Pricing Intelligence", "Design Intelligence", "Market Intelligence"],
    index=0
)

# 5. DEFINIZIONE DEI FILTRI (Data Schema: WatchBase)
with st.sidebar.expander("🔍 FILTERS", expanded=True):
    brand_sel = st.multiselect("Brand (Top 25)", options=data['Brand'].unique()) # [cite: 26]
    movement_sel = st.selectbox("Movement", ["Automatic", "Manual", "Quartz"]) # [cite: 29]
    case_material = st.multiselect("Case Material", ["Steel", "Titanium", "Gold", "Bronze", "Carbon"]) # [cite: 30]
    diameter = st.slider("Diameter (mm)", 34, 48, (38, 42)) # [cite: 32]
    thickness = st.slider("Thickness (mm)", 6, 18, (8, 14)) # [cite: 33]

# 6. VISTE CORE

if menu == "My Watches":
    st.header("My Watches (Landing View)") # [cite: 16, 38]
    st.write("Visualizzazione a griglia degli orologi del brand.")
    
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            # Card eleganti basate sulle specifiche [cite: 39, 40]
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #EEE; margin-bottom: 10px;">
                <p style="font-weight: bold; margin-bottom: 2px;">All Dial Model {i+1}</p>
                <p style="font-size: 0.8em; color: gray;">Ref: M001.431.11.0{i}1.02</p>
                <hr style="margin: 10px 0;">
                <p style="color: #2E5BFF; font-weight: bold; font-size: 1.1em;">€ {1200 + (i*150)}</p>
                <p style="font-size: 0.8em;">Tech Status: <span style="color: green;">Up to date</span></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Set as Target {i+1}", key=f"target_{i}"):
                st.success(f"Orologio {i+1} impostato come Target globale") # [cite: 43]

elif menu == "Pricing Intelligence":
    st.header("Pricing & Value-for-Money Matrix") # [cite: 18, 45]
    # Scatter Plot: Asse X (Prezzo), Asse Y (Power Score) [cite: 46, 47, 48]
    fig = px.scatter(data, x='Price', y='PowerScore', color='Brand',
                     labels={'Price': 'Prezzo di listino (€)', 'PowerScore': 'Power Score (h)'})
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Design Intelligence":
    st.header("White Space Heatmap") # [cite: 19, 51]
    # Matrice: Asse X (Diametro), Asse Y (Spessore) [cite: 53, 54]
    fig = px.density_heatmap(data, x='Diameter', y='Thickness', 
                             color_continuous_scale='RdYlGn_r',
                             labels={'Diameter': 'Diametro cassa (mm)', 'Thickness': 'Spessore (mm)'})
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Verde: Opportunità | Rosso: Saturazione") # [cite: 56, 57]

elif menu == "Market Intelligence":
    st.header("Tech Evolution Tracker") # [cite: 20, 58]
    
    # Sezione AI Insights (Alert Strategici) [cite: 61]
    st.subheader("🤖 AI Strategic Insights")
    st.warning("Il mercato si sta spostando verso lo standard 72h; il tuo modello attuale è al di sotto della media del 30%.") # [cite: 62, 63]
    st.success("Aumento dell'uso del Titanio (+12%) rilevato nella categoria Diver sotto i 3.000€.") # [cite: 64, 65]
    
    # Grafico temporale mock per Power Reserve [cite: 59, 60]
    chart_data = pd.DataFrame(np.random.randint(42, 72, 12), columns=['Media Riserva di Carica'])
    st.line_chart(chart_data)

st.sidebar.markdown("---")
st.sidebar.caption("Data Source: WatchBase Professional API") # [cite: 5]
