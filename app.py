import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from config.rate_limiter import limiter
from handlers.custom_exceptions import APIKeyException
from handlers.exception_handler import (
    validation_exception_handler, general_exception_handler, api_key_exception_handler, ratelimit_exceeded_handler)

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

app.add_middleware(SlowAPIMiddleware)

# Initialize the rate limiter
app.state.limiter = limiter

# Register the custom exception handlers
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(APIKeyException, api_key_exception_handler)
app.add_exception_handler(RateLimitExceeded, ratelimit_exceeded_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Include routes
app.include_router(send_message.router, prefix="/api/v1")


@app.get("/")
async def root(request: Request):
    return {"status": 200, "message": "Server is up and running!", "data": "Made with ❤️"}
