import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. INJECT ADVANCED CUSTOM CSS (Il "Vibe" Professionale)
def inject_custom_css():
    st.markdown("""
        <style>
        /* Sfondo generale Off-White */
        .main { background-color: #F8F9FC; }
        
        /* Sidebar pulita e minimale */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E5E7EB !important;
        }
        
        /* Titolo Sidebar */
        .sidebar-title {
            font-size: 24px;
            font-weight: 700;
            color: #1F2937;
            margin-bottom: 20px;
            padding: 0 10px;
        }

        /* Pulsanti Menu: Allineati a sinistra, senza bordi, effetto Hover */
        .stButton > button {
            width: 100% !important;
            border: none !important;
            background-color: transparent !important;
            text-align: left !important;
            padding: 12px 15px !important;
            border-radius: 10px !important;
            color: #4B5563 !important;
            font-size: 16px !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
        }
        
        .stButton > button:hover {
            background-color: #F3F4F6 !important;
            color: #2E5BFF !important;
        }

        /* CARD STYLE: Ombre morbide e bordi arrotondati */
        .watch-card {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
            border: 1px solid #F3F4F6;
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .watch-card:hover {
            transform: translateY(-5px);
        }

        /* Typography per le Card */
        .card-title { font-size: 18px; font-weight: 600; color: #111827; margin-bottom: 4px; }
        .card-ref { font-size: 13px; color: #6B7280; margin-bottom: 15px; }
        .card-price { font-size: 22px; font-weight: 700; color: #2E5BFF; }
        .card-status { font-size: 12px; font-weight: 500; padding: 4px 8px; border-radius: 6px; background: #ECFDF5; color: #059669; }

        /* Nasconde i pallini dei radio button standard se presenti */
        [data-testid="stMarkdownContainer"] p { margin-bottom: 0; }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 3. MOCK DATA
@st.cache_data
def get_mock_data():
    brands = ["Mido", "Patek Philippe", "Audemars Piguet", "Rolex", "Cartier"]
    return pd.DataFrame({
        'Model': [f'Watch {i}' for i in range(25)],
        'Price': np.random.randint(800, 50000, 25),
        'PowerScore': np.random.randint(38, 80, 25),
        'Diameter': np.random.randint(34, 48, 25),
        'Thickness': np.random.randint(6, 18, 25),
        'Brand': np.random.choice(brands, 25)
    })

data = get_mock_data()

# 4. SIDEBAR NAVIGATION (Menu con icone e allineamento corretto)
st.sidebar.markdown('<div class="sidebar-title">watch42</div>', unsafe_allow_html=True)

if 'menu' not in st.session_state:
    st.session_state.menu = "My Watches"

# Pulsanti stilizzati come voci di menu 
if st.sidebar.button("⌚  My Watches"):
    st.session_state.menu = "My Watches"
if st.sidebar.button("📊  Pricing Intelligence"):
    st.session_state.menu = "Pricing Intelligence"
if st.sidebar.button("🗺️  Design Intelligence"):
    st.session_state.menu = "Design Intelligence"
if st.sidebar.button("📈  Market Intelligence"):
    st.session_state.menu = "Market Intelligence"

# 5. VISTE CORE

if st.session_state.menu == "My Watches":
    st.header("My Watches")
    st.caption("Visualizzazione a griglia degli orologi del brand[cite: 16].")
    
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            # Card HTML personalizzata per il look premium [cite: 39, 41]
            st.markdown(f"""
            <div class="watch-card">
                <div class="card-title">All Dial Model {i+1}</div>
                <div class="card-ref">Ref: M001.431.11.0{i}1.02</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
                    <div class="card-price">€ {1200 + (i*150)}</div>
                    <div class="card-status">Up to date</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Bottone d'azione discreto [cite: 43]
            if st.button(f"Set as Target", key=f"target_{i}"):
                st.toast(f"Modello {i+1} impostato come Target!")

elif st.session_state.menu == "Pricing Intelligence":
    st.header("Pricing Intelligence")
    fig = px.scatter(data, x='Price', y='PowerScore', color='Brand',
                     labels={'Price': 'Prezzo (€)', 'PowerScore': 'Power Score'})
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.menu == "Design Intelligence":
    st.header("Design Intelligence")
    fig = px.density_heatmap(data, x='Diameter', y='Thickness',
                             color_continuous_scale='RdYlGn_r',
                             labels={'Diameter': 'Diametro (mm)', 'Thickness': 'Spessore (mm)'})
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.menu == "Market Intelligence":
    st.header("Market Intelligence")
    st.subheader("🤖 AI Strategic Insights")
    st.warning("Il mercato si sta spostando verso lo standard 72h[cite: 62].")
    st.success("Aumento dell'uso del Titanio (+12%) rilevato[cite: 64].")
    st.line_chart(pd.DataFrame(np.random.randint(42, 72, 12), columns=['Media Riserva di Carica']))

st.sidebar.markdown("---")
