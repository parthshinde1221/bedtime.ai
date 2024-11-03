import os
from make_dataset import download_dataset
from preprocess import preprocess_data
from preprocess_inner import prepare_train_val_test_data
import mlflow

def prepare_data():
    raw_dir = "data/raw"
    processed_dir = "data/processed"

    # Check if raw data exists, if not, download it
    if not os.path.exists(os.path.join(raw_dir, 'label_names.txt')):
        print("Raw data not found. Downloading dataset...")
        download_results = download_dataset(raw_dir)
        if not download_results:
            print("Failed to download dataset. Exiting.")
            return

    # Now proceed with preprocessing
    with mlflow.start_run(run_name="data_preparation"):
        results = preprocess_data(raw_dir, processed_dir)
        
        # Log general parameters about the raw and processed directories
        mlflow.log_param("raw_data_dir", raw_dir)
        mlflow.log_param("processed_data_dir", processed_dir)
        mlflow.log_param("train_size", results['train_size'])
        mlflow.log_param("num_classes", results['num_classes'])
        
        # Log the processed data files as artifacts
        for file in os.listdir(processed_dir):
            mlflow.log_artifact(os.path.join(processed_dir, file))
        
        # Prepare train, validation, and test data
        train_test_results = prepare_train_val_test_data(processed_dir)
        
        # Log sizes of the train, validation, and test sets
        mlflow.log_param("train_data_size", train_test_results['train_size'])
        mlflow.log_param("val_data_size", train_test_results['val_size'])
        mlflow.log_param("test_data_size", train_test_results['test_size'])
        
        # Log the train/validation/test split files as artifacts
        mlflow.log_artifact(os.path.join(processed_dir, 'X_train.npz'))
        mlflow.log_artifact(os.path.join(processed_dir, 'y_train.npz'))
        mlflow.log_artifact(os.path.join(processed_dir, 'X_val.npz'))
        mlflow.log_artifact(os.path.join(processed_dir, 'y_val.npz'))
        mlflow.log_artifact(os.path.join(processed_dir, 'X_test.npz'))
        mlflow.log_artifact(os.path.join(processed_dir, 'y_test.npz'))

    print(f"Data preparation completed. Processed {results['train_size']} images across {results['num_classes']} classes.")
    print(f"Training data: {train_test_results['train_size']} images, Validation data: {train_test_results['val_size']} images, Test data: {train_test_results['test_size']} images.")

if __name__ == "__main__":
    prepare_data()
