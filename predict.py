from ultralytics import YOLO

class predict:
    def __init__(self):
        # Load the model
        self.model = YOLO('./runs/detect/Final_Model3/weights/best.pt')
    def predict_image(self, image):
        pred = self.model.predict(image, device='cuda' , verbose=False)
        return pred
