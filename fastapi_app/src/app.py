from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.categories import router as categories_router
from .api.locations import router as locations_router
from .api.comments import router as comments_router
from .api.posts import router as posts_router
from .api.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключение всех роутеров
    app.include_router(categories_router, prefix="/categories", tags=["Categories"])
    app.include_router(locations_router, prefix="/locations", tags=["Locations"])
    app.include_router(comments_router, prefix="/comments", tags=["Comments"])
    app.include_router(posts_router, prefix="/posts", tags=["Posts"])
    app.include_router(users_router, prefix="/users", tags=["Users"])

    return app