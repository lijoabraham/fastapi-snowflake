from fastapi import FastAPI, Body, Depends

from app.model import UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from snowflake_connector import snowpark_connect
from snowflake.snowpark.functions import col

users = []
def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

app = FastAPI()

@app.get("/user/{uid}", dependencies=[Depends(JWTBearer())], tags=["posts"])
def main(uid: int):
    session = snowpark_connect()
    df_table = session.table("users")
    df = df_table.filter(col("user_id") == uid)
    user = df.to_pandas()
    # print(user.to_dict())
    return {"result" : user.to_dict(), "status_code":"200"} 

@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
