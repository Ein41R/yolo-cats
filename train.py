from ultralytics import YOLO

model = YOLO("yolov8n.yaml")
model.train(
    data="config.yaml",
    epochs=300,
    patience=50,
    lr0=0.001,
    optimizer="AdamW",
    cos_lr=True,
    close_mosaic=10,
    imgsz=640,
)