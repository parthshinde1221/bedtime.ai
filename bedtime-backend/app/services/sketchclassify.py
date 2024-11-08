import os
import torch
import numpy as np
from app.models.efficient_b0 import load_model
from app.models.dataset import Dataset
from app.utils import preprocess_image
from fastapi import HTTPException

# Initialize the device and model once at the start
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = load_model(num_classes=250, model_path="app/artifacts/model.pth")
model.to(device)
model.eval()  


label_map = {str(i): label for i, label in enumerate(["airplane", "alarm clock", "angel", "ant", "apple", "arm", "armchair", "ashtray", "axe", "backpack", "banana", "barn", "baseball bat", "basket", "bathtub", "bear (animal)", "bed", "bee", "beer-mug", "bell", "bench", "bicycle", "binoculars", "blimp", "book", "bookshelf", "boomerang", "bottle opener", "bowl", "brain", "bread", "bridge", "bulldozer", "bus", "bush", "butterfly", "cabinet", "cactus", "cake", "calculator", "camel", "camera", "candle", "cannon", "canoe", "car (sedan)", "carrot", "castle", "cat", "cell phone", "chair", "chandelier", "church", "cigarette", "cloud", "comb", "computer monitor", "computer-mouse", "couch", "cow", "crab", "crane (machine)", "crocodile", "crown", "cup", "diamond", "dog", "dolphin", "donut", "door", "door handle", "dragon", "duck", "ear", "elephant", "envelope", "eye", "eyeglasses", "face", "fan", "feather", "fire hydrant", "fish", "flashlight", "floor lamp", "flower with stem", "flying bird", "flying saucer", "foot", "fork", "frog", "frying-pan", "giraffe", "grapes", "grenade", "guitar", "hamburger", "hammer", "hand", "harp", "hat", "head", "head-phones", "hedgehog", "helicopter", "helmet", "horse", "hot air balloon", "hot-dog", "hourglass", "house", "human-skeleton", "ice-cream-cone", "ipod", "kangaroo", "key", "keyboard", "knife", "ladder", "laptop", "leaf", "lightbulb", "lighter", "lion", "lobster", "loudspeaker", "mailbox", "megaphone", "mermaid", "microphone", "microscope", "monkey", "moon", "mosquito", "motorbike", "mouse (animal)", "mouth", "mug", "mushroom", "nose", "octopus", "owl", "palm tree", "panda", "paper clip", "parachute", "parking meter", "parrot", "pear", "pen", "penguin", "person sitting", "person walking", "piano", "pickup truck", "pig", "pigeon", "pineapple", "pipe (for smoking)", "pizza", "potted plant", "power outlet", "present", "pretzel", "pumpkin", "purse", "rabbit", "race car", "radio", "rainbow", "revolver", "rifle", "rollerblades", "rooster", "sailboat", "santa claus", "satellite", "satellite dish", "saxophone", "scissors", "scorpion", "screwdriver", "sea turtle", "seagull", "shark", "sheep", "ship", "shoe", "shovel", "skateboard", "skull", "skyscraper", "snail", "snake", "snowboard", "snowman", "socks", "space shuttle", "speed-boat", "spider", "sponge bob", "spoon", "squirrel", "standing bird", "stapler", "strawberry", "streetlight", "submarine", "suitcase", "sun", "suv", "swan", "sword", "syringe", "t-shirt", "table", "tablelamp", "teacup", "teapot", "teddy-bear", "telephone", "tennis-racket", "tent", "tiger", "tire", "toilet", "tomato", "tooth", "toothbrush", "tractor", "traffic light", "train", "tree", "trombone", "trousers", "truck", "trumpet", "tv", "umbrella", "van", "vase", "violin", "walkie talkie", "wheel", "wheelbarrow", "windmill", "zebra"])}


def sketch_classify(image_data: bytes):
    if not isinstance(image_data, bytes):
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Invalid input type",
                "message": "'image_data' must be provided in bytes format."
            }
        )

    try:
        image_tensor = preprocess_image(image_data).to(device)

        # Perform inference
        with torch.no_grad():
            output = model(image_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            confidence, predicted_idx = torch.max(probabilities, dim=0)

            # Get the predicted label
            predicted_label = label_map.get(str(predicted_idx.item()), "Unknown")

        # Return the structured response
        return {
            "prediction": predicted_label,
            "confidence": confidence.item()
        }

    except Exception as e:
        # Return a structured error response if an error occurs
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Classification error",
                "message": f"An error occurred during image classification: {str(e)}"
            }
        )