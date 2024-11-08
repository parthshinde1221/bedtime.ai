from pydantic_settings import BaseSettings
from typing import ClassVar
import torch

class Config(BaseSettings):
    MODEL_PATH: str = "app/artifacts/model.pth"
    NUM_CLASSES: int = 250
