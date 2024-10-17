from fastapi import FastAPI, Depends
from handlers import users_handler, books_handler
from schemas.user import UserCreate,UserUpdate,UserAuthorize
from database import metadata, engine, database
from models import users
from models.Users import UserRole
from fastapi import Form, File, UploadFile
from utils.token import validate_token_and_role

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users/")
async def read_users():
    return await users_handler.read_users(database)

@app.post("/users/")
async def create_user(user: UserCreate, role: UserRole):
    return await users_handler.create_user(user, database, role)

@app.delete("/users/")
async def delete_user(email: str):
    return await users_handler.delete_user(email, database)

@app.put("/users/")
async def update_user(user: UserUpdate):
    return await users_handler.update_user(user, database)

@app.put("/users/authorize/")
async def authorize_user(user: UserAuthorize):
    return await users_handler.authorize_user(user, database)

@app.post("/books/create-book")
async def create_book(title = Form(..., examples=['Title']),
                    author = Form(..., examples=['Author']),
                    description = Form(..., examples=['Description']),
                    file: UploadFile = File(...),
                    ):
    return await books_handler.upload_book(database, title, author, description, file)

@app.get("/books/get-book/{book_id}")
async def get_book(book_id: int,
                   ):
    return await books_handler.get_book(book_id, database)

@app.get("/books/download-book/{book_id}")
async def download_book(book_id: int,
                   ):
    return await books_handler.download_book(book_id, database)

@app.delete("/books/delete-book/{book_id}")
async def delete_book(book_id: int,
                   ):
    return await books_handler.delete_book(book_id, database)

@app.put("/books/update-book/{book_id}")
async def update_book(book_id: int,
                      title = Form(None, examples=['newTitle']),
                      author = Form(None, examples=['newAuthor']),
                      description = Form(None, examples=['newDescription']),
                   ):
    return await books_handler.update_book(book_id, database, title, author, description)
