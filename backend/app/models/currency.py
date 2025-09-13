import uuid
from sqlalchemy import Column, String

from app.infrastructure.db.database import Base

class Currency(Base):
    __tablename__ = "currencies"
    
    iso_code = Column(String(3), primary_key=True)
    name = Column(String, nullable=False)
    symbol = Column(String)
