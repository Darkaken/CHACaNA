import os
from env import Parameters
from loop import main_loop
from CameraControl.sunrise_sunset_api import check_and_update_sun_times

def main():
    parameters = Parameters

    os.makedirs(os.path.dirname(parameters.filename), exist_ok=True)

    check_and_update_sun_times(
        lat=parameters.latitude,
        lng=parameters.longitude,
        filename=parameters.filename,
        offset_hours=parameters.offset_hours
    ) # si ejecutamos el programa de nuevo, revisamos los tiempos de sunrise/sunset estén actualizados

    main_loop(parameters)

if __name__ == "__main__":
    main()
