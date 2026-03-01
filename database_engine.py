import pandas as pd
import numpy as np
import streamlit as st
import os
import random

class WatchDatabase:
    def __init__(self, file_path='watches_database.csv'):
        self.file_path = file_path
        # Carichiamo i dati all'inizializzazione
        self.df = self.get_get_or_create_dataset()

    @st.cache_data(show_spinner="Caricamento database Watch42...")
    def get_get_or_create_dataset(_self):
        """
        Gestisce la persistenza e il caricamento dei dati.
        Usa st.cache_data per evitare di rigenerare/rileggere il CSV inutilmente.
        """
        if os.path.exists(_self.file_path):
            df = pd.read_csv(_self.file_path)
        else:
            # Generazione Mock Data Avanzata
            brands = ["Rolex", "Patek Philippe", "Oris", "Nomos", "F.P. Journe", "H. Moser & Cie", "MB&F"] 
            brands += [f"Independent Lab {i}" for i in range(1, 94)]
            
            styles = ["Dress", "Diver", "Chronograph", "GMT", "Pilot/Field", "Minimalist"]
            materials = ["Steel", "Titanium", "Rose Gold", "Platinum", "Ceramic"]
            complications = ["None", "Date", "Moonphase", "Tourbillon", "Perpetual Calendar"]

            data = []
            for brand in brands:
                # Generiamo circa 50 referenze per brand per arrivare a ~5000 record
                for i in range(1, 51):
                    diameter_val = random.choice([36, 38, 39, 40, 41, 42, 44])
                    data.append({
                        "brand": brand,
                        "model_name": f"{random.choice(['Heritage', 'Endeavour', 'Legacy', 'Pro'])} {i}",
                        "reference": f"REF-{brand[:3].upper()}-{random.randint(1000, 9999)}",
                        "watch_style": random.choice(styles),
                        "material": random.choice(materials),
                        "diameter": diameter_val,  # Salvato come int per facilitare i filtri
                        "complication": random.choice(complications),
                        "price_estimate": random.randint(2000, 150000)
                    })
            
            df = pd.DataFrame(data)
            df.to_csv(_self.file_path, index=False)
        return df

    def filter_data(self, filters=None):
        """
        Funzione helper per il Designer.
        Accetta un dizionario di filtri (es. {'brand': 'Rolex', 'diameter': (38, 40)})
        """
        filtered_df = self.df.copy()
        
        if not filters:
            return filtered_df

        for column, value in filters.items():
            if value and column in filtered_df.columns:
                if isinstance(value, list): # Multi-select
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
                elif isinstance(value, tuple): # Range (es. diametro o prezzo)
                    filtered_df = filtered_df[filtered_df[column].between(value[0], value[1])]
                else: # Valore singolo
                    filtered_df = filtered_df[filtered_df[column] == value]
        
        return filtered_df

# Singleton per l'accesso globale
db_engine = WatchDatabase()
