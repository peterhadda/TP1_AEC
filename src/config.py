from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent


CONFIG = {
    "raw_dir": PROJECT_DIR / "data" / "raw",
    "processed_dir": PROJECT_DIR / "data" / "processed",
    "output_file": "provinces_data.json",
    "latino_population_url": "https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=9810035101",
    "latino_population_download_url": "https://www150.statcan.gc.ca/n1/tbl/csv/98100351-fra.zip",
    "excluded_provinces": {
        "Yukon",
        "Northwest Territories",
        "Nunavut",
    },
    "province_aliases": {
        "Quebec": "Quebec",
        "Québec": "Quebec",
        "QuÃ©bec": "Quebec",
        "Ontario": "Ontario",
        "Alberta": "Alberta",
        "Calgary": "Alberta",
        "British Columbia": "British Columbia",
        "Colombie-Britannique": "British Columbia",
        "Manitoba": "Manitoba",
        "Saskatchewan": "Saskatchewan",
        "Nova Scotia": "Nova Scotia",
        "Nouvelle-Écosse": "Nova Scotia",
        "Nouvelle-Ã‰cosse": "Nova Scotia",
        "New Brunswick": "New Brunswick",
        "Nouveau-Brunswick": "New Brunswick",
        "Prince Edward Island": "Prince Edward Island",
        "Île-du-Prince-Édouard": "Prince Edward Island",
        "ÃŽle-du-Prince-Ã‰douard": "Prince Edward Island",
        "Newfoundland and Labrador": "Newfoundland and Labrador",
        "Terre-Neuve-et-Labrador": "Newfoundland and Labrador",
        "Yukon": "Yukon",
        "Yukon Territory": "Yukon",
    },
    "items": {
        "crime_rate": {
            "script": "crime_rate.py",
            "province_field": "province",
            "value_field": "crime_rate",
            "final_field": "nombre_crime",
        },
        "weather": {
            "script": "weather.py",
            "province_field": None,
            "value_field": None,
            "final_field": "avg_temperature",
        },
        "unemployment_rate": {
            "script": "taux_de_chaumage.py",
            "province_field": "provinces",
            "value_field": "rate",
            "final_field": "unemployment_rate",
        },
        "taxes": {
            "script": "taxes.py",
            "province_field": "Province",
            "value_field": "Total Tax Rate",
            "final_field": "total_tax_rate",
        },
        "avg_food_price": {
            "script": "province_prices.py",
            "province_field": "province",
            "value_field": "cout_hebdomadaire_nourriture_par_personne",
            "final_field": "cout_hebdomadaire_nourriture_par_personne",
        },
        "avg_other_products_price": {
            "script": "province_prices.py",
            "province_field": "province",
            "value_field": "cout_hebdomadaire_autres_produits_par_personne",
            "final_field": "cout_hebdomadaire_autres_produits_par_personne",
        },
        "job_perspective": {
            "script": "Perspective.py",
            "province_field": "Province/Territoire",
            "value_field": "Perspective",
            "final_field": "job_persecptive",
        },
        "latino_minority": {
            "script": "latino_minority.py",
            "province_field": "province",
            "value_field": "latino_americain",
            "final_field": "latino_americain",
        },
    },
}
