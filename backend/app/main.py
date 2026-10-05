from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.auth_test import router as auth_test_router
from backend.app.api.routes.products import router as products_router
from backend.app.api.routes.events import router as events_router
from backend.app.api.routes.behaviors import router as behaviors_router
from backend.app.api.routes.recommendations import router as recommendations_router
from backend.app.api.routes.evaluation import router as evaluation_router
from backend.app.api.routes.orders import router as orders_router
from backend.app.api.routes.cart import router as cart_router
from backend.app.api.routes.wishlist import router as wishlist_router


app = FastAPI(
    title="RecoFlow",
    description="Event-driven personalized recommendation and ranking platform",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok",
        "service": "recoflow",
    }


app.include_router(auth_router)
app.include_router(auth_test_router)
app.include_router(products_router)
app.include_router(events_router)
app.include_router(behaviors_router)
app.include_router(recommendations_router)
app.include_router(evaluation_router)
app.include_router(orders_router)
app.include_router(cart_router)
app.include_router(wishlist_router)