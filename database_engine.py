import pandas as pd
import streamlit as st
import os

USER_BRAND_NAME = "MY BRAND"

class WatchDatabase:
    def __init__(self, file_path='db-watches.csv'):
        self.file_path = file_path
        self.df = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
            # Pulizia colonne numeriche per evitare grafici vuoti
            cols = ['price_estimate', 'mov_reserve', 'case_thickness', 'power_score']
            for col in cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            return df
        else:
            st.error(f"Errore: Il file {self.file_path} non è presente su GitHub.")
            return pd.DataFrame()

    def update_watch_data(self, reference, updated_data):
        idx = self.df.index[self.df['reference'] == reference].tolist()
        if idx:
            for key, value in updated_data.items():
                if key in self.df.columns:
                    self.df.at[idx[0], key] = value
            self.df.to_csv(self.file_path, index=False)
            return True
        return False

db_engine = WatchDatabase()
