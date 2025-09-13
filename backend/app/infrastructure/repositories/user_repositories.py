from decimal import Decimal
from uuid import UUID
import asyncpg


class UserRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def update_user(self, id: UUID, name: str, email: str, currency_code: str | None, goal: Decimal | None, savings: Decimal | None, balance: Decimal | None):
        row = await self.conn.fetchrow("""
            UPDATE users
            SET name = $2,
                email = $3,
                currency_code = $4,
                goal = $5,
                savings = $6,
                balance = $7
            WHERE id = $1 
            RETURNING name, email, currency_code, goal, savings, balance
        """, id, name, email, currency_code, goal, savings, balance)

        return dict(row) if row else None
    
    async def get_user_details(self, user_id: UUID):
        row = await self.conn.fetchrow("""
            SELECT name, email, currency_code, goal, savings, balance
            FROM users
            WHERE users.id = $1
        """, user_id)

        return dict(row)
    
    async def update_user_balance(self, category_type: str, transaction_amount: Decimal, user_id: UUID):
        balance_change = transaction_amount if category_type == 'income' else -transaction_amount
        return await self.conn.execute("""
            UPDATE users 
            SET balance = balance + $1
            WHERE id = $2
            RETURNING id
        """, balance_change, user_id)