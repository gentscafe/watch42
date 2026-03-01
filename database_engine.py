import pandas as pd
import numpy as np
import streamlit as st
import os
import random

class WatchDatabase:
    def __init__(self, file_path='watches_database.csv'):
        self.file_path = file_path
        # Inizializza il dataframe caricandolo dal CSV o generandolo
        self.df = self.get_or_create_dataset()

    @st.cache_data(show_spinner="Sincronizzazione Database Watch42...")
    def get_or_create_dataset(_self):
        """
        Controlla se esiste il database locale. 
        Se non esiste, genera 5.000 record mock ottimizzati per un'app di orologeria.
        """
        if os.path.exists(_self.file_path):
            df = pd.read_csv(_self.file_path)
        else:
            # Configurazione parametri per la generazione
            brands = ["Patek Philippe", "F.P. Journe", "H. Moser & Cie", "MB&F", "De Bethune", 
                      "Urwerk", "Ressence", "Voutilainen", "Akrivia", "Grönefeld"]
            # Aggiungiamo 90 brand indipendenti fittizi per arrivare a 100
            brands += [f"Indie Maker {i}" for i in range(1, 91)]
            
            styles = ["Dress", "Diver", "Chronograph", "GMT", "Pilot/Field", "Artistic", "Skeleton"]
            materials = ["Steel", "Titanium", "Rose Gold", "Platinum", "Tantalum", "Ceramic"]
            mov_types = ["Manual Wind", "Automatic", "Manual Wind"] # Più manuali per il settore Indie
            mov_origins = ["In-House", "In-House", "Boutique Manufacture", "Modified ETA", "Sellita Based"]
            complications = ["None", "Date", "Moonphase", "Tourbillon", "Perpetual Calendar", "Power Reserve"]
            
            # URL Mock per il Designer (immagini placeholder basate sullo stile)
            img_placeholders = {
                "Dress": "https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?q=80&w=300&h=300&auto=format&fit=crop",
                "Diver": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?q=80&w=300&h=300&auto=format&fit=crop",
                "Chronograph": "https://images.unsplash.com/photo-1547996160-81dfa63595dd?q=80&w=300&h=300&auto=format&fit=crop",
                "GMT": "https://images.unsplash.com/photo-1526045431048-f857369aba09?q=80&w=300&h=300&auto=format&fit=crop",
                "Pilot/Field": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?q=80&w=300&h=300&auto=format&fit=crop",
                "Artistic": "https://images.unsplash.com/photo-1619134778706-7015533a6150?q=80&w=300&h=300&auto=format&fit=crop",
                "Skeleton": "https://images.unsplash.com/photo-1639037687665-98314545239a?q=80&w=300&h=300&auto=format&fit=crop"
            }

            data = []
            for brand in brands:
                # 50 modelli per ogni brand = 5.000 record totali
                for i in range(1, 51):
                    watch_style = random.choice(styles)
                    data.append({
                        "brand": brand,
                        "model_name": f"{random.choice(['Legacy', 'Endeavour', 'Horizon', 'Epoch'])} {i}",
                        "reference": f"REF-{brand[:3].upper()}-{random.randint(1000, 9999)}",
                        "watch_style": watch_style,
                        "material": random.choice(materials),
                        "diameter": random.choice([36, 37, 38, 39, 40, 41, 42]),
                        "movement_type": random.choice(mov_types),
                        "movement_origin": random.choice(mov_origins),
                        "complication": random.choice(complications),
                        "price_estimate": random.randint(5000, 250000),
                        "img_url": img_placeholders[watch_style]
                    })
            
            df = pd.DataFrame(data)
            df.to_csv(_self.file_path, index=False)
        return df

    def filter_data(self, filters=None):
        """
        Metodo principale per il Web Designer.
        Esempio d'uso: filter_data({'brand': ['Rolex'], 'diameter': (38, 40)})
        """
        filtered_df = self.df.copy()
        
        if not filters:
            return filtered_df

        for column, value in filters.items():
            if value and column in filtered_df.columns:
                # Gestione Multi-select (liste)
                if isinstance(value, list) and len(value) > 0:
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
                # Gestione Range (tuple per slider numerici)
                elif isinstance(value, tuple):
                    filtered_df = filtered_df[filtered_df[column].between(value[0], value[1])]
                # Gestione Ricerca Testuale (stringhe)
                elif isinstance(value, str) and value != "":
                    filtered_df = filtered_df[filtered_df[column].str.contains(value, case=False, na=False)]
        
        return filtered_df

# Istanza globale pronta per essere importata in app.py
db_engine = WatchDatabase()
