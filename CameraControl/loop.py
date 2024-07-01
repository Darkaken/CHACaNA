
import time
from datetime import datetime, timedelta
from sunrise_sunset_api import check_and_update_sun_times, read_sun_times_from_file
from weather_api import is_nighttime_and_clear

from cameraFunctions.end import endSequence
from cameraFunctions.start import startSequence

def get_today_check_time(hour=13, minute=0):
    """Returns today's datetime at the specified hour and minute."""
    now = datetime.now()
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)

def main_loop(parameters):
    print(f"\nStarting Main Loop\n")
    while True:
        now = datetime.now()
        print(f"Time: {now}, see you in {parameters.refresh_rate} minutes!")
        # Check if it's 1 PM today to update sunrise/sunset times
        today_check_time = get_today_check_time(hour=13, minute=0)

        time_check = today_check_time <= now < today_check_time + timedelta(minutes=parameters.refresh_rate)

        if time_check:
            print("Checking and updating sunrise/sunset times...")
            check_and_update_sun_times(
                lat=parameters.latitude,
                lng=parameters.longitude,
                filename=parameters.filename,
                offset_hours=parameters.offset_hours
            )
        
        # Read the updated times
        sun_times = read_sun_times_from_file(parameters.filename)
        if sun_times and 'error' not in sun_times:
            sunrise_time = sun_times['sunrise']
            sunset_time = sun_times['sunset']
            
            # Convert times to datetime objects
            sunrise_datetime = datetime.strptime(sunrise_time, '%I:%M:%S %p').time()
            sunset_datetime = datetime.strptime(sunset_time, '%I:%M:%S %p').time()
            current_time = now.time()

            # Check if current time matches sunrise or sunset
            if sunrise_datetime <= current_time < (datetime.combine(now, sunrise_datetime) + timedelta(minutes=parameters.refresh_rate)).time():
                print("It's sunrise time!")
                endSequence(parameters.end_sequence_filepath)
                
            if sunset_datetime <= current_time < (datetime.combine(now, sunset_datetime) + timedelta(minutes=parameters.refresh_rate)).time():
                print("It's sunset time!")
                if is_nighttime_and_clear():
                    startSequence(parameters.start_sequence_filepath)

        # Wait for the next refresh interval
        time.sleep(parameters.refresh_rate * 60)