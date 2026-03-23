import io
import zipfile
import unicodedata

import pandas as pd
import requests

from config import CONFIG


def normalize_text(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", str(text))
    without_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    normalized = without_accents.replace(" ", " ").replace("’", "'").strip().lower()
    return " ".join(normalized.split())


def find_column(columns, candidates):
    for col in columns:
        col_norm = normalize_text(col)
        for candidate in candidates:
            if candidate in col_norm:
                return col
    return None


def run():
    response = requests.get(CONFIG["ai_usage_zip_url"], timeout=60)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        csv_name = next(
            name
            for name in archive.namelist()
            if name.lower().endswith(".csv") and "metadata" not in name.lower()
        )
        with archive.open(csv_name) as file_obj:
            df = pd.read_csv(file_obj, encoding="utf-8-sig", sep=";")

    columns = list(df.columns)

    geo_col = find_column(columns, ["geo", "geographie", "geography"])
    value_col = find_column(columns, ["valeur", "value", "estimate"])
    ai_col = find_column(columns, ["intelligence artificielle", "artificial intelligence"])
    char_col = find_column(columns, ["caracteristiques de l'entreprise", "business characteristics"])

    if geo_col is None:
        raise ValueError("Impossible de trouver la colonne geographie.")
    if value_col is None:
        raise ValueError("Impossible de trouver la colonne valeur.")
    if ai_col is None:
        raise ValueError("Impossible de trouver la colonne d'utilisation IA.")
    if char_col is None:
        raise ValueError("Impossible de trouver la colonne de caracteristiques d'entreprise.")

    mask_ai_used = df[ai_col].astype(str).str.contains(
        r"^\s*(?:Oui,|Yes,)",
        case=False,
        na=False,
        regex=True,
    )

    mask_all_industries = df[char_col].astype(str).str.contains(
        "ensemble des industries|all industries",
        case=False,
        na=False,
        regex=True,
    )

    filtered = df.loc[mask_ai_used & mask_all_industries, [geo_col, value_col]].copy()

    wanted = {normalize_text(p) for p in CONFIG["ai_usage_provinces"]}
    filtered = filtered[filtered[geo_col].astype(str).map(normalize_text).isin(wanted)].copy()

    filtered[value_col] = pd.to_numeric(filtered[value_col], errors="coerce")
    filtered = filtered.dropna(subset=[value_col])
    filtered = filtered.drop_duplicates(subset=[geo_col], keep="first")

    return dict(zip(filtered[geo_col], filtered[value_col]))
