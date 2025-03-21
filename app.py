import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from handlers.custom_exceptions import APIKeyException
from handlers.exception_handler import (
    validation_exception_handler, general_exception_handler, api_key_exception_handler)

from routes import send_message

load_dotenv()

DEBUG = bool(int(os.getenv("DEBUG", 1)))

app = FastAPI(
    title="Telegram Bot Backend",
    description="This is Telegram Bot Backend API Documentation",
    version="2.0.0",
    docs_url="/docs" if DEBUG else None,  # Disable Swagger UI
    redoc_url="/redoc" if DEBUG else None,  # Disable ReDoc
    openapi_url="/openapi.json" if DEBUG else None,  # Disable OpenAPI
)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(APIKeyException, api_key_exception_handler)


# Include routes
app.include_router(send_message.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": 200, "message": "Server is up and running!", "data": "Made with ❤️"}
