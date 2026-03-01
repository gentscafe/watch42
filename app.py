# --- GRIGLIA CARD OTTIMIZZATA ---
if my_watches_df.empty:
    st.info(f"Nessun orologio trovato per il brand {USER_BRAND_NAME}. Genera il database o aggiungi prodotti.")
else:
    # Mostriamo gli orologi in una griglia a 3 colonne
    cols = st.columns(3)
    for i, (idx, row) in enumerate(my_watches_df.iterrows()):
        with cols[i % 3]:
            # Container della Card
            with st.container(border=True):
                # Immagine e Info Principali
                st.markdown(f"""
                <div style="height:120px; background-color:#F3F4F6; border-radius:15px; display:flex; justify-content:center; align-items:center; font-size:40px;">⌚</div>
                <div style="font-weight:700; font-size:17px; margin-top:15px; color:#111827;">{row['model_name']}</div>
                <div style="color:#6B7280; font-size:12px; margin-bottom:10px;">Ref: {row['reference']}</div>
                
                <div class="info-grid">
                    <div class="info-row"><span class="info-label">Materiale</span><span class="info-value">{row['material']}</span></div>
                    <div class="info-row"><span class="info-label">Diametro</span><span class="info-value">{row['diameter']}mm</span></div>
                    <div class="info-row"><span class="info-label">Riserva</span><span class="info-value">{row['mov_reserve']}h</span></div>
                    <div class="info-row"><span class="info-label">Prezzo</span><span class="info-value">€{row['price_estimate']:,}</span></div>
                </div>
                """, unsafe_allow_html=True)
                
                # Pulsanti d'azione
                btn_col1, btn_col2 = st.columns(2)
                
                # Il pulsante Modifica imposta l'ID nella sessione e ricarica
                if btn_col1.button("📝 Modifica", key=f"edit_btn_{idx}", use_container_width=True):
                    st.session_state.edit_id = idx
                    st.rerun()
                
                if btn_col2.button("🎯 Target", key=f"target_btn_{idx}", use_container_width=True):
                    st.toast(f"Target impostato: {row['model_name']}")
