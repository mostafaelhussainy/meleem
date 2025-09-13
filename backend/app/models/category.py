import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, String

from app.infrastructure.db.database import Base
from app.schemas.transaction_schema import CategoryType



class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    type = Column(Enum(CategoryType, name="category_type"), nullable=False)  # 👈

