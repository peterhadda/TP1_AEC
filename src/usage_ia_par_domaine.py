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

    # On garde uniquement les lignes ou l'IA est utilisee
    mask_ai_used = df[ai_col].astype(str).str.contains(
        r"^\s*(?:Oui,|Yes,)",
        case=False,
        na=False,
        regex=True,
    )

    filtered = df.loc[mask_ai_used, [geo_col, char_col, value_col]].copy()

    # Filtrer seulement les provinces voulues
    wanted = {normalize_text(p) for p in CONFIG["ai_usage_provinces"]}
    filtered = filtered[filtered[geo_col].astype(str).map(normalize_text).isin(wanted)].copy()

    # Enlever la ligne 'ensemble des industries' pour garder le detail par industrie
    filtered = filtered[
        ~filtered[char_col].astype(str).str.contains(
            "ensemble des industries|all industries",
            case=False,
            na=False,
            regex=True,
        )
    ].copy()

    # Garder uniquement les vraies categories d'industries (codes SCIAN entre crochets)
    filtered = filtered[
        filtered[char_col].astype(str).str.contains(r"\[[0-9]{2}(?:-[0-9]{2})?\]", na=False, regex=True)
    ].copy()

    # Exclure des dimensions non-industrielles qui peuvent encore passer dans certains jeux de donnees
    excluded_keywords = [
        "proprietaire",
        "age de l'entreprise",
        "employees",
        "employes",
        "a importe",
        "a exporte",
        "a transfere",
        "activites commerciales internationales",
        "activite de l'entreprise",
    ]
    filtered = filtered[
        ~filtered[char_col].astype(str).map(normalize_text).str.contains("|".join(excluded_keywords), na=False, regex=True)
    ].copy()

    filtered[value_col] = pd.to_numeric(filtered[value_col], errors="coerce")
    filtered = filtered.dropna(subset=[value_col])

    # S'il y a des doublons province + industrie, on garde la premiere
    filtered = filtered.drop_duplicates(subset=[geo_col, char_col], keep="first")

    result = {}
    for _, row in filtered.iterrows():
        province = row[geo_col]
        industry = row[char_col]
        value = float(row[value_col])

        if province not in result:
            result[province] = {}

        result[province][industry] = value

    return result
