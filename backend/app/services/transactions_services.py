from datetime import datetime, timedelta, timezone
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4
from asyncpg import Connection

from app.core.filters_utils import DateFilterEnum, Utils
from app.schemas.transaction_schema import CategoryType

from ..infrastructure.repositories.transaction_repositories import TransactionRepository
from ..core.exceptions.exceptions import InvalidCategoryException

class RecurringFrequencyEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"

class TransactionServices:
    def __init__(self, conn: Connection):
        self.conn = conn
        self.repo = TransactionRepository(conn)
        self.utils = Utils()

    async def get_all_user_transactions(
        self, 
        user_id: UUID, 
        category_type: CategoryType | None,
        transaction_created_at: DateFilterEnum | None
    ):
        created_at = None
        if (transaction_created_at):
            created_at = self.utils.get_date_range(transaction_created_at)

        transactions = await self.repo.get_all_user_transactions(user_id, category_type, created_at)
        return transactions
    
    async def add_user_transaction(
        self, 
        transaction_name: str, 
        transaction_amount: Decimal, 
        currency_code: str,
        user_id: UUID,
        category_id: UUID
    ):
        category_exists = await self.repo.check_category_exists(category_id)
        if not category_exists:
            raise InvalidCategoryException()

        transaction_id = uuid4()
        transaction = await self.repo.add_user_transaction(
            transaction_id, 
            transaction_name, 
            transaction_amount, 
            currency_code,
            user_id,
            category_id
        )
        return transaction
    
    @staticmethod
    def get_next_due_date(frequency: str) -> datetime:
        frequency_due_date = datetime.now(timezone.utc)
        if frequency == RecurringFrequencyEnum.daily:
            frequency_due_date = frequency_due_date + timedelta(days=1)
        elif frequency == RecurringFrequencyEnum.weekly:
            frequency_due_date = frequency_due_date + timedelta(weeks=1)
        elif frequency == RecurringFrequencyEnum.monthly:
            # Handle month rollover properly
            if frequency_due_date.month == 12:
                frequency_due_date = frequency_due_date.replace(year=frequency_due_date.year + 1, month=1)
            else:
                frequency_due_date = frequency_due_date.replace(month=frequency_due_date.month + 1)
        elif frequency == RecurringFrequencyEnum.yearly:
            frequency_due_date = frequency_due_date.replace(year=frequency_due_date.year + 1)
        
        return frequency_due_date
 

    async def add_user_recurring_transaction(
        self, 
        user_id: UUID,
        transaction_name: str, 
        transaction_amount: Decimal, 
        currency_code: str,
        category_id: UUID,
        frequency: str,
        next_due_date: datetime | None
    ):
        category_exists = await self.repo.check_category_exists(category_id)
        if not category_exists:
            raise InvalidCategoryException()

        transaction_id = uuid4()
        transaction = await self.repo.add_user_recurring_transaction(
            transaction_id, 
            transaction_name, 
            transaction_amount, 
            currency_code,
            user_id,
            category_id,
            frequency,
            next_due_date
        )
        return transaction