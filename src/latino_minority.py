import io
import zipfile
from urllib.request import urlopen

import pandas as pd

from config import CONFIG


FRENCH_PROVINCES = [
    "Terre-Neuve-et-Labrador",
    "Île-du-Prince-Édouard",
    "Nouvelle-Écosse",
    "Nouveau-Brunswick",
    "Québec",
    "Ontario",
    "Manitoba",
    "Saskatchewan",
    "Alberta",
    "Colombie-Britannique",
]

LATINO_COLUMN = "Minorité visible (15):Latino-Américain[8]"
AGE_COLUMN = "Âge (15C)"
GENDER_COLUMN = "Genre (3)"
STATS_COLUMN = "Statistiques (2)"
PROVINCE_COLUMN = "GÉO"


def charger_table_source():
    with urlopen(CONFIG["latino_population_download_url"]) as response:
        archive = zipfile.ZipFile(io.BytesIO(response.read()))
        with archive.open("98100351.csv") as csv_file:
            return pd.read_csv(csv_file, sep=";", encoding="utf-8")


def nettoyer_nombre(valeur):
    if pd.isna(valeur):
        return None

    return int(float(valeur))


def run():
    df = charger_table_source()

    filtres = (
        df[AGE_COLUMN].eq("Total - Âge")
        & df[GENDER_COLUMN].eq("Total - Genre")
        & df[STATS_COLUMN].eq("Chiffres de 2021")
        & df[PROVINCE_COLUMN].isin(FRENCH_PROVINCES)
    )

    resultat = df.loc[filtres, [PROVINCE_COLUMN, LATINO_COLUMN]].copy()
    resultat.columns = ["province", "latino_americain"]
    resultat["latino_americain"] = resultat["latino_americain"].apply(nettoyer_nombre)

    return resultat.reset_index(drop=True)


if __name__ == "__main__":
    print()
