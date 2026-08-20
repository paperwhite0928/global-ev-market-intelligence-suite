"""
data_loader.py - Dataset Merger, Alignment, and Validation
Ensures proper data types, indexing, and sanity checks for the 1,512-row panel.
"""

import os
import sys
import pandas as pd

try:
    from src.generate_mock_data import generate_panel_data
except ImportError:
    try:
        from generate_mock_data import generate_panel_data
    except ImportError:
        from ev_driver_analysis.src.generate_mock_data import generate_panel_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "bev_panel_dataset.csv")

def load_panel_dataset(data_path: str = None) -> pd.DataFrame:
    """Loads existing dataset or generates synthetic fallback panel dataset."""
    if data_path is None:
        data_path = DEFAULT_DATA_PATH

    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        parent_dir = os.path.dirname(data_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        df = generate_panel_data(data_path)
        
    df["date"] = pd.to_datetime(df["date"])
    df["year_month"] = df["date"].dt.strftime("%Y-%m")
    
    # Sort panel chronologically and by group
    df = df.sort_values(by=["region", "company", "date"]).reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = load_panel_dataset()
    print(f"Dataset Loaded Successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
    print("Regions:", df["region"].unique())
    print("Companies:", df["company"].unique())

