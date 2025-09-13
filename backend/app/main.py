from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager

from .core.dependencies.auth import get_current_user
from .infrastructure.db.connection import connect_to_db, disconnect_from_db
from .core.exceptions.exception_handlers import register_exception_handlers
from .api.v1 import auth_routes, user_routes, transactions_routes, listing_routes
from .api.v2 import auth_routes as auth_routes_v2, listing_routes as listing_routes_v2, user_routes as user_routes_v2, transaction_routes as transactions_routes_v2
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    yield
    await disconnect_from_db()


app = FastAPI(
    lifespan=lifespan,
    title="My API",
    description="API with JWT authentication",
    version="1.0.0",
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": True},
)

register_exception_handlers(app)


app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(listing_routes.router, prefix="/api/v1/listing", tags=["listing"])
app.include_router(
    user_routes.router,
    prefix="/api/v1/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)],  # ✅ protect all user routes with full JWT validation
)
app.include_router(
    transactions_routes.router,
    prefix="/api/v1/transactions",
    tags=["transactions"],
    dependencies=[Depends(get_current_user)],  
)


app.include_router(auth_routes_v2.router, prefix="/api/v2/auth", tags=["auth-v2"])
app.include_router(listing_routes_v2.router, prefix="/api/v2/listing", tags=["listing-v2"])
app.include_router(user_routes_v2.router, prefix="/api/v2/user", tags=["user-v2"])
app.include_router(transactions_routes_v2.router, prefix="/api/v2/transactions", tags=["transactions-v2"])
