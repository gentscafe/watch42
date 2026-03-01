import pandas as pd
import numpy as np
import streamlit as st
import os
import random

# --- CONFIGURAZIONE IDENTITÀ ---
# Definiamo il brand che rappresenta l'utente del servizio
USER_BRAND_NAME = "Watch42 Lab"

class WatchDatabase:
    def __init__(self, file_path='watches_database.csv'):
        self.file_path = file_path
        # Schede tecniche reali per i movimenti (Mappatura 1:1)
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
            },
            "Miyota 9015": {
                "mov_brand": "Citizen/Miyota", "mov_ref": "9015", "mov_base": "None",
                "mov_type": "Automatic", "mov_display": "Analog", "mov_diam": 26.00,
                "mov_jewels": 24, "mov_reserve": 42, "mov_freq": 28800,
                "mov_hands": "Hours, Minutes, Seconds", "mov_astro": "Date"
            },
            "NOMOS DUW 3001": {
                "mov_brand": "NOMOS", "mov_ref": "DUW 3001", "mov_base": "In-House",
                "mov_type": "Automatic", "mov_display": "Analog", "mov_diam": 28.80,
                "mov_jewels": 27, "mov_reserve": 43, "mov_freq": 21600,
                "mov_hands": "Hours, Minutes, Seconds", "mov_astro": "None"
            }
        }
        self.df = self.get_or_create_dataset()

    @st.cache_data(show_spinner="Generazione Database Tecnico Watch42...")
    def get_or_create_dataset(_self):
        if os.path.exists(_self.file_path):
            return pd.read_csv(_self.file_path)
        
        # Aggiungiamo il brand dell'utente alla lista dei brand
        brands = [USER_BRAND_NAME, "Mido", "Patek Philippe", "Nomos Glashütte", "F.P. Journe", "H. Moser & Cie"]
        brands += [f"Independent Lab {i}" for i in range(1, 91)]
        
        styles = ["Dress", "Diver", "Chronograph", "GMT", "Pilot/Field"]
        materials = ["Steel", "Titanium", "Gold", "Platinum"]
        versions = ["Series 1", "Mark II", "Limited Edition", "Prototype"]

        data = []
        mov_names = list(_self.MOVEMENT_TECH_SHEETS.keys())

        for brand in brands:
            # Generiamo 50 modelli per ogni brand (incluso quello dell'utente)
            for i in range(1, 51):
                mov_name = random.choice(mov_names)
                tech_sheet = _self.MOVEMENT_TECH_SHEETS[mov_name]
                watch_style = random.choice(styles)
                
                record = {
                    "brand": brand,
                    "model_name": f"{random.choice(['Legacy', 'Heritage', 'Vision'])} {i}",
                    "model_version": random.choice(versions),
                    "reference": f"REF-{brand[:3].upper()}-{random.randint(1000, 9999)}",
                    "watch_style": watch_style,
                    "material": random.choice(materials),
                    "diameter": random.choice([38, 39, 40, 41, 42]),
                    "price_estimate": random.randint(1500, 120000),
                    "img_url": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?q=80&w=300&h=300&auto=format&fit=crop"
                }
                
                record.update(tech_sheet)
                data.append(record)
        
        df = pd.DataFrame(data)
        df.to_csv(_self.file_path, index=False)
        return df

    def filter_data(self, filters=None):
        filtered_df = self.df.copy()
        if not filters: return filtered_df
        for col, val in filters.items():
            if val and col in filtered_df.columns:
                if isinstance(val, list): filtered_df = filtered_df[filtered_df[col].isin(val)]
                elif isinstance(val, tuple): filtered_df = filtered_df[filtered_df[col].between(val[0], val[1])]
                elif isinstance(val, str): filtered_df = filtered_df[filtered_df[col].str.contains(val, case=False)]
        return filtered_df

    def get_my_watches(self):
        """Restituisce esclusivamente gli orologi appartenenti al brand dell'utente"""
        return self.df[self.df['brand'] == USER_BRAND_NAME]

db_engine = WatchDatabase()
