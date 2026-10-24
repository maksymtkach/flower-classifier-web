from src.augmentation import augment_and_save_dataset
from src.utils.download import download_file_from_url

from pathlib import Path

from src.utils.files import extract_tar, delete_file

FLOWERS_DATASET_URL = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
AUGMENTED_DIR = PROJECT_ROOT / "data/flower_photos_augmented"

def main():
    file = download_file_from_url(FLOWERS_DATASET_URL, DATA_DIR)
    data = extract_tar(file, DATA_DIR)
    delete_file(file)
    augmented_data = augment_and_save_dataset(data, AUGMENTED_DIR)

if __name__ == "__main__":
    main()