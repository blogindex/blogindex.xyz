from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from .routers import authors, sites, auth

app = FastAPI(
)
root_path = app.root_path

app.add_middleware(SessionMiddleware, secret_key="!secret")

# Include routes
app.include_router(authors.router)
app.include_router(sites.router)
app.include_router(auth.router)