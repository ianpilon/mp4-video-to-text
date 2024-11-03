from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from moviepy.editor import VideoFileClip
import os
import shutil
import tempfile
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Starting conversion of {file.filename}")
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create paths for temporary files
            temp_input = Path(temp_dir) / f"input_{file.filename}"
            temp_output = Path(temp_dir) / f"output_{file.filename.replace('.mp4', '.mp3')}"

            # Save uploaded file
            with open(temp_input, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Convert to MP3
            video = VideoFileClip(str(temp_input))
            video.audio.write_audiofile(str(temp_output))
            video.close()

            # Return the converted file
            return FileResponse(
                str(temp_output),
                media_type="audio/mpeg",
                filename=temp_output.name
            )

    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return {"error": str(e)}

# Clean up function to remove old files
@app.on_event("startup")
async def startup_event():
    # Clean uploads directory
    for file in os.listdir("uploads"):
        file_path = os.path.join("uploads", file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error: {e}")

    # Clean downloads directory
    for file in os.listdir("downloads"):
        file_path = os.path.join("downloads", file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error: {e}")
