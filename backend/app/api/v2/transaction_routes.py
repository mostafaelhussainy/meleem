from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, status

from ...infrastructure.db.database import get_db
from ...core.filters_utils import DateFilterEnum
from ...core.dependencies.auth import get_current_user
from ...schemas.transaction_schema import AddUserRecurringTransactionRequest, AddUserTransactionRequest, CategoryType
from ...services.transactions_services__sqlalchemy import SQLAlchemyTransactionServices

router = APIRouter()

@router.get('/')
async def get_all_user_transactions( 
    db: AsyncSession = Depends(get_db), 
    user_id: UUID = Depends(get_current_user),
    category_type: CategoryType | None = Query(None, description="Whether this transactions has a specific type or not"),
    transaction_created_at: DateFilterEnum | None = Query(None, description="When these transactions created at")
):
    transactions_services = SQLAlchemyTransactionServices(db)
    transactions = await transactions_services.get_all_user_transactions(user_id, category_type, transaction_created_at)
    return transactions

@router.post('/add-transaction', status_code=status.HTTP_201_CREATED)
async def add_user_transaction(
    request: AddUserTransactionRequest,
    db: AsyncSession = Depends(get_db), 
    user_id: UUID = Depends(get_current_user)
):
    transactions_services = SQLAlchemyTransactionServices(db)
    transaction = await transactions_services.add_user_transaction(
        request.transaction_name, 
        request.transaction_amount, 
        request.currency_code,
        user_id,
        request.category_id
    )
    return transaction

@router.post(
    '/add-recurring-transaction', 
    status_code=status.HTTP_201_CREATED,
)
async def add_user_recurring_transaction(
    request: AddUserRecurringTransactionRequest,
    db: AsyncSession = Depends(get_db), 
    user_id: UUID = Depends(get_current_user)
):
    transactions_services = SQLAlchemyTransactionServices(db)
    transaction = await transactions_services.add_user_recurring_transaction(
        user_id,
        request.transaction_name, 
        request.transaction_amount, 
        request.currency_code,
        request.category_id,
        request.frequency,
        request.next_due_date
    )
    return transaction
