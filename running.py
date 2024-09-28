from screenshots import screenshot
from PIL import Image
import time
from predict import predict
import pyautogui
import threading

def process_predictions(ss, predictor):
    # Get predictions from the model
    predictions = predictor.predict_image(ss)

    # Initialize lists to hold bounding boxes
    fruit_bboxes = []
    bomb_bboxes = []

    # Loop through the predictions and collect fruit and bomb bounding boxes
    for result in predictions:
        boxes = result.boxes
        for box in boxes:
            bbox = box.xyxy[0].cpu().numpy()  # Get the bounding box coordinates
            label = result.names[int(box.cls[0])]  # Get the label
            confidence = box.conf[0].cpu().numpy()  # Get the confidence score
            if label == 'Fruit':
                fruit_bboxes.append(bbox.tolist())
            if label == 'Bomb':
                bomb_bboxes.append(bbox.tolist())

    return fruit_bboxes, bomb_bboxes

def get_center(bbox):
    x_min, y_min, x_max, y_max = bbox
    x_center = int((x_min + x_max) / 2)
    y_center = int((y_min + y_max) / 2)
    return x_center, y_center

def move_mouse_through_fruits(fruit_centers, bomb_bboxes):
    if not fruit_centers:
        return

    # Sort fruits by distance from current mouse position
    current_position = pyautogui.position()
    fruit_centers.sort(key=lambda p: (p[0] - current_position[0]) ** 2 + (p[1] - current_position[1]) ** 2)

    # Press and hold the mouse button down to simulate swipe
    pyautogui.mouseDown()

    for center in fruit_centers:
        # Check if path to fruit intersects with any bombs
        if not intersects_bomb(current_position, center, bomb_bboxes):
            # Move the mouse quickly to the fruit center
            pyautogui.moveTo(center[0], center[1], duration=0.01)
            current_position = center
    pyautogui.mouseUp()

def intersects_bomb(start, end, bomb_bboxes):
    # Simple line-box intersection test
    for bbox in bomb_bboxes:
        x_min, y_min, x_max, y_max = bbox
        if line_intersects_rect(start, end, (x_min, y_min, x_max, y_max)):
            return True
    return False

def line_intersects_rect(p1, p2, rect):
    # Simple check if the line from p1 to p2 intersects the rectangle
    x_min, y_min, x_max, y_max = rect

    # Check if either point is inside the rectangle
    if point_in_rect(p1, rect) or point_in_rect(p2, rect):
        return True

    # Check for line intersection with rectangle sides
    # Line from p1 to p2
    line = (p1, p2)

    # Rectangle sides
    sides = [
        ((x_min, y_min), (x_max, y_min)),  # Top
        ((x_max, y_min), (x_max, y_max)),  # Right
        ((x_max, y_max), (x_min, y_max)),  # Bottom
        ((x_min, y_max), (x_min, y_min))   # Left
    ]

    for side in sides:
        if lines_intersect(line, side):
            return True

    return False

def point_in_rect(point, rect):
    x, y = point
    x_min, y_min, x_max, y_max = rect
    return x_min <= x <= x_max and y_min <= y <= y_max

def lines_intersect(a, b):
    # Check if line segments a and b intersect
    (x1, y1), (x2, y2) = a
    (x3, y3), (x4, y4) = b

    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    return (ccw(a[0], b[0], b[1]) != ccw(a[1], b[0], b[1]) and
            ccw(a[0], a[1], b[0]) != ccw(a[0], a[1], b[1]))

if __name__ == '__main__':
    screenshotter = screenshot()  # Instantiate the screenshot class
    predictor = predict()  # Instantiate the predict class

    while True:
        # Take screenshot
        start = time.time()

        ss = screenshotter.screenshot()

        # Process predictions
        fruit_bboxes, bomb_bboxes = process_predictions(ss, predictor)

        # Get fruit centers
        fruit_centers = [get_center(bbox) for bbox in fruit_bboxes]

        # Optionally, we can run mouse movement in a separate thread
        threading.Thread(target=move_mouse_through_fruits, args=(fruit_centers, bomb_bboxes)).start()
        end = time.time()
        print(end - start)
