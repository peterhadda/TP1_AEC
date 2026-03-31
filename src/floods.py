import requests
from bs4 import BeautifulSoup

from config import CONFIG


def normalize_text(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def _extract_no_floods_row(table):
    for tr in table.find_all("tr"):
        row_text = normalize_text(tr.get_text(" ", strip=True)).lower()
        if row_text.startswith("no floods"):
            return tr
    return None


def run():
    response = requests.get(
        CONFIG["floods_url"],
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    target_table = None
    for table in soup.find_all("table"):
        text = normalize_text(table.get_text(" ", strip=True))
        if "No floods" in text and "British Columbia" in text and "Ontario" in text:
            target_table = table
            break

    if target_table is None:
        raise ValueError("Table cible introuvable pour no floods.")

    province_ids = {}
    for th in target_table.find_all("th"):
        label = normalize_text(th.get_text())
        if label in CONFIG["floods_provinces"]:
            province_ids[label] = th.get("id")

    if not province_ids:
        raise ValueError("Colonnes provinces introuvables dans la table no floods.")

    no_flood_row = _extract_no_floods_row(target_table)
    if no_flood_row is None:
        raise ValueError("Ligne no floods introuvable.")

    values = {}
    for td in no_flood_row.find_all("td"):
        headers_attr = td.get("headers", "")
        value_text = normalize_text(td.get_text())

        for province, province_id in province_ids.items():
            if province_id and province_id in headers_attr:
                try:
                    values[province] = float(value_text)
                except ValueError:
                    pass

    return {province: values.get(province, 100.0) for province in CONFIG["floods_provinces"]}
