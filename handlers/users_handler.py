from fastapi import HTTPException
from sqlalchemy import select, insert
from utils.password import hash_password, verify_password
from models import users
from databases import Database
from schemas.user import UserCreate, UserUpdate, UserAuthorize
from models.Users import UserRole
from utils.token import create_access_token

async def create_user(user: UserCreate, db: Database, role: UserRole):
    query = users.select().where(users.c.email == user.email)
    existing_user = await db.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    pwd_hash = hashed_password.decode('utf-8')
    
    query = insert(users).values(name=user.name, 
                                email=user.email, 
                                hashed_password=pwd_hash,
                                role=role)
    await db.execute(query)
    return {"name": user.name, "email": user.email, "role": role}

async def read_users(db: Database):
    query = users.select()
    return await db.fetch_all(query)

async def delete_user(email: str, db: Database):
    query = users.select().where(users.c.email==email)
    result = await db.fetch_one(query)
    if (result!=None):
        query = users.delete().where(users.c.email==email)
        await db.execute(query)
        return {"name": result.name, "email": result.email}
    raise HTTPException(status_code=400, detail="No user found")

async def update_user(user: UserUpdate, db: Database):
    query = users.select().where(users.c.email==user.oldEmail)
    result = await db.fetch_one(query)
    if (result!=None):
        if (verify_password(user.oldPassword,result.hashed_password)):
            hashed_password = hash_password(user.newPassword)
            pwd_hash = hashed_password.decode('utf-8')
            query = users.update().where(users.c.email==user.oldEmail).values(name=user.newName,
                                                                           email=user.newEmail,
                                                                           hashed_password=pwd_hash,
                                                                           role=user.newRole)
            await db.execute(query)
            return {"old info":{"name": result.name, "email": result.email},
                    "new info":{"name": user.newName, "email": user.newEmail, "role": user.newRole}}
        raise HTTPException(status_code=401, detail="User or password not correct")
    raise HTTPException(status_code=400, detail="No user found")

async def authorize_user(user: UserAuthorize, db: Database):
    query = users.select().where(users.c.email == user.email)
    existing_user = await db.fetch_one(query)
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if (verify_password(user.password,existing_user.hashed_password)):
        token = create_access_token(data={"sub": existing_user.name,"role":existing_user.role.value})
        return {"token":token}
        
    raise HTTPException(status_code=401, detail="User or password not correct")