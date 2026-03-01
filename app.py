import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. INJECT CUSTOM CSS
# CSS personalizzato per rimuovere i radio button e creare menu con icone moderne
def inject_custom_css():
    st.markdown("""
        <style>
        .main { background-color: #F8F9FC; }
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E5E7EB;
        }
        /* Stile per i pulsanti del menu nella sidebar */
        .stButton > button {
            width: 100%;
            border: none;
            background-color: transparent;
            text-align: left;
            padding: 10px 15px;
            border-radius: 8px;
            color: #1F2937;
            transition: all 0.3s;
        }
        .stButton > button:hover {
            background-color: #F3F4F6;
            color: #2E5BFF;
        }
        /* Stile card */
        div[data-testid="metric-container"], .stPlotlyChart {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #F3F4F6;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 3. MOCK DATA
@st.cache_data
def get_mock_data():
    brands = ["Mido", "Patek Philippe", "Audemars Piguet", "Rolex", "Cartier"]
    df = pd.DataFrame({
        'Model': [f'Watch {i}' for i in range(25)],
        'Price': np.random.randint(800, 50000, 25),
        'PowerScore': np.random.randint(38, 80, 25),
        'Diameter': np.random.randint(34, 48, 25),
        'Thickness': np.random.randint(6, 18, 25),
        'Brand': np.random.choice(brands, 25)
    })
    return df

data = get_mock_data()

# 4. SIDEBAR NAVIGATION CON ICONE (Specifica 1. ARCHITETTURA)
st.sidebar.title("watch42")

# Inizializzazione dello stato della navigazione
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = "My Watches"

# Pulsanti del menu con icone moderne
if st.sidebar.button("⌚ My Watches"):
    st.session_state.menu_option = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"):
    st.session_state.menu_option = "Pricing Intelligence"
if st.sidebar.button("🗺️ Design Intelligence"):
    st.session_state.menu_option = "Design Intelligence"
if st.sidebar.button("📈 Market Intelligence"):
    st.session_state.menu_option = "Market Intelligence"

menu = st.session_state.menu_option

# 5. LOGICA DELLE VISTE CORE

if menu == "My Watches":
    st.header("My Watches (Landing View)")
    st.write("Visualizzazione a griglia degli orologi del brand[cite: 16].")
    
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #EEE; margin-bottom: 10px;">
                <p style="font-weight: bold; margin-bottom: 2px;">All Dial Model {i+1}</p>
                <p style="font-size: 0.8em; color: gray;">Ref: M001.431.11.0{i}1.02</p>
                <hr style="margin: 10px 0;">
                <p style="color: #2E5BFF; font-weight: bold; font-size: 1.1em;">€ {1200 + (i*150)}</p>
                <p style="font-size: 0.8em;">Status: <span style="color: green;">Up to date</span></p>
            </div>
            """, unsafe_allow_html=True)
            # Bottone per impostare il target globale per comparazioni 
            if st.button(f"Set as Target {i+1}", key=f"target_{i}"):
                st.success(f"Orologio {i+1} impostato come Target")

elif menu == "Pricing Intelligence":
    st.header("Pricing Intelligence")
    st.write("Accesso alla Pricing & Value-for-Money Matrix[cite: 18].")
    fig = px.scatter(data, x='Price', y='PowerScore', color='Brand',
                     labels={'Price': 'Prezzo di listino (€) [cite: 47]', 'PowerScore': 'Power Score [cite: 48]'})
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Design Intelligence":
    st.header("Design Intelligence")
    st.write("Accesso alla White Space Heatmap[cite: 19].")
    fig = px.density_heatmap(data, x='Diameter', y='Thickness',
                             color_continuous_scale='RdYlGn_r',
                             labels={'Diameter': 'Diametro cassa (mm) [cite: 53]', 'Thickness': 'Spessore (mm) [cite: 54]'})
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Verde: Opportunità | Rosso: Saturazione [cite: 56, 57]")

elif menu == "Market Intelligence":
    st.header("Market Intelligence")
    st.write("Accesso al Tech Evolution Tracker[cite: 20].")
    st.subheader("🤖 AI Strategic Insights")
    st.warning("Il mercato si sta spostando verso lo standard 72h[cite: 62].")
    st.success("Aumento dell'uso del Titanio (+12%)[cite: 64].")
    
    chart_data = pd.DataFrame(np.random.randint(42, 72, 12), columns=['Media Riserva di Carica'])
    st.line_chart(chart_data)

st.sidebar.markdown("---")
