import streamlit as st
from database_engine import db_engine, USER_BRAND_NAME

# ... (Configurazione Pagina e CSS invariati) ...

# SIDEBAR
st.sidebar.markdown(f'<div style="padding: 20px; color: #2E5BFF; font-weight: 800; font-size: 20px;">{USER_BRAND_NAME}</div>', unsafe_allow_html=True)

if st.session_state.nav == "My Watches":
    st.header(f"Dashboard Proprietaria: {USER_BRAND_NAME}")
    
    # Filtriamo gli orologi di MY BRAND
    my_watches_df = db_engine.get_my_watches()
    
    if my_watches_df.empty:
        st.warning(f"Database in aggiornamento... Se non vedi orologi, attendi la fine della generazione di '{USER_BRAND_NAME}'.")
    else:
        # Visualizzazione Card (Logica a 3 colonne)
        cols = st.columns(3)
        for i, (idx, row) in enumerate(my_watches_df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    # Qui va il tuo template HTML delle card
                    st.write(f"**{row['model_name']}**")
                    st.write(f"Prezzo Stimato: €{row['price_estimate']:,}")
                    if st.button("Modifica", key=f"btn_{idx}"):
                        st.session_state.edit_id = idx
                        st.rerun()
