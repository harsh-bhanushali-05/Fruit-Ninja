from ultralytics import YOLO


def train_model():
    # Load the YOLO model
    model = YOLO('yolov8n.pt')

    # Train the model
    model.train(
        data='./data.yaml',
        epochs=10,
        imgsz=(1080, 1920),
        batch=32,
        name='test_model',
        save=True
    )

    # Validate the model
    model.val(data='./data.yaml')


if __name__ == '__main__':
    # Ensure this is the main entry point
    train_model()
