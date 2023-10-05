from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from .routers import authors, sites, auth

description= """
API to read, add, edit, and delete blog sites, posts, and authors.

See [Our GitHub Repository](https://github.com/blogindex/blogindex.xyz) for more information.
"""  # noqa: E501

app = FastAPI(
    title="The Blog Index",
    description=description,
    summary="The Blog Index API - Find, Add, Update Blog Listsings",
    version="0.0.1-pre-alpha",
    contact={
        "name": "BeardedTek (William Kenny)",
        "url": "https://theblogindex.org",
        "email": "api@theblogindex.org"
    },
    license_info={
        "name": "GNU Affero General Public License",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html"
    },

)
root_path = app.root_path

app.add_middleware(SessionMiddleware, secret_key="!secret")

# Include routes
app.include_router(authors.router)
app.include_router(sites.router)
app.include_router(auth.router)