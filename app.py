import streamlit as st
import pandas as pd
import plotly.express as px
from database_engine import db_engine, USER_BRAND_NAME

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Market Intelligence", layout="wide")

# 2. CSS PROFESSIONALE
st.markdown("""
    <style>
    .main { background-color: #F8F9FC; }
    [data-testid="stSidebar"] { background-color: #FBFBFE !important; border-right: 1px solid #E5E7EB !important; }
    .sidebar-header { font-size: 11px; font-weight: 700; color: #9CA3AF; text-transform: uppercase; padding: 25px 20px 10px 20px; }
    .info-grid { margin: 10px 0; padding: 12px; background-color: #F9FAFB; border-radius: 10px; border: 1px solid #F3F4F6; }
    .info-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .info-label { color: #6B7280; font-weight: 500; }
    .info-value { color: #111827; font-weight: 600; }
    .edit-section-header { font-size: 14px; font-weight: 700; color: #2E5BFF; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 2px solid #EEF2FF; }
    </style>
""", unsafe_allow_html=True)

# 3. GESTIONE STATO
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

# 4. SIDEBAR PERMANENTE
st.sidebar.markdown(f'<div style="padding: 20px; color: #2E5BFF; font-weight: 800; font-size: 24px;">{USER_BRAND_NAME}</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-header">NAVIGAZIONE</div>', unsafe_allow_html=True)

if st.sidebar.button("⌚ My Watches", use_container_width=True):
    st.session_state.nav = "My Watches"
    st.session_state.edit_ref = None
    st.rerun()

if st.sidebar.button("📊 Pricing Intelligence", use_container_width=True):
    st.session_state.nav = "Pricing"
    st.session_state.edit_ref = None
    st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🗄️ Watch DB Explorer", use_container_width=True):
    st.session_state.nav = "DB"
    st.rerun()

# 5. LOGICA VISTA: MY WATCHES
if st.session_state.nav == "My Watches":
    if st.session_state.edit_ref is not None:
        # --- PANNELLO MODIFICA ---
        watch = db_engine.df[db_engine.df['reference'] == st.session_state.edit_ref].iloc[0]
        st.header(f"Configuratore: {watch['model_name']}")
        
        if st.button("← Torna alla lista"):
            st.session_state.edit_ref = None
            st.rerun()

        t1, t2, t3 = st.tabs(["💎 Estetica", "⚙️ Meccanica", "🚀 Mercato"])
        with t1:
            new_name = st.text_input("Modello", value=watch['model_name'])
            new_mat = st.selectbox("Materiale", ["Steel", "Gold", "Titanium", "Platinum"], index=0)
        with t2:
            new_res = st.number_input("Riserva (h)", value=int(watch['mov_reserve']))
            new_freq = st.number_input("Frequenza (vph)", value=int(watch['mov_freq']))
        with t3:
            new_price = st.number_input("Prezzo (€)", value=int(watch['price_estimate']))

        if st.button("💾 Salva Modifiche", type="primary", use_container_width=True):
            db_engine.update_watch_data(st.session_state.edit_ref, {
                "model_name": new_name, "material": new_mat,
                "mov_reserve": new_res, "mov_freq": new_freq, "price_estimate": new_price
            })
            st.success("Dati aggiornati!")
            st.session_state.edit_ref = None
            st.rerun()
    else:
        # --- GRIGLIA CARD ---
        st.header(f"Portfolio: {USER_BRAND_NAME}")
        my_df = db_engine.get_my_watches()
        cols = st.columns(3)
        for i, (idx, row) in enumerate(my_df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"""
                    <div style="height:100px; background-color:#F3F4F6; border-radius:12px; display:flex; justify-content:center; align-items:center; font-size:35px;">⌚</div>
                    <div style="font-weight:700; font-size:18px; margin-top:12px;">{row['model_name']}</div>
                    <div style="color:#6B7280; font-size:11px; margin-bottom:10px;">REF: {row['reference']}</div>
                    <div class="info-grid">
                        <div class="info-row"><span class="info-label">Materiale</span><span class="info-value">{row['material']}</span></div>
                        <div class="info-row"><span class="info-label">Riserva</span><span class="info-value">{row['mov_reserve']}h</span></div>
                        <div class="info-row"><span class="info-label">Prezzo</span><span class="info-value">€{row['price_estimate']:,}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Modifica", key=f"ed_{row['reference']}", use_container_width=True):
                        st.session_state.edit_ref = row['reference']
                        st.rerun()

# 6. LOGICA VISTA: PRICING INTELLIGENCE
elif st.session_state.nav == "Pricing":
    st.header("📊 Pricing Intelligence Matrix")
    
    # Selettori per il grafico nella sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Analisi Competitiva")
    y_options = {"mov_reserve": "Riserva di Carica", "case_thickness": "Spessore", "mov_freq": "Frequenza"}
    y_choice = st.sidebar.selectbox("Parametro Y", options=list(y_options.keys()), format_func=lambda x: y_options[x])
    
    my_refs = db_engine.get_my_watches()['reference'].tolist()
    target_ref = st.sidebar.selectbox("Orologio Target (Il Tuo)", options=my_refs)
    
    # Preparazione DataFrame per il grafico
    plot_df = db_engine.df.copy()
    plot_df['Status'] = 'Competitor'
    plot_df.loc[plot_df['brand'] == USER_BRAND_NAME, 'Status'] = 'Il Tuo Brand'
    plot_df.loc[plot_df['reference'] == target_ref, 'Status'] = 'TARGET SELEZIONATO'

    # Creazione Scatter Plot
    
    fig = px.scatter(
        plot_df, x="price_estimate", y=y_choice, color="Status",
        hover_name="brand", hover_data=["model_name", "material"],
        color_discrete_map={'Competitor': '#E5E7EB', 'Il Tuo Brand': '#2E5BFF', 'TARGET SELEZIONATO': '#FF4B4B'},
        labels={"price_estimate": "Prezzo (€)", y_choice: y_options[y_choice]},
        height=600, template="plotly_white"
    )
    fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_traces(marker=dict(size=22, symbol="star"), selector=dict(name='TARGET SELEZIONATO'))
    
    st.plotly_chart(fig, use_container_width=True)

# 7. LOGICA VISTA: DB EXPLORER
elif st.session_state.nav == "DB":
    st.header("🗄️ Watch Database Explorer")
    st.dataframe(db_engine.df, use_container_width=True)
