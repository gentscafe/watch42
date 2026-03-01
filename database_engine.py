import pandas as pd
import numpy as np
import streamlit as st
import os
import random

# --- CONFIGURAZIONE IDENTITÀ ---
# Il nome esatto che apparirà in "My Watches"
USER_BRAND_NAME = "MY BRAND"

class WatchDatabase:
    def __init__(self, file_path='watches_v3.csv'):
        self.file_path = file_path
        self.MOVEMENT_TECH_SHEETS = {
            "Mido 72": {
                "mov_brand": "Mido", "mov_ref": "Mido 72", "mov_base": "ETA A31.111",
                "mov_type": "Automatic", "mov_display": "Analog", "mov_diam": 25.60,
                "mov_jewels": 21, "mov_reserve": 72, "mov_freq": 25200,
                "mov_hands": "Hours, Minutes, Seconds", "mov_astro": "Moonphase"
            },
            "Patek 240 Q": {
                "mov_brand": "Patek Philippe", "mov_ref": "240 Q", "mov_base": "In-House",
                "mov_type": "Automatic", "mov_display": "Analog", "mov_diam": 27.50,
                "mov_jewels": 27, "mov_reserve": 48, "mov_freq": 21600,
                "mov_hands": "Hours, Minutes, Seconds, 24h", "mov_astro": "Perpetual Calendar"
            },
            "NH34": {
                "mov_brand": "Seiko", "mov_ref": "NH34", "mov_base": "4R34",
                "mov_type": "Automatic", "mov_display": "Analog", "mov_diam": 27.40,
                "mov_jewels": 24, "mov_reserve": 41, "mov_freq": 21600,
                "mov_hands": "Hours, Minutes, Seconds, GMT", "mov_astro": "None"
            }
        }
        self.df = self.get_or_create_dataset()

    def calculate_power_score(self, reserve, frequency):
        return round((reserve * frequency) / 10000, 2)

    @st.cache_data(show_spinner="Generazione Ecosistema MY BRAND...")
    def get_or_create_dataset(_self):
        if os.path.exists(_self.file_path):
            return pd.read_csv(_self.file_path)
        
        # Inseriamo 'MY BRAND' nella lista
        brands = [USER_BRAND_NAME, "Patek Philippe", "Rolex", "Mido", "Nomos Glashütte"]
        brands += [f"Independent Lab {i}" for i in range(1, 95)]
        
        data = []
        mov_names = list(_self.MOVEMENT_TECH_SHEETS.keys())

        for brand in brands:
            for i in range(1, 51):
                mov_name = random.choice(mov_names)
                tech = _self.MOVEMENT_TECH_SHEETS[mov_name]
                thickness = round(random.uniform(7.0, 15.0), 1)
                p_score = self.calculate_power_score(tech['mov_reserve'], tech['mov_freq'])
                
                record = {
                    "brand": brand,
                    "model_name": f"Model {i}",
                    "reference": f"REF-{brand[:3].upper()}-{random.randint(1000, 9999)}",
                    "material": random.choice(["Steel", "Gold", "Titanium"]),
                    "diameter": random.choice([38, 40, 42]),
                    "case_thickness": thickness,
                    "power_score": p_score,
                    "price_estimate": random.randint(2000, 80000),
                    "img_url": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?q=80&w=300"
                }
                record.update(tech)
                data.append(record)
        
        df = pd.DataFrame(data)
        df.to_csv(_self.file_path, index=False)
        return df

    def get_my_watches(self):
        return self.df[self.df['brand'] == USER_BRAND_NAME]

db_engine = WatchDatabase()
