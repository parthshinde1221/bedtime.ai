# app/main.py
from fastapi import FastAPI
from app.routers import infer

app = FastAPI()

# Include routers
app.include_router(infer.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Project!"}
