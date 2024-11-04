
import torch
import torch.nn as nn
from torchvision.models import efficientnet_b0

def get_efficientnet_b0_single_channel(num_classes):
    # Load the pre-trained EfficientNet-B0 model
    efficientnet = efficientnet_b0(pretrained=True)
    
    # Modify the first convolutional layer to accept single-channel input
    original_conv1 = efficientnet.features[0][0]
    efficientnet.features[0][0] = nn.Conv2d(
        in_channels=1,
        out_channels=original_conv1.out_channels,
        kernel_size=original_conv1.kernel_size,
        stride=original_conv1.stride,
        padding=original_conv1.padding,
        bias=(original_conv1.bias is not None)
    )
    
    # Copy and average the weights from the original conv1 layer
    with torch.no_grad():
        efficientnet.features[0][0].weight = nn.Parameter(
            original_conv1.weight.mean(dim=1, keepdim=True)
        )
    
    # Replace the final fully connected layer to match the number of classes
    efficientnet.classifier[1] = nn.Linear(efficientnet.classifier[1].in_features, num_classes)
    
    return efficientnet

# Usage
def load_model(num_classes):
    model = get_efficientnet_b0_single_channel(num_classes=num_classes)
    return model



# import torch
# import torch.nn as nn
# import torchvision.models as models

# def get_resnet50_single_channel(num_classes):
#     # Load the pre-trained ResNet-50 model
#     resnet50 = models.resnet50(pretrained=True)
    
#     # Modify the first convolutional layer to accept single-channel input
#     original_conv1 = resnet50.conv1
#     resnet50.conv1 = nn.Conv2d(
#         in_channels=1,
#         out_channels=original_conv1.out_channels,
#         kernel_size=original_conv1.kernel_size,
#         stride=original_conv1.stride,
#         padding=original_conv1.padding,
#         bias=(original_conv1.bias is not None)
#     )
    
#     # Copy and average the weights from the original conv1 layer
#     with torch.no_grad():
#         resnet50.conv1.weight = nn.Parameter(
#             original_conv1.weight.mean(dim=1, keepdim=True)
#         )
    
#     # Replace the final fully connected layer
#     resnet50.fc = nn.Linear(resnet50.fc.in_features, num_classes)
    
#     return resnet50

# # Usage


# def load_model(num_classes):
#     model = get_resnet50_single_channel(num_classes=num_classes)
#     return model

# import torch
# import torch.nn as nn
# import torchvision.models as models

# def get_resnet18_single_channel(num_classes):
#     # Load the pre-trained ResNet-18 model
#     resnet18 = models.resnet18(pretrained=True)
    
#     # Modify the first convolutional layer to accept single-channel input
#     original_conv1 = resnet18.conv1
#     resnet18.conv1 = nn.Conv2d(
#         in_channels=1,
#         out_channels=original_conv1.out_channels,
#         kernel_size=original_conv1.kernel_size,
#         stride=original_conv1.stride,
#         padding=original_conv1.padding,
#         bias=(original_conv1.bias is not None)
#     )
    
#     # Copy and average the weights from the original conv1 layer
#     with torch.no_grad():
#         resnet18.conv1.weight = nn.Parameter(
#             original_conv1.weight.mean(dim=1, keepdim=True)
#         )
    
#     # Replace the final fully connected layer to match the number of classes
#     resnet18.fc = nn.Linear(resnet18.fc.in_features, num_classes)
    
#     return resnet18

# # Usage
# def load_model(num_classes):
#     model = get_resnet18_single_channel(num_classes=num_classes)
#     return model