class InvalidPasswordException(Exception):
    """Raised when the password does not meet security requirements"""
    pass

class UserAlreadyExistException(Exception):
    """Raised when the user trying to register with existing email"""
    pass

class UserEmailDoesNotExistException(Exception):
    """Raised when the user trying to login with none existing email"""
    pass

class UserDoesNotExistException(Exception):
    """Raised when the user doesn't exist"""
    pass

class AuthorizationTokenMissingException(Exception):
    """Raised when the request is missing authorization token"""
    pass

class InvalidAuthorizationTokenFormatException(Exception):
    """Raised when the request has invalid authorization token format"""
    pass

class InvalidAuthorizationTokenException(Exception):
    """Raised when the request has invalid authorization token"""
    pass

class InvalidCategoryException(Exception):
    """Raised when the category does not exist"""
    pass