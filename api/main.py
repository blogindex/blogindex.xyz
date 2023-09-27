from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import authors, sites, auth, logs


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(authors.router)
app.include_router(sites.router)
app.include_router(auth.router)
app.include_router(logs.router)