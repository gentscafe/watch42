import streamlit as st
import pandas as pd
import plotly.express as px
from database_engine import db_engine, USER_BRAND_NAME

# 1. SETUP
st.set_page_config(page_title="watch42", layout="wide")

if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

# 2. PULIZIA DATI FORZATA (Assicura che il grafico veda numeri)
df_main = db_engine.df.copy()
for col in ['price_estimate', 'mov_reserve', 'case_thickness', 'power_score']:
    df_main[col] = pd.to_numeric(df_main[col], errors='coerce').fillna(0.0)

# 3. SIDEBAR
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
    st.header(f"Portfolio: {USER_BRAND_NAME}")
    
    # Filtriamo i dati per il tuo brand
    my_df = df_main[df_main['brand'] == USER_BRAND_NAME]
    
    if st.session_state.edit_ref:
        # PANNELLO MODIFICA
        watch_data = my_df[my_df['reference'] == st.session_state.edit_ref]
        if not watch_data.empty:
            watch = watch_data.iloc[0]
            st.subheader(f"Modifica: {watch['model_name']}")
            if st.button("← Indietro"):
                st.session_state.edit_ref = None
                st.rerun()
            
            new_price = st.number_input("Prezzo (€)", value=float(watch['price_estimate']))
            if st.button("Salva"):
                db_engine.update_watch_data(st.session_state.edit_ref, {"price_estimate": new_price})
                st.success("Salvato!")
                st.session_state.edit_ref = None
                st.rerun()
    else:
        # GRIGLIA CARD (Con protezione errore)
        if my_df.empty:
            st.warning("Nessun orologio trovato per il tuo brand.")
        else:
            cols = st.columns(3)
            for i, (idx, row) in enumerate(my_df.iterrows()):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"### {row['model_name']}")
                        st.write(f"Ref: {row['reference']}")
                        st.write(f"**Prezzo: €{row['price_estimate']:,}**")
                        if st.button("📝 Modifica", key=f"btn_{row['reference']}", use_container_width=True):
                            st.session_state.edit_ref = row['reference']
                            st.rerun()

# --- VISTA: PRICING INTELLIGENCE ---
elif st.session_state.nav == "Pricing":
    st.header("📊 Analisi di Mercato")
    
    try:
        c1, c2 = st.columns(2)
        y_map = {"mov_reserve": "Riserva di Carica", "case_thickness": "Spessore", "power_score": "Power Score"}
        y_choice = c1.selectbox("Parametro Asse Y", options=list(y_map.keys()), format_func=lambda x: y_map[x])
        
        my_watches = df_main[df_main['brand'] == USER_BRAND_NAME]
        target_ref = c2.selectbox("Orologio Target", options=my_watches['reference'].tolist())

        # Prepariamo il DF per il grafico con categorie stringa esplicite
        df_plot = df_main.copy()
        df_plot['Categoria'] = 'Altro'
        df_plot.loc[df_plot['brand'] == USER_BRAND_NAME, 'Categoria'] = 'Mio Brand'
        df_plot.loc[df_plot['reference'] == target_ref, 'Categoria'] = 'TARGET'

        fig = px.scatter(
            df_plot, 
            x="price_estimate", 
            y=y_choice, 
            color="Categoria",
            hover_name="brand",
            color_discrete_map={'Altro': '#D1D5DB', 'Mio Brand': '#2E5BFF', 'TARGET': '#EF4444'},
            labels={"price_estimate": "Prezzo (€)", y_choice: y_map[y_choice]},
            height=600,
            template="plotly_white"
        )
        fig.update_traces(marker=dict(size=10, opacity=0.6))
        fig.update_traces(marker=dict(size=20, symbol="star"), selector=dict(name='TARGET'))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Errore nel generare il grafico: {e}")

# --- VISTA: EXPLORER ---
elif st.session_state.nav == "Explorer":
    st.header("🗄️ Database Explorer")
    st.dataframe(df_main, use_container_width=True)
