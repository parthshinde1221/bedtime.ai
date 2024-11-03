from datasets import load_dataset
import os
from PIL import Image
from tqdm import tqdm

def download_dataset(save_dir):
    try:
        # Load both train and test splits
        train_dataset = load_dataset("sdiaeyu6n/tu-berlin", split="train")
        test_dataset = load_dataset("sdiaeyu6n/tu-berlin", split="test")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

    # Create directories if they don't exist
    os.makedirs(os.path.join(save_dir, 'train'), exist_ok=True)
    os.makedirs(os.path.join(save_dir, 'test'), exist_ok=True)

    # Save images and labels
    for split, dataset in [('train', train_dataset), ('test', test_dataset)]:
        for idx, item in tqdm(enumerate(dataset), desc=f"Saving {split} images", total=len(dataset)):
            image_path = os.path.join(save_dir, split, f"{idx}_{item['label']}.png")
            try:
                item['image'].save(image_path)
            except Exception as e:
                print(f"Error saving image {idx} in {split} split: {e}")

    # Save label names
    label_names = train_dataset.features['label'].names
    with open(os.path.join(save_dir, 'label_names.txt'), 'w') as f:
        for name in label_names:
            f.write(f"{name}\n")

    # Save class indices and their corresponding labels
    with open(os.path.join(save_dir, 'class_labels.txt'), 'w') as f:
        for idx, name in enumerate(label_names):
            f.write(f"{idx},{name}\n")

    print(f"Number of classes: {len(label_names)}")
    print(f"First few class names: {label_names[:5]}")
    print(f"Train dataset size: {len(train_dataset)}")
    print(f"Test dataset size: {len(test_dataset)}")
    
    return {
        "num_classes": len(label_names),
        "train_size": len(train_dataset),
        "test_size": len(test_dataset)
    }

if __name__ == "__main__":
    results = download_dataset("data/raw")
    if results:
        print(f"Dataset downloaded. Classes: {results['num_classes']}, Train size: {results['train_size']}, Test size: {results['test_size']}")
    else:
        print("Failed to download dataset.")
