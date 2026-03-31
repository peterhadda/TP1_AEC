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
        tableau = soup.find("table", id="provoutlooktable_region")

        if not tableau:
            return []

        perspectives = []

        for ligne in tableau.select("tbody tr"):
            province_tag = ligne.find("th")
            perspective_tag = ligne.select_one("span.outlooknote.value.object-nowrap")

            if province_tag and perspective_tag:
                province = province_tag.get_text(strip=True)
                perspective = perspective_tag.get_text(strip=True)
                perspectives.append(
                    {
                        "Province/Territoire": province,
                        "Perspective": perspective,
                    }
                )

        return perspectives

    except Exception as e:
        print("Erreur :", e)
        return []


url = "https://www.jobbank.gc.ca/marketreport/outlook-occupation/296608/ca"
provinces = extraire_perspectives_canada(url)
