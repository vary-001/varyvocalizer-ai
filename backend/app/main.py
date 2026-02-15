from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from .config import settings
from .tasks import separate_audio
from celery.result import AsyncResult

app = FastAPI(title="VaryVocalizer API")

# CORS - Allow your frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Clean filename to avoid spaces/weird characters breaking the path
    safe_filename = file.filename.replace(" ", "_")
    file_location = os.path.join(settings.UPLOAD_DIR, safe_filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    task = separate_audio.delay(file_location, safe_filename)
    
    return {"task_id": task.id, "filename": safe_filename}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == 'PENDING':
        return {"state": "PENDING"}
    elif task_result.state != 'FAILURE':
        return {"state": task_result.state, "result": task_result.result}
    else:
        return {"state": "FAILURE", "error": str(task_result.info)}

@app.get("/download/{song_folder}/{stem}")
async def download_stem(song_folder: str, stem: str):
    # Construct path: storage/separated/htdemucs/song_name/stem_file
    # Note: stem will be "vocals.mp3" or "no_vocals.mp3"
    file_path = os.path.join(settings.RESULTS_DIR, "htdemucs", song_folder, stem)
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return HTTPException(status_code=404, detail="File not found")