from ultralytics import YOLO

model = YOLO("yolov8n.yaml")

model.train(data="config.yaml", epochs=500)//no improvement after 232 epochs