import asyncpg
from uuid import UUID
from decimal import Decimal


class AuthRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def get_user_by_email(self, email: str):
        row = await self.conn.fetchrow("SELECT * FROM users WHERE email=$1", email)
        return dict(row) if row else None
        
    async def create_user(self, id: UUID, name: str, email: str, hashed_password: str, currency_code: str | None, goal: Decimal | None, savings: Decimal | None, balance: Decimal | None):
        row = await self.conn.fetchrow("""
            INSERT INTO users(id, name, email, hashed_password, currency_code, goal, savings, balance)
            VALUES($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """, id, name, email, hashed_password, currency_code, goal, savings, balance)
        return row["id"] if row else None

    async def get_user_by_id(self, user_id):
        row = await self.conn.fetchrow("""
            SELECT * FROM users
            WHERE id=$1
        """, user_id)
        return dict(row) if row else None