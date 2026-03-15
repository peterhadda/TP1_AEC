import requests
from bs4 import BeautifulSoup


def extraire_perspectives_canada(url):
    try:
        # 1. Requête avec des headers pour simuler un navigateur
        headers = {'User-Agent': 'Mozilla/5.0'}
        reponse = requests.get(url, headers=headers)
        reponse.raise_for_status()

        # 2. Analyse HTML
        soup = BeautifulSoup(reponse.text, 'html.parser')

        # 3. Cibler le tableau des perspectives
        # Le Guichet-Emplois utilise souvent des structures de tableaux standard
        tableau = soup.find('table')

        if not tableau:
            print("Tableau de données non trouvé.")
            return

        print(f"Perspectives d'emploi (prochains 3 ans) - Source : Guichet-Emplois\n")
        print(f"{'Province/Territoire':<30} | {'Perspectives'}")
        print("-" * 50)

        # 4. Parcourir les lignes du tableau (en sautant l'en-tête)
        lignes = tableau.find_all('tr')
        for ligne in lignes:
            colonnes = ligne.find_all('td')
            if len(colonnes) >= 2:
                lieu = colonnes[0].get_text(strip=True)
                # On nettoie le texte pour enlever les mentions de "étoiles"
                perspective = colonnes[1].get_text(strip=True)
                print(f"{lieu:<30} | {perspective}")

    except Exception as e:
        print(f"Erreur lors de la collecte : {e}")


# URL spécifique fournie
url_cible = "https://www.jobbank.gc.ca/marketreport/outlook-occupation/296608/ca"
extraire_perspectives_canada(url_cible)