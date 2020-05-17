from adafruit_circuitplayground.express import cpx
import adafruit_fancyled.adafruit_fancyled as fancy
import time
import math
import random
import rgb2hsv

cpx.pixels.brightness = 1.0

STILL = 0

CLOCKWISE = 1
COUNTERCLOCKWISE = 2

BRIGHTER = 1
DIMMER = 2

def toggle(original, a, b):
    if original == a:
        return b
    else:
        return a

class MagicPixel:
    def __init__(self, baseHsvColor) :
        r = random.randint(1,2)
        self._brightnessDirection = r
        self._baseHsvColor = baseHsvColor
        self._brightness = float(baseHsvColor[2])
        self._velocity = 1

    def SetBrightness(self, brightnessLevel):
        self._brightness = brightnessLevel

    def GetAdjustedColor(self):
        (r,g,b) = rgb2hsv.hsv_to_rgb(self._baseHsvColor.hue, self._baseHsvColor.saturation, self._brightness)
        newColorRgb = fancy.CRGB(r/255,g/255,b/255)
        return newColorRgb.pack()

    def AnimatePixel(self):
        r = random.randint(1,3)
        self._velocity = r

        r = random.randint(1,100)
        if r >93:
            self._brightnessDirection = toggle(self._brightnessDirection, BRIGHTER, DIMMER)

        if self._brightnessDirection == DIMMER:
            if self._brightness <= 0.5:
                self._brightnessDirection = BRIGHTER
        elif self._brightnessDirection == BRIGHTER:
            if self._brightness >= 1.0:
                self._brightnessDirection = DIMMER

        if self._brightnessDirection == BRIGHTER:
            self._brightness += 0.008 * self._velocity
            self._brightness = min(1.0, self._brightness)
        elif self._brightnessDirection == DIMMER:
            self._brightness -= 0.008 * self._velocity
            self._brightness = max(0.5, self._brightness)

class MagicFace:
    def __init__(self, name, baseColor, pixelCount):
        self._pixelArray = []
        self._name = name
        self._baseColor = baseColor
        self._rotationDirection = CLOCKWISE
        i = 1
        while i <= pixelCount:
            self._pixelArray.append(MagicPixel(baseColor))
            i += 1

    def AnimateRotation(self):
        r = random.randint(1,100)
        if r > 50:
            self._rotationDirection = toggle(self._rotationDirection, CLOCKWISE, COUNTERCLOCKWISE)

        r = random.randint(1,100)
        if r > 15:
            tmp = self._pixelArray[0]
            if self._rotationDirection == COUNTERCLOCKWISE:
                for i in range(0,9):
                    self._pixelArray[i] = self._pixelArray[i+1]
                self._pixelArray[9] = tmp
            else:
                tmp = self._pixelArray[9]
                for i in range(9,0,-1):
                    self._pixelArray[i] = self._pixelArray[i-1]
                self._pixelArray[0] = tmp

    def Show(self):
        if self._rotationDirection > STILL:
            self.AnimateRotation()
        i = 0
        while  i < len(self._pixelArray):
            self._pixelArray[i].AnimatePixel()
            cpx.pixels[i] = self._pixelArray[i].GetAdjustedColor()
            i+=1

        cpx.pixels.show()

class KeyOfAaravos:
    def __init__(self):
        self._faceData = [
#           ("Name", hue, saturation, value, pixelCount),
#            ("Dark",  0.833333, 1.0, 1.0, 10),
            ("Sky",   0.545139, 1.0, 1.0, 10),
            ("Ocean", 0.611635, 1.0, 1.0, 10),
            ("Earth", 0.277487, 1.0, 1.0, 10),
            ("Sun",   0.083660, 1.0, 1.0, 10),
            ("Moon",  0.551282, 0.1, 0.8, 10),
            ("Star",  0.843137, 0.6, 0.7, 10)
        ]
        self._currentFaceIndex = -1
        self.NextFace()

    def Show(self):
        self.face.Show()

    def NextFace(self):
        self._currentFaceIndex+=1
        if (self._currentFaceIndex > len(self._faceData) - 1):
            self._currentFaceIndex = 0
        data = self._faceData[self._currentFaceIndex]
        self.face = MagicFace(data[0], fancy.CHSV(data[1], data[2], data[3]), data[4])
