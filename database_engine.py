import pandas as pd
import os
import random

DB_FILE = 'watches_database.csv'

def generate_mock_data():
    """Genera 5000 record di orologi se il database non esiste."""
    brands = ["Rolex", "Patek Philippe", "Audemars Piguet", "Oris", "Nomos"] + [f"Indie_Brand_{i}" for i in range(1, 96)]
    styles = ["Dress", "Diver", "Chronograph", "Casual", "Pilot/Field", "GMT", "Digital"]
    
    data = []
    for brand in brands:
        for i in range(1, 51):
            data.append({
                "watch_style": random.choice(styles),
                "brand": brand,
                "model_name": f"Edition {i}",
                "reference": f"REF-{random.randint(100, 999)}",
                "material": random.choice(["Steel", "Titanium", "Gold"]),
                "diameter": f"{random.choice([38, 40, 42])}mm"
            })
    df = pd.DataFrame(data)
    df.to_csv(DB_FILE, index=False)
    return df

def get_watch_dataset():
    """Funzione principale per recuperare i dati."""
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return generate_mock_data()
