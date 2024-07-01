import subprocess
from CameraControl.env import Parameters
import json

def startSequence(filepath):

    with open(Parameters.camera_state_filepath, 'r') as file:
        last_state_registered = json.load(file)
        if last_state_registered["cameraStatus"] == "Off":
            print("Starting sequence...")
            # subprocess.run(["/bin/bash", f"{filepath}"], check=True)

    with open(Parameters.camera_state_filepath, 'w') as file:
        json.dump({"cameraStatus": "On"}, file, indent=4)

