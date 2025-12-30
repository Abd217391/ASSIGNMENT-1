from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

 
def create_access_token(data: dict):
    try:
        #this first is use to check if secret key is missing or not
        if not SECRET_KEY or not isinstance(SECRET_KEY, str):
            raise ValueError("SECRET_KEY is missing or invalid")
            #exception will be created

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return encoded_jwt

    except JWTError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"JWT error: {str(error)}"
        )

    
