from sqlalchemy import Column, String, ARRAY
from src.db.database import Base


class Pill(Base):
    __tablename__ = "pills"

    name = Column(String, primary_key=True, index=True)
    barcodes = Column(ARRAY(String), nullable=False, default=[])