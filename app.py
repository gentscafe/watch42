import streamlit as st
import pandas as pd
import plotly.express as px
from database_engine import db_engine, USER_BRAND_NAME

# 1. SETUP PAGINA
st.set_page_config(page_title="watch42 | CEO Dashboard", layout="wide")

# CSS di base
st.markdown("""
    <style>
    .info-grid { margin: 10px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px; border: 1px solid #F3F4F6; }
    .info-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# 2. NAVIGAZIONE
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

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
    my_df = db_engine.get_my_watches()
    
    if st.session_state.edit_ref:
        # PANNELLO MODIFICA
        watch = my_df[my_df['reference'] == st.session_state.edit_ref].iloc[0]
        st.header(f"🔧 Modifica: {watch['model_name']}")
        if st.button("← Annulla"):
            st.session_state.edit_ref = None
            st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            u_name = st.text_input("Nome Modello", value=watch['model_name'])
            u_price = st.number_input("Prezzo Listino (€)", value=float(watch['price_estimate']))
        with col2:
            u_reserve = st.number_input("Riserva (h)", value=float(watch['mov_reserve']))
            u_thick = st.number_input("Spessore (mm)", value=float(watch['case_thickness']))
            
        if st.button("💾 Salva Modifiche", type="primary"):
            db_engine.update_watch_data(st.session_state.edit_ref, {
                "model_name": u_name, "price_estimate": u_price,
                "mov_reserve": u_reserve, "case_thickness": u_thick
            })
            st.success("Database aggiornato!")
            st.session_state.edit_ref = None
            st.rerun()
    else:
        st.header(f"Portfolio: {USER_BRAND_NAME}")
        cols = st.columns(3)
        for i, (idx, row) in enumerate(my_df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {row['model_name']}")
                    st.write(f"Ref: {row['reference']}")
                    st.markdown(f"""
                    <div class="info-grid">
                        <div class="info-row"><span class="info-label">Prezzo</span><span class="info-value">€{row['price_estimate']:,}</span></div>
                        <div class="info-row"><span class="info-label">Riserva</span><span class="info-value">{row['mov_reserve']}h</span></div>
                        <div class="info-row"><span class="info-label">Spessore</span><span class="info-value">{row['case_thickness']}mm</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("📝 Modifica", key=f"ed_{row['reference']}", use_container_width=True):
                        st.session_state.edit_ref = row['reference']
                        st.rerun()

# --- VISTA: PRICING INTELLIGENCE ---
elif st.session_state.nav == "Pricing":
    st.header("📊 Analisi Competitiva (Pricing Matrix)")
    
    # Selettori superiori
    c1, c2 = st.columns(2)
    y_map = {"mov_reserve": "Riserva di Carica", "case_thickness": "Spessore", "power_score": "Power Score"}
    y_choice = c1.selectbox("Confronta Prezzo vs:", options=list(y_map.keys()), format_func=lambda x: y_map[x])
    
    my_refs = db_engine.get_my_watches()['reference'].tolist()
    target_ref = c2.selectbox("Seleziona il Tuo Orologio Target", options=my_refs)

    # Preparazione dati grafico
    df_plot = db_engine.df.copy()
    df_plot['Categoria'] = 'Competitor'
    df_plot.loc[df_plot['brand'] == USER_BRAND_NAME, 'Categoria'] = 'Mio Brand'
    df_plot.loc[df_plot['reference'] == target_ref, 'Categoria'] = 'TARGET'

    # Grafico Scatter
    fig = px.scatter(
        df_plot, x="price_estimate", y=y_choice, color="Categoria",
        hover_name="brand", hover_data=["model_name", "reference"],
        color_discrete_map={'Competitor': '#D1D5DB', 'Mio Brand': '#2E5BFF', 'TARGET': '#EF4444'},
        labels={"price_estimate": "Prezzo (€)", y_choice: y_map[y_choice]},
        height=600, template="plotly_white"
    )
    fig.update_traces(marker=dict(size=12, opacity=0.7))
    fig.update_traces(marker=dict(size=25, symbol="star", opacity=1), selector=dict(name='TARGET'))
    
    st.plotly_chart(fig, use_container_width=True)

# --- VISTA: DATABASE EXPLORER ---
elif st.session_state.nav == "Explorer":
    st.header("🗄️ Market Database Explorer")
    st.dataframe(db_engine.df, use_container_width=True, hide_index=True)
