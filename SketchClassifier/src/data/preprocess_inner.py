import os
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def prepare_train_val_test_data(processed_dir, test_size=0.2, random_state=42):
    train_images_file = os.path.join(processed_dir, 'train_images.npz')
    train_labels_file = os.path.join(processed_dir, 'train_labels.npz')
    test_images_file = os.path.join(processed_dir, 'test_images.npz')
    test_labels_file = os.path.join(processed_dir, 'test_labels.npz')
    
    if not all(os.path.exists(file) for file in [train_images_file, train_labels_file, test_images_file, test_labels_file]):
        logging.error("Processed data files not found.")
        raise FileNotFoundError("Processed data files not found.")
    
    # Load the data
    train_images = np.load(train_images_file)['images']
    train_labels = np.load(train_labels_file)['labels']
    test_images = np.load(test_images_file)['images']
    test_labels = np.load(test_labels_file)['labels']

    logging.info(f"Loaded {train_images.shape[0]} train images and {train_labels.shape[0]} train labels")
    logging.info(f"Loaded {test_images.shape[0]} test images and {test_labels.shape[0]} test labels")

    # Check for empty datasets
    if train_images.size == 0 or train_labels.size == 0 or test_images.size == 0 or test_labels.size == 0:
        logging.error("One of the datasets is empty.")
        raise ValueError("One of the datasets is empty.")

    # Normalize the images
    train_images = train_images.astype(np.float32) / 255.0
    test_images = test_images.astype(np.float32) / 255.0

    # Split the train set into train and validation sets
    stratified_split = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)

    for train_index, val_index in stratified_split.split(train_images, train_labels):
        X_train, X_val = train_images[train_index], train_images[val_index]
        y_train, y_val = train_labels[train_index], train_labels[val_index]

    logging.info("Saving final datasets...")
    np.savez_compressed(os.path.join(processed_dir, 'X_train.npz'), images=X_train)
    np.savez_compressed(os.path.join(processed_dir, 'y_train.npz'), labels=y_train)
    np.savez_compressed(os.path.join(processed_dir, 'X_val.npz'), images=X_val)
    np.savez_compressed(os.path.join(processed_dir, 'y_val.npz'), labels=y_val)
    np.savez_compressed(os.path.join(processed_dir, 'X_test.npz'), images=test_images)
    np.savez_compressed(os.path.join(processed_dir, 'y_test.npz'), labels=test_labels)

    logging.info("Training, validation, and test data preparation completed.")
    return {
        "train_size": len(X_train),
        "val_size": len(X_val),
        "test_size": len(test_images)
    }
