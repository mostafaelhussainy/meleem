from uuid import UUID
from asyncpg import Connection
from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies.auth import get_current_user
from app.core.filters_utils import DateFilterEnum
from app.infrastructure.db.connection import get_db_connection
from app.schemas.transaction_schema import AddUserRecurringTransactionRequest, AddUserTransactionRequest, CategoryType

from ...services.transactions_services import TransactionServices

router = APIRouter()

@router.get('/')
async def get_all_user_transactions( 
    conn: Connection = Depends(get_db_connection), 
    user_id: UUID = Depends(get_current_user),
    category_type: CategoryType | None = Query(None, description="Whether this transactions has a specific type or not"),
    transaction_created_at: DateFilterEnum | None = Query(None, description="When these transactions created at")
):
    transactions_services = TransactionServices(conn)
    transactions = await transactions_services.get_all_user_transactions(user_id, category_type, transaction_created_at)
    return transactions

@router.post('/add-transaction', status_code=status.HTTP_201_CREATED)
async def add_user_transaction(
    request: AddUserTransactionRequest,
    conn: Connection = Depends(get_db_connection), 
    user_id: UUID = Depends(get_current_user)
):
    transactions_services = TransactionServices(conn)
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
    summary="Create a recurring transaction",
    description="""
    Create a recurring transaction that will automatically create transactions based on the specified frequency.
    
    - **frequency**: How often the transaction repeats (daily, weekly, monthly, yearly)
    - **next_due_date**: When the first transaction should occur (optional, defaults to now)
    
    The system will create actual transactions based on the schedule when the user logs in.
    """,
    response_description="The created recurring transaction details"
)
async def add_user_recurring_transaction(
    request: AddUserRecurringTransactionRequest,
    conn: Connection = Depends(get_db_connection), 
    user_id: UUID = Depends(get_current_user)
):
    transactions_services = TransactionServices(conn)
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
