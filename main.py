from fastapi import FastAPI, Path, Query, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt_manager import create_token, validate_token
from config.database import Session, engine, Base
from models.work_of_art import WorkOfArt

users = [
    {"id": 1, "name": "Eulaloquita", "user_type": "user", "age": 21, "email": "sarita@gmail.com", "password": "123"},
    {"id": 2, "name": "Yeloquito", "user_type": "admin", "age": 22,  "email": "yeye@gmail.com", "password": "12"},
]


app = FastAPI()
app.title = "Art gallery with FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        for user in users:
            if data["email"] == user["email"]: 
                if data["password"] != user["password"]:
                    raise HTTPException(status_code=403, detail="The credentials are incorrect.")
        
        

class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=20)
    user_type: str
    age: int
    email: str
    password: str

    # default
    class Config:
        json_schema_extra = {
            "example": {"id": 1, "name": "Eulaloquita", "user_type": "user", "age": 21, "email": "sarita@gmail.com", "password": "123"},
        }

# test
@app.get("/hello/{name}", tags=["testing"])
async def read_root(name: str):
    return {"Hello": name}


# users:
@app.get("/users", tags=["Users"], response_model=List[User], status_code=200, dependencies=[Depends(JWTBearer())])
async def get_users() -> List[User]:
    return JSONResponse(content=users, status_code=200)


@app.get("/users/{id}", tags=["Users"], response_model=User)
async def get_user_by_id(id: int = Path(ge=1, le=4)):
    for user in users:
        if id == user["id"]:
            return JSONResponse(content=user, status_code=200)
    return JSONResponse(content=[], status_code=404)


# using query params and validate it
@app.get("/users/", tags=["Users"], response_model=List[User])
async def get_users_by_type(type: str, age: int = Query(ge=1, le=4)):
    return [user for user in users if type == user["user_type"] and age == user["age"]]


# login
@app.post("/login", tags=["auth"])
async def login(email:str, password: str):
    for user in users: 
        if email == user["email"] and password == user["password"]:
            data = {
                "email": email,
                "password": password
            }
            token:str = create_token(data)
            return JSONResponse(content=token, status_code=200)
    return JSONResponse(content=[], status_code=404)


# using schemas from pydantic
@app.post("/users", tags=["Users"], response_model=dict)
async def create_user(user: User) -> dict:
    users.append(user)
    return JSONResponse(content=users, status_code=201)


@app.put("/users/{id}", tags=["Users"], response_model=List[User])
async def create_user(id: int, new_user: User) -> List[User]:
    for user in users:
        if user["id"] == id:
            user["age"] = new_user.age
            return JSONResponse(content=[], status_code=200)
    return JSONResponse(content=[], status_code=404)

