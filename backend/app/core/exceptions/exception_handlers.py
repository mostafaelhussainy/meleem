from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .exceptions import (
    AuthorizationTokenMissingException, 
    InvalidAuthorizationTokenFormatException, 
    InvalidPasswordException, 
    UserAlreadyExistException, 
    UserDoesNotExistException, 
    UserEmailDoesNotExistException,
    InvalidCategoryException
)


def register_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "detail": exc.errors()[0]["msg"] if exc.errors() else "Validation error"
            }
        )

    @app.exception_handler(InvalidPasswordException)
    async def invalid_password_handler(request: Request, exc: InvalidPasswordException):
        return JSONResponse(
            status_code=422, 
            content={"detail":  str(exc)}
        )

    @app.exception_handler(UserAlreadyExistException)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExistException):
        return JSONResponse(
            status_code=400, 
            content={"detail":  str(exc)}
        )

    @app.exception_handler(UserEmailDoesNotExistException)
    @app.exception_handler(UserDoesNotExistException)
    async def user_does_not_exist_handler(request: Request, exc: UserEmailDoesNotExistException | UserDoesNotExistException):
        return JSONResponse(
            status_code=400, 
             content={"detail":  str(exc)}
        )
    
    @app.exception_handler(AuthorizationTokenMissingException)
    async def authorization_token_missing_handler(request: Request, exc: AuthorizationTokenMissingException):
         return JSONResponse(
            status_code=401,
            content={"detail":  str(exc)}
        )

    @app.exception_handler(InvalidAuthorizationTokenFormatException)
    async def invalid_authorization_token_format_handler(request: Request, exc: InvalidAuthorizationTokenFormatException):
         return JSONResponse(
            status_code=401,
            content={"detail":  str(exc)}
        )

    @app.exception_handler(InvalidCategoryException)
    async def invalid_category_handler(request: Request, exc: InvalidCategoryException):
         return JSONResponse(
            status_code=400,
            content={"detail": "Category does not exist"}
        )

