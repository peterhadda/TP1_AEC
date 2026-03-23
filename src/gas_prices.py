from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import requests

from config import CONFIG


FUEL_TYPE = "Essence ordinaire sans plomb aux stations libre-service"
CSV_NAME = "18100001.csv"
PROVINCE_PATTERNS = [
    ("Terre-Neuve-et-Labrador", "Newfoundland and Labrador"),
    ("\u00cele-du-Prince-\u00c9douard", "Prince Edward Island"),
    ("Nouvelle-\u00c9cosse", "Nova Scotia"),
    ("Nouveau-Brunswick", "New Brunswick"),
    ("partie ontarienne", "Ontario"),
    (", Ontario", "Ontario"),
    (", Qu\u00e9bec", "Quebec"),
    (", Manitoba", "Manitoba"),
    (", Saskatchewan", "Saskatchewan"),
    (", Alberta", "Alberta"),
    ("Colombie-Britannique", "British Columbia"),
]


EXCLUDED_GEOGRAPHIES = {
    "Canada",
    "Whitehorse, Yukon",
    "Yellowknife, Territoires du Nord-Ouest",
}


def load_gas_prices() -> pd.DataFrame:
    response = requests.get(CONFIG["gas_prices_zip_url"], timeout=30)
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as zip_file:
        with zip_file.open(CSV_NAME) as csv_file:
            return pd.read_csv(csv_file, sep=";", dtype=str, encoding="utf-8-sig")


def normalize_province(geo: str) -> str | None:
    if pd.isna(geo):
        return None

    value = str(geo).strip()
    if value in EXCLUDED_GEOGRAPHIES:
        return None

    for pattern, province in PROVINCE_PATTERNS:
        if pattern in value:
            return province

    return None


def run() -> pd.DataFrame:
    df = load_gas_prices()
    latest_period = df["P\u00c9RIODE DE R\u00c9F\u00c9RENCE"].max()

    df = df[
        (df["P\u00c9RIODE DE R\u00c9F\u00c9RENCE"] == latest_period)
        & (df["Type de carburant"] == FUEL_TYPE)
    ].copy()

    df["province"] = df["G\u00c9O"].apply(normalize_province)
    df = df[df["province"].notna()].copy()
    df["essence_ordinaire_cents_litre"] = pd.to_numeric(
        df["VALEUR"].str.replace(",", ".", regex=False), errors="coerce"
    )

    result = (
        df.groupby("province", as_index=False)["essence_ordinaire_cents_litre"]
        .mean()
        .round(2)
    )

    return result.sort_values("province").reset_index(drop=True)


if __name__ == "__main__":
    print(run())