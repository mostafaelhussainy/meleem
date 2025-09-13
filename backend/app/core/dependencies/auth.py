from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from datetime import datetime
from uuid import UUID

from ..config import settings
from ..exceptions.exceptions import (
    AuthorizationTokenMissingException,
    InvalidAuthorizationTokenFormatException,
    InvalidAuthorizationTokenException,
)

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> UUID:
    if not credentials:
        raise AuthorizationTokenMissingException("Authorization token is missing")

    if credentials.scheme.lower() != "bearer":
        raise InvalidAuthorizationTokenFormatException("Invalid token format")

    token = credentials.credentials
    
    try:
        # Verify and decode the JWT token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise InvalidAuthorizationTokenException("Token has expired")
            
        # Get user_id from token
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidAuthorizationTokenException("Invalid token payload")
            
        # Store user context in request state
        request.state.user_id = user_id
        return UUID(user_id)
        
    except jwt.InvalidTokenError:
        raise InvalidAuthorizationTokenException("Invalid token")
