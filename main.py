from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings.config import env
from app.routers import router


def get_application() -> FastAPI:
    app = FastAPI(title=env.PROJECT_NAME)
    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=env.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST",],
        allow_headers=["*"],
    )
    return app


app = get_application()
