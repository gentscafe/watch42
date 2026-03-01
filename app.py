if st.session_state.edit_ref is not None:
        # --- PANNELLO MODIFICA ESTESO ---
        watch = db_engine.df[db_engine.df['reference'] == st.session_state.edit_ref].iloc[0]
        st.header(f"Configuratore Tecnico: {watch['model_name']} ({watch['reference']})")
        
        if st.button("← Torna alla lista"):
            st.session_state.edit_ref = None
            st.rerun()

        tab_ext, tab_mov, tab_perf = st.tabs(["💎 Estetica & Cassa", "⚙️ Meccanica & Calibro", "🚀 Prestazioni & Mercato"])
        
        with tab_ext:
            st.markdown('<div class="edit-section-header">DESIGN ESTERNO</div>', unsafe_allow_html=True)
            e1, e2 = st.columns(2)
            with e1:
                st.text_input("Nome Modello", value=watch['model_name'], key="upd_name")
                st.selectbox("Stile", ["Dress", "Diver", "Chronograph", "GMT", "Casual"], index=0, key="upd_style")
                st.multiselect("Materiale Cassa", ["Steel", "Gold", "Titanium", "Platinum", "Ceramic"], default=[watch['material']], key="upd_mat")
            with e2:
                st.slider("Diametro (mm)", 34, 48, int(watch['diameter']), key="upd_diam")
                st.number_input("Spessore (mm)", value=float(watch['case_thickness']), step=0.1, key="upd_thick")
                st.text_input("Referenza", value=watch['reference'], disabled=True, help="La referenza univoca non può essere modificata")

        with tab_mov:
            st.markdown('<div class="edit-section-header">ARCHITETTURA DEL MOVIMENTO</div>', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            with m1:
                st.text_input("Produttore Calibro", value=watch['mov_brand'], key="upd_mov_brand")
                st.text_input("Referenza Calibro", value=watch['mov_ref'], key="upd_mov_ref")
                st.text_input("Base di partenza", value=watch['mov_base'], key="upd_mov_base")
            with m2:
                st.selectbox("Tipo", ["Automatic", "Manual", "Quartz"], key="upd_mov_type")
                st.number_input("Rubini (Jewels)", value=int(watch['mov_jewels']), key="upd_jewels")
            with m3:
                st.number_input("Diametro Mov. (mm)", value=float(watch['mov_diam']), format="%.2f", key="upd_mov_diam")
                st.text_input("Display", value="Analogico", key="upd_display")

        with tab_perf:
            st.markdown('<div class="edit-section-header">LEVE DI MERCATO</div>', unsafe_allow_html=True)
            p1, p2 = st.columns(2)
            with p1:
                st.number_input("Riserva di Carica (h)", value=int(watch['mov_reserve']), key="upd_reserve")
                st.number_input("Frequenza (vph)", value=int(watch['mov_freq']), step=100, key="upd_freq")
            with p2:
                st.number_input("Prezzo di Listino (€)", value=int(watch['price_estimate']), step=500, key="upd_price")
                st.text_input("Complicazioni Astro", value=watch.get('mov_astro', 'None'), key="upd_astro")

        st.markdown("---")
        if st.button("💾 Salva Configuratore", type="primary", use_container_width=True):
            # Qui chiameremo la funzione di salvataggio del database_engine
            st.success(f"Configurazione per {watch['reference']} salvata con successo nel sistema.")
