from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable API Keys
api_keys = [
    "Super Secret API Key"
]

# API Key Header Definition
api_key_header = APIKeyHeader(name="X-API-Key")

# API Key Handler
def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or missing API Key"
    )




# Database definition to be used in path functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
        "/users/create",
        response_model=schemas.User,
        )
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    print(f"-------------------\n {user.email}\n ---------------------")
    try:
        user_by_email = crud.get_user_by_email(db, email=user.email)
        if user_by_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        print(f"-------------------\n {user}\n ---------------------")
    except TypeError:
        pass
    return crud.create_user(db=db, user=user)

@app.get("/users/get", response_model=list[schemas.User])
def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/get/by-email/{email}", response_model = list[schemas.User])
def get_users_by_email(
        email: str,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    users = crud.get_user_by_email(email, db)
    return users

@app.get("/users/get/by-id/{user_id}", response_model = list[schemas.User])
def get_users_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    users = crud.get_user_by_id(db, id)
    return users


@app.post("/key/create", response_model = list[schemas.KeyDisplay])
def create_key(
        key: schemas.KeyCreate,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    key = crud.create_key(key,db)
    return key

@app.get("/key/get/by-user_id/{user_id}", response_model = list[schemas.Key])
def get_user_keys(
        user_id: int,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    keys = crud.get_user_keys(user_id, db)