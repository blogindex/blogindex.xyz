from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .routers import authors, sites, auth, logs

app = FastAPI(
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key="!secret")

# Include routes
app.include_router(authors.router)
app.include_router(sites.router)
app.include_router(auth.router)
app.include_router(logs.router)