from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.sketchclassify import sketch_classify
from pydantic import BaseModel
from app.services.storybuilding import generate_story
from fastapi.responses import FileResponse
import base64
import random  # Import random module
import os

router = APIRouter()

class ImageData(BaseModel):
    image_base64: str

@router.post("/infer/sketchclassify")
async def infer(image_data: ImageData):
    try:
        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data.image_base64)
        print("Debug: File size (bytes):", len(image_bytes))  # Check size

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="No image provided or image is empty."
            )
        predictions=  sketch_classify(image_bytes)
        
        base64_audio = generate_story(predictions)
        return {"success": True, "audio": base64_audio}
 
    except base64.binascii.Error:
        raise HTTPException(
            status_code=422,
            detail="Invalid base64-encoded data."
        )

@router.post("/infer/update")
async def infer_update(data: dict):
    try:
        # Pass the data dictionary directly to the generate_story function
        base64_audio = generate_story(data)
        return {"success": True, "audio": base64_audio}
    except Exception as e:
        return {"success": False, "error": str(e)}