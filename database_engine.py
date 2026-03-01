import pandas as pd
import streamlit as st
import os

# --- CONFIGURAZIONE IDENTITÀ ---
USER_BRAND_NAME = "MY BRAND"

class WatchDatabase:
    def __init__(self, file_path='db-watches.csv'):
        self.file_path = file_path
        self.df = self.load_data()

    def load_data(self):
        """Carica il database dal file CSV fornito"""
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
            # Rimuoviamo colonne indice superflue se presenti
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])
            
            # Assicuriamo che i tipi numerici siano corretti
            cols_to_fix = ['price_estimate', 'mov_reserve', 'case_thickness', 'mov_freq', 'power_score']
            for col in cols_to_fix:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            return df
        else:
            st.error(f"File {self.file_path} non trovato!")
            return pd.DataFrame()

    def update_watch_data(self, reference, updated_data):
        """Salva le modifiche direttamente sul file CSV"""
        idx = self.df.index[self.df['reference'] == reference].tolist()
        if idx:
            for key, value in updated_data.items():
                if key in self.df.columns:
                    self.df.at[idx[0], key] = value
            
            # Ricalcolo automatico del Power Score se cambiano i dati tecnici
            res = self.df.at[idx[0], 'mov_reserve']
            freq = self.df.at[idx[0], 'mov_freq']
            # Formula: (Riserva * Frequenza) / 10.000
            self.df.at[idx[0], 'power_score'] = round((res * freq) / 10000, 2)
            
            self.df.to_csv(self.file_path, index=False)
            return True
        return False

    def get_my_watches(self):
        """Filtra solo gli orologi del brand utente"""
        return self.df[self.df['brand'] == USER_BRAND_NAME]

db_engine = WatchDatabase()
