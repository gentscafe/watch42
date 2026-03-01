import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS DEFINITIVO (Fix Sidebar e Card)
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] {
        background-color: #FBFBFE !important;
        border-right: 1px solid #E5E7EB !important;
    }
    .sidebar-header {
        font-size: 11px; font-weight: 700; color: #9CA3AF;
        letter-spacing: 1.5px; text-transform: uppercase;
        padding: 30px 25px 15px 25px;
    }
    .watch-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3F4F6; margin-bottom: 10px;
    }
    .card-image-placeholder {
        height: 140px; background-color: #F3F4F6; border-radius: 15px;
        display: flex; justify-content: center; align-items: center;
        font-size: 45px; margin-bottom: 15px;
    }
    .watch-details {
        margin: 15px 0; padding: 12px;
        background-color: #F9FAFB; border-radius: 10px;
    }
    .detail-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; }
    .detail-label { color: #6B7280; font-weight: 500; }
    .detail-value { color: #111827; font-weight: 600; }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important; border: none !important;
        background-color: transparent !important; text-align: left !important;
        padding: 12px 25px !important; display: flex !important;
        align-items: center !important; justify-content: flex-start !important; gap: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. DATI DI ESEMPIO
def get_clean_data():
    return [
        {"Model": "All Dial Model 1", "Ref": "M001.431.11.001.02", "Price": "1.200", "Mat": "Steel", "Dia": "42mm", "Mov": "Manual"},
        {"Model": "All Dial Model 2", "Ref": "M001.431.11.011.02", "Price": "1.350", "Mat": "Titanium", "Dia": "38mm", "Mov": "Manual"},
        {"Model": "All Dial Model 3", "Ref": "M001.431.11.021.02", "Price": "1.500", "Mat": "Titanium", "Dia": "38mm", "Mov": "Manual"},
        {"Model": "All Dial Model 4", "Ref": "M001.431.11.031.02", "Price": "1.650", "Mat": "Steel", "Dia": "40mm", "Mov": "Manual"},
        {"Model": "All Dial Model 5", "Ref": "M001.431.11.041.02", "Price": "1.800", "Mat": "Gold", "Dia": "42mm", "Mov": "Automatic"},
        {"Model": "All Dial Model 6", "Ref": "M001.431.11.051.02", "Price": "1.950", "Mat": "Steel", "Dia": "38mm", "Mov": "Automatic"}
    ]

# 4. SIDEBAR
st.sidebar.markdown('<div class="sidebar-header">MENU</div>', unsafe_allow_html=True)
if 'menu' not in st.session_state: st.session_state.menu = "My Watches"

if st.sidebar.button("⌚ My Watches"): st.session_state.menu = "My Watches"
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.menu = "Pricing Intelligence"
if st.sidebar.button("🗺️ Design Intelligence"): st.session_state.menu = "Design Intelligence"
if st.sidebar.button("📈 Market Intelligence"): st.session_state.menu = "Market Intelligence"

menu = st.session_state.menu

# 5. LOGICA DELLE VISTE
if menu == "My Watches":
    st.header("My Watches")
    watches = get_clean_data()
    cols = st.columns(3)
    for i, w in enumerate(watches):
        with cols[i % 3]:
            card_html = f"""
            <div class="watch-card">
                <div class="card-image-placeholder">⌚</div>
                <div style="font-size: 17px; font-weight: 700; color: #111827;">{w['Model']}</div>
                <div style="color: #6B7280; font-size: 12px; margin-bottom: 10px;">Ref: {w['Ref']}</div>
                <div class="watch-details">
                    <div class="detail-row"><span class="detail-label">Material</span><span class="detail-value">{w['Mat']}</span></div>
                    <div class="detail-row"><span class="detail-label">Diameter</span><span class="detail-value">{w['Dia']}</span></div>
                    <div class="detail-row"><span class="detail-label">Movement</span><span class="detail-value">{w['Mov']}</span></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div style="font-size: 20px; font-weight: 700; color: #2E5BFF;">€ {w['Price']}</div>
                    <div style="font-size: 12px; color: #059669; font-weight: 600;">● Up to date</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            st.button("Set as Target", key=f"target_{i}")

elif menu == "Pricing Intelligence":
    st.header("Pricing Intelligence")
    df_graph = pd.DataFrame({
        'Price': np.random.randint(800, 15000, 50),
        'PowerScore': np.random.randint(40, 80, 50),
        'Brand': np.random.choice(['Mido', 'Rolex', 'Tudor', 'Omega'], 50)
    })
    fig = px.scatter(df_graph, x='Price', y='PowerScore', color='Brand', title="Price vs Power Score")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Design Intelligence":
    st.header("Design Intelligence")
    df_design = pd.DataFrame({
        'Diameter': np.random.randint(34, 46, 100),
        'Thickness': np.random.randint(8, 16, 100)
    })
    fig = px.density_heatmap(df_design, x='Diameter', y='Thickness', title="Market White Space (Heatmap)")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Market Intelligence":
    st.header("Market Intelligence")
    st.subheader("Tech Trend Tracker")
    chart_data = pd.DataFrame(np.random.randint(40, 75, (20, 2)), columns=['Market Avg', 'Your Brand'])
    st.line_chart(chart_data)
    st.success("AI Insight: L'uso del titanio sta crescendo del 15% nel tuo segmento.")
