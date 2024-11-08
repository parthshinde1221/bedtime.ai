import torch
import torch.nn as nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

def load_model(num_classes, model_path="app/artifacts/model.pth"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = efficientnet_b0(weights=EfficientNet_B0_Weights.IMAGENET1K_V1)
    model.features[0][0] = nn.Conv2d(
        in_channels=1, 
        out_channels=model.features[0][0].out_channels,
        kernel_size=model.features[0][0].kernel_size,
        stride=model.features[0][0].stride,
        padding=model.features[0][0].padding,
        bias=False
    )
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    
    # Load model weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)  
    model.eval()     
    return model
