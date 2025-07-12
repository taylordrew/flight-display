import sys
import os

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FlightDisplay','opensky-api','python'))

sys.path.append(config_path)

from opensky_api import OpenSkyApi as osa

api = osa()
states = api.get_states()
print(states)

