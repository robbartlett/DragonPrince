from adafruit_circuitplayground.express import cpx
import dragonPrince
import random
import time

theKey = dragonPrince.KeyOfAaravos()

while True:
    random.seed(time.time())
    if cpx.button_b:
        theKey.NextFace()
    theKey.Show()