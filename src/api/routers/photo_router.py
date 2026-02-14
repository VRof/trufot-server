from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from pathlib import Path
import shutil

from src.api.schemas import PhotoUploadResponse

router = APIRouter(prefix="/photos", tags=["pills photos"])

PHOTOS_BASE_DIR = "/app/photos"


@router.post("/upload", response_model=PhotoUploadResponse, status_code=201)
async def upload_photo(
        uid: str = Form(...),
        photo: UploadFile = File(...)
):
    """
    Upload photo. Filename format: YYYY-MM-DD_HH-MM-SS.ext
    Example: 2024-02-14_15-30-45.jpg
    """

    # Validate image
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Parse filename: YYYY-MM-DD_HH-MM-SS.ext
    try:
        filename = photo.filename
        name_without_ext = filename.rsplit(".", 1)[0]
        date_str, time_str = name_without_ext.split("_")
        file_ext = filename.split(".")[-1]
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename format. Expected: YYYY-MM-DD_HH-MM-SS.ext"
        )

    # Create path: photos/{uid}/{date}/{time}.ext
    photo_dir = Path(PHOTOS_BASE_DIR) / uid / date_str
    photo_dir.mkdir(parents=True, exist_ok=True)

    file_path = photo_dir / f"{time_str}.{file_ext}"

    # Save file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    return PhotoUploadResponse(
        message="Photo uploaded successfully",
        file_path=str(file_path),
        uid=uid,
        date=date_str,
        time=time_str
    )


@router.get("/list/{uid}")
async def list_photos(uid: str):
    """List all photos for a user"""
    user_dir = Path(PHOTOS_BASE_DIR) / uid

    if not user_dir.exists():
        return {"uid": uid, "photos": []}

    photos = []
    for date_dir in sorted(user_dir.iterdir()):
        if date_dir.is_dir():
            for photo_file in sorted(date_dir.iterdir()):
                if photo_file.is_file():
                    photos.append(str(photo_file))

    return {"uid": uid, "total": len(photos), "photos": photos}