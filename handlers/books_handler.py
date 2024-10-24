from fastapi import Form, File, UploadFile, Depends, HTTPException
import os
from dotenv import load_dotenv
from databases import Database
from models import books
from sqlalchemy import select, insert
from starlette.responses import FileResponse
from utils.token import validate_token_and_role

load_dotenv()
upload_folder = os.getenv("UPLOAD_FOLDER")
os.makedirs(upload_folder, exist_ok=True)

async def upload_book(
                    db: Database,
                    title = Form(..., example='Title'),
                      author = Form(..., example='Author'),
                      description = Form(..., example='Description'),
                    file: UploadFile = File(...),
                ):
    file_path = os.path.join(upload_folder, file.filename)
    with open(file_path, "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)
    
    query = insert(books).values(title=title, 
                                author=author, 
                                description=description,
                                link=file_path)
    await db.execute(query)
    
    return {
        "title": title,
        "author": author,
        "description": description,
        "link": file_path,
        "BOOK CREATED" : "SUCCESSFULLY"
    }
    
async def get_book(book_id: int,
                   db: Database,
                   user = Depends(validate_token_and_role(["user", "admin", "aproved_user"])) 
                   ):
    query = books.select().where(books.c.id == book_id)
    book = await db.fetch_one(query=query)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    download_link = f'/books/download/{book_id}'
    
    return {
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "link": download_link
    }
    
async def download_book(book_id: int,
                        db: Database,
                        user = Depends(validate_token_and_role(["user", "admin", "aproved_user"])) 
                        ):
    query = books.select().where(books.c.id == book_id)
    book = await db.fetch_one(query=query)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    file_path = book.link
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(path=file_path, filename=os.path.basename(file_path))

async def delete_book(book_id: int,
                      db: Database,
                      user = Depends(validate_token_and_role(["admin"]))
                      ):
    query = books.select().where(books.c.id == book_id)
    book = await db.fetch_one(query=query)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    file_path = book.link

    if os.path.exists(file_path):
        os.remove(file_path)

    query = books.delete().where(books.c.id == book_id)
    await db.execute(query)

    return {"message": "Book deleted successfully",
            "title": book.title,
            "author": book.author,
            "description": book.description}

async def update_book(book_id: int,
                      db: Database,
                      title = Form(...),
                      author = Form(...),
                      description = Form(...),
                      user = Depends(validate_token_and_role(["admin"]))
                      ):
    query = books.select().where(books.c.id == book_id)
    existing_book = await db.fetch_one(query=query)

    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    query = books.update().where(books.c.id == book_id).values(
        title=title if title else existing_book.title,
        author=author if author else existing_book.author,
        description=description if description else existing_book.description
    )
    await db.execute(query)

    return {"message": "Book updated successfully"}