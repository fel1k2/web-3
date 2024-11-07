from fastapi import FastAPI, Depends, Form, File, UploadFile
from handlers import users_handler, books_handler, reviews_handler
from schemas.user import UserCreate, UserUpdate, UserAuthorize
from schemas.review import ReviewCreate, ReviewUpdate
from database import metadata, engine, database
from models import users
from models.Users import UserRole
from utils.token import validate_token_and_role

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users/", tags=["Users"])
async def read_users():
    return await users_handler.read_users(database)

@app.post("/users/", tags=["Users"])
async def create_user(user: UserCreate, role: UserRole):
    return await users_handler.create_user(user, database, role)
###
@app.delete("/users/", tags=["Users"])
async def delete_user(email: str):
    return await users_handler.delete_user(email, database)
###
@app.put("/users/", tags=["Users"])
async def update_user(user: UserUpdate):
    return await users_handler.update_user(user, database)

@app.put("/users/authorize/", tags=["Users"])
async def authorize_user(user: UserAuthorize):
    return await users_handler.authorize_user(user, database)

#@app.get("/with-credentials")
#async def check_credentials(user = Depends(validate_token_and_role([ "approved_user", "admin"]))):
#    return {"msg": "Welcome allowed user"}

#@app.get("/without-credentials")
#async def check_credentials():
#     return {"msg": "Welcome all"}

@app.post("/books/create-book", tags=["Books Managment"])
async def create_book(title = Form(..., examples=['Title']),
                    author = Form(..., examples=['Author']),
                    description = Form(..., examples=['Description']),
                    file: UploadFile = File(...),
                    user = Depends(validate_token_and_role(["admin"]))
                    ):
    return await books_handler.upload_book(database, title, author, description, file)

@app.get("/books/get-book/{book_id}", tags=["Books Managment"])
async def get_book(book_id: int,
                   user = Depends(validate_token_and_role(["user", "admin", "aproved_user"]))
                   ):
    return await books_handler.get_book(book_id, database)

@app.get("/books/download-book/{book_id}", tags=["Books Managment"])
async def download_book(book_id: int,
                        user = Depends(validate_token_and_role(["user", "admin", "aproved_user"]))
                   ):
    return await books_handler.download_book(book_id, database)

@app.delete("/books/delete-book/{book_id}", tags=["Books Managment"])
async def delete_book(book_id: int,
                      user = Depends(validate_token_and_role(["admin"]))
                   ):
    return await books_handler.delete_book(book_id, database)

@app.put("/books/update-book/{book_id}", tags=["Books Managment"])
async def update_book(book_id: int,
                      title = Form(None, examples=['newTitle']),
                      author = Form(None, examples=['newAuthor']),
                      description = Form(None, examples=['newDescription']),
                      user = Depends(validate_token_and_role(["admin"])) 
                   ):
    return await books_handler.update_book(book_id, database, title, author, description)

@app.post("/reviews/", tags=["Reviews Managment"], summary="Endpoint for review creation")
async def create_review(review: ReviewCreate, user = Depends(validate_token_and_role(["user", "approved_user","admin"]))):
    return await reviews_handler.create_review(review, user, database)

@app.get("/reviews/{book_id}", tags=["Reviews Managment"], description="Description")
async def get_reviews_for_book(book_id: int, user = Depends(validate_token_and_role(["user", "approved_user","admin"]))):
    return await reviews_handler.get_reviews_for_book(book_id, database)

@app.put("/reviews/{review_id}", tags=["Reviews Managment"], response_description="Response contains message about results")
async def update_review(review_id: int, updated_review: ReviewUpdate, user = Depends(validate_token_and_role(["user", "approved_user","admin"]))):
    return await reviews_handler.update_review(review_id, updated_review, user, database)

@app.delete("/reviews/{review_id}", tags=["Reviews Managment"])
async def delete_review(review_id: int, user = Depends(validate_token_and_role(["admin"]))):
    return await reviews_handler.delete_review(review_id, user, database)
