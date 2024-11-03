# src/models/train_model.py

import mlflow
import numpy as np
import json
import os

def load_data():
    processed_dir = "data/processed"
    X_train = np.load(os.path.join(processed_dir, 'train_images.npy'))
    y_train = np.load(os.path.join(processed_dir, 'train_labels.npy'))
    X_test = np.load(os.path.join(processed_dir, 'test_images.npy'))
    y_test = np.load(os.path.join(processed_dir, 'test_labels.npy'))
    
    with open(os.path.join(processed_dir, 'label_map.json'), 'r') as f:
        label_map = json.load(f)
    
    return X_train, y_train, X_test, y_test, label_map

def train_model():
    with mlflow.start_run():
        # Load prepared data
        X_train, y_train, X_test, y_test, label_map = load_data()
        
        mlflow.log_param("data_source", "prepared_data")
        mlflow.log_param("num_train_samples", len(X_train))
        mlflow.log_param("num_test_samples", len(X_test))
        mlflow.log_param("num_classes", len(label_map))

        # Your model training code here
        # ...

if __name__ == "__main__":
    train_model()