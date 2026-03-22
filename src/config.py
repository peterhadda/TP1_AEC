from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent


CONFIG = {
    "raw_dir": PROJECT_DIR / "data" / "raw",
    "processed_dir": PROJECT_DIR / "data" / "processed",
    "output_file": "provinces_data.json",

    "province_aliases": {
        "Québec": "Quebec",
        "Quebec": "Quebec",
        "Ontario": "Ontario",
        "Alberta": "Alberta",
        "Calgary": "Alberta",
        "British Columbia": "British Columbia",
        "British Colombia": "British Columbia",
        "Manitoba": "Manitoba",
        "Saskatchewan": "Saskatchewan",
        "Nova Scotia": "Nova Scotia",
        "New Brunswick": "New Brunswick",
        "Prince Edward Island": "Prince Edward Island",
        "NewfoundLand": "Newfoundland and Labrador",
        "Newfoundland and Labrador": "Newfoundland and Labrador",
        "Yukon": "Yukon",
        "Yukon Territory": "Yukon",
    },

    "items": {
        "crime_rate": {
            "script": "crime_rate.py",
            "province_field": "province",
            "value_field": "crime_rate",
            "final_field": "nombre_crime"
        },
        "weather": {
            "script": "weather.py",
            "province_field": None,
            "value_field": None,
            "final_field": "avg_temperature"
        },
        "unemployment_rate": {
            "script": "taux_de_chaumage.py",
            "province_field": "provinces",
            "value_field": "rate",
            "final_field": "unemployment_rate"
        },
        "taxes": {
            "script": "taxes.py",
            "province_field": "Province",
            "value_field": "Total Tax Rate",
            "final_field": "total_tax_rate"
        },
        "job_perspective": {
            "script": "Perspective.py",
            "province_field": "Province/Territoire",
            "value_field": "Perspective",
            "final_field": "job_persecptive"
        }
    }
}
