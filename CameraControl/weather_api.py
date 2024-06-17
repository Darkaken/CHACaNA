import requests

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def is_nighttime_and_clear(weather_data):
    # Check if it is nighttime
    is_nighttime = weather_data['current_weather']['is_day'] == 0

    # Check if the sky is clear or has very few clouds
    weather_code = weather_data['current_weather']['weathercode']
    is_clear_skies = weather_code == 0  # Assuming clear skies if weather code is 0

    return is_nighttime and is_clear_skies

# Falta integrar esto al main loop
# Link de interes: https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM
