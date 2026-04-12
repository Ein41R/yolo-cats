from pathlib import Path
import random

from ultralytics import YOLO


ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL_DIR = ROOT / "runs" / "detect"
DEFAULT_IMAGESETS = {
    "1": ("datasets/train/images", ROOT / "datasets" / "train" / "images"),
    "2": ("images/cat images", ROOT / "images" / "cat images"),
}


def prompt_with_default(message: str, default: str) -> str:
    value = input(f"{message} [{default}]: ").strip()
    return value or default


def prompt_choice(message: str, default: str, options: dict[str, str]) -> str:
    choices = ", ".join(f"{key}={label}" for key, label in options.items())
    value = input(f"{message} ({choices}) [{default}]: ").strip()
    return value or default


def prompt_int(message: str, default: int, minimum: int = 1) -> int:
    raw_value = input(f"{message} [{default}]: ").strip()
    if not raw_value:
        return default

    try:
        parsed = int(raw_value)
    except ValueError:
        print(f"Invalid number '{raw_value}', using {default}.")
        return default

    if parsed < minimum:
        print(f"Number must be at least {minimum}, using {default}.")
        return default

    return parsed


def available_model_dirs() -> list[Path]:
    if not DEFAULT_MODEL_DIR.exists():
        return []
    def run_sort_key(path: Path) -> tuple[int, str]:
        suffix = path.name.removeprefix("train")
        try:
            return int(suffix), path.name
        except ValueError:
            return 0, path.name

    return sorted((path for path in DEFAULT_MODEL_DIR.glob("train*") if path.is_dir()), key=run_sort_key)


def resolve_model_path(train_dir: str, version: str) -> Path:
    suffix = "last.pt" if version == "2" else "best.pt"
    return ROOT / "runs" / "detect" / f"train{train_dir}" / "weights" / suffix


def resolve_imageset(choice: str) -> tuple[str, Path]:
    if choice in DEFAULT_IMAGESETS:
        return DEFAULT_IMAGESETS[choice]

    custom_path = Path(choice)
    if not custom_path.is_absolute():
        custom_path = ROOT / custom_path

    return choice, custom_path


print("YOLO image prediction helper")
print("Press Enter to accept the default for each prompt.\n")

model_versions = {"1": "best.pt", "2": "last.pt"}
version_choice = prompt_choice("Choose model version", "1", model_versions)
version = model_versions.get(version_choice, model_versions["1"])

model_dirs = available_model_dirs()
if model_dirs:
    print("Available training runs:")
    for index, model_dir in enumerate(model_dirs, start=1):
        print(f"  {index}. {model_dir.name}")
    default_train_dir = model_dirs[-1].name.removeprefix("train")
else:
    default_train_dir = ""

train_number = prompt_with_default(
    f"Enter train number for runs/detect/train<NUM>/weights/{version}",
    default_train_dir,
)
model_path = resolve_model_path(train_number, version)

if not model_path.exists():
    raise FileNotFoundError(f"Model not found: {model_path}")

model = YOLO(str(model_path))
print(f"Loaded model: {model_path}\n")

print("Image sets:")
for key, (label, _) in DEFAULT_IMAGESETS.items():
    print(f"  {key}. {label}")
print("  3. custom path")

imageset_choice = prompt_choice("Choose image set", "1", {"1": "datasets/train/images", "2": "images/cat images", "3": "custom path"})
if imageset_choice == "3":
    imageset_label = prompt_with_default("Enter image folder path", "datasets/train/images")
    _, image_path = resolve_imageset(imageset_label)
else:
    _, image_path = resolve_imageset(imageset_choice)

if not image_path.exists():
    raise FileNotFoundError(f"Image folder not found: {image_path}")

images = sorted(
    path for path in image_path.iterdir() if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
)
if not images:
    raise RuntimeError(f"No image files found in {image_path}")

sample_size = prompt_int("How many images should be predicted", 10, minimum=1)
sample_size = min(sample_size, len(images))

print()
print("Prediction summary")
print(f"  Model:  {model_path}")
print(f"  Images: {image_path} ({len(images)} found)")
print(f"  Count:  {sample_size}")
print("  Output: Ultralytics default runs/detect/predict* folder")
print()

selected_images = random.sample(images, sample_size)

for index, image in enumerate(selected_images, start=1):
    print(f"[{index}/{sample_size}] Predicting {image.name}")
    model.predict(str(image), save=True, imgsz=320, conf=0.25)

print("\nDone.")