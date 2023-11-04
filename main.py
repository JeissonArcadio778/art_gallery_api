from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Art gallery with FastAPI"
app.version = "0.0.1"


class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=20)
    user_type: str
    age: int

    # default
    class Config:
        json_schema_extra = {
            "example": {"id": 1, "name": "Eulaloquita", "user_type": "user", "age": 21},
        }


users = [
    {"id": 1, "name": "Eulaloquita", "user_type": "user", "age": 21},
    {"id": 2, "name": "Yeloquito", "user_type": "admin", "age": 22},
]


# test
@app.get("/hello/{name}", tags=["testing"])
async def read_root(name: str):
    return {"Hello": name}


# users:
@app.get("/users", tags=["Users"], response_model=List)
async def get_users() -> List[User]:
    return JSONResponse(content=[], status_code=200)


@app.get("/users/{id}", tags=["Users"], response_model=User)
async def get_user_by_id(id: int = Path(ge=1, le=4)):
    return [user for user in users if id == user["id"]]


# using query params and validate it
@app.get("/users/", tags=["Users"])
async def get_users_by_type(type: str, age: int = Query(ge=1, le=4)):
    return [user for user in users if type == user["user_type"] and age == user["age"]]


# using schemas from pydantic
@app.post("/users", tags=["Users"])
async def create_user(user: User):
    users.append(user)
    return JSONResponse(content=users, status_code=202)


@app.put("/users/{id}", tags=["Users"])
async def create_user(id: int, new_user: User):
    for user in users:
        if user["id"] == id:
            user["age"] = new_user.age
            return JSONResponse(content=[], status_code=200)
    return JSONResponse(content=[], status_code=404)
