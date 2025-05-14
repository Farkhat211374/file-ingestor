from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.utils.errors.base import (
    AppException,
    NotFoundException,
    BadRequestException,
)

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"error": exc.message}
    )

async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"error": exc.message}
    )

async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"error": exc.message}
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal Server Error"}
    )
