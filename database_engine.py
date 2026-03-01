import pandas as pd
import numpy as np
import streamlit as st
import os
import random

USER_BRAND_NAME = "MY BRAND"

class WatchDatabase:
    def __init__(self, file_path='watches_final_v2.csv'):
        self.file_path = file_path
        self.df = self.get_or_create_dataset()

    @st.cache_data(show_spinner="Generazione dati di mercato...")
    def get_or_create_dataset(_self):
        if os.path.exists(_self.file_path):
            return pd.read_csv(_self.file_path)
        
        brands = [USER_BRAND_NAME, "Patek Philippe", "Rolex", "Mido", "Omega", "Cartier"]
        brands += [f"Indie Brand {i}" for i in range(1, 60)]
        
        data = []
        for b in brands:
            for i in range(1, 15):
                # Generiamo valori casuali ma coerenti
                reserve = random.choice([42, 48, 70, 72, 80])
                freq = random.choice([21600, 25200, 28800])
                thickness = round(random.uniform(8.5, 14.5), 1)
                
                row = {
                    "brand": b,
                    "model_name": f"Vision {i}",
                    "reference": f"REF-{random.randint(1000, 9999)}",
                    "material": random.choice(["Steel", "Gold", "Titanium"]),
                    "price_estimate": random.randint(2000, 65000),
                    "mov_reserve": reserve,
                    "case_thickness": thickness,
                    "mov_freq": freq,
                    "power_score": round((reserve * freq) / 10000, 2)
                }
                data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(_self.file_path, index=False)
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
