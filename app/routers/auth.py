from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserSignup,
    ChangePassword,
    UpdateProfile,
    UserOut
)
from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token, verify_access_token

router = APIRouter(prefix="/auth", tags=["FORM"])

# Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(token)
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user



@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

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
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    return {"access_token": token, "token_type": "bearer"}



@router.put("/change-password")
def change_password(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=401, detail="Invalid old password")

    if verify_password(data.new_password, current_user.password):
        raise HTTPException(
            status_code=400,
            detail="New password must be different"
        )

    current_user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}


@router.put("/profile/update")
def update_profile(
    data: UpdateProfile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not data.firstname and not data.lastname:
        raise HTTPException(
            status_code=400,
            detail="At least firstname or lastname is required"
        )

    if data.firstname:
        current_user.firstname = data.firstname

    if data.lastname:
        current_user.lastname = data.lastname

    db.commit()
    db.refresh(current_user)

    return {
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "createdat": current_user.createdat
    }


# ---------------- ADMIN: LIST USERS (PROTECTED) ----------------
@router.get("/admin/users")
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).all()
    return users
