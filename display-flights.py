import requests
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# ==== CONFIG ====
USERNAME = "drewt"
PASSWORD = "Eugene03"
LAT = 41.992935
LON = -93.613698
MAX_DISTANCE_KM = 100

# ==== LED MATRIX SETUP ====
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # change if needed

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")
color = graphics.Color(255, 255, 0)

def get_nearby_flights():
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, auth=(USERNAME, PASSWORD), timeout=10)
        data = response.json()

        nearby = []
        for s in data.get("states", []):
            callsign = s[1].strip() if s[1] else "N/A"
            lat = s[6]
            lon = s[5]
            altitude = s[7]

            if lat is None or lon is None:
                continue

            # rough bounding box
            if abs(lat - LAT) < 1.0 and abs(lon - LON) < 1.0:
                nearby.append((callsign, altitude))

        return nearby[:5] if nearby else [("No flights nearby", None)]
    except Exception as e:
        return [(f"Error: {e}", None)]

def scroll_text(lines):
    for call, alt in lines:
        text = f"{call} {int(alt)} ft" if alt else call
        pos = canvas.width
        while pos + len(text)*6 > 0:
            canvas.Clear()
            graphics.DrawText(canvas, font, pos, 20, color, text)
            pos -= 1
            time.sleep(0.05)
            canvas = matrix.SwapOnVSync(canvas)

# ==== MAIN LOOP ====
try:
    while True:
        flights = get_nearby_flights()
        scroll_text(flights)
        time.sleep(10)
except KeyboardInterrupt:
    print("Exiting...")
    matrix.Clear()
