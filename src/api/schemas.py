from pydantic import BaseModel
from typing import List
from datetime import datetime

class PingResponse(BaseModel):
    status: str
    timestamp: datetime

class PillBase(BaseModel):
    name: str
    barcodes: List[str]

class PillCreate(PillBase):
    pass

class PillResponse(PillBase):
    class Config:
        from_attributes = True
        
class PhotoUploadResponse(BaseModel):
    message: str
    file_path: str
    uid: str
    date: str
    time: str