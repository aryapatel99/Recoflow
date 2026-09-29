from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.auth_test import router as auth_test_router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "RecoFlow event-driven personalized "
        "recommendation and ranking platform."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    tags=["System"],
)
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }


app.include_router(auth_router)
app.include_router(auth_test_router)