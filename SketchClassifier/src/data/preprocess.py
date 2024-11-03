import os
import numpy as np
from PIL import Image
import json
from tqdm import tqdm
from skimage.transform import resize
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_single_image(img_path, target_size, reverse_label_map, verbose=False):
    try:
        if verbose:
            print(f"Processing image: {img_path}")
        with Image.open(img_path) as img:
            img_array = np.array(img.convert('L'), dtype=np.uint8)
        
        # Resize image
        img_array = resize(img_array, target_size, anti_aliasing=True)
        img_array = (img_array * 255).astype(np.uint8)  # Scale to 0-255 range
        
        # Extract label (index) from filename
        filename = os.path.basename(img_path)
        label_index = int(filename.split('_')[1].split('.')[0])
        if verbose:
            print(f"Extracted label index '{label_index}' from filename '{filename}'")

        # Check if label index exists in reverse_label_map
        if label_index not in reverse_label_map:
            if verbose:
                print(f"Warning: Label index '{label_index}' not found in reverse_label_map.")
            return None, None
        
        # Get the corresponding label name
        label = reverse_label_map[label_index]
        if verbose:
            print(f"Mapped label index '{label_index}' to label '{label}'")

        return img_array, label_index
    except Exception as e:
        if verbose:
            print(f"Error processing image {img_path}: {e}")
        return None, None

def preprocess_data(raw_dir, processed_dir, target_size=(224, 224), max_images=20000, verbose=False):
    os.makedirs(processed_dir, exist_ok=True)

    # Load label names
    label_names_file = os.path.join(raw_dir, 'label_names.txt')
    if verbose:
        print(f"Loading label names from {label_names_file}")
    with open(label_names_file, 'r') as f:
        label_names = [line.strip() for line in f]

    # Create label map and reverse label map
    label_map = {name: idx for idx, name in enumerate(label_names)}
    reverse_label_map = {idx: name for name, idx in label_map.items()}
    if verbose:
        print(f"Created reverse_label_map: {reverse_label_map}")

    # Process train and test data
    for split in ['train', 'test']:
        split_dir = os.path.join(raw_dir, split)
        if not os.path.exists(split_dir):
            if verbose:
                print(f"Directory {split_dir} not found. Skipping...")
            continue

        if verbose:
            print(f"Processing {split} data in {split_dir}")
        
        # Initialize empty lists for images and labels
        images = []
        labels = []
        
        # Paths for processed files
        images_file = os.path.join(processed_dir, f'{split}_images.npz')
        labels_file = os.path.join(processed_dir, f'{split}_labels.npz')

        # Flags to determine what needs processing
        process_images = not os.path.exists(images_file)
        process_labels = not os.path.exists(labels_file)

        if not process_images and not process_labels:
            if verbose:
                print(f"Both processed files for {split} data already exist. Skipping...")
            continue

        image_paths = [os.path.join(split_dir, filename) for filename in os.listdir(split_dir)[:max_images]]
        if verbose:
            print(f"Processing up to {max_images} images for {split} split")

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_single_image, img_path, target_size, reverse_label_map, verbose): img_path for img_path in image_paths}
            for future in tqdm(as_completed(futures), total=len(futures), desc=f"Processing {split} images"):
                img_array, label_index = future.result()
                if img_array is not None and label_index is not None:
                    if process_images:
                        images.append(img_array)
                    if process_labels:
                        labels.append(label_index)

        if verbose:
            print(f"Finished processing {split} images. Collected {len(images)} images and {len(labels)} labels.")
        
        # Save processed data only for missing files
        if process_images:
            if images:
                np.savez_compressed(images_file, images=np.array(images))
                if verbose:
                    print(f"Saved images to {images_file}")
            else:
                if verbose:
                    print(f"No images to save for {split}.")

        if process_labels:
            if labels:
                np.savez_compressed(labels_file, labels=np.array(labels))
                if verbose:
                    print(f"Saved labels to {labels_file}")
            else:
                if verbose:
                    print(f"No labels to save for {split}.")

    # Save label map if it doesn't exist
    label_map_file = os.path.join(processed_dir, 'label_map.json')
    if not os.path.exists(label_map_file):
        with open(label_map_file, 'w') as f:
            json.dump(label_map, f)
        if verbose:
            print(f"Saved label map to {label_map_file}")

    if verbose:
        print("Preprocessing completed.")
        print(f"Processed data saved in {processed_dir}")

    return {
        "train_size": len(images) if process_images else "Already processed",
        "num_classes": len(label_map)
    }

def inspect_npz_file(file_path):
    print(f"Inspecting file: {file_path}")
    with np.load(file_path) as data:
        for key in data.files:
            array = data[key]
            print(f"Array '{key}':")
            print(f"  Shape: {array.shape}")
            print(f"  Data type: {array.dtype}")
            print(f"  Number of elements: {array.size}")
            print()

if __name__ == "__main__":
    # Set verbose to True or False based on preference
    results = preprocess_data("data/raw", "data/processed", max_images=20000, verbose=True)
    print(f"Preprocessing completed. Processed {results['train_size']} images across {results['num_classes']} classes.")
    
    # Inspect the saved npz files
    print("\nInspecting processed .npz files:")
    inspect_npz_file("data/processed/train_images.npz")
    inspect_npz_file("data/processed/test_labels.npz")
