import requests
from datetime import datetime, timedelta
import json, os

def convert_to_local_time(utc_time_str, offset_hours):

    # Convierte de UTC a hora local

    utc_time = datetime.strptime(utc_time_str, '%I:%M:%S %p')
    local_time = utc_time - timedelta(hours=offset_hours)
    return local_time.strftime('%I:%M:%S %p')

def get_sunrise_sunset(lat, lng, date='today', offset_hours=4):

    # Retorna varios datos sobre la hora de la salida y puesta de sol, 
    # con la siguiente estructura:

        # {
        #   "sunrise": "07:43:18 AM",
        #   "sunset": "05:43:11 PM",
        #   "solar_noon": "12:43:14 PM",
        #   "day_length": "09:59:53",
        #   "civil_twilight_begin": "07:17:13 AM",
        #   "civil_twilight_end": "06:09:15 PM",
        #   "nautical_twilight_begin": "06:46:13 AM",
        #   "nautical_twilight_end": "06:40:15 PM",
        #   "astronomical_twilight_begin": "06:15:57 AM",
        #   "astronomical_twilight_end": "07:10:31 PM"
        # }

    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            results = data['results']
            for key in results:
                if 'day_length' not in key:
                    results[key] = convert_to_local_time(results[key], offset_hours)
            return results
        else:
            return {'error': data['status']}
    else:
        return {'error': 'Request failed'}

def save_sun_times_to_file(sun_times, filename):
    today = datetime.now().strftime('%Y-%m-%d')
    sun_times['date'] = today
    with open(filename, 'w') as file:
        json.dump(sun_times, file, indent=4)

def read_sun_times_from_file(filename):
    if not os.path.exists(filename):
        return None
    if os.path.getsize(filename) == 0:
        return None
    with open(filename, 'r') as file:
        sun_times = json.load(file)
    return sun_times

def check_and_update_sun_times(lat, lng, filename, offset_hours=4):
    sun_times = read_sun_times_from_file(filename)
    today = datetime.now().strftime('%Y-%m-%d')
    if sun_times is None or sun_times.get('date') != today:
        sun_times = get_sunrise_sunset(lat, lng, offset_hours=offset_hours)
        if 'error' not in sun_times:
            save_sun_times_to_file(sun_times, filename)
            print("Sunrise and Sunset times have been updated in the file.")
        else:
            print("Error:", sun_times['error'])
    else:
        print("Sunrise and Sunset times are already up-to-date.")