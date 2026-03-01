import streamlit as st
from database_engine import db_engine, USER_BRAND_NAME

st.set_page_config(page_title="watch42", layout="wide")

# --- SIDEBAR (Sempre visibile all'inizio) ---
st.sidebar.title(USER_BRAND_NAME)
st.sidebar.subheader("NAVIGAZIONE")
if st.sidebar.button("⌚ My Watches"): 
    st.session_state.nav = "My Watches"
    st.session_state.edit_id = None
    st.rerun()
if st.sidebar.button("📊 Pricing Intelligence"): st.session_state.nav = "Pricing"
st.sidebar.markdown("---")
if st.sidebar.button("🗄️ Watch DB Explorer"): st.session_state.nav = "DB"

# Inizializzazione stati
if 'nav' not in st.session_state: st.session_state.nav = "My Watches"
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# --- LOGICA PAGINA MY WATCHES ---
if st.session_state.nav == "My Watches":
    if st.session_state.edit_id is not None:
        # VISTA MODIFICA
        st.header(f"Modifica: {st.session_state.edit_id}")
        if st.button("← Torna alla lista"):
            st.session_state.edit_id = None
            st.rerun()
        
        # Qui recuperiamo l'orologio per popolare i campi
        # (Aggiungeremo i Tab qui sotto se questa struttura ti convince)
        st.info("Pannello di modifica in costruzione... Salva i file per testare la stabilità.")
        
    else:
        # VISTA GRIGLIA
        st.header(f"Portfolio: {USER_BRAND_NAME}")
        df = db_engine.get_my_watches()
        
        cols = st.columns(3)
        for i, (idx, row) in enumerate(df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{row['model_name']}**")
                    st.write(f"Ref: {row['reference']}")
                    st.write(f"Prezzo: €{row['price_estimate']:,}")
                    
                    if st.button("Modifica", key=f"ed_{idx}", use_container_width=True):
                        st.session_state.edit_id = row['reference']
                        st.rerun()
