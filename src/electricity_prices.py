import re
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import CONFIG


PROVINCE_CODES = {
    "ON": "Ontario",
    "QC": "Quebec",
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "SK": "Saskatchewan",
    "NS": "Nova Scotia",
    "NL": "Newfoundland and Labrador",
    "PE": "Prince Edward Island",
    "NB": "New Brunswick",
}


def creer_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1600,2200")
    return webdriver.Chrome(options=options)


def extraire_electricite_par_barre():
    driver = creer_driver()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(CONFIG["electricity_cost_url"])
        time.sleep(4)

        bars = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "path.recharts-rectangle"))
        )

        resultats = []
        deja_vus = set()

        for bar in bars:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bar)
                time.sleep(0.2)

                ActionChains(driver).move_to_element(bar).pause(0.3).perform()
                time.sleep(0.5)

                tooltip = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".recharts-tooltip-wrapper"))
                )

                texte = tooltip.text.strip()
                if not texte or texte in deja_vus:
                    continue

                deja_vus.add(texte)
                lignes = [x.strip() for x in texte.split("\n") if x.strip()]
                lieu = lignes[0] if lignes else None

                match_valeur = re.search(r"(\d+[.,]\d+)", texte)
                valeur = float(match_valeur.group(1).replace(",", ".")) if match_valeur else None

                ville = None
                province_code = None
                if lieu and "," in lieu:
                    partie = [x.strip() for x in lieu.split(",")]
                    if len(partie) >= 2:
                        ville = partie[0]
                        province_code = partie[1]

                resultats.append(
                    {
                        "ville": ville,
                        "province_code": province_code,
                        "electricite_cents_kwh": valeur,
                    }
                )
            except Exception:
                continue

        return pd.DataFrame(resultats).drop_duplicates(subset=["ville", "province_code"]).reset_index(drop=True)
    finally:
        driver.quit()


def run():
    df = extraire_electricite_par_barre()
    if df.empty:
        return pd.DataFrame(columns=["province", "electricite_cents_kwh"])

    df = df[df["province_code"].isin(PROVINCE_CODES)].copy()
    df["province"] = df["province_code"].map(PROVINCE_CODES)

    resultat = (
        df.groupby("province", as_index=False)["electricite_cents_kwh"]
        .mean()
        .round(2)
    )

    return resultat


if __name__ == "__main__":
    print(run())
