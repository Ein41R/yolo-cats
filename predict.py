# import cv2
import os

from ultralytics import YOLO

model = YOLO("dalast.pt")

dir = input("chooose imageset: (default=d/t/images), (1=d/t/images), (2=images/cat images)")

if dir == "2":
    images = os.listdir("images/cat images")
    path = "images/cat images"

else:
    images = os.listdir("datasets/train/images")
    path = "datasets/train/images"
print(f"found {len(images)} images in {path}\n")

sample_size = input(f"how many images to predict? (default=10)")
try:
    sample_size = int(sample_size)
except Exception:
    sample_size = 10


for image in images[0:int(sample_size)]:
    source = os.path.join(path, image)
    model.predict(source, save=True, imgsz=320, conf=0.25)