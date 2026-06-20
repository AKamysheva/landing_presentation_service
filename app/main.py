from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers.api import router as api_router
from app.exceptions import EmailSendError, RateLimitExceededError
from app.logging import logger

app = FastAPI()


app.include_router(api_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(
        f"{request.client.host} {request.method} {request.url.path} -> {response.status_code}"
    )

    return response


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(f"Unhandled error at {request.url.path}: {exc}")
    if isinstance(exc, RateLimitExceededError):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"},
        )
    elif isinstance(exc, EmailSendError):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
