from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.db.database import get_db
from src.api.models import Pill
from src.api.schemas import PillCreate, PillResponse

router = APIRouter(prefix="/pills", tags=["pills"])


@router.post("/", response_model=PillResponse, status_code=201)
def add_barcode(pill: PillCreate, db: Session = Depends(get_db)):
    """Add barcode(s) to a pill. Creates pill if it doesn't exist."""
    db_pill = db.query(Pill).filter(Pill.name == pill.name).first()

    if db_pill:
        # Pill exists - add new barcodes to existing list (avoid duplicates)
        existing_barcodes = set(db_pill.barcodes)
        new_barcodes = set(pill.barcodes)
        db_pill.barcodes = list(existing_barcodes | new_barcodes)
    else:
        # Pill doesn't exist - create new
        db_pill = Pill(name=pill.name, barcodes=pill.barcodes)
        db.add(db_pill)

    db.commit()
    db.refresh(db_pill)
    return db_pill


@router.get("/", response_model=List[PillResponse])
def get_all_pills(db: Session = Depends(get_db)):
    """Get all pills"""
    pills = db.query(Pill).all()
    return pills


@router.get("/{pill_name}", response_model=PillResponse)
def get_barcodes_by_name(pill_name: str, db: Session = Depends(get_db)):
    """Get barcodes for a specific pill by name"""
    pill = db.query(Pill).filter(Pill.name == pill_name).first()
    if not pill:
        raise HTTPException(status_code=404, detail="Pill not found")
    return pill