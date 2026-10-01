from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.auth_test import router as auth_test_router
from backend.app.api.routes.events import router as events_router
from backend.app.api.routes.products import router as products_router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "RecoFlow event-driven personalized "
        "recommendation platform"
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    tags=["System"],
)
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
    }


app.include_router(auth_router)
app.include_router(auth_test_router)
app.include_router(products_router)
app.include_router(events_router)