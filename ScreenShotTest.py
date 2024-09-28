# chk the coordinates of the screen shot according to the display size and resolution
import time

from PIL import ImageGrab


class Screenshot:
    def __init__(self):
        pass

    def screenshot(self, region):
        time.sleep(1)
        screenshot = ImageGrab.grab(bbox=region)  # Capture the region specified by the bbox
        screenshot.save('screenshot.png')
        return screenshot


# Example usage
# Define a region: (left, top, right, bottom)
region = (350, 100, 1850, 950) # change this values


sc = Screenshot()
screenshot_img = sc.screenshot(region=region)
screenshot_img.show()  # This will display the captured region
