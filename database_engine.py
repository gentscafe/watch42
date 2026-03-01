import pandas as pd
import numpy as np
import streamlit as st
import os
import random

USER_BRAND_NAME = "MY BRAND"

# Funzione esterna alla classe per evitare NameError nella cache
def calc_score(reserve, freq):
    return round((reserve * freq) / 10000, 2)

class WatchDatabase:
    def __init__(self, file_path='watches_v5.csv'): # v5 forza un reset pulito
        self.file_path = file_path
        self.MOVEMENT_TECH_SHEETS = {
            "Mido 72": {"mov_brand": "Mido", "mov_reserve": 72, "mov_freq": 25200, "mov_ref": "Mido 72"},
            "Patek 240 Q": {"mov_brand": "Patek", "mov_reserve": 48, "mov_freq": 21600, "mov_ref": "240 Q"},
            "NH34": {"mov_brand": "Seiko", "mov_reserve": 41, "mov_freq": 21600, "mov_ref": "NH34"}
        }
        self.df = self.get_or_create_dataset()

    @st.cache_data(show_spinner="Generazione Dati...")
    def get_or_create_dataset(_self):
        if os.path.exists(_self.file_path):
            return pd.read_csv(_self.file_path)
        
        brands = [USER_BRAND_NAME, "Patek Philippe", "Rolex", "Mido"]
        brands += [f"Independent {i}" for i in range(1, 90)]
        data = []
        for b in brands:
            for i in range(1, 51):
                m_key = random.choice(list(_self.MOVEMENT_TECH_SHEETS.keys()))
                m = _self.MOVEMENT_TECH_SHEETS[m_key]
                p_score = calc_score(m['mov_reserve'], m['mov_freq'])
                row = {
                    "brand": b, "model_name": f"Model {i}", "reference": f"REF-{random.randint(1000, 9999)}",
                    "material": random.choice(["Steel", "Gold", "Titanium"]), "diameter": random.choice([39, 40, 42]),
                    "price_estimate": random.randint(2000, 50000), "power_score": p_score, **m
                }
                data.append(row)
        df = pd.DataFrame(data)
        df.to_csv(_self.file_path, index=False)
        return df

    def get_my_watches(self):
        return self.df[self.df['brand'] == USER_BRAND_NAME]

db_engine = WatchDatabase()
