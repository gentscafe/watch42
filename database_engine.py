import pandas as pd
import numpy as np
import streamlit as st
import os
import random

USER_BRAND_NAME = "MY BRAND"

class WatchDatabase:
    def __init__(self, file_path='watches_v7.csv'):
        self.file_path = file_path
        self.MOVEMENT_TECH_SHEETS = {
            "Mido 72": {"mov_brand": "Mido", "mov_reserve": 72, "mov_freq": 25200, "mov_ref": "Mido 72", "mov_base": "ETA", "mov_type": "Automatic", "mov_diam": 25.6, "mov_jewels": 21},
            "Patek 240 Q": {"mov_brand": "Patek", "mov_reserve": 48, "mov_freq": 21600, "mov_ref": "240 Q", "mov_base": "In-house", "mov_type": "Automatic", "mov_diam": 27.5, "mov_jewels": 27},
            "NH34": {"mov_brand": "Seiko", "mov_reserve": 41, "mov_freq": 21600, "mov_ref": "NH34", "mov_base": "4R34", "mov_type": "Automatic", "mov_diam": 27.4, "mov_jewels": 24}
        }
        self.df = self.get_or_create_dataset()

    @st.cache_data(show_spinner="Sincronizzazione Database...")
    def get_or_create_dataset(_self):
        if os.path.exists(_self.file_path):
            return pd.read_csv(_self.file_path)
        
        brands = [USER_BRAND_NAME, "Patek Philippe", "Rolex", "Mido", "Nomos"]
        brands += [f"Indie Brand {i}" for i in range(1, 80)]
        data = []
        for b in brands:
            for i in range(1, 15):
                m_key = random.choice(list(_self.MOVEMENT_TECH_SHEETS.keys()))
                m = _self.MOVEMENT_TECH_SHEETS[m_key]
                row = {
                    "brand": b, "model_name": f"Vision {i}", "reference": f"REF-{random.randint(1000, 9999)}",
                    "material": random.choice(["Steel", "Gold", "Titanium"]), "diameter": random.choice([39, 40, 42]),
                    "case_thickness": round(random.uniform(9, 14), 1), "price_estimate": random.randint(3000, 50000),
                    "watch_style": random.choice(["Diver", "Dress", "GMT"]), **m
                }
                data.append(row)
        df = pd.DataFrame(data)
        df.to_csv(_self.file_path, index=False)
        return df

    def update_watch_data(self, reference, updated_data):
        """Salva permanentemente le modifiche nel CSV"""
        idx = self.df.index[self.df['reference'] == reference].tolist()
        if idx:
            for key, value in updated_data.items():
                self.df.at[idx[0], key] = value
            self.df.to_csv(self.file_path, index=False)
            st.cache_data.clear() # Forza il ricaricamento dei dati
            return True
        return False

    def get_my_watches(self):
        return self.df[self.df['brand'] == USER_BRAND_NAME]

db_engine = WatchDatabase()
