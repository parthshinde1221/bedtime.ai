from PIL import Image
from io import BytesIO
from torchvision import transforms

def preprocess_image(image_data: bytes):
    image = Image.open(BytesIO(image_data)).convert("L")  
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    image = transform(image).unsqueeze(0)  
    return image
