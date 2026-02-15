import subprocess
import os
from celery import Celery
from .config import settings

celery_app = Celery(
    "vary_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery_app.task(bind=True, name="separate_audio")
def separate_audio(self, file_path: str, filename: str):
    """
    Runs Demucs in '2-stem' mode:
    1. vocals.mp3
    2. no_vocals.mp3 (The Instrumental)
    """
    
    output_dir = settings.RESULTS_DIR
    
    # The Command
    # --two-stems=vocals : This is the magic flag. It mixes the instrumental parts.
    command = [
        "demucs",
        "-n", "htdemucs",      # High Quality Model
        "--two-stems=vocals",  # Force 2 outputs only
        "--mp3",               # Output MP3
        "--mp3-bitrate", "320",# High Quality Bitrate
        "-o", output_dir,
        file_path
    ]

    try:
        print(f"--> Starting Vocal Removal for {filename}...")
        subprocess.run(command, check=True)
        
        # Demucs folder structure: output_dir/htdemucs/song_name/
        song_folder_name = os.path.splitext(filename)[0]
        
        # Verify files exist
        # Demucs names the instrumental "no_vocals.mp3" when using this flag
        result_path = os.path.join(output_dir, "htdemucs", song_folder_name)
        
        if not os.path.exists(result_path):
            return {"status": "failed", "error": "Output folder not found"}

        # Return simplified structure
        return {
            "status": "completed",
            "song_id": song_folder_name,
            "stems": {
                "vocals": f"/download/{song_folder_name}/vocals.mp3",
                "instrumental": f"/download/{song_folder_name}/no_vocals.mp3"
            }
        }

    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": "Processing failed inside Demucs"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}