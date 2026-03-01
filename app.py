import streamlit as st
import pandas as pd
from database_engine import db_engine, USER_BRAND_NAME

# 1. INIZIALIZZAZIONE (Deve essere in cima)
st.set_page_config(page_title="watch42", layout="wide")

if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_ref' not in st.session_state: st.session_state.edit_ref = None

# 2. SIDEBAR (Sempre presente)
st.sidebar.title(f"Admin: {USER_BRAND_NAME}")
if st.sidebar.button("⌚ My Watches", use_container_width=True):
    st.session_state.nav = "My Watches"
    st.session_state.edit_ref = None
    st.rerun()
if st.sidebar.button("📊 Pricing Intelligence", use_container_width=True):
    st.session_state.nav = "Pricing"

# 3. LOGICA PAGINA
if st.session_state.nav == "My Watches":
    if st.session_state.edit_ref:
        # --- PANNELLO MODIFICA ---
        watch = db_engine.df[db_engine.df['reference'] == st.session_state.edit_ref].iloc[0]
        st.header(f"Modifica: {watch['model_name']} ({watch['reference']})")
        
        if st.button("← Annulla e torna alla lista"):
            st.session_state.edit_ref = None
            st.rerun()

        tab1, tab2, tab3 = st.tabs(["💎 Estetica", "⚙️ Meccanica", "🚀 Mercato"])
        
        with tab1:
            new_name = st.text_input("Nome Modello", value=watch['model_name'])
            new_mat = st.selectbox("Materiale", ["Steel", "Gold", "Titanium", "Platinum"], index=0)
        with tab2:
            new_res = st.number_input("Riserva (h)", value=int(watch['mov_reserve']))
            new_freq = st.number_input("Frequenza (vph)", value=int(watch['mov_freq']))
        with tab3:
            new_price = st.number_input("Prezzo (€)", value=int(watch['price_estimate']))

        if st.button("💾 Salva Modifiche Permanenti", type="primary"):
            success = db_engine.update_watch_data(st.session_state.edit_ref, {
                "model_name": new_name, "material": new_mat,
                "mov_reserve": new_res, "mov_freq": new_freq,
                "price_estimate": new_price
            })
            if success:
                st.success("Database aggiornato con successo!")
                st.session_state.edit_ref = None
                st.rerun()
    else:
        # --- GRIGLIA CARD ---
        st.header(f"Portfolio: {USER_BRAND_NAME}")
        df = db_engine.get_my_watches()
        cols = st.columns(3)
        for i, (idx, row) in enumerate(df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {row['model_name']}")
                    st.write(f"Ref: {row['reference']} | {row['material']}")
                    st.write(f"**Prezzo: €{row['price_estimate']:,}**")
                    if st.button("📝 Modifica", key=f"btn_{row['reference']}", use_container_width=True):
                        st.session_state.edit_ref = row['reference']
                        st.rerun()
