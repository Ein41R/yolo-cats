import os

from PIL import Image, ImageDraw


def yolo_to_xyxy(x_center, y_center, width, height, image_w, image_h):
	"""Convert normalized YOLO bbox to pixel corner coordinates."""
	box_w = width * image_w
	box_h = height * image_h
	x1 = int((x_center * image_w) - (box_w / 2))
	y1 = int((y_center * image_h) - (box_h / 2))
	x2 = int((x_center * image_w) + (box_w / 2))
	y2 = int((y_center * image_h) + (box_h / 2))

	x1 = max(0, min(x1, image_w - 1))
	y1 = max(0, min(y1, image_h - 1))
	x2 = max(0, min(x2, image_w - 1))
	y2 = max(0, min(y2, image_h - 1))
	return x1, y1, x2, y2


def draw_boxes_on_dataset(base_dir="dataset/trains"):
	images_dir = os.path.join(base_dir, "images")
	labels_dir = os.path.join(base_dir, "labels")
	output_dir = os.path.join(base_dir, "images_with_boxes")
	os.makedirs(output_dir, exist_ok=True)

	valid_ext = {".png", ".jpg", ".jpeg"}

	for image_name in sorted(os.listdir(images_dir)):
		image_path = os.path.join(images_dir, image_name)
		if not os.path.isfile(image_path):
			continue

		stem, ext = os.path.splitext(image_name)
		if ext.lower() not in valid_ext:
			continue

		label_path = os.path.join(labels_dir, f"{stem}.txt")
		if not os.path.exists(label_path):
			print(f"Skipping {image_name}: no label file found")
			continue

		image = Image.open(image_path).convert("RGB")
		draw = ImageDraw.Draw(image)
		w, h = image.size

		with open(label_path, "r", encoding="utf-8") as label_file:
			for line in label_file:
				parts = line.strip().split()
				if len(parts) < 5:
					continue

				_, x_center, y_center, width, height = parts[:5]
				x1, y1, x2, y2 = yolo_to_xyxy(
					float(x_center),
					float(y_center),
					float(width),
					float(height),
					w,
					h,
				)
				draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=2)

		out_path = os.path.join(output_dir, image_name)
		image.save(out_path)
		print(f"Saved: {out_path}")


if __name__ == "__main__":
	draw_boxes_on_dataset()

