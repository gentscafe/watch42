import pandas as pd
import numpy as np
import streamlit as st
import os
import random

USER_BRAND_NAME = "MY BRAND"

class WatchDatabase:
    def __init__(self, file_path='watches_final.csv'):
        self.file_path = file_path
        # Schede tecniche base per garantire dati reali
        self.TECH_POOL = [
            {"mov_brand": "Mido", "mov_reserve": 72, "mov_freq": 25200, "mov_ref": "Mido 72", "case_thickness": 11.5},
            {"mov_brand": "Patek", "mov_reserve": 48, "mov_freq": 21600, "mov_ref": "240 Q", "case_thickness": 8.8},
            {"mov_brand": "Seiko", "mov_reserve": 41, "mov_freq": 21600, "mov_ref": "NH34", "case_thickness": 13.2},
            {"mov_brand": "ETA", "mov_reserve": 80, "mov_freq": 28800, "mov_ref": "Powermatic", "case_thickness": 10.5}
        ]
        self.df = self.get_or_create_dataset()

    @st.cache_data(show_spinner="Sincronizzazione Mercato...")
    def get_or_create_dataset(_self):
        if os.path.exists(_self.file_path):
            return pd.read_csv(_self.file_path)
        
        brands = [USER_BRAND_NAME, "Patek Philippe", "Rolex", "Mido", "Cartier", "Omega", "Zenith"]
        brands += [f"Indie Brand {i}" for i in range(1, 50)]
        
        data = []
        for b in brands:
            # Generiamo modelli con prezzi e caratteristiche varie
            for i in range(1, 15):
                tech = random.choice(_self.TECH_POOL)
                row = {
                    "brand": b,
                    "model_name": f"Vision {i}",
                    "reference": f"REF-{random.randint(1000, 9999)}",
                    "material": random.choice(["Steel", "Gold", "Titanium"]),
                    "diameter": random.choice([38, 39, 40, 41, 42]),
                    "price_estimate": random.randint(2000, 60000),
                    # Campi fondamentali per l'asse Y del grafico
                    "mov_reserve": tech["mov_reserve"],
                    "case_thickness": tech["case_thickness"],
                    "mov_freq": tech["mov_freq"],
                    "power_score": round((tech["mov_reserve"] * tech["mov_freq"]) / 10000, 2)
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
