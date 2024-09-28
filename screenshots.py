# take a screenshot of the screen
from PIL import ImageGrab
class screenshot:
    def __init__(self):
        pass
    def screenshot(self):
        screenshot = ImageGrab.grab()
        return screenshot