import requests
from bs4 import BeautifulSoup


def extraire_perspectives_canada(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        # On cible le bon tableau
        tableau = soup.find("table", id="provoutlooktable_region")

        if not tableau:
            print("Tableau non trouvé.")
            return

        print(f"{'Province/Territoire':<30} | {'Perspective'}")
        print("-" * 55)

        for ligne in tableau.select("tbody tr"):
            # Province = dans le <th>
            province_tag = ligne.find("th")

            # Perspective = dans le span spécial
            perspective_tag = ligne.select_one("span.outlooknote.value.object-nowrap")

            if province_tag and perspective_tag:
                province = province_tag.get_text(strip=True)
                perspective = perspective_tag.get_text(strip=True)
                print(f"{province:<30} | {perspective}")

    except Exception as e:
        print("Erreur :", e)


url = "https://www.jobbank.gc.ca/marketreport/outlook-occupation/296608/ca"
extraire_perspectives_canada(url)