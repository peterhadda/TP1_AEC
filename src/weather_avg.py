import requests


PROVINCE_COORDINATES = {
    "Quebec": (45.5017, -73.5673),
    "Ontario": (43.6532, -79.3832),
    "Alberta": (51.0447, -114.0719),
    "British Columbia": (49.2827, -123.1207),
    "New Brunswick": (45.9636, -66.6431),
    "Manitoba": (49.9636, -97.1380),
    "Nova Scotia": (44.6488, -63.5752),
    "Saskatchewan": (50.4452, -104.6189),
    "Prince Edward Island": (46.2382, -63.1311),
    "Newfoundland and Labrador": (47.5615, -52.7126),
}


def get_weather_average(year, latitude, longitude):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "hourly": "temperature_2m",
        "timezone": "auto",
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    temperatures = data["hourly"]["temperature_2m"]
    return round(sum(temperatures) / len(temperatures), 2)


def run():
    year = 2025
    averages = {}

    for province, (latitude, longitude) in PROVINCE_COORDINATES.items():
        averages[province] = get_weather_average(year, latitude, longitude)

    return averages


data_temp = run()
