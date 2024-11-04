import os
import yaml
import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
import mlflow
import mlflow.pytorch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from src.models import load_model

# Custom Dataset Class
class SketchDataset(Dataset):
    def __init__(self, data_path, label_path, transform=None):
        self.data = np.load(data_path)['images']
        self.labels = np.load(label_path)['labels']
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = self.data[idx]
        label = int(self.labels[idx])
        image = Image.fromarray(image.astype('uint8'), mode='L')
        if self.transform:
            image = self.transform(image)
        else:
            image = transforms.ToTensor()(image)
        return image, label

def train_model(config):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Data transforms
    train_transforms = transforms.Compose([
        transforms.RandomRotation(10),
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])  # Adjust as per your dataset
    ])

    val_transforms = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])  # Adjust as per your dataset
    ])

    # Create datasets
    train_dataset = SketchDataset(
        os.path.join(config["data"]["processed_dir"], 'X_train.npz'),
        os.path.join(config["data"]["processed_dir"], 'y_train.npz'),
        #transform=train_transforms
    )

    val_dataset = SketchDataset(
        os.path.join(config["data"]["processed_dir"], 'X_val.npz'),
        os.path.join(config["data"]["processed_dir"], 'y_val.npz'),
        #transform=val_transforms
    )

    # Create data loaders
    train_loader = DataLoader(train_dataset,num_workers=4, batch_size=config["training"]["batch_size"], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=config["training"]["batch_size"], shuffle=False)

    # Initialize model, criterion
    model = load_model(num_classes=config["model"]["num_classes"]).to(device)
    criterion = nn.CrossEntropyLoss()

    # Separate parameters for different learning rates
    feature_extractor_params = []
    classifier_params = []
    for name, param in model.named_parameters():
        if 'fc' in name or 'conv1' in name:
            classifier_params.append(param)
        else:
            feature_extractor_params.append(param)

    # Use different learning rates
    optimizer = optim.Adam([
        {'params': feature_extractor_params, 'lr': config["training"]["pre_trained_lr"]},
        {'params': classifier_params, 'lr': config["training"]["classifier_lr"]}
    ])

    # Learning rate scheduler
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=config["training"]["lr_step_size"], gamma=config["training"]["lr_gamma"])

    # Early stopping parameters
    patience = config["training"].get("patience", 5)
    min_delta = config["training"].get("min_delta", 0.01)
    best_val_loss = float("inf")
    patience_counter = 0

    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    with mlflow.start_run(run_name=config["mlflow"]["run_name"]):
        mlflow.log_params(config["model"])
        mlflow.log_params(config["training"])

        # Training loop
        for epoch in range(config["training"]["num_epochs"]):
            model.train()
            running_loss = 0.0
            correct_train = 0
            total_train = 0
            for i, (images, labels) in enumerate(train_loader):
                images, labels = images.to(device), labels.to(device)

                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # Statistics
                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total_train += labels.size(0)
                correct_train += (predicted == labels).sum().item()

                # Log batch loss
                mlflow.log_metric("batch_train_loss", loss.item(), step=epoch * len(train_loader) + i)

            avg_train_loss = running_loss / len(train_loader)
            train_accuracy = 100 * correct_train / total_train
            mlflow.log_metric("epoch_train_loss", avg_train_loss, step=epoch)
            mlflow.log_metric("epoch_train_accuracy", train_accuracy, step=epoch)

            # Validation phase
            model.eval()
            val_loss = 0.0
            correct_val = 0
            total_val = 0
            with torch.no_grad():
                for images, labels in val_loader:
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    val_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    total_val += labels.size(0)
                    correct_val += (predicted == labels).sum().item()

            avg_val_loss = val_loss / len(val_loader)
            val_accuracy = 100 * correct_val / total_val
            mlflow.log_metric("epoch_val_loss", avg_val_loss, step=epoch)
            mlflow.log_metric("epoch_val_accuracy", val_accuracy, step=epoch)

            print(f"Epoch [{epoch + 1}/{config['training']['num_epochs']}], "
                  f"Train Loss: {avg_train_loss:.4f}, Train Acc: {train_accuracy:.2f}%, "
                  f"Val Loss: {avg_val_loss:.4f}, Val Acc: {val_accuracy:.2f}%")

            # Early stopping check
            if avg_val_loss < best_val_loss - min_delta:
                best_val_loss = avg_val_loss
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= patience:
                print("Early stopping triggered.")
                break

            # Step the scheduler
            scheduler.step()

if __name__ == "__main__":
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    train_model(config)
