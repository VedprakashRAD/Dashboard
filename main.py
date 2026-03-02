from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Dashboard Symbol Identification API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load symbols data
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "symbols_data.json")

def load_symbols():
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

SYMBOLS_DB = load_symbols()

class SymbolResponse(BaseModel):
    id: int
    name: str
    description: str
    recommendation: str
    severity: str
    confidence: float

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Serve all static files under /frontend and /assets
# Using html=True allows serving index.html automatically
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
# Ensure the main frontend directory is accessible
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/symbols", response_model=List[dict])
async def get_all_symbols():
    return SYMBOLS_DB

from backend.inference import inference_engine

class PredictResponse(BaseModel):
    status: str
    message: Optional[str] = None
    symbols: List[dict] = []

@app.post("/predict", response_model=PredictResponse)
async def predict_symbol(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save temp file for YOLO
    temp_path = f"tmp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Run inference logic using our singleton engine
        result = inference_engine.predict(temp_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
