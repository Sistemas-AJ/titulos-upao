from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.database.session import create_db_and_tables
from backend.routers.health import router as health_router
from backend.routers.reference_titles import router as reference_titles_router
from backend.routers.title_sessions import router as title_sessions_router
from backend.routers.users import router as users_router


settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(health_router)
app.include_router(reference_titles_router)
app.include_router(users_router)
app.include_router(title_sessions_router)
