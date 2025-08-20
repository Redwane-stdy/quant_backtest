import yfinance as yf
import pandas as pd
import logging

def get_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Télécharge les données de marché depuis Yahoo Finance.
    Si échec => fallback vers données simulées.
    """
    try:
        df = yf.download(symbol, start=start, end=end, progress=False)
        if df.empty:
            raise ValueError("Aucune donnée téléchargée.")
        df = df[["Open", "High", "Low", "Close", "Volume"]]
        df.reset_index(inplace=True)
        df.rename(columns={"Date": "datetime"}, inplace=True)
        return df
    except Exception as e:
        logging.warning(f"Échec du téléchargement des données : {e}")
        from data.sample_data import generate_sample_data
        return generate_sample_data(start, end)
