import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String

from app.infrastructure.db.database import Base



class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, unique=True, nullable=False)
    
