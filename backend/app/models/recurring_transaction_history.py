import uuid
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, Numeric, DateTime

from app.infrastructure.db.database import Base

class RecurringTransactionHistory(Base):
    __tablename__ = "recurring_transaction_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recurring_transaction_id = Column(UUID(as_uuid=True), ForeignKey("recurring_transactions.id"), nullable=False)
    triggered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
