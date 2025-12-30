from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserSignup, ChangePassword
from app.utils.password import hash_password, verify_password
from app.core.security import create_access_token, verify_access_token


router = APIRouter(prefix="/auth", tags=["FORM"])

# OAuth2 scheme (used for protected routes)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extract and verify JWT token.
    Returns payload if token is valid.
    """
    payload = verify_access_token(token)
    return payload


# ---------------- SIGNUP ----------------
@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
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


# ---------------- LOGIN (OAuth2) ----------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ---------------- CHANGE PASSWORD ----------------
@router.put("/change-password")
def change_password(data: ChangePassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # New password must be different
    if verify_password(data.new_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from the old password"
        )

    user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}


from app.schemas.user import UpdateProfile
from app.schemas.user import UserSignup, ChangePassword, UpdateProfile


# ---------------- UPDATE PROFILE ----------------
@router.put("/profile/update")
def update_profile(
    data: UpdateProfile,
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

    
    if not data.firstname and not data.lastname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (firstname or lastname) is required"
        )

   
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    
    if data.firstname:
        user.firstname = data.firstname

    if data.lastname:
        user.lastname = data.lastname

    db.commit()
    db.refresh(user)

    return {
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "createdat": user.createdat
    }
from app.schemas.user import UserOut
from typing import List
# ---------------- ADMIN: LIST ALL USERS ----------------
"""@router.get("/admin/users", response_model=List[UserOut])
def list_all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    users = db.query(User).all()
    return users
"""

from typing import List
from app.schemas.user import UserOut
from app.models.user import User

@router.get("/admin/users", response_model=List[UserOut])
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # OPTIONAL: if you have admin role
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admins only")

    users = db.query(User).all()
    return users

