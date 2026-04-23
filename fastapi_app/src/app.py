from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

#from src.api.base import router as base_router
from src.api.locations import router as locations_router
from src.api.users import router as users_router
from src.api.categories import router as categories_router
from src.api.posts import router as posts_router
from src.api.comments import router as comments_router
from src.api.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(locations_router, prefix="/blog")
    app.include_router(users_router, prefix="/blog")
    app.include_router(categories_router, prefix="/blog")
    app.include_router(posts_router, prefix="/blog")
    app.include_router(comments_router, prefix="/blog")
    app.include_router(auth_router, prefix="/blog")

    print("\n=== ЗАРЕГИСТРИРОВАННЫЕ МАРШРУТЫ ===")
    for route in app.routes:
        if hasattr(route, "path"):
            print(f"{route.methods if hasattr(route, 'methods') else 'ANY'} {route.path}")
    print("================================\n")

    return app