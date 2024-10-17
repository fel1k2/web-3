from jose import jwt, JWTError
from typing import Optional, List
from datetime import datetime,timedelta
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

SECRET_KEY = "web-tech-2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    load_dotenv()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

oauth2_scheme = HTTPBearer()

def validate_token_and_role(required_roles: List[str]):
    def token_validator(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        token = token.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            name = payload.get("sub")
            role = payload.get("role") 
            if name is None or role is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User or UserRole is not identified"
                )
            if role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Your role is not valid fot this request"
                )
            return {"name": name, "role": role}
        except JWTError:
            raise HTTPException(
            status_code=401,
            detail = "Token is not valid"
        )
    return token_validator