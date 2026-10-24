import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

from src.utils.files import folder_not_empty

HEIGHT, WIDTH = 180, 180
# Images are loaded a bit larger than the target size so RandomCrop has room to crop from.
LOAD_HEIGHT, LOAD_WIDTH = HEIGHT + 20, WIDTH + 20
TRAINING_BATCH_SIZE = 32
COPIES_PER_IMAGE = 5

basic_augmentation = keras.Sequential([
        layers.RandomRotation(0.2),
        layers.RandomCrop(HEIGHT, WIDTH),
    ], name="basic_data_augmentation")

def augment_and_save_dataset(flowers_data, output_dir=None, copies_per_image=COPIES_PER_IMAGE):
    """Expand the flower photos dataset on disk.

    For every original image, save a (center-cropped) copy of the original plus
    `copies_per_image` randomly rotated/cropped copies into a new directory that
    mirrors the original class-subfolder structure. Returns the new directory.
    """
    if folder_not_empty(output_dir):
        print("There is data in preferred directory", output_dir)
        return output_dir

    augmentation = basic_augmentation
    center_crop = layers.CenterCrop(HEIGHT, WIDTH)

    class_dirs = [d for d in flowers_data.iterdir() if d.is_dir()]

    for class_dir in class_dirs:
        out_class_dir = output_dir / class_dir.name
        out_class_dir.mkdir(parents=True, exist_ok=True)

        for image_path in class_dir.glob('*'):
            image = cv2.imread(str(image_path))
            if image is None:
                continue
            image_resized = cv2.resize(image, (LOAD_WIDTH, LOAD_HEIGHT))
            batch = np.expand_dims(image_resized, axis=0)

            original_cropped = center_crop(batch).numpy()[0]
            original_cropped = np.clip(original_cropped, 0, 255).astype(np.uint8)
            cv2.imwrite(str(out_class_dir / image_path.name), original_cropped)

            for i in range(copies_per_image):
                augmented = augmentation(batch, training=True).numpy()[0]
                augmented = np.clip(augmented, 0, 255).astype(np.uint8)
                augmented_path = out_class_dir / f"{image_path.stem}_aug{i}{image_path.suffix}"
                cv2.imwrite(str(augmented_path), augmented)

    print(f"Expanded dataset saved to {output_dir}")
    return output_dir