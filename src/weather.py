import requests
import iso
from datetime import date, timedelta

def get_weather(year,LAT,LONG):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": LAT,
        "longitude": LONG,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "hourly": "temperature_2m",
        "timezone":"auto"
    }
    response = requests.get(url, params=params)
    data=response.json()
    temps=data["hourly"]["temperature_2m"]
    return sum(temps)/len(temps)


data_temp={"Quebec":get_weather(2025,45.5017,-73.5673),
           "Ontario":get_weather(2025,43.6532,-79.3832),
           "Calgary":get_weather(2025,51.0447,-114.0719),
           "British Colombia":get_weather(2025,49.2827,-123.1207),
           "New Brunswick":get_weather(2025,45.9636,-66.6431),
           "Manitoba":get_weather(2025,49.9636,-97.138),
           "Nova Scotia":get_weather(2025,44.6488,-63.5752),
           "Saskatchewan":get_weather(2025,50.4452,-104.6189),
           "Prince Edward Island":get_weather(2025,46.2382,-63.1311),
           "NewfoundLand":get_weather(2025,47.5615,-52.7126)
           }

print(data_temp)
