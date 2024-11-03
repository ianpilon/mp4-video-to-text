from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from moviepy.editor import VideoFileClip
import os
import shutil

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create uploads and downloads directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("downloads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert to MP3
        output_path = f"downloads/{os.path.splitext(file.filename)[0]}.mp3"
        video = VideoFileClip(file_path)
        video.audio.write_audiofile(output_path)
        video.close()

        # Clean up uploaded file
        os.remove(file_path)

        # Return the converted file
        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            filename=os.path.basename(output_path)
        )

    except Exception as e:
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
