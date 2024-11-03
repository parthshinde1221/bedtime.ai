import os
import numpy as np
from sklearn.model_selection import train_test_split

def prepare_train_val_test_data(processed_dir, test_size=0.2, random_state=42):
    # Load processed training data
    train_images_file = os.path.join(processed_dir, 'train_images.npz')
    train_labels_file = os.path.join(processed_dir, 'train_labels.npz')
    test_images_file = os.path.join(processed_dir, 'test_images.npz')
    test_labels_file = os.path.join(processed_dir, 'test_labels.npz')
    
    # Check if files exist
    if not all(os.path.exists(file) for file in [train_images_file, train_labels_file, test_images_file, test_labels_file]):
        raise FileNotFoundError("Processed data files not found. Please run preprocess_data first.")
    
    # Load train images and labels
    train_images = np.load(train_images_file)['images']
    train_labels = np.load(train_labels_file)['labels']
    
    # Load test images and labels
    test_images = np.load(test_images_file)['images']
    test_labels = np.load(test_labels_file)['labels']

    # Debugging check
    print(f"Loaded {train_images.shape[0]} train images and {train_labels.shape[0]} train labels")
    print(f"Loaded {test_images.shape[0]} test images and {test_labels.shape[0]} test labels")

    # Ensure data isn't empty
    if train_images.size == 0 or train_labels.size == 0 or test_images.size == 0 or test_labels.size == 0:
        raise ValueError("One of the datasets is empty. Check the data preparation process.")

    # Normalize images
    train_images = train_images.astype(np.float32) / 255.0  # Scale train images to [0, 1]
    test_images = test_images.astype(np.float32) / 255.0  # Scale test images to [0, 1]
    
    # Split train data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        train_images, train_labels, test_size=test_size, random_state=random_state
    )
    
    # Save the split data
    np.savez_compressed(os.path.join(processed_dir, 'X_train.npz'), images=X_train)
    np.savez_compressed(os.path.join(processed_dir, 'y_train.npz'), labels=y_train)
    np.savez_compressed(os.path.join(processed_dir, 'X_val.npz'), images=X_val)
    np.savez_compressed(os.path.join(processed_dir, 'y_val.npz'), labels=y_val)
    
    # Save test data
    np.savez_compressed(os.path.join(processed_dir, 'X_test.npz'), images=test_images)
    np.savez_compressed(os.path.join(processed_dir, 'y_test.npz'), labels=test_labels)
    
    print("Training, validation, and test data preparation completed.")
    return {
        "train_size": len(X_train),
        "val_size": len(X_val),
        "test_size": len(test_images)
    }
