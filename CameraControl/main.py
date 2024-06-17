import os
from env import Parameters
from loop import main_loop

def main():
    parameters = Parameters

    os.makedirs(os.path.dirname(parameters.filename), exist_ok=True)
    main_loop(parameters)

if __name__ == "__main__":
    main()
