from fastapi import FastAPI

from .base import AppException, NotFoundException, BadRequestException
from .handlers import (
    app_exception_handler,
    not_found_exception_handler,
    bad_request_exception_handler,
    unhandled_exception_handler,
)

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
