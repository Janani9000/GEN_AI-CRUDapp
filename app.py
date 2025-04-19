from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
import mysql.connector
from mysql.connector import IntegrityError

app = FastAPI(
    title="User CRUD API", description="API for basic user operations", version="1.0.0"
)

# MySQL connection
mydb = mysql.connector.connect(
    host="localhost", user="root", password="mysql123", database="crud_new"
)
mycursor = mydb.cursor(dictionary=True)


# Pydantic model for request body
class User(BaseModel):
    name: str = Field(..., min_length=1, description="Name cannot be empty")
    email: EmailStr


@app.get("/")
def home():
    return {"message": "Welcome to the CRUD API"}


# Create
@app.post("/users")
def create_user(user: User):
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    val = (user.name, user.email)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        return {"message": "User created successfully", "user_id": mycursor.lastrowid}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")


# Read All
@app.get("/users")
def get_all_users():
    mycursor.execute("SELECT * FROM users")
    result = mycursor.fetchall()
    return result


# Read One
@app.get("/users/{user_id}")
def get_user(user_id: int):
    mycursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = mycursor.fetchone()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


# Update
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    sql = "UPDATE users SET name = %s, email = %s WHERE id = %s"
    val = (user.name, user.email, user_id)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount:
        return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")


# Delete
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    sql = "DELETE FROM users WHERE id = %s"
    val = (user_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
