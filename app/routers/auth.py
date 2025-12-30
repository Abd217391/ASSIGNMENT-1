from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserSignup, UserLogin, ChangePassword
from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["FORM"])


@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    #this will help us gte the email for the login
    db_user = db.query(User).filter(User.email == user.email).first()

   
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    
    try:
        token = create_access_token({"user_id": db_user.id})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token generation failed"
        )

  
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }



@router.put("/change-password")
def change_password(data: ChangePassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

   
    if not user or not verify_password(data.old_password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

   
    if verify_password(data.new_password, user.password):
        raise HTTPException(
            status_code=400,
            detail="New password must be different from the old password"
        )

    
    user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}

