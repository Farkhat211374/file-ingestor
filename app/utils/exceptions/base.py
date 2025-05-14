class AppException(Exception):
    """Base class for custom application exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotFoundException(AppException):
    """Raised when a requested resource is not found."""
    pass

class BadRequestException(AppException):
    """Raised when the client sends invalid data."""
    pass
