import pandas as pd
import numpy as np
import streamlit as st
import os
import random

USER_BRAND_NAME = "MY BRAND"

class WatchDatabase:
    def __init__(self, file_path='watches_v11_fix.csv'):
        self.file_path = file_path
        self.df = self.get_or_create_dataset()

    @st.cache_data(show_spinner="Validazione Dati...")
    def get_or_create_dataset(_self):
        if os.path.exists(_self.file_path):
            df = pd.read_csv(_self.file_path)
        else:
            brands = [USER_BRAND_NAME, "Patek Philippe", "Rolex", "Mido", "Omega", "Cartier", "Zenith", "IWC"]
            brands += [f"Brand Indie {i}" for i in range(1, 40)]
            data = []
            for b in brands:
                for i in range(1, 12):
                    res = float(random.choice([42, 48, 70, 72, 80]))
                    thk = float(round(random.uniform(8.0, 15.0), 1))
                    data.append({
                        "brand": b,
                        "model_name": f"Vision {i}",
                        "reference": f"REF-{random.randint(1000, 9999)}",
                        "material": random.choice(["Steel", "Gold", "Titanium", "Platinum"]),
                        "price_estimate": float(random.randint(3000, 70000)),
                        "mov_reserve": res,
                        "case_thickness": thk,
                        "mov_freq": float(random.choice([21600, 25200, 28800])),
                        "power_score": float(round((res * 2.8), 1))
                    })
            df = pd.DataFrame(data)
            df.to_csv(_self.file_path, index=False)
        
        # FORZATURA TIPI DATI (Risolve il problema del grafico vuoto)
        cols_float = ['price_estimate', 'mov_reserve', 'case_thickness', 'mov_freq', 'power_score']
        for col in cols_float:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
        return df

    def update_watch_data(self, reference, updated_data):
        idx = self.df.index[self.df['reference'] == reference].tolist()
        if idx:
            for key, value in updated_data.items():
                self.df.at[idx[0], key] = value
            self.df.to_csv(self.file_path, index=False)
            st.cache_data.clear()
            return True
        return False

db_engine = WatchDatabase()
