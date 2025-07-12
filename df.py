import sys
import os
import time
from math import radians, cos, sin, sqrt, atan2
#Make your own file "credentials.py" and assign my_lat, my_long to whatever coords you choose
from credentials import my_lat, my_long

#Setting path to opensky_api
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FlightDisplay','opensky-api','python'))
sys.path.append(config_path)

#Calling opensky_api
from opensky_api import OpenSkyApi as osa
api = osa()

#Bounded box parameters
radius_miles = 40
delta_lat = radius_miles / 69
delta_long = radius_miles / (69*cos(radians(my_lat)))
latmin = my_lat - delta_lat
latmax = my_lat + delta_lat
longmin = my_long - delta_long
longmax = my_long + delta_long

#Get all states within the bounded box
states = api.get_states(bbox=(latmin, latmax, longmin, longmax))
print(states)

display_text = ""
if states and states.states:
    for s in states.states:
        if s.callsign:
            callsign = s.callsign.strip()
            display_text += f"{callsign} "
        if not display_text:
            display_text = "Flights found, no call signs available."

else: display_text = "No flights found."



#Displaying the Code on RGB LED Matrix
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

#Configuring options for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 2

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()
textColor = graphics.Color(255,255,0)
pos = canvas.width
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/6x10.bdf")

while True:
    canvas.Clear()
    len_px = graphics.DrawText(canvas, font, pos, 20, textColor, display_text)
    pos -= 1
    if pos + len_px < 0:
        pos = canvas.width
        time.sleep(0.05)
        
