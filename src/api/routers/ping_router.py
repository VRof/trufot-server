from datetime import datetime, timezone

from fastapi import APIRouter

from src.api.schemas import PingResponse

router = APIRouter()

@router.get("/ping",summary="server ping", response_model=PingResponse,tags=["server health check"] )
async def ping():
    return PingResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc)
)

