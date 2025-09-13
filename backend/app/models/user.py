import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, LargeBinary, String, Numeric

from app.infrastructure.db.database import Base



class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)  
    currency_code = Column(String(3), ForeignKey("currencies.iso_code"), nullable=False)
    goal = Column(Numeric(precision=18, scale=4), nullable=False, server_default="0")  
    savings = Column(Numeric(18, 4), nullable=False, server_default="0")
    balance = Column(Numeric(18, 4), nullable=False, server_default="0")
