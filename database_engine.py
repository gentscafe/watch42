import pandas as pd
import numpy as np
import streamlit as st
import os
import random

USER_BRAND_NAME = "MY BRAND"

class WatchDatabase:
    def __init__(self, file_path='watches_ULTIMATE.csv'):
        self.file_path = file_path
        self.df = self.get_or_create_dataset()

    @st.cache_data(show_spinner="Reset e Sincronizzazione Dati...")
    def get_or_create_dataset(_self):
        # Se il file esiste, lo carichiamo e forziamo i tipi numerici
        if os.path.exists(_self.file_path):
            df = pd.read_csv(_self.file_path)
        else:
            # Generazione forzata di 1000 record con colonne garantite
            brands = [USER_BRAND_NAME, "Patek Philippe", "Rolex", "Mido", "Omega"]
            brands += [f"Competitor {i}" for i in range(1, 50)]
            
            data = []
            for b in brands:
                for i in range(1, 15):
                    res = float(random.choice([42, 48, 70, 72]))
                    thk = float(round(random.uniform(8.0, 15.0), 1))
                    price = float(random.randint(2000, 50000))
                    
                    data.append({
                        "brand": b,
                        "model_name": f"Model {i}",
                        "reference": f"REF-{b[:3].upper()}-{random.randint(100, 999)}",
                        "material": random.choice(["Steel", "Gold", "Titanium"]),
                        "price_estimate": price,
                        "mov_reserve": res,
                        "case_thickness": thk,
                        "power_score": float(round((res * 28800) / 10000, 2))
                    })
            df = pd.DataFrame(data)
            df.to_csv(_self.file_path, index=False)
        
        # OPERAZIONE CRUCIALE: Forza la conversione numerica prima di restituire il DF
        for col in ['price_estimate', 'mov_reserve', 'case_thickness', 'power_score']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
        return df

    def update_watch_data(self, reference, updated_data):
        idx = self.df.index[self.df['reference'] == reference].tolist()
        if idx:
            for key, value in updated_data.items():
                self.df.at[idx[0], key] = value
            self.df.to_csv(self.file_path, index=False)
            return True
        return False

    def get_my_watches(self):
        return self.df[self.df['brand'] == USER_BRAND_NAME]

db_engine = WatchDatabase()
