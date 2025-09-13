import uuid
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import Column, ForeignKey, String, Numeric, DateTime

from app.infrastructure.db.database import Base

class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    amount = Column(Numeric(precision=18, scale=4), nullable=False)
    currency_id = Column(String(3), ForeignKey("currencies.iso_code"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    frequency = Column(ENUM('daily', 'weekly', 'monthly', 'yearly', name='recurring_transactions_frequency', create_type=False), nullable=False)
    next_due_date = Column(DateTime(timezone=True), nullable=False)