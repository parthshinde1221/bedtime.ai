# app/routers/items.py
from fastapi import APIRouter
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.sketchclassify import sketch_classify
from pydantic import BaseModel
import base64
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
        return sketch_classify(image_bytes)

    except base64.binascii.Error:
        raise HTTPException(
            status_code=422,
            detail="Invalid base64-encoded data."
        )
